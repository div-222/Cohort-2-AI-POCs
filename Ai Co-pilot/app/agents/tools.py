"""Tool Agent — simulated enterprise integrations.

Per POC scope, tools are mocked: they generate realistic-looking results
(ticket numbers, message receipts) and append to an on-disk activity log
instead of hitting real ServiceNow / Slack / SMTP endpoints. The interface is
deliberately shaped like a real tool-calling layer so it can be swapped later.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Dict

from .. import config


def _log(entry: Dict) -> None:
    try:
        with open(config.TOOL_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass


def _ticket_number(seed: str) -> str:
    h = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:7].upper()
    return f"INC{int(h, 16) % 9000000 + 1000000}"


def create_ticket(summary: str, description: str = "", domain: str = "IT", priority: str = "Medium") -> Dict:
    ts = datetime.now(timezone.utc).isoformat()
    number = _ticket_number(summary + ts)
    result = {
        "tool": "ServiceNow.create_ticket",
        "status": "created",
        "ticket_number": number,
        "summary": summary,
        "description": description,
        "domain": domain,
        "priority": priority,
        "assignment_group": "HR Support" if domain == "HR" else "IT Service Desk",
        "ts": ts,
        "simulated": True,
    }
    _log(result)
    return result


def send_slack(channel: str, message: str) -> Dict:
    ts = datetime.now(timezone.utc).isoformat()
    result = {
        "tool": "Slack.post_message",
        "status": "sent",
        "channel": channel or "#it-helpdesk",
        "message": message,
        "ts": ts,
        "simulated": True,
    }
    _log(result)
    return result


def send_email(to: str, subject: str, body: str = "") -> Dict:
    ts = datetime.now(timezone.utc).isoformat()
    result = {
        "tool": "Email.send",
        "status": "queued",
        "to": to or "employee@sails.example",
        "subject": subject,
        "body": body,
        "ts": ts,
        "simulated": True,
    }
    _log(result)
    return result


DISPATCH = {
    "create_ticket": create_ticket,
    "send_slack": send_slack,
    "send_email": send_email,
}

# Only these kwargs are forwarded to each tool; the planner LLM sometimes
# hallucinates extra keys, so we filter defensively.
ALLOWED_ARGS = {
    "create_ticket": {"summary", "description", "domain", "priority"},
    "send_slack": {"channel", "message"},
    "send_email": {"to", "subject", "body"},
}


def execute(tool_spec: Dict, query: str, domain: str = "IT") -> Dict:
    """Run a tool described by the planner. Fills in safe defaults."""
    name = (tool_spec or {}).get("name")
    if name not in DISPATCH:
        return {"tool": name or "unknown", "status": "skipped", "reason": "unknown tool"}

    # Keep only recognized args for the chosen tool.
    raw = (tool_spec or {}).get("args") or {}
    args = {k: v for k, v in raw.items() if k in ALLOWED_ARGS[name]}

    if name == "create_ticket":
        args.setdefault("summary", query[:120])
        args.setdefault("description", query)
        args.setdefault("domain", domain or "IT")
    elif name == "send_slack":
        args.setdefault("channel", "#hr-helpdesk" if domain == "HR" else "#it-helpdesk")
        args.setdefault("message", f"Employee query: {query}")
    elif name == "send_email":
        args.setdefault("subject", f"Helpdesk: {query[:60]}")
        args.setdefault("to", "helpdesk@sails.example")
        args.setdefault("body", query)

    return DISPATCH[name](**args)


def recent_activity(limit: int = 25):
    items = []
    try:
        with open(config.TOOL_LOG_PATH, "r", encoding="utf-8") as f:
            for line in f:
                items.append(json.loads(line))
    except FileNotFoundError:
        return []
    return list(reversed(items))[:limit]
