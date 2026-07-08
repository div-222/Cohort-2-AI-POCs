# AI Agentic Engineering Journey — Cohort-2 POCs

A curated collection of Proof-of-Concept implementations charting a progressive learning path through **AI Agentic Engineering** — from foundational agent patterns to production-grade multi-agent orchestration systems.

---

## 🎯 Purpose of This Repository

This repository serves as a **hands-on learning lab** for mastering modern AI agent development. Each POC builds upon core agentic engineering principles, demonstrating how to:

- **Design autonomous AI agents** that reason, plan, and execute tasks
- **Implement tool-calling patterns** for action-oriented AI systems
- **Build memory systems** that enable agents to learn from interactions
- **Optimize context and costs** for production deployment
- **Orchestrate multi-agent pipelines** for complex workflows

The projects progress from **foundational single-agent patterns** to **enterprise-grade multi-agent architectures**, providing a complete curriculum for AI agent development.

---

## 🧭 What is AI Agentic Engineering?

AI Agentic Engineering is the discipline of designing systems where LLMs act as **autonomous agents** — capable of:

| Capability | Description | Example |
|------------|-------------|---------|
| **Reasoning** | Breaking down complex problems into steps | Planner determining search strategy |
| **Tool Use** | Invoking external functions/APIs | Creating tickets, sending emails |
| **Memory** | Retaining context across interactions | Recalling past similar questions |
| **Planning** | Multi-step execution strategies | Intent detection → retrieval → synthesis |
| **Reflection** | Self-correction and optimization | Context deduplication and reranking |

### The Agentic Spectrum

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AI AGENT COMPLEXITY SPECTRUM                          │
├──────────────────┬──────────────────┬──────────────────┬────────────────────┤
│   BASIC CHAT     │   TOOL-CALLING   │   RAG + MEMORY   │   MULTI-AGENT      │
│                  │                  │                  │   ORCHESTRATION    │
│  prompt → text   │  prompt → tool   │  query → retrieve│   plan → delegate  │
│                  │  → execute       │  → reason        │   → coordinate     │
│                  │  → respond       │  → remember      │   → synthesize     │
├──────────────────┴──────────────────┴──────────────────┴────────────────────┤
│  POC 2: Basics ─────────────────────────────────────► POC 1: Production     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
Cohort-2-AI-POCs/
│
├── Pydantic-Validated Dynamic Tool Registry/   # POC 2: Foundation Patterns
│   ├── calc pydantic agent.py      # Basic tool calling introduction
│   └── Employee look up.py         # 6 progressive use-case demos
│
└── Ai Co-pilot/                    # POC 1: Production Multi-Agent System
    ├── app/                        # Core application modules
    │   ├── agents/                 # Specialized AI agents
    │   │   ├── planner.py          # Intent detection & routing
    │   │   ├── retriever.py        # Vector search agent
    │   │   ├── context_optimizer.py # Dedup + rerank + compress
    │   │   ├── reasoning.py        # Grounded answer synthesis
    │   │   ├── memory.py           # Semantic memory system
    │   │   ├── tools.py            # Simulated enterprise tools
    │   │   └── cost_monitor.py     # Token/USD tracking
    │   ├── orchestrator.py         # Multi-agent coordinator
    │   ├── vectorstore.py          # ChromaDB integration
    │   └── llm.py                  # Gemini LLM wrapper
    ├── data/                       # Sample HR/IT policy documents
    ├── storage/                    # Persistent data (costs, tools)
    ├── CONCEPTS.md                 # Detailed technical deep-dive
    └── README.md                   # Setup & usage guide
```

---

## 🚀 Learning Path: From Foundations to Production

### Recommended Progression

```
Step 1                          Step 2                          Step 3
┌─────────────────┐             ┌─────────────────┐             ┌─────────────────┐
│ PydanticAI Demo │────────────▶│  AI Co-Pilot    │────────────▶│   CONCEPTS.md   │
│ (Basic Patterns)│             │ (Multi-Agent)   │             │  (Deep Dive)    │
└─────────────────┘             └─────────────────┘             └─────────────────┘
     Learn:                          Apply:                         Master:
 • Tool calling                  • Agent orchestration          • Architecture decisions
 • Structured output             • Semantic memory              • Optimization strategies
 • Dependency injection          • Context optimization         • Production patterns
 • Message history               • Cost monitoring              • Scale considerations
