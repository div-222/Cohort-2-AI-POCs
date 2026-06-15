"""AI Co-Pilot for HR / IT Helpdesk — Streamlit web interface.

Run with:  streamlit run streamlit_app.py
"""
from __future__ import annotations

import pandas as pd
import streamlit as st

from app import config, vectorstore
from app.agents import memory, tools
from app.agents.cost_monitor import CostMonitor
from app.ingest import build_index
from app.orchestrator import CoPilot

st.set_page_config(
    page_title="AI Co-Pilot · HR / IT Helpdesk",
    page_icon="🤖",
    layout="wide",
)

# --- Session state --------------------------------------------------------
if "copilot" not in st.session_state:
    st.session_state.copilot = CoPilot()
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of dicts: role, content, meta

copilot: CoPilot = st.session_state.copilot

EXAMPLES = [
    "How many earned leaves do I get and can I carry them forward?",
    "What is the maternity leave policy?",
    "How do I reset my VPN password?",
    "How do I request a new laptop?",
    "My Outlook isn't connecting — how do I configure it?",
    "Raise a ticket: my laptop won't power on.",
]


# --- Sidebar --------------------------------------------------------------
def sidebar():
    with st.sidebar:
        st.title("🤖 AI Co-Pilot")
        st.caption("Agentic RAG · Semantic Memory · Context Optimizer")

        # LLM status
        if config.llm_available():
            st.success(f"LLM: Gemini `{config.GEMINI_MODEL}`")
        else:
            st.error("No GOOGLE_API_KEY — running in extractive (no-LLM) mode.")
            st.caption("Add your key to `.env` and restart for full answers.")

        # Knowledge base status
        st.divider()
        st.subheader("📚 Knowledge Base")
        n = vectorstore.document_count()
        if n == 0:
            st.warning("Index is empty. Build it to enable retrieval.")
        else:
            st.metric("Indexed chunks", n)
        if st.button("🔁 (Re)build index", use_container_width=True):
            with st.spinner("Chunking + embedding the policy corpus…"):
                report = build_index(verbose=False)
            st.success(f"Indexed {report['files']} docs → {report['chunks']} chunks.")
            st.rerun()

        # Settings
        st.divider()
        st.subheader("⚙️ Agent Settings")
        copilot.settings["use_memory"] = st.toggle("Semantic Memory", value=True)
        copilot.settings["use_optimizer"] = st.toggle("Context Optimizer", value=True)
        copilot.settings["allow_tools"] = st.toggle("Tool Calling (simulated)", value=True)
        copilot.settings["top_k"] = st.slider("Retriever top-K", 3, 15, config.RETRIEVE_TOP_K)

        # Memory
        st.divider()
        st.subheader("🧠 Semantic Memory")
        st.metric("Stored interactions", memory.count())

        # Cost dashboard
        st.divider()
        st.subheader("💰 Cost Monitor")
        s = copilot.cost.session_summary()
        c1, c2 = st.columns(2)
        c1.metric("Session cost", f"${s['cost_usd']:.5f}")
        c2.metric("Requests", s["requests"])
        c1.metric("Input tok", f"{s['input_tokens']:,}")
        c2.metric("Output tok", f"{s['output_tokens']:,}")
        daily = CostMonitor.daily_summary()
        if daily:
            with st.expander("Daily cost (all sessions)"):
                df = pd.DataFrame(
                    [{"date": k, **v} for k, v in daily.items()]
                ).set_index("date")
                st.dataframe(df, use_container_width=True)

        # Tool activity
        st.divider()
        st.subheader("🛠️ Tool Activity")
        acts = tools.recent_activity(limit=8)
        if not acts:
            st.caption("No tool calls yet.")
        for a in acts:
            label = a.get("ticket_number") or a.get("channel") or a.get("to") or ""
            st.caption(f"`{a['tool']}` · {a['status']} · {label}")


