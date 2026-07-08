# Cohort-2 AI POCs

A collection of Proof-of-Concept implementations demonstrating advanced AI/LLM patterns and architectures for enterprise applications.

---

## 📁 Repository Structure

```
Cohort-2-AI-POCs/
├── Ai Co-pilot/                    # Agentic RAG HR/IT Helpdesk
│   ├── app/                        # Core application modules
│   │   ├── agents/                 # Specialized AI agents
│   │   └── ...
│   ├── data/                       # Sample HR/IT policy documents
│   ├── storage/                    # Persistent data (costs, tools)
│   ├── CONCEPTS.md                 # Detailed technical deep-dive
│   └── README.md                   # Setup & usage guide
│
└── Pydantic-Validated Dynamic Tool Registry/   # PydanticAI Demos
    ├── calc pydantic agent.py      # Basic tool calling example
    └── Employee look up.py         # Comprehensive use-case demos
```

---

## 🤖 POC 1: AI Co-Pilot for HR/IT Helpdesk (Agentic RAG)

An intelligent helpdesk assistant that answers employee HR and IT questions using a multi-agent RAG architecture.

### Key Concepts Implemented

| Concept | Description | Why It Matters |
|---------|-------------|----------------|
| **Agentic RAG** | Multi-agent orchestration (Planner → Retriever → Optimizer → Reasoning) | Dynamic routing vs. fixed pipelines |
| **Semantic Memory** | Stores past Q&A pairs; recalls similar questions | Learns from experience; faster responses |
| **Context Optimizer** | Deduplication + Cross-encoder reranking + Compression | Reduces tokens by 40-60%; improves quality |
| **Tool Calling** | Simulated ServiceNow, Slack, Email integrations | Action-oriented AI beyond text generation |
| **Cost Monitor** | Per-call token/USD tracking with daily rollups | Financial transparency & optimization |

### Agent Pipeline

```
Query → Planner (intent/routing) → Memory Recall
                                 → Retriever (vector search)
                                 → Context Optimizer (rerank + compress)
                                 → Reasoning (grounded answer + citations)
                                 → Tool Execution (optional)
                                 → Memory Store
                                 → Cost Tracking
```

### Tech Stack

- **UI**: Streamlit
- **LLM**: Google Gemini (`gemini-2.0-flash`)
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` (local)
- **Reranking**: `ms-marco-MiniLM-L-6-v2` (local cross-encoder)
- **Vector DB**: ChromaDB (persistent, embedded)

### Quick Start

```powershell
cd '.\Ai Co-pilot\'
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Add GOOGLE_API_KEY to .env
streamlit run streamlit_app.py
```

📖 **[Detailed Concepts Documentation →](./Ai%20Co-pilot/CONCEPTS.md)**

---

## 🔧 POC 2: Pydantic-Validated Dynamic Tool Registry

Demonstrates building AI agents with **PydanticAI** framework and local LLMs via Ollama.

### Key Concepts Implemented

| Concept | Description | Example |
|---------|-------------|---------|
| **Basic Agent Chat** | Simple prompt → response | Python mentor agent |
| **Plain Tool Calling** | `@agent.tool_plain` decorator | Calculator (add, multiply) |
| **Structured Output** | Pydantic models as output type | Leave decision with risk level |
| **Dependency Injection** | `deps_type` + `RunContext` | Employee database lookup |
| **Message History** | Conversation memory | Multi-turn context retention |
| **Runtime Schema Override** | Dynamic `output_type` | Sentiment analysis |

### Use Cases Demonstrated

```python
# 1. Basic Chat
agent = Agent(MODEL, system_prompt="You are a Python mentor.")
result = agent.run_sync("Explain what an AI agent is.")

# 2. Tool Plain (Function Calling)
@calc_agent.tool_plain
def add(a: int, b: int) -> int:
    return a + b

# 3. Structured Output (Pydantic Validation)
class LeaveDecision(BaseModel):
    approved: bool
    reason: str
    risk_level: Literal["low", "medium", "high"]

result = policy_agent.run_sync("...", output_type=LeaveDecision)

# 4. Dependency Injection + Context-Aware Tools
@employee_agent.tool
def get_employee(ctx: RunContext[EmployeeDB], employee_id: int):
    return ctx.deps.records.get(employee_id)

# 5. Conversation Memory
second = agent.run_sync("What is my project?", message_history=first.all_messages())

# 6. Runtime Output Override
result = agent.run_sync("Classify sentiment", output_type=Sentiment)
```

### Tech Stack

- **Framework**: PydanticAI
- **LLM Backend**: Ollama (local) with `qwen3.5:4b`
- **Validation**: Pydantic v2

### Quick Start

```powershell
# Ensure Ollama is running with qwen3.5:4b
ollama run qwen3.5:4b

cd '.\Pydantic-Validated Dynamic Tool Registry\'
pip install pydantic-ai openai pydantic
python 'Employee look up.py'
```

---

## 🎯 Concepts Comparison

| Feature | AI Co-Pilot (Agentic RAG) | PydanticAI Tool Registry |
|---------|---------------------------|--------------------------|
| **Architecture** | Multi-agent orchestration | Single-agent patterns |
| **LLM** | Cloud (Gemini) | Local (Ollama) |
| **Memory** | Semantic memory (vector-based) | Message history (in-memory) |
| **Tools** | Simulated enterprise tools | Pydantic-validated functions |
| **Output Validation** | Manual parsing | Native Pydantic integration |
| **Focus** | Production-grade RAG | Framework patterns & validation |

---

## 📚 Learning Path

1. **Start with PydanticAI demos** to understand basic agent patterns
2. **Explore AI Co-Pilot** to see how patterns scale to production
3. **Read [CONCEPTS.md](./Ai%20Co-pilot/CONCEPTS.md)** for deep architectural understanding

---

## 🔑 Key Takeaways

### Agentic RAG (AI Co-Pilot)
- **Planning** separates intent detection from execution
- **Semantic Memory** enables learning from past interactions
- **Context Optimization** dramatically reduces costs while improving quality
- **Agent Traces** provide transparency and debuggability

### PydanticAI (Tool Registry)
- **Type Safety** with Pydantic models ensures reliable outputs
- **Dependency Injection** enables clean architecture
- **Tool Registration** is declarative and intuitive
- **Local LLMs** (Ollama) enable offline/private deployment

---

## 📝 License

These POCs are for educational and demonstration purposes.