```

---

## 🔧 POC 2: PydanticAI Tool Registry — Foundation Patterns

**Start here** to build foundational understanding of AI agent capabilities with the **PydanticAI** framework.

### Project Purpose

This POC demonstrates **6 essential agent patterns** that form the building blocks for more complex systems. Using **local LLMs via Ollama**, it provides a safe sandbox to experiment with agent behaviors.

### Core Agentic Engineering Concepts

| Pattern | Concept | What You Learn |
|---------|---------|----------------|
| **Basic Chat** | Agent instantiation | How to create and configure an LLM-backed agent |
| **Tool Plain** | Function calling | Enabling agents to execute Python functions |
| **Structured Output** | Schema validation | Forcing LLM outputs to conform to Pydantic models |
| **Dependency Injection** | Context awareness | Passing external data sources to agent tools |
| **Message History** | Conversation memory | Maintaining context across multiple turns |
| **Runtime Override** | Dynamic behavior | Changing output schemas at execution time |

### Implementation Highlights

```python
# Pattern 1: Basic Agent — Foundation of all agents
agent = Agent(MODEL, system_prompt="You are a Python mentor.")
result = agent.run_sync("Explain what an AI agent is.")

# Pattern 2: Tool Calling — Enabling agent actions
@calc_agent.tool_plain
def add(a: int, b: int) -> int:
    """Tools give agents the ability to ACT, not just respond."""
    return a + b

# Pattern 3: Structured Output — Reliable, typed responses
class LeaveDecision(BaseModel):
    approved: bool
    reason: str
    risk_level: Literal["low", "medium", "high"]

result = policy_agent.run_sync(query, output_type=LeaveDecision)
# result.output is guaranteed to be a valid LeaveDecision instance

# Pattern 4: Dependency Injection — Clean data access
@employee_agent.tool
def get_employee(ctx: RunContext[EmployeeDB], employee_id: int):
    """RunContext provides type-safe access to injected dependencies."""
    return ctx.deps.records.get(employee_id)

# Pattern 5: Message History — Multi-turn context
second = agent.run_sync("What is my project?", 
                        message_history=first.all_messages())

# Pattern 6: Runtime Schema Override — Flexible agents
result = versatile_agent.run_sync(text, output_type=Sentiment)
```

### Tech Stack

| Component | Technology | Why |
|-----------|------------|-----|
| **Framework** | PydanticAI | Type-safe agent framework with native Pydantic integration |
| **LLM** | Ollama (`qwen3.5:4b`) | Local inference for privacy and offline development |
| **Validation** | Pydantic v2 | Industry-standard schema validation |

### Quick Start

```powershell
# 1. Start Ollama with the required model
ollama run qwen3.5:4b

# 2. Navigate and install
cd '.\Pydantic-Validated Dynamic Tool Registry\'
pip install pydantic-ai openai pydantic

# 3. Run the comprehensive demo
python 'Employee look up.py'
```

---

## 🤖 POC 1: AI Co-Pilot — Production Multi-Agent System

**Advance here** after mastering foundational patterns. This POC demonstrates how individual agent patterns **compose into production-grade systems**.

### Project Purpose

Build an intelligent HR/IT helpdesk assistant using **Agentic RAG** — a multi-agent architecture where specialized agents collaborate to produce accurate, grounded, and cost-efficient answers.

### Why Multi-Agent Architecture?

| Traditional RAG | Agentic RAG (This POC) |
|-----------------|------------------------|
| Fixed pipeline | **Dynamic routing** via intelligent Planner |
| Stateless | **Semantic memory** learns from interactions |
| Raw context chunks | **Optimized context** (deduplicated, reranked, compressed) |
| Black box | **Full transparency** with agent traces |
| Cost-unaware | **Per-request cost tracking** |
| Text-only | **Tool integration** (tickets, emails, notifications) |

### Agent Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER QUERY                                         │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  PLANNER AGENT                                                               │
│  • Intent Classification (HR / IT / TOOL / GENERAL)                          │
│  • Execution Plan Generation                                                 │
│  • Domain Filter Decision                                                    │
│  • Tool Invocation Decision                                                  │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│ SEMANTIC MEMORY │    │ RETRIEVER AGENT     │    │ TOOL AGENT          │
│                 │    │                     │    │                     │
│ • Recall past   │    │ • Vector similarity │    │ • ServiceNow ticket │
│   similar Q&A   │    │ • Domain filtering  │    │ • Slack notify      │
│ • Confidence    │    │ • Top-K retrieval   │    │ • Email send        │
│   thresholding  │    │                     │    │                     │
└────────┬────────┘    └──────────┬──────────┘    └──────────┬──────────┘
         │                        │                          │
         │                        ▼                          │
         │             ┌─────────────────────┐               │
         │             │ CONTEXT OPTIMIZER   │               │
         │             │                     │               │
         │             │ • Deduplication     │               │
         │             │ • Cross-encoder     │               │
         │             │   reranking         │               │
         │             │ • Compression       │               │
         │             │ • Token savings     │               │
         │             └──────────┬──────────┘               │
         │                        │                          │
         └────────────────────────┼──────────────────────────┘
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  REASONING AGENT                                                             │
│  • Grounded answer synthesis                                                 │
│  • Inline source citations                                                   │
│  • Fallback handling                                                         │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
┌─────────────────────┐                         ┌─────────────────────┐
│ MEMORY STORE        │                         │ COST MONITOR        │
│                     │                         │                     │
│ • Store successful  │                         │ • Token counting    │
│   Q&A pairs         │                         │ • USD estimation    │
│ • Feedback scoring  │                         │ • Daily rollups     │
│ • Future recall     │                         │ • Optimization      │
└─────────────────────┘                         └─────────────────────┘
```