# --- Render one assistant message detail ----------------------------------
def render_details(meta: dict, idx: int):
    resp = meta["resp"]

    # Agent trace
    with st.expander("🔎 Agent trace (how this answer was produced)"):
        for step in resp["trace"]:
            st.markdown(f"- {step}")

    cols = st.columns(3)

    # Sources
    with cols[0]:
        st.markdown("**📚 Sources**")
        if resp["sources"]:
            for s in resp["sources"]:
                st.caption(f"• {s}")
        else:
            st.caption("—")

    # Optimizer
    with cols[1]:
        st.markdown("**✨ Context Optimizer**")
        rpt = resp["optimizer_report"]
        if rpt:
            st.caption(f"Chunks: {rpt['chunks_in']} → {rpt['chunks_out']}")
            st.caption(f"Tokens: {rpt['tokens_before']} → {rpt['tokens_after']}")
            st.caption(f"Saved: **{rpt['saved_pct']}%**")
        else:
            st.caption("—")

    # Cost
    with cols[2]:
        st.markdown("**💰 This request**")
        rc = resp["request_cost"]
        st.caption(f"In/Out tok: {rc.get('input_tokens',0)} / {rc.get('output_tokens',0)}")
        st.caption(f"Cost: **${rc.get('cost_usd',0):.6f}**")

    # Retrieved chunks
    if resp["optimized"]:
        with st.expander("📄 Retrieved context (post-optimization)"):
            for c in resp["optimized"]:
                m = c["metadata"]
                score = c.get("rerank_score", c.get("similarity"))
                st.markdown(f"**{m.get('title')} — {m.get('heading')}**  ·  score `{score}`")
                st.caption(c["text"][:600] + ("…" if len(c["text"]) > 600 else ""))
                st.divider()

    # Memory recall
    if resp["memory_recall"]:
        with st.expander("🧠 Related memory"):
            for mh in resp["memory_recall"]:
                st.caption(f"sim `{mh['similarity']}` · {mh['question']}")

    # Feedback
    mem_id = resp.get("memory_id")
    if mem_id:
        fb_cols = st.columns([1, 1, 6])
        if fb_cols[0].button("👍", key=f"up_{idx}"):
            memory.update_feedback(mem_id, "up")
            st.toast("Thanks — memory reinforced.")
        if fb_cols[1].button("👎", key=f"down_{idx}"):
            memory.update_feedback(mem_id, "down")
            st.toast("Noted — memory score lowered.")


# --- Main -----------------------------------------------------------------
def main():
    sidebar()

    st.title("Internal HR / IT Helpdesk Co-Pilot")
    st.caption(
        "Ask about leave, reimbursement, travel, insurance, benefits, onboarding · "
        "password reset, VPN, laptops, software, email, security."
    )

    if vectorstore.document_count() == 0:
        st.info("👈 Build the knowledge-base index from the sidebar to get started.")

    # Example chips
    with st.expander("💡 Example questions", expanded=not st.session_state.messages):
        cols = st.columns(2)
        for i, ex in enumerate(EXAMPLES):
            if cols[i % 2].button(ex, key=f"ex_{i}", use_container_width=True):
                st.session_state.pending = ex
                st.rerun()

    # Replay history
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("meta"):
                render_details(msg["meta"], idx)

    # Input
    prompt = st.chat_input("Ask a HR or IT question…")
    if "pending" in st.session_state:
        prompt = st.session_state.pop("pending")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking across agents…"):
                resp = copilot.ask(prompt)
            if resp.llm_error:
                st.warning(f"LLM unavailable: {resp.llm_error}")
            st.markdown(resp.answer)
            meta = {"resp": _resp_to_dict(resp)}
            render_details(meta, len(st.session_state.messages))

        st.session_state.messages.append(
            {"role": "assistant", "content": resp.answer, "meta": meta}
        )
        st.rerun()


def _resp_to_dict(resp) -> dict:
    return {
        "trace": resp.trace,
        "sources": resp.sources,
        "optimizer_report": resp.optimizer_report,
        "optimized": resp.optimized,
        "memory_recall": resp.memory_recall,
        "memory_id": resp.memory_id,
        "request_cost": resp.request_cost,
        "llm_error": resp.llm_error,
    }


if __name__ == "__main__":
    main()
