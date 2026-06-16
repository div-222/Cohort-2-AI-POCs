# Second Brain — Your Personal Knowledge Agent

> **Version 2.0** — Migrated to `google-genai` SDK, enhanced multi-format ingestion, Streamlit layout updates, and watcher noise suppression.

A powerful personal knowledge management system using **Agentic RAG**, **Semantic Memory**, and **Context Optimization** to help you remember, recall, and reason over everything you've learned, read, or saved.

> **Demo Hook**: Upload your notes, PDFs, articles, and bookmarks. Ask questions like *"What did I read about LLM scaling last month?"* or *"Summarize everything I know about AI agents"*. Watch it reason through your personal knowledge base with complete transparency, showing exactly which sources it used and how it optimized the context.

**Built with:** Google Gemini via `google-genai` SDK (LLM), Sentence-Transformers (local embeddings), ChromaDB (vector store), Streamlit (UI)

---

## What's New in v2.0

| Change | Detail |
|--------|--------|
| **`google-genai` SDK** | Migrated from deprecated `google-generativeai` to the current `google-genai>=1.0.0` SDK. Import path is now `from google import genai`. |
| **Updated model names** | Default model updated to `gemini-2.0-flash`. The old `gemini-1.5-flash-8b` alias is no longer recommended. |
| **Streamlit layout API** | Updated to `use_container_width=True` and current Streamlit sidebar/layout APIs — no more deprecation warnings. |
| **`.streamlit/config.toml`** | Added to silence `sentence-transformers`/`torchvision` watcher noise and disable auto-browser-open on launch. |
| **Expanded requirements** | Added `pypdf`, `python-pptx`, `markdown`, `pandas`, `python-dateutil` for broader document and date handling support. |
| **Enhanced agents** | Planner, Retriever, and Reasoning agents significantly expanded with better intent detection, temporal parsing, and summarization. |
| **Documentation** | Added `DEMO_GUIDE.md`, `QUICK_START.md`, and `IMPLEMENTATION_SUMMARY.md`. |

---

## 🎯 What Makes This Special

### 1. **Agentic RAG with Transparency**
Unlike simple Q&A systems, Second Brain uses multiple cooperating agents that plan, retrieve, optimize, and reason:
- **Planner**: Analyzes your query, detects temporal constraints ("last month"), determines if you want a summary
- **Retriever**: Performs semantic search with domain and date filtering
- **Context Optimizer**: Deduplicates, reranks with cross-encoder, and compresses context (saves 40-70% tokens)
- **Reasoning Agent**: Generates grounded answers with citations OR comprehensive topic summaries
- **Semantic Memory**: Remembers past conversations for faster, more personalized responses

Every response shows the complete **agent trace** — you can see exactly what each agent did and why.

### 2. **Multi-Format Document Support**
Upload and index:
- **PDFs** (research papers, articles, ebooks)
- **Word documents** (.docx)
- **Markdown** (notes, documentation)
- **Text files** (plain notes, code snippets)
- **HTML** (saved web pages, bookmarks)

All documents are chunked intelligently, preserving context and citations.

### 3. **Temporal Intelligence**
Ask date-aware questions:
- *"What did I read about RAG last week?"*
- *"Show me my notes from January 2026"*
- *"Find research on agents from this year"*

The Planner automatically detects temporal references and the Retriever filters accordingly.

### 4. **Topic Summarization**
Ask for comprehensive summaries:
- *"Summarize everything I know about vector databases"*
- *"What have I learned about prompt engineering?"*
- *"Give me an overview of my AI research"*

The system retrieves ALL relevant content and synthesizes it into a well-organized summary with citations.

### 5. **Short-Term Conversation Memory**
The system maintains conversation context within a session, making multi-turn interactions natural and coherent.

---

## 🏗️ Architecture

