"""Agentic RAG Orchestrator.

Coordinates the agents into a single decision-making loop:

    Planner -> (Memory recall) -> Retriever -> Context Optimizer
            -> Reasoning -> (Tool Agent) -> Memory store -> Cost Monitor

Every step contributes to a structured ``trace`` so the UI can show *why* an
answer was produced (the "agentic" transparency the spec asks for).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from . import config
from .agents import (
    context_optimizer,
    memory,
    planner,
    reasoning,
    retriever,
    tools,
)
from .agents.cost_monitor import CostMonitor
from .llm import LLMError


@dataclass
class CoPilotResponse:
    answer: str
    plan: planner.Plan
    memory_hit: Optional[dict] = None
    memory_recall: List[dict] = field(default_factory=list)
    retrieved: List[dict] = field(default_factory=list)
    optimized: List[dict] = field(default_factory=list)
    optimizer_report: Dict = field(default_factory=dict)
    tool_result: Optional[dict] = None
    sources: List[str] = field(default_factory=list)
    memory_id: Optional[str] = None
    request_cost: Dict = field(default_factory=dict)
    llm_error: Optional[str] = None
    trace: List[str] = field(default_factory=list)


class CoPilot:
    """Holds session-scoped state (cost monitor + settings)."""

    def __init__(self, settings: Optional[dict] = None):
        self.cost = CostMonitor()
        self.settings = settings or {}

    def _opt(self, key: str, default):
        return self.settings.get(key, default)

    @staticmethod
    def _extractive(chunks: List[dict], note: str = "") -> str:
        """Answer without the LLM: surface the most relevant policy excerpts."""
        header = f"⚠️ {note} Showing the most relevant policy excerpts:\n\n" if note else ""
        if not chunks:
            return (header or "⚠️ ") + "Nothing matched in the knowledge base. " \
                   "Consider raising a ticket."
        bullets = "\n\n".join(
            f"**{c['metadata'].get('title','Doc')} — {c['metadata'].get('heading','')}**\n"
            f"{c['text']}"
            for c in chunks[:3]
        )
        return header + bullets

    def ask(self, query: str) -> CoPilotResponse:
        trace: List[str] = []
        use_llm = config.llm_available()
        cost_cursor = self.cost.mark()

        # 1) PLANNER ------------------------------------------------------
        p, plan_usage = planner.plan(query, use_llm=use_llm)
        if plan_usage:
            self.cost.record(plan_usage, label="planner")
        trace.append(f"🧭 Planner: intent={p.intent}, domain={p.domain_filter}, "
                     f"tool={'yes' if p.tool else 'no'} — {p.rationale}")

        resp = CoPilotResponse(answer="", plan=p, trace=trace)

        # Ambiguous? ask a follow-up immediately.
        if p.needs_followup and p.followup_question:
            resp.answer = f"❓ {p.followup_question}"
            trace.append("⏸️ Planner requested a follow-up question.")
            resp.request_cost = self.cost.request_summary(cost_cursor)
            return resp

        # 2) MEMORY recall ------------------------------------------------
        memory_hit = None
        if self._opt("use_memory", True) and p.search_memory:
            resp.memory_recall = memory.recall(query)
            memory_hit = memory.best_hit(query)
            if memory_hit:
                trace.append(f"🧠 Semantic Memory: confident hit "
                             f"(sim={memory_hit['similarity']}) — boosting answer.")
            elif resp.memory_recall:
                trace.append(f"🧠 Semantic Memory: {len(resp.memory_recall)} related "
                             f"past interaction(s), none above threshold.")
            else:
                trace.append("🧠 Semantic Memory: empty / no related history.")
        resp.memory_hit = memory_hit

        # 3) RETRIEVER ----------------------------------------------------
        retrieved: List[dict] = []
        if p.search_documents:
            top_k = self._opt("top_k", config.RETRIEVE_TOP_K)
            retrieved = retriever.retrieve(query, domain_filter=p.domain_filter, top_k=top_k)
            trace.append(f"📚 Retriever: {len(retrieved)} candidate chunk(s) "
                         f"(domain filter: {p.domain_filter or 'none'}).")
        resp.retrieved = retrieved

        # 4) CONTEXT OPTIMIZER -------------------------------------------
        if self._opt("use_optimizer", True) and retrieved:
            report = context_optimizer.optimize(query, retrieved)
            resp.optimized = report.chunks
            resp.optimizer_report = report.as_dict()
            trace.append(
                f"✨ Context Optimizer: {report.chunks_in}→{report.chunks_out} chunks, "
                f"~{report.saved_pct}% tokens saved "
                f"({report.tokens_before}→{report.tokens_after})."
            )
        else:
            resp.optimized = retrieved[: self._opt("top_n", config.RERANK_TOP_N)]
            if retrieved:
                trace.append("✨ Context Optimizer: disabled (passing top chunks through).")

        # 5) REASONING ----------------------------------------------------
        if use_llm:
            try:
                ans, ans_usage = reasoning.answer(query, resp.optimized, memory_hit)
                if ans_usage.model != "(no-llm)":
                    self.cost.record(ans_usage, label="reasoning")
                resp.answer = ans
                trace.append("💬 Reasoning: grounded answer generated.")
            except LLMError as e:
                resp.llm_error = str(e)
                resp.answer = self._extractive(resp.optimized, note=str(e))
                trace.append(f"⚠️ Reasoning: LLM call failed — {str(e)[:80]}… "
                             "Returned extractive snippets.")
        else:
            resp.answer = self._extractive(
                resp.optimized, note="No GOOGLE_API_KEY set."
            )
            trace.append("💬 Reasoning: LLM unavailable — returned extractive snippets.")

        # Sources
        seen = set()
        for c in resp.optimized:
            t = c["metadata"].get("title", "Document")
            if t not in seen:
                seen.add(t)
                resp.sources.append(t)

        # 6) TOOL AGENT ---------------------------------------------------
        if self._opt("allow_tools", True) and p.tool and p.intent == "TOOL":
            tool_result = tools.execute(p.tool, query, domain=p.domain_filter or "IT")
            resp.tool_result = tool_result
            trace.append(f"🛠️ Tool Agent: {tool_result.get('tool')} → "
                         f"{tool_result.get('status')} "
                         f"{tool_result.get('ticket_number', '')}".strip())
            if tool_result.get("ticket_number"):
                resp.answer += (
                    f"\n\n✅ I've raised a ticket for you: "
                    f"**{tool_result['ticket_number']}** "
                    f"(assigned to {tool_result['assignment_group']})."
                )

        # 7) MEMORY store -------------------------------------------------
        if (self._opt("use_memory", True) and resp.answer and p.intent != "GENERAL"
                and not resp.llm_error):
            # Don't re-store a near-identical confident hit or a failed answer.
            if not memory_hit:
                resp.memory_id = memory.store(
                    query, p.intent, resp.answer, resp.sources, score=0.7
                )
                trace.append("🧠 Semantic Memory: stored this interaction.")

        # 8) COST ---------------------------------------------------------
        resp.request_cost = self.cost.request_summary(cost_cursor)
        return resp