### Key Agentic Engineering Concepts

| Concept | Implementation | Business Value |
|---------|----------------|----------------|
| **Agentic RAG** | Multi-agent orchestration with dynamic routing | Intelligent, context-aware responses |
| **Semantic Memory** | ChromaDB-backed Q&A storage with similarity recall | System learns and improves over time |
| **Context Optimizer** | Dedup + cross-encoder rerank + compression | 40-60% token reduction, better accuracy |
| **Tool Calling** | Simulated ServiceNow, Slack, Email integrations | Action-oriented AI beyond text generation |
| **Cost Monitor** | Per-call token/USD tracking with daily rollups | Financial transparency & optimization |
| **Agent Traces** | Full execution path logging | Debugging, compliance, explainability |

### Tech Stack

| Component | Technology | Why |
|-----------|------------|-----|
| **UI** | Streamlit | Rapid prototyping, interactive debugging |
| **LLM** | Google Gemini (`gemini-2.0-flash`) | Production-grade, cost-effective |
| **Embeddings** | `all-MiniLM-L6-v2` (local) | Offline-capable, zero cloud cost |
| **Reranking** | `ms-marco-MiniLM-L-6-v2` (local) | Quality boost without API calls |
| **Vector DB** | ChromaDB (persistent) | Embedded, no infrastructure |

### Quick Start

```powershell
# 1. Setup environment
cd '.\Ai Co-pilot\'
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key
# Create .env file with: GOOGLE_API_KEY=your_key_here

# 4. Launch application
streamlit run streamlit_app.py

# 5. In browser: Click "🔁 (Re)build index" in sidebar (one-time)
# 6. Ask questions or click example chips
```

📖 **[Detailed Technical Deep-Dive → CONCEPTS.md](./Ai%20Co-pilot/CONCEPTS.md)**

---

## 🎯 Concepts Comparison Matrix

| Dimension | POC 2: PydanticAI Foundations | POC 1: AI Co-Pilot Production |
|-----------|-------------------------------|-------------------------------|
| **Complexity** | Single-agent patterns | Multi-agent orchestration |
| **LLM** | Local (Ollama) | Cloud (Gemini) |
| **Memory** | In-memory message history | Persistent semantic memory (vector DB) |
| **Tools** | Pydantic-validated functions | Simulated enterprise integrations |
| **Output** | Native Pydantic validation | Manual parsing + validation |
| **Context** | Direct prompt | Optimized (dedup + rerank + compress) |
| **Cost** | N/A (local) | Per-request tracking |
| **Transparency** | Return values | Full agent traces |
| **Focus** | Pattern learning | Production architecture |

---

## 🔑 Key Takeaways by Concept

### Agent Orchestration
- **Single Agent**: Good for focused tasks; simple to debug
- **Multi-Agent**: Essential for complex workflows; requires careful coordination
- **Planner Pattern**: Separating "what to do" from "how to do it" enables flexibility

### Memory Systems
- **Message History**: Simple; perfect for session-scoped context
- **Semantic Memory**: Enables learning across sessions; requires vector storage
- **Memory Recall**: Similarity thresholding prevents irrelevant retrievals

### Tool Integration
- **Tool Plain**: Stateless functions; ideal for calculations, transformations
- **Context Tools**: Access to dependencies; essential for data-driven operations
- **Enterprise Tools**: Real-world actions (tickets, notifications); requires careful error handling

### Output Quality
- **Structured Output**: Eliminates parsing errors; enables downstream processing
- **Context Optimization**: Better input = better output; reduces costs simultaneously
- **Grounding**: Citations build trust; enable verification

### Production Readiness
- **Cost Monitoring**: Essential for budget management and optimization
- **Agent Traces**: Required for debugging, compliance, and user trust
- **Fallback Handling**: Graceful degradation ensures reliability

---

## 📚 Additional Resources

### Within This Repository
- [AI Co-Pilot CONCEPTS.md](./Ai%20Co-pilot/CONCEPTS.md) — Deep architectural analysis
- [AI Co-Pilot README.md](./Ai%20Co-pilot/README.md) — Detailed setup and usage

### External Learning
- [PydanticAI Documentation](https://ai.pydantic.dev/)
- [LangChain Agent Concepts](https://python.langchain.com/docs/concepts/agents/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)

---

## 📝 License

These POCs are for educational and demonstration purposes within the AI Agentic Engineering learning cohort.