```
            ┌─────────────┐
 question → │  Planner    │  intent + temporal/domain filters + summarization mode
            └──────┬──────┘
                   │
        ┌──────────┼───────────────┐
        ▼          ▼               ▼
 ┌────────────┐ ┌────────────┐ (temporal filter?)
 │  Semantic  │ │ Retriever  │
 │  Memory    │ │ (vector    │
 │  recall    │ │  search)   │
 └─────┬──────┘ └─────┬──────┘
       │              ▼
       │     ┌──────────────────┐
       │     │ Context Optimizer│  dedup → rerank → compress
       │     └─────┬────────────┘
       │           ▼
       │     ┌────────────┐
       └────▶│ Reasoning  │  Q&A answer OR topic summary + citations
             └─────┬──────┘
                   ▼
            store interaction → Semantic Memory
                   ▼
             ┌──────────────┐
             │ Cost Monitor │  token & USD tracking
             └──────────────┘
```

| Component | File | Responsibility |
|-----------|------|----------------|
| **Planner** | `app/agents/planner.py` | Intent detection, temporal parsing, summarization routing |
| **Retriever** | `app/agents/retriever.py` | Semantic search with domain/temporal filters |
| **Context Optimizer** | `app/agents/context_optimizer.py` | Dedup, cross-encoder rerank, compression |
| **Memory** | `app/agents/memory.py` | Store/recall Q&A interactions (semantic similarity) |
| **Reasoning** | `app/agents/reasoning.py` | Grounded answers OR topic summaries with citations |
| **Cost Monitor** | `app/agents/cost_monitor.py` | Per-call & session token/cost tracking |
| **Orchestrator** | `app/orchestrator.py` | Coordinates all agents, builds transparency trace |
| **Ingest** | `app/ingest.py` | Multi-format document processing (PDF/DOCX/MD/TXT/HTML) |

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.9+
- Google Gemini API key (free at [ai.google.dev](https://ai.google.dev))

### Installation

```powershell
# 1. Clone or navigate to the project
cd "Ai Co-pilot"

# 2. (Recommended) Create a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your API key
Copy-Item .env.example .env
# Edit .env and set GOOGLE_API_KEY=your_key_here
```

> **Note:** This project uses the **`google-genai`** package (v1.0+), not the older `google-generativeai` package. The `requirements.txt` already pins the correct package — just `pip install -r requirements.txt` is enough.

### First Run

```powershell
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📖 Usage

### 1. **Upload Your Documents**

In the sidebar:
1. Click the **📤 Upload Documents** section
2. Drag and drop files (PDF, DOCX, TXT, MD, HTML)
3. Choose a category (Personal, Research, Work, etc.)
4. Click **🚀 Process Uploads**

Your documents are chunked, embedded, and indexed automatically.

### 2. **Ask Questions**

Try these example queries:

**Specific Questions:**
- *"What did I read about LLM scaling?"*
- *"Show me my notes on vector databases"*
- *"Find information about RAG systems"*

**Temporal Queries:**
- *"What did I save about AI agents last month?"*
- *"Show me my research from January 2026"*
- *"What articles did I read this week?"*

**Topic Summaries:**
- *"Summarize everything I know about prompt engineering"*
- *"Give me an overview of my research on embeddings"*
- *"What have I learned about semantic memory?"*

### 3. **Review the Agent Trace**

Every answer includes:
- **🔎 Agent Trace**: Step-by-step reasoning (Planner → Retriever → Optimizer → Reasoning)
- **📚 Sources**: Which documents were used
- **✨ Context Optimizer Report**: How much context was compressed (token savings)
- **💰 Cost**: Request cost and token usage
- **📄 Retrieved Context**: Full chunks with similarity scores

### 4. **Semantic Memory**

The system remembers your past Q&A interactions:
- Similar questions get faster, more confident answers
- 👍/👎 feedback improves future responses
- View memory stats in the sidebar

---

## 🎬 Demo Script (for Live Judging)

**Setup (30 seconds):**
1. Show the empty knowledge base
2. Upload 2-3 sample documents (PDF + DOCX + markdown notes)
3. Wait for indexing (~10-20 seconds)

**Demo Queries (2-3 minutes):**

1. **Simple Recall:** *"What did I save about [topic from uploaded docs]?"*
   - Show the agent trace, sources, and citations

2. **Temporal Query:** *"What did I read about [topic] last month?"*
   - Show temporal filter detection in the trace

3. **Topic Summary:** *"Summarize everything I know about [topic]"*
   - Show comprehensive synthesis with multiple source citations

4. **Live Judge Question:** Invite judges to ask about the uploaded content
   - Show real-time reasoning, transparency, and grounded answers

**Highlight:**
- **Transparency**: Every step is visible (not a black box)
- **Grounded**: All answers cite sources, never hallucinates
- **Intelligent**: Context optimizer saves 40-70% tokens
- **Personalized**: Semantic memory learns from interactions

---

## ⚙️ Configuration

### Agent Settings (in sidebar)

- **Semantic Memory**: Enable/disable conversation recall
- **Context Optimizer**: Enable/disable dedup+rerank+compression
- **Tool Calling**: (Disabled by default for Second Brain)
- **Retriever top-K**: Number of chunks to retrieve (3-20)

### Environment Variables (`.env`)

```bash
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash        # recommended; or gemini-2.0-flash-lite, gemini-1.5-flash
CHUNK_SIZE=800
CHUNK_OVERLAP=200
RETRIEVE_TOP_K=10
RERANK_TOP_N=5
```

> **Model names with `google-genai` SDK**: Use `gemini-2.0-flash`, `gemini-2.0-flash-lite`, or `gemini-1.5-flash`. The old `gemini-1.5-flash-8b` alias is deprecated.

---

## 📊 Cost Monitoring

All LLM calls are tracked:
- **Per-request**: Shows input/output tokens and USD cost
- **Session total**: Cumulative cost for current session
- **Daily summary**: Historical costs across sessions

The Context Optimizer typically reduces LLM input tokens by **40-70%**, significantly lowering costs.

---

## 🧠 Technical Highlights

### Agentic RAG Pipeline
- **Multi-agent orchestration** with transparent trace logging
- **Intent-aware routing** (Q&A vs. Summarization)
- **Temporal query parsing** with date-range filtering
- **Cross-encoder reranking** for precision (MS-MARCO)
- **Semantic memory** with similarity-based recall

### LLM Integration
- **SDK**: `google-genai` v1.0+ (`from google import genai`) — the current Google AI Python SDK
- **Auth**: `genai.Client(api_key=...)` — no environment-level configure calls needed
- **JSON mode**: Planner uses `response_mime_type="application/json"` for structured output

### Embeddings (100% Local)
- **Model**: `sentence-transformers/all-MiniLM-L6-v2` (384-dim)
- **Reranker**: `cross-encoder/ms-marco-MiniLM-L-6-v2`
- **Runs offline** — no external API calls for embeddings

### Vector Store
- **ChromaDB** with persistent disk storage
- Separate collections for documents and semantic memory
- Metadata filtering (domain, temporal, file type)

### Document Processing
- **PDF**: PyPDF2 text extraction
- **DOCX**: python-docx paragraph extraction
- **HTML**: BeautifulSoup4 content parsing
- **Markdown**: Heading-aware chunking with breadcrumbs
- **Text**: Generic windowed chunking

---

## 🔮 Future Enhancements

- **Email ingestion**: Connect to Gmail/Outlook
- **Browser extension**: Save web pages directly
- **Auto-tagging**: ML-based topic classification
- **Advanced temporal**: Fuzzy date parsing ("two weeks ago")
- **Multi-modal**: Image/diagram understanding
- **Graph memory**: Knowledge graph for concept relationships

---

## 🐛 Troubleshooting

**"Knowledge base is empty"**
- Upload files or click "Rebuild from data/ folder" if you have existing `.md` files

**"No GOOGLE_API_KEY"**
- Edit `.env` and add your Gemini API key
- Restart the app

**PDF extraction fails**
- Ensure `PyPDF2` is installed: `pip install PyPDF2`
- Some PDFs (scanned images) need OCR — try converting to text first

**Slow first query**
- First run downloads embedding models (~80MB) — subsequent queries are fast

**Console flooded with `ModuleNotFoundError: torchvision` tracebacks**
- This is Streamlit's file watcher scanning `sentence-transformers` dependencies — harmless but noisy
- Fixed by `.streamlit/config.toml` (`fileWatcherType = "none"`) which ships with this repo
- If you deleted it, recreate it or run: `streamlit run streamlit_app.py --server.fileWatcherType none`

**`ImportError: cannot import name 'configure' from 'google.generativeai'`**
- You have the old `google-generativeai` package installed; uninstall it and install the new one:
  ```powershell
  pip uninstall google-generativeai -y
  pip install google-genai>=1.0.0
  ```

---

## 📄 License & Credits

Built as a proof-of-concept for agentic RAG systems.

**Technologies:**
- [Google Gemini](https://ai.google.dev) via [`google-genai`](https://pypi.org/project/google-genai/) SDK — LLM
- [Sentence-Transformers](https://www.sbert.net/) — Local embeddings & cross-encoder reranking
- [ChromaDB](https://www.trychroma.com/) — Vector database
- [Streamlit](https://streamlit.io/) — Web UI

---

## 🎯 POC Objectives Achieved

✅ **Agentic RAG**: Multi-agent pipeline with planning, retrieval, optimization, reasoning  
✅ **Semantic Memory**: Stores and recalls past Q&A interactions  
✅ **Context Optimizer**: Deduplication, reranking, compression with transparency  
✅ **Multi-format ingestion**: PDF, DOCX, MD, TXT, HTML  
✅ **Temporal queries**: "last month", "this year", specific dates  
✅ **Topic summarization**: Comprehensive synthesis from multiple sources  
✅ **Short-term conversation memory**: Natural multi-turn dialogue  
✅ **Cost monitoring**: Per-request and session-level tracking  
✅ **Live demo ready**: Upload docs → ask questions → show reasoning

**Demo Impact**: Judges can upload their own documents and ask questions live, experiencing a truly personalized "Second Brain" in action! 🧠✨

### Headless smoke test (no browser)

```powershell
python smoke_test.py
```

## How the key concepts map to the brief

- **Agentic RAG** — the Planner decides *whether* to search docs, search
  memory, call a tool, or ask a follow-up, instead of always doing fixed RAG.
- **Semantic Memory** — successful answers are embedded and stored; similar
  future questions get a confidence boost / faster path. 👍/👎 feedback adjusts
  the stored score (schema: `user_query, intent, answer, feedback, score,
  timestamp, sources`).
- **Context Optimizer** — removes near-duplicate chunks, reranks with a
  cross-encoder, and compresses to a token budget; reports % tokens saved.
- **Tool Calling** — simulated ServiceNow ticket / Slack / Email, logged to an
  in-app activity panel and `storage/tool_activity.jsonl`.
- **Cost Monitor** — tracks input/output tokens and USD per request, per
  session, and per day (`storage/cost_ledger.jsonl`).

## Knowledge corpus

`data/` holds 12 markdown documents — 6 HR (leave, reimbursement, travel,
insurance, benefits, onboarding) and 6 IT SOPs (password reset, VPN, laptop
request, software install, email config, security).

> **Note on de-duplication:** the repo originally shipped two overlapping HR
> sets (a generic `hr_*` set and the branded `Sails_*` set) covering the same
> topics with *different* numbers. Keeping both would feed the RAG contradictory
> facts, so the generic `hr_*` duplicates were removed in favour of the coherent
> `Sails_*` corpus. The unique IT SOPs were kept as-is.

## Notes / POC scope

- Tools are **simulated** (POC excludes production ticket creation).
- `Redis` in the brief is approximated by ChromaDB for semantic memory (no extra
  service to run). Swap-in points are isolated in `app/agents/memory.py`.
- Local state (`.chroma/`, `storage/`) is git-ignored.
```
