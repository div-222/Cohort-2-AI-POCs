# AI Co-Pilot for Internal HR / IT Helpdesk — Agentic RAG POC

A locally-runnable web app that answers employee HR & IT questions by reasoning
over the company's policy/SOP corpus. It implements the concepts from the
requirements brief: **Agentic RAG**, **Semantic Memory**, a **Context
Optimizer**, simulated **Tool Calling**, and a **Cost Monitor**.

> Built for *Sails Software Solutions* internal helpdesk content. LLM:
> **Google Gemini** (via a GCP/AI-Studio API key). Embeddings & reranking run
> **fully locally** (sentence-transformers), so retrieval works offline.

---

## What it does

Ask a question like *"How many earned leaves do I get?"* or *"How do I reset my
VPN password?"* and a pipeline of cooperating agents produces a grounded,
cited answer — and can raise a (simulated) ServiceNow ticket when you ask.

Every answer ships with a transparent **agent trace**, the **sources** used,
the **token savings** from the Context Optimizer, and the **cost** of the
request.

## Architecture — the agent pipeline

```
            ┌─────────────┐
 question → │  Planner    │  intent (HR/IT/TOOL/GENERAL) + execution plan
            └──────┬──────┘
                   │
        ┌──────────┼───────────────┐
        ▼          ▼               ▼
 ┌────────────┐ ┌────────────┐ (plan says tool?)
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
       └────▶│ Reasoning  │  grounded answer + citations
             └─────┬──────┘
                   ▼
             ┌────────────┐      ┌──────────────┐
             │ Tool Agent │ ───▶ │ Cost Monitor │  (wraps every LLM call)
             │ (simulated)│      └──────────────┘
             └─────┬──────┘
                   ▼
            store interaction → Semantic Memory
```

| Agent | File | Responsibility |
|-------|------|----------------|
| Planner | `app/agents/planner.py` | Intent detection + routing (LLM JSON, with keyword fallback) |
| Retriever | `app/agents/retriever.py` | Domain-filtered vector search |
| Context Optimizer | `app/agents/context_optimizer.py` | Dedup, cross-encoder rerank, compression + token-savings report |
| Memory | `app/agents/memory.py` | Store/recall successful Q&A (semantic similarity), feedback scoring |
| Reasoning | `app/agents/reasoning.py` | Grounded answer with inline citations |
| Tool | `app/agents/tools.py` | Simulated ServiceNow / Slack / Email |
| Cost Monitor | `app/agents/cost_monitor.py` | Per-call & per-day token/USD tracking |
| Orchestrator | `app/orchestrator.py` | Runs the loop, builds the trace |

## Tech stack

- **UI:** Streamlit (localhost web app)
- **LLM:** Google Gemini (`google-generativeai`)
- **Embeddings/Rerank:** `sentence-transformers` (MiniLM bi-encoder + MS-MARCO cross-encoder) — local
- **Vector store / memory:** ChromaDB (persistent, on disk)

## Setup

```powershell
# 1. (recommended) create a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. install deps  (first run downloads ~small ST models on first query)
pip install -r requirements.txt

# 3. add your Gemini key
Copy-Item .env.example .env
#   then edit .env and set GOOGLE_API_KEY=...
```

> No key? The app still runs in **extractive mode**: it retrieves and optimizes
> context and shows the relevant policy excerpts, but won't synthesize prose.

## Run

```powershell
streamlit run streamlit_app.py
```

Then in the browser:
1. Click **🔁 (Re)build index** in the sidebar (one-time; chunks + embeds the corpus).
2. Ask a question or click an example chip.

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

---

## 📖 Deep Dive Documentation

For a comprehensive technical explanation of all concepts, algorithms, and design patterns used in this POC, see:

**[CONCEPTS.md →](./CONCEPTS.md)**

This document covers:
- Agentic RAG architecture and agent pipeline
- Semantic Memory implementation and feedback loops
- Context Optimizer's 3-stage pipeline (dedup → rerank → compress)
- Tool calling patterns and safety features
- Cost monitoring and token tracking
- Vector database design with ChromaDB
- Embedding and cross-encoder reranking details
- Document ingestion and chunking strategies
- Design patterns (Pipeline, Strategy, Singleton, etc.)
```
