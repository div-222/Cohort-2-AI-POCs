"""Second Brain — Personal Knowledge Agent with Agentic RAG.

Run with:  streamlit run streamlit_app.py
"""
from __future__ import annotations

import pandas as pd
import streamlit as st

from app import config, vectorstore
from app.agents import memory, tools
from app.agents.cost_monitor import CostMonitor
from app.ingest import build_index, ingest_uploaded_file
from app.orchestrator import CoPilot

st.set_page_config(
    page_title="Second Brain · Personal Knowledge Agent",
    page_icon="🧠",
    layout="wide",
)

# --- Session state --------------------------------------------------------
if "copilot" not in st.session_state:
    st.session_state.copilot = CoPilot()
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of dicts: role, content, meta
if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = []  # short-term conversation context

copilot: CoPilot = st.session_state.copilot

EXAMPLES = [
    "What did I read about LLM scaling last month?",
    "Summarize everything I know about AI agents",
    "What are my key notes on RAG systems?",
    "Find information about vector databases in my documents",
    "What did I save about prompt engineering?",
    "Show me my research on semantic memory",
]


# --- Sidebar --------------------------------------------------------------
def sidebar():
    with st.sidebar:
        st.title("� Second Brain")
        st.caption("Your Personal Knowledge Agent")
        st.caption("Agentic RAG · Semantic Memory · Context Optimizer")

        # LLM status
        if config.llm_available():
            st.success(f"LLM: Gemini `{config.GEMINI_MODEL}`")
        else:
            st.error("No GOOGLE_API_KEY — running in extractive (no-LLM) mode.")
            st.caption("Add your key to `.env` and restart for full answers.")

        # File Upload Section
        st.divider()
        st.subheader("📤 Upload Documents")
        st.caption("Upload PDFs, Word docs, text files, notes, bookmarks")
        
        uploaded_files = st.file_uploader(
            "Drag and drop files here",
            accept_multiple_files=True,
            type=["pdf", "docx", "txt", "md", "html", "htm"],
            label_visibility="collapsed"
        )
        
        if uploaded_files:
            upload_domain = st.selectbox(
                "Categorize as:", 
                ["Personal", "Research", "Work", "General", "Email", "Notes"],
                key="upload_domain"
            )
            
            if st.button("🚀 Process Uploads", type="primary", width="stretch"):
                progress_bar = st.progress(0)
                total_chunks = 0
                
                for idx, uploaded_file in enumerate(uploaded_files):
                    with st.spinner(f"Processing {uploaded_file.name}..."):
                        file_content = uploaded_file.read()
                        file_type = uploaded_file.name.split('.')[-1].lower()
                        
                        result = ingest_uploaded_file(
                            file_content=file_content,
                            filename=uploaded_file.name,
                            file_type=file_type,
                            domain=upload_domain
                        )
                        
                        if "error" not in result:
                            total_chunks += result["chunks"]
                            st.success(f"✓ {uploaded_file.name}: {result['chunks']} chunks")
                        else:
                            st.error(f"✗ {uploaded_file.name}: {result['error']}")
                    
                    progress_bar.progress((idx + 1) / len(uploaded_files))
                
                st.success(f"🎉 Processed {len(uploaded_files)} files → {total_chunks} chunks added to your brain!")
                st.rerun()

        # Knowledge base status
        st.divider()
        st.subheader("📚 Knowledge Base")
        n = vectorstore.document_count()
        if n == 0:
            st.warning("Knowledge base is empty. Upload files or rebuild index.")
        else:
            st.metric("Total chunks in your brain", f"{n:,}")
        
        if st.button("🔁 Rebuild from data/ folder", width="stretch"):
            with st.spinner("Indexing all documents in data/ folder…"):
                report = build_index(verbose=False)
            st.success(f"Indexed {report['files']} docs → {report['chunks']} chunks.")
            st.rerun()

        # Settings
        st.divider()
        st.subheader("⚙️ Agent Settings")
        copilot.settings["use_memory"] = st.toggle("Semantic Memory", value=True)
        copilot.settings["use_optimizer"] = st.toggle("Context Optimizer", value=True)
        copilot.settings["allow_tools"] = st.toggle("Tool Calling", value=False)
        copilot.settings["top_k"] = st.slider("Retriever top-K", 3, 20, config.RETRIEVE_TOP_K)

        # Memory
        st.divider()
        st.subheader("🧠 Semantic Memory")
        mem_count = memory.count()
        st.metric("Stored interactions", mem_count)
        if mem_count > 0:
            st.caption(f"Your Second Brain remembers {mem_count} past conversations")

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
                st.dataframe(df, width="stretch")


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

    st.title("🧠 Second Brain — Your Personal Knowledge Agent")
    st.caption(
        "Upload your notes, PDFs, bookmarks, and documents. Ask questions and get "
        "intelligent answers from your personal knowledge base with complete transparency."
    )

    if vectorstore.document_count() == 0:
        st.info("👈 Upload some documents or rebuild the index from the sidebar to get started.")

    # Example chips
    with st.expander("💡 Example questions", expanded=not st.session_state.messages):
        cols = st.columns(2)
        for i, ex in enumerate(EXAMPLES):
            if cols[i % 2].button(ex, key=f"ex_{i}", width="stretch"):
                st.session_state.pending = ex
                st.rerun()

    # Replay history
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("meta"):
                render_details(msg["meta"], idx)

    # Input
    prompt = st.chat_input("Ask about anything in your knowledge base…")
    if "pending" in st.session_state:
        prompt = st.session_state.pop("pending")

    if prompt:
        # Store in short-term conversation memory
        st.session_state.conversation_memory.append({
            "role": "user",
            "content": prompt,
            "timestamp": pd.Timestamp.now()
        })
        
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
        
        # Store assistant response in short-term memory
        st.session_state.conversation_memory.append({
            "role": "assistant",
            "content": resp.answer,
            "timestamp": pd.Timestamp.now()
        })

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
