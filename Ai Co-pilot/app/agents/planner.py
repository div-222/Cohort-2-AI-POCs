"""Planner Agent.

Detects intent and produces an execution plan: which knowledge sources to
search, whether a tool should be called, and whether a follow-up question is
needed. Uses a single JSON-mode LLM call, with a deterministic keyword
fallback so the app still routes sensibly if the LLM is unavailable.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from ..llm import LLMResult, generate, parse_json

INTENTS = ["HR", "IT", "TOOL", "GENERAL"]

SYSTEM = """You are the Planner in an internal HR/IT helpdesk co-pilot.
Classify the employee's query and produce a short execution plan.

Return STRICT JSON with this schema:
{
  "intent": "HR" | "IT" | "TOOL" | "GENERAL",
  "domain_filter": "HR" | "IT" | null,   // restrict document search to one domain, or null
  "search_documents": true|false,
  "search_memory": true|false,
  "tool": null | {"name": "create_ticket"|"send_slack"|"send_email",
                  "reason": "...",
                  "args": { ... }},
  "needs_followup": true|false,
  "followup_question": "" ,
  "rationale": "one sentence"
}

Guidance:
- HR: leave, reimbursement, travel, insurance, benefits, onboarding.
- IT: password reset, VPN, laptop request, software install, email config, security.
- TOOL: the user explicitly asks to raise a ticket, notify someone, or email.
  Still set domain_filter so we can attach relevant context.
- Use search_memory=true for common/repetitive questions.
- Only set needs_followup=true if the request is genuinely ambiguous.
Output JSON only."""


@dataclass
class Plan:
    intent: str = "GENERAL"
    domain_filter: Optional[str] = None
    search_documents: bool = True
    search_memory: bool = True
    tool: Optional[dict] = None
    needs_followup: bool = False
    followup_question: str = ""
    rationale: str = ""
    raw: dict = field(default_factory=dict)


_HR_KW = ("leave", "reimburse", "travel", "insurance", "benefit", "onboard",
          "salary", "maternity", "paternity", "holiday", "comp-off", "encash")
_IT_KW = ("password", "vpn", "laptop", "software", "install", "email", "outlook",
          "security", "remote", "access", "wifi", "network", "mfa", "2fa")
_TOOL_KW = ("raise a ticket", "create a ticket", "open a ticket", "log a ticket",
            "notify", "send an email", "email it", "slack", "escalate")


def _fallback(query: str) -> Plan:
    q = query.lower()
    tool = None
    if any(k in q for k in _TOOL_KW):
        intent = "TOOL"
        tool = {"name": "create_ticket", "reason": "user asked to raise a ticket", "args": {}}
    elif any(k in q for k in _IT_KW):
        intent = "IT"
    elif any(k in q for k in _HR_KW):
        intent = "HR"
    else:
        intent = "GENERAL"
    domain = intent if intent in ("HR", "IT") else None
    if intent == "TOOL":
        domain = "IT" if any(k in q for k in _IT_KW) else ("HR" if any(k in q for k in _HR_KW) else None)
    return Plan(
        intent=intent,
        domain_filter=domain,
        search_documents=True,
        search_memory=True,
        tool=tool,
        rationale="keyword fallback (LLM unavailable)",
    )


def plan(query: str, use_llm: bool = True) -> tuple[Plan, Optional[LLMResult]]:
    """Return (Plan, llm_usage_or_None)."""
    if not use_llm:
        return _fallback(query), None
    try:
        res = generate(query, system=SYSTEM, json_mode=True, temperature=0.0)
        data = parse_json(res.text)
        if not data or data.get("intent") not in INTENTS:
            return _fallback(query), res
        p = Plan(
            intent=data.get("intent", "GENERAL"),
            domain_filter=data.get("domain_filter"),
            search_documents=bool(data.get("search_documents", True)),
            search_memory=bool(data.get("search_memory", True)),
            tool=data.get("tool"),
            needs_followup=bool(data.get("needs_followup", False)),
            followup_question=data.get("followup_question", "") or "",
            rationale=data.get("rationale", ""),
            raw=data,
        )
        return p, res
    except Exception:
        return _fallback(query), None
