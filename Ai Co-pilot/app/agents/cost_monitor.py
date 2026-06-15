"""Cost Monitoring Agent.

Tracks input/output tokens and USD cost per LLM call, accumulates per-request
and per-day totals, and persists a ledger to disk so cost survives restarts.
"""
from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List

from .. import config
from ..llm import LLMResult


@dataclass
class CostMonitor:
    """Per-session cost tracker. One instance lives in the orchestrator."""

    events: List[Dict] = field(default_factory=list)

    def record(self, result: LLMResult, label: str = "llm") -> Dict:
        price = config.price_for(result.model)
        cost = (
            result.input_tokens / 1_000_000 * price["input"]
            + result.output_tokens / 1_000_000 * price["output"]
        )
        event = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "label": label,
            "model": result.model,
            "input_tokens": result.input_tokens,
            "output_tokens": result.output_tokens,
            "cost_usd": round(cost, 6),
        }
        self.events.append(event)
        self._persist(event)
        return event

    def _persist(self, event: Dict) -> None:
        try:
            with open(config.COST_LEDGER_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(event) + "\n")
        except Exception:
            pass

    # --- Session rollups --------------------------------------------------
    def session_summary(self) -> Dict:
        in_tok = sum(e["input_tokens"] for e in self.events)
        out_tok = sum(e["output_tokens"] for e in self.events)
        cost = sum(e["cost_usd"] for e in self.events)
        return {
            "requests": len(self.events),
            "input_tokens": in_tok,
            "output_tokens": out_tok,
            "total_tokens": in_tok + out_tok,
            "cost_usd": round(cost, 6),
        }

    def last_request_cost(self) -> Dict:
        if not self.events:
            return {"input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0}
        return self.events[-1]

    def mark(self) -> int:
        """Return a cursor (event index) to roll up a single user request."""
        return len(self.events)

    def request_summary(self, since: int) -> Dict:
        """Sum every LLM call recorded since ``mark()`` (e.g. planner+reasoning)."""
        evts = self.events[since:]
        in_tok = sum(e["input_tokens"] for e in evts)
        out_tok = sum(e["output_tokens"] for e in evts)
        cost = sum(e["cost_usd"] for e in evts)
        return {
            "calls": len(evts),
            "input_tokens": in_tok,
            "output_tokens": out_tok,
            "cost_usd": round(cost, 6),
        }

    @staticmethod
    def daily_summary() -> Dict[str, Dict]:
        """Read the on-disk ledger and roll up cost per calendar day (UTC)."""
        days: Dict[str, Dict] = defaultdict(
            lambda: {"requests": 0, "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0}
        )
        try:
            with open(config.COST_LEDGER_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    e = json.loads(line)
                    day = e["ts"][:10]
                    d = days[day]
                    d["requests"] += 1
                    d["input_tokens"] += e["input_tokens"]
                    d["output_tokens"] += e["output_tokens"]
                    d["cost_usd"] = round(d["cost_usd"] + e["cost_usd"], 6)
        except FileNotFoundError:
            pass
        return dict(sorted(days.items(), reverse=True))
