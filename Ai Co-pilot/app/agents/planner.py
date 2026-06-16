"""Planner Agent.

Detects intent and produces an execution plan: which knowledge sources to
search, whether a tool should be called, temporal filters for date-based
queries, and whether a follow-up question is needed. Uses a single JSON-mode 
LLM call, with a deterministic keyword fallback.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Dict

from ..llm import LLMResult, generate, parse_json

INTENTS = ["RESEARCH", "PERSONAL", "WORK", "GENERAL", "SUMMARIZE"]

SYSTEM = """You are the Planner in a personal knowledge management system called "Second Brain".
Classify the user's query and produce a short execution plan.

Return STRICT JSON with this schema:
{
  "intent": "RESEARCH" | "PERSONAL" | "WORK" | "GENERAL" | "SUMMARIZE",
  "domain_filter": "Research" | "Personal" | "Work" | "Email" | "Notes" | null,
  "search_documents": true|false,
  "search_memory": true|false,
  "temporal_filter": {
    "type": "last_week" | "last_month" | "last_year" | "specific_month" | "date_range" | null,
    "year": number | null,
    "month": number | null,
    "days_ago": number | null
  },
  "summarize_topic": true|false,  // true if user asks to "summarize everything about X"
  "topic": "",  // extracted topic name if summarize_topic=true
  "needs_followup": true|false,
  "followup_question": "" ,
  "rationale": "one sentence"
}

Guidance:
- RESEARCH: queries about articles, papers, learning materials, study notes
- PERSONAL: personal notes, bookmarks, saved content
- WORK: work-related documents, emails, policies
- SUMMARIZE: when user asks "summarize everything about X" or "what do I know about X"
- Temporal filters: detect phrases like "last month", "last week", "this year", "in January"
  Examples:
  - "last month" → {"type": "last_month", "days_ago": 30}
  - "last week" → {"type": "last_week", "days_ago": 7}
  - "in January 2026" → {"type": "specific_month", "year": 2026, "month": 1}
  - "this year" → {"type": "last_year", "year": 2026}
- For summarization queries, set summarize_topic=true and extract the topic
- Use search_memory=true for all queries to leverage past conversations
Output JSON only."""


@dataclass
class Plan:
    intent: str = "GENERAL"
    domain_filter: Optional[str] = None
    search_documents: bool = True
    search_memory: bool = True
    tool: Optional[dict] = None
    temporal_filter: Optional[Dict] = None
    summarize_topic: bool = False
    topic: str = ""
    needs_followup: bool = False
    followup_question: str = ""
    rationale: str = ""
    raw: dict = field(default_factory=dict)


_RESEARCH_KW = ("research", "article", "paper", "study", "learning", "llm", "ai", 
                "scaling", "rag", "agent", "vector", "embedding", "model")
_PERSONAL_KW = ("note", "bookmark", "saved", "remember", "personal", "thought")
_TEMPORAL_KW = ("last week", "last month", "this year", "last year", "yesterday",
                "january", "february", "march", "april", "may", "june",
                "july", "august", "september", "october", "november", "december")
_SUMMARIZE_KW = ("summarize", "summary", "everything about", "all about", 
                 "what do i know", "what did i read", "tell me about")


def _extract_temporal_filter(query: str) -> Optional[Dict]:
    """Extract temporal filter from query using simple pattern matching."""
    q = query.lower()
    
    if "last week" in q or "past week" in q:
        return {"type": "last_week", "days_ago": 7}
    elif "last month" in q or "past month" in q:
        return {"type": "last_month", "days_ago": 30}
    elif "last year" in q or "past year" in q:
        return {"type": "last_year", "days_ago": 365}
    elif "this year" in q:
        current_year = datetime.now().year
        return {"type": "last_year", "year": current_year}
    
    # Check for specific months
    months = {
        "january": 1, "february": 2, "march": 3, "april": 4,
        "may": 5, "june": 6, "july": 7, "august": 8,
        "september": 9, "october": 10, "november": 11, "december": 12
    }
    for month_name, month_num in months.items():
        if month_name in q:
            return {"type": "specific_month", "month": month_num, "year": datetime.now().year}
    
    return None


def _fallback(query: str) -> Plan:
    q = query.lower()
    tool = None
    summarize = any(k in q for k in _SUMMARIZE_KW)
    
    if any(k in q for k in _RESEARCH_KW):
        intent = "RESEARCH"
        domain = "Research"
    elif any(k in q for k in _PERSONAL_KW):
        intent = "PERSONAL"
        domain = "Personal"
    else:
        intent = "GENERAL"
        domain = None
    
    if summarize:
        intent = "SUMMARIZE"
    
    temporal = _extract_temporal_filter(query)
    
    # Extract topic for summarization
    topic = ""
    if summarize:
        for kw in _SUMMARIZE_KW:
            if kw in q:
                topic = q.split(kw, 1)[-1].strip().strip("?.,!\"'")
                break
    
    return Plan(
        intent=intent,
        domain_filter=domain,
        search_documents=True,
        search_memory=True,
        tool=tool,
        temporal_filter=temporal,
        summarize_topic=summarize,
        topic=topic,
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
            temporal_filter=data.get("temporal_filter"),
            summarize_topic=bool(data.get("summarize_topic", False)),
            topic=data.get("topic", ""),
            needs_followup=bool(data.get("needs_followup", False)),
            followup_question=data.get("followup_question", "") or "",
            rationale=data.get("rationale", ""),
            raw=data,
        )
        return p, res
    except Exception:
        return _fallback(query), None
