"""Headless end-to-end smoke test (no Streamlit, no API key required).

Builds the index, runs a few queries through the full agent pipeline, and
prints the trace. With GOOGLE_API_KEY set it produces real answers; without it
the pipeline degrades to extractive snippets so you can still verify retrieval,
the Context Optimizer, and Semantic Memory.
"""
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")  # emoji-safe on Windows consoles
except Exception:
    pass

from app import config, vectorstore
from app.ingest import build_index
from app.orchestrator import CoPilot

QUERIES = [
    "How many earned leaves do I get and can I carry them forward?",
    "How do I reset my VPN password?",
    "Raise a ticket: my laptop won't power on.",
]


def main():
    print(f"LLM available: {config.llm_available()} (model={config.GEMINI_MODEL})")
    if vectorstore.document_count() == 0:
        print("\nBuilding index…")
        build_index(verbose=True)
    else:
        print(f"\nIndex already has {vectorstore.document_count()} chunks.")

    bot = CoPilot()
    for q in QUERIES:
        print("\n" + "=" * 78)
        print("Q:", q)
        r = bot.ask(q)
        print("-" * 78)
        for step in r.trace:
            print(" ", step)
        print("-" * 78)
        print("A:", r.answer[:600])
        print("Sources:", r.sources)
        print("Request cost:", r.request_cost)

    print("\n" + "=" * 78)
    print("Session cost:", bot.cost.session_summary())


if __name__ == "__main__":
    main()
