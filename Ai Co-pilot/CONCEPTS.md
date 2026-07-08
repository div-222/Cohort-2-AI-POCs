# AI Co-Pilot POC — Concepts & Technical Deep Dive

This document provides an in-depth explanation of all concepts, design patterns, and architectural decisions implemented in the AI Co-Pilot for Internal HR/IT Helpdesk POC.

---

## Table of Contents

1. [Overview](#overview)
2. [Core Concepts](#core-concepts)
   - [Agentic RAG Architecture](#1-agentic-rag-architecture)
   - [Semantic Memory](#2-semantic-memory)
   - [Context Optimizer](#3-context-optimizer)
   - [Tool Calling](#4-tool-calling-function-calling)
   - [Cost Monitor](#5-cost-monitor)
3. [Agent Pipeline Deep Dive](#agent-pipeline-deep-dive)
   - [Planner Agent](#planner-agent)
   - [Retriever Agent](#retriever-agent)
   - [Reasoning Agent](#reasoning-agent)
   - [Memory Agent](#memory-agent)
   - [Orchestrator](#orchestrator)
4. [Technical Implementation Details](#technical-implementation-details)
   - [Vector Database (ChromaDB)](#vector-database-chromadb)
   - [Embeddings & Reranking](#embeddings--reranking)
   - [LLM Integration (Gemini)](#llm-integration-gemini)
   - [Document Ingestion Pipeline](#document-ingestion-pipeline)
5. [Design Patterns Used](#design-patterns-used)
6. [Key Algorithms](#key-algorithms)

---

## Overview

The AI Co-Pilot is a locally-runnable web application that implements an **Agentic RAG (Retrieval-Augmented Generation)** system. Unlike traditional RAG pipelines that simply retrieve and generate, this implementation uses a multi-agent architecture where specialized agents collaborate to produce accurate, grounded, and cost-efficient answers.

### Key Differentiators

| Feature | Traditional RAG | Agentic RAG (This POC) |
|---------|----------------|------------------------|
| Decision Making | Fixed pipeline | Dynamic routing via Planner |
| Memory | Stateless | Semantic memory of past interactions |
| Context Quality | Raw chunks | Optimized, deduplicated, reranked |
| Transparency | Black box | Full agent trace visible |
| Cost Awareness | None | Per-request cost tracking |
| Tool Integration | None | Simulated enterprise tools |

---

## Core Concepts

### 1. Agentic RAG Architecture

**What is it?**

Agentic RAG extends the basic RAG paradigm by adding an intelligent orchestration layer. Instead of a linear retrieve-then-generate flow, multiple specialized agents collaborate, making decisions about:

- **What to search** (documents, memory, or both)
- **How to search** (domain filtering, semantic similarity)
- **What to return** (grounded answers, follow-up questions, or tool actions)

**How it works in this POC:**

```
User Query
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ PLANNER AGENT                                           │
│ • Intent Classification (HR/IT/TOOL/GENERAL)            │
│ • Execution Plan Generation                             │
│ • Domain Filter Decision                                │
│ • Tool Invocation Decision                              │
└────────────────────────────┬────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
    ┌─────────┐        ┌──────────┐        ┌──────────┐
    │ MEMORY  │        │ RETRIEVER│        │ TOOL     │
    │ RECALL  │        │ SEARCH   │        │ DISPATCH │
    └────┬────┘        └────┬─────┘        └────┬─────┘
         │                  │                   │
         │                  ▼                   │
         │         ┌────────────────┐           │
         │         │CONTEXT OPTIMIZER│          │
         │         │• Deduplication  │          │
         │         │• Reranking      │          │
         │         │• Compression    │          │
         │         └───────┬────────┘           │
         │                 │                    │
         └─────────────────┼────────────────────┘
                           ▼
                  ┌────────────────┐
                  │ REASONING      │
                  │ AGENT          │
                  │ • Grounded     │
                  │   Answer       │
                  │ • Citations    │
                  └───────┬────────┘
                          │
                          ▼
                  ┌────────────────┐
                  │ SEMANTIC       │
                  │ MEMORY STORE   │
                  │ (for future    │
                  │  recall)       │
                  └───────┬────────┘
                          │
                          ▼
                  ┌────────────────┐
                  │ COST MONITOR   │
                  │ • Token Count  │
                  │ • USD Cost     │
                  └────────────────┘
```

**Key Benefits:**
- **Intelligent Routing**: Questions go to the right subsystem
- **Fallback Handling**: LLM-free operation with keyword fallback
- **Transparency**: Every decision is logged and visible

---

### 2. Semantic Memory

**What is it?**

Semantic Memory enables the system to remember successful past interactions and use them to answer similar future questions faster and with higher confidence. It's analogous to how a support agent builds expertise over time.

**Technical Implementation:**

```python
# Memory Schema (stored in ChromaDB)
{
    "user_query": "How many earned leaves do I get?",
    "intent": "HR",
    "answer": "You are entitled to 18 earned leaves per year...",
    "feedback": "up",  # 👍 or 👎 from user
    "score": 1.0,       # Confidence score (adjusts with feedback)
    "timestamp": "2024-01-15T10:30:00Z",
    "sources": "Leave Policy | Benefits Guide"
}
```

**How it works:**

1. **Query Embedding**: User's question is converted to a vector
2. **Similarity Search**: Find past Q&A pairs with similar questions
3. **Confidence Thresholding**: Only use memory if similarity > 0.86
4. **Answer Boosting**: High-confidence hits influence the final answer
5. **Feedback Loop**: User ratings adjust stored scores

**Benefits:**
- Faster responses for common questions
- Improved accuracy through learned patterns
- Self-improving system

---

### 3. Context Optimizer

**What is it?**

The Context Optimizer transforms raw retrieved chunks into a lean, high-signal context before feeding it to the reasoning LLM. This reduces token usage, improves answer quality, and lowers costs.

**Three-Stage Pipeline:**

#### Stage 1: Deduplication

**Problem**: Retrieved chunks often have overlapping content due to chunking overlap or similar document sections.

**Solution**: Use embedding cosine similarity to detect near-duplicates:

```python
def _dedup(chunks):
    kept = []
    kept_vecs = []
    for chunk, vec in zip(chunks, vectors):
        # If this chunk is >93% similar to any kept chunk, skip it
        if any(cosine(vec, kv) >= 0.93 for kv in kept_vecs):
            continue
        kept.append(chunk)
        kept_vecs.append(vec)
    return kept
```

#### Stage 2: Cross-Encoder Reranking

**Problem**: Bi-encoder (embedding) similarity isn't optimal for relevance ranking.

**Solution**: Use a cross-encoder model that jointly processes query-document pairs:

```python
# MS-MARCO Cross-Encoder: More accurate relevance scoring
scores = cross_encoder.predict([
    [query, doc1],
    [query, doc2],
    [query, doc3]
])
# Sort chunks by relevance score
chunks.sort(key=lambda c: c['rerank_score'], reverse=True)
```

**Why Cross-Encoder > Bi-Encoder for ranking:**
| Aspect | Bi-Encoder | Cross-Encoder |
|--------|-----------|---------------|
| Speed | Fast (single encoding) | Slower (pairwise) |
| Accuracy | Good | Excellent |
| Use Case | Initial retrieval | Final ranking |

#### Stage 3: Context Compression

**Problem**: LLMs have context limits; more tokens = more cost.

**Solution**: Keep top-N chunks within a character budget:

```python
RERANK_TOP_N = 4           # Keep best 4 chunks
MAX_CONTEXT_CHARS = 6000   # Hard cap

final_chunks = []
chars_used = 0
for chunk in ranked_chunks[:RERANK_TOP_N]:
    if chars_used + len(chunk) > MAX_CONTEXT_CHARS:
        # Truncate at word boundary
        remaining = MAX_CONTEXT_CHARS - chars_used
        chunk = chunk[:remaining].rsplit(' ', 1)[0] + ' …'
    final_chunks.append(chunk)
    chars_used += len(chunk)
```

**Token Savings Report:**
```
Chunks: 8 → 4
Tokens: 1,240 → 520
Saved: 58.1%
```

---

### 4. Tool Calling (Function Calling)

**What is it?**

Tool Calling enables the AI to take actions beyond generating text—raising tickets, sending notifications, triggering workflows. This POC implements a simulated tool layer that mimics enterprise integrations.

**Supported Tools:**

| Tool | Simulated Integration | Purpose |
|------|----------------------|---------|
| `create_ticket` | ServiceNow | Log IT/HR support requests |
| `send_slack` | Slack | Post to helpdesk channels |
| `send_email` | SMTP | Email notifications |

**How Tool Calling Works:**

```python
# 1. Planner detects tool intent via LLM
{
    "intent": "TOOL",
    "tool": {
        "name": "create_ticket",
        "reason": "user explicitly asked to raise a ticket",
        "args": {"summary": "Laptop won't power on", "priority": "High"}
    }
}

# 2. Tool Agent executes (simulated)
def create_ticket(summary, description, domain, priority):
    ticket_number = generate_ticket_id()  # e.g., INC1234567
    log_to_activity_file(result)
    return {
        "tool": "ServiceNow.create_ticket",
        "status": "created",
        "ticket_number": ticket_number,
        "assignment_group": "IT Service Desk"
    }
```

**Safety Features:**
- **Argument Filtering**: Only allowed kwargs are passed (defensive against LLM hallucination)
- **Default Values**: Safe defaults prevent incomplete tool calls
- **Activity Logging**: All tool actions are persisted for audit

---

### 5. Cost Monitor

**What is it?**

The Cost Monitor tracks every LLM API call's token usage and computes real-time USD costs. It provides transparency for development and helps identify optimization opportunities.

**Metrics Tracked:**

| Metric | Scope | Purpose |
|--------|-------|---------|
| Input Tokens | Per call, per request, per session | Measure prompt complexity |
| Output Tokens | Per call, per request, per session | Measure response length |
| USD Cost | All scopes | Financial tracking |
| Daily Rollups | Cross-session | Usage trends |

**Pricing Configuration:**

```python
PRICING = {
    "gemini-2.0-flash":      {"input": 0.10,  "output": 0.40},  # per 1M tokens
    "gemini-2.5-pro":        {"input": 1.25,  "output": 10.00},
}

# Cost calculation
cost = (input_tokens / 1_000_000 * input_price) + \
       (output_tokens / 1_000_000 * output_price)
```

**Persistence:**
```json
// storage/cost_ledger.jsonl
{"ts": "2024-01-15T10:30:00Z", "label": "planner", "model": "gemini-2.0-flash", 
 "input_tokens": 850, "output_tokens": 120, "cost_usd": 0.000133}
{"ts": "2024-01-15T10:30:01Z", "label": "reasoning", "model": "gemini-2.0-flash",
 "input_tokens": 1200, "output_tokens": 350, "cost_usd": 0.000260}
```

**Dashboard View:**
```
Session Cost:    $0.00039
Requests:        1
Input Tokens:    2,050
Output Tokens:   470
```

---

## Agent Pipeline Deep Dive

### Planner Agent

**File**: `app/agents/planner.py`

**Responsibility**: Intent detection + execution plan generation

**LLM Prompt Design:**

```python
SYSTEM = """You are the Planner in an internal HR/IT helpdesk co-pilot.
Classify the employee's query and produce a short execution plan.

Return STRICT JSON with this schema:
{
  "intent": "HR" | "IT" | "TOOL" | "GENERAL",
  "domain_filter": "HR" | "IT" | null,
  "search_documents": true|false,
  "search_memory": true|false,
  "tool": null | {"name": "...", "reason": "...", "args": {...}},
  "needs_followup": true|false,
  "followup_question": "",
  "rationale": "one sentence"
}
"""
```

**Fallback Mechanism:**

When the LLM is unavailable, the planner uses keyword matching:

```python
_IT_KW = ("password", "vpn", "laptop", "software", "email", ...)
_HR_KW = ("leave", "reimburse", "travel", "insurance", ...)
_TOOL_KW = ("raise a ticket", "create a ticket", ...)

def _fallback(query):
    if any(k in query for k in _TOOL_KW):
        return Plan(intent="TOOL", ...)
    elif any(k in query for k in _IT_KW):
        return Plan(intent="IT", ...)
    # ... etc
```

---

### Retriever Agent

**File**: `app/agents/retriever.py`

**Responsibility**: Domain-filtered vector search

**Key Features:**
- **Domain Filtering**: Restricts search to HR or IT documents based on Planner's decision
- **Graceful Fallback**: If filtered search returns nothing, retries without filter
- **Configurable Top-K**: Default 8 candidates for reranking

```python
def retrieve(query, domain_filter=None, top_k=8):
    where = {"domain": domain_filter} if domain_filter in ("HR", "IT") else None
    hits = vectorstore.query(query, top_k=top_k, where=where)
    
    # Fallback to unfiltered if no results
    if not hits and where:
        hits = vectorstore.query(query, top_k=top_k)
    
    return hits
```

---

### Reasoning Agent

**File**: `app/agents/reasoning.py`

**Responsibility**: Generate grounded, cited answers

**Prompt Engineering:**

```python
SYSTEM = """You are an internal HR/IT helpdesk co-pilot for employees of
Sails Software Solutions. Answer ONLY from the provided context snippets.

Rules:
- Be concise, accurate, and practical. Use short paragraphs or bullet points.
- Cite the source document(s) inline like [Leave Policy] using the snippet titles.
- If the context does not contain the answer, say so plainly and suggest
  raising a ticket — do NOT guess policy numbers or steps.
- For IT how-to questions, give clear numbered steps.
"""
```

**Context Formatting:**
```
[1] Leave Policy — Earned Leave
Employees are entitled to 18 earned leaves per year...

[2] Leave Policy — Carry Forward
Unused earned leaves can be carried forward up to a maximum of...

Employee question: How many earned leaves do I get and can I carry them forward?

Answer grounded in the context, with inline source citations.
```

---

### Memory Agent

**File**: `app/agents/memory.py`

**Responsibility**: Store/recall past successful Q&A interactions

**Operations:**

| Function | Description |
|----------|-------------|
| `store()` | Persist a successful Q&A pair |
| `recall()` | Find similar past interactions |
| `best_hit()` | Get top match if confidence > threshold |
| `update_feedback()` | Adjust scores based on 👍/👎 |

**Score Adjustment Algorithm:**
```python
def update_feedback(mem_id, feedback):
    score = current_score
    if feedback == "up":      # 👍
        score = min(1.0, score + 0.1)  # Boost confidence
    else:                     # 👎
        score = max(0.0, score - 0.4)  # Significant penalty
```

---

### Orchestrator

**File**: `app/orchestrator.py`

**Responsibility**: Coordinates all agents into a unified loop

**Execution Flow:**

```python
def ask(query):
    trace = []
    
    # 1. PLANNING
    plan, usage = planner.plan(query)
    cost.record(usage)
    trace.append(f"🧭 Planner: intent={plan.intent}")
    
    # 2. MEMORY RECALL
    if settings["use_memory"]:
        memory_hit = memory.best_hit(query)
        if memory_hit:
            trace.append(f"🧠 Memory hit (sim={memory_hit['similarity']})")
    
    # 3. RETRIEVAL
    chunks = retriever.retrieve(query, domain_filter=plan.domain_filter)
    trace.append(f"📚 Retrieved {len(chunks)} chunks")
    
    # 4. CONTEXT OPTIMIZATION
    if settings["use_optimizer"]:
        report = context_optimizer.optimize(query, chunks)
        chunks = report.chunks
        trace.append(f"✨ Optimized: {report.saved_pct}% tokens saved")
    
    # 5. REASONING
    answer, usage = reasoning.answer(query, chunks, memory_hit)
    cost.record(usage)
    
    # 6. TOOL EXECUTION
    if plan.tool and settings["allow_tools"]:
        tool_result = tools.execute(plan.tool, query)
        trace.append(f"🛠️ Tool: {tool_result['status']}")
    
    # 7. MEMORY STORAGE
    memory.store(query, plan.intent, answer, sources)
    
    return CoPilotResponse(answer=answer, trace=trace, ...)
```

---

## Technical Implementation Details

### Vector Database (ChromaDB)

**File**: `app/vectorstore.py`

**Collections:**

| Collection | Purpose | Embedding Source |
|------------|---------|------------------|
| `documents` | Chunked HR/IT policy corpus | Local sentence-transformers |
| `memory` | Past Q&A interactions | Local sentence-transformers |

**Key Configuration:**
```python
# HNSW index with cosine distance
collection.create(metadata={"hnsw:space": "cosine"})
```

**Why ChromaDB?**
- Persistent (survives restarts)
- Embedded (no external server needed)
- Supports metadata filtering
- Python-native

---

### Embeddings & Reranking

**File**: `app/embeddings.py`

**Models Used:**

| Model | Type | Purpose | Size |
|-------|------|---------|------|
| `all-MiniLM-L6-v2` | Bi-encoder | Fast embedding | 80MB |
| `ms-marco-MiniLM-L-6-v2` | Cross-encoder | Accurate reranking | 80MB |

**Lazy Loading:**
```python
_embedder = None

def _get_embedder():
    global _embedder
    if _embedder is None:
        from sentence_transformers import SentenceTransformer
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedder
```

**Embedding Normalization:**
```python
vecs = model.encode(texts, normalize_embeddings=True)
# Normalized vectors enable direct dot-product similarity
```

---

### LLM Integration (Gemini)

**File**: `app/llm.py`

**Key Features:**
- JSON mode for structured Planner output
- Temperature control per use case
- Token usage extraction for cost tracking
- Graceful error handling with user-friendly messages

**Error Categories:**
```python
def friendly_error(exc):
    msg = str(exc).lower()
    if "api key not valid" in msg:
        return "Gemini API key is invalid..."
    if "quota" in msg or "429" in msg:
        return "Gemini quota/rate limit hit..."
    if "permission" in msg or "403" in msg:
        return "Gemini permission denied..."
```

---

### Document Ingestion Pipeline

**File**: `app/ingest.py`

**Process:**

1. **Read Markdown Files**: From `data/` directory
2. **Domain Classification**: Based on filename prefix (`it_` → IT, else → HR)
3. **Heading-Aware Chunking**: Preserve section boundaries
4. **Window Sub-Splitting**: Large sections split with overlap
5. **Metadata Attachment**: Source, title, domain, heading
6. **Embedding + Storage**: Into ChromaDB

**Chunking Strategy:**
```
CHUNK_SIZE = 900        # Target characters per chunk
CHUNK_OVERLAP = 150     # Overlap between consecutive chunks
```

**Heading-Based Splitting:**
```python
def _split_by_headings(md):
    """Return (heading_breadcrumb, section_text) tuples."""
    # Detects: # H1, ## H2, ### H3, #### H4
    # Maintains breadcrumb: "Leave Policy > Earned Leave > Carry Forward"
```

---

## Design Patterns Used

### 1. **Pipeline Pattern**
The orchestrator implements a pipeline of agents, each transforming the data.

### 2. **Strategy Pattern**
Different agents can be enabled/disabled via settings toggles.

### 3. **Singleton Pattern**
Embedding models and ChromaDB client are module-level singletons.

### 4. **Decorator Pattern**
Cost tracking wraps every LLM call transparently.

### 5. **Facade Pattern**
`CoPilot` class provides a unified interface to the agent ecosystem.

### 6. **Repository Pattern**
`vectorstore.py` abstracts all database operations.

---

## Key Algorithms

### Cosine Similarity for Deduplication
```python
def cosine(a, b):
    return sum(x * y for x, y in zip(a, b))  # Works because vectors are normalized
```

### Token Estimation
```python
def approx_tokens(text):
    return max(1, len(text) // 4)  # ~4 chars per English token
```

### Confidence-Based Memory Hit
```python
MEMORY_HIT_THRESHOLD = 0.86

def best_hit(query):
    hits = recall(query, top_k=1)
    if hits and hits[0]["similarity"] >= MEMORY_HIT_THRESHOLD:
        return hits[0]
    return None
```

---

## Summary

This POC demonstrates a production-grade architecture for building intelligent, transparent, and cost-aware AI assistants. The key innovations are:

1. **Multi-Agent Collaboration**: Specialized agents with clear responsibilities
2. **Hybrid Retrieval**: Bi-encoder search + cross-encoder reranking
3. **Learning System**: Semantic memory improves over time
4. **Cost Transparency**: Every token is tracked and priced
5. **Graceful Degradation**: Works without LLM using keyword fallbacks
6. **Full Observability**: Agent traces show decision reasoning

These patterns are directly applicable to enterprise AI deployments where accuracy, cost control, and auditability are critical.
