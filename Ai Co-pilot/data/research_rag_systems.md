# Research Notes: Retrieval-Augmented Generation (RAG)

*Date: February 2026*

## What is RAG?

RAG combines the generative capabilities of LLMs with external knowledge retrieval. Instead of relying solely on parametric knowledge (what's in the model weights), RAG systems:

1. **Retrieve** relevant documents from an external corpus
2. **Augment** the prompt with retrieved context
3. **Generate** a response grounded in the retrieved information

## Architecture Components

### 1. Document Store
- Vector database (Pinecone, Weaviate, ChromaDB, Qdrant)
- Traditional search (Elasticsearch, Solr)
- Hybrid approaches combining both

### 2. Retriever
- **Dense retrieval**: Bi-encoder models (BERT, Sentence-Transformers)
- **Sparse retrieval**: BM25, TF-IDF
- **Hybrid retrieval**: Combining dense + sparse with score fusion

### 3. Generator
- Any LLM (GPT-4, Claude, Gemini, Llama)
- Instruction-tuned models work best
- Context window size is critical (longer = better)

## Advantages of RAG

1. **Up-to-date information**: Update the corpus without retraining
2. **Reduced hallucination**: Answers grounded in retrieved facts
3. **Citation/Attribution**: Can point to source documents
4. **Domain adaptation**: Add domain-specific knowledge easily
5. **Interpretability**: Show which documents influenced the answer

## Challenges and Solutions

### Challenge: Retrieval Quality
- **Problem**: Irrelevant or low-quality documents retrieved
- **Solutions**:
  - Reranking with cross-encoders (more expensive but accurate)
  - Query expansion and reformulation
  - Hybrid retrieval (dense + sparse)
  - Metadata filtering

### Challenge: Context Window Limits
- **Problem**: Too many documents exceed LLM context limit
- **Solutions**:
  - Document compression/summarization
  - Iterative refinement (multiple passes)
  - Hierarchical retrieval (rough → fine)

### Challenge: Conflicting Information
- **Problem**: Retrieved documents contradict each other
- **Solutions**:
  - Confidence scoring
  - Temporal ordering (prefer recent)
  - Majority voting across sources

## Advanced RAG Patterns

### Agentic RAG
Multiple agents handle different aspects:
- **Planner**: Decides what to retrieve
- **Retriever**: Executes search
- **Reranker**: Scores and filters results
- **Summarizer**: Compresses context
- **Generator**: Produces final answer

Benefits: More transparent, optimizable, controllable

### HyDE (Hypothetical Document Embeddings)
1. Generate a hypothetical answer to the query
2. Embed the hypothetical answer
3. Search for documents similar to the hypothetical answer
4. Use retrieved documents to generate actual answer

Surprisingly effective! The "fake" answer helps find better real documents.

### Self-RAG
Model decides:
- **When** to retrieve (not every query needs retrieval)
- **Which** documents to use (dynamic filtering)
- **How** to cite (inline references, footnotes)

## RAG vs. Fine-Tuning

| Aspect | RAG | Fine-Tuning |
|--------|-----|-------------|
| **Update speed** | Instant (update corpus) | Slow (retrain) |
| **Cost** | Low (inference + retrieval) | High (training compute) |
| **Accuracy** | Good for facts | Better for style/format |
| **Transparency** | High (show sources) | Low (black box) |
| **Best for** | Knowledge-intensive tasks | Task-specific behavior |

**Verdict**: Use both! Fine-tune for task behavior, RAG for knowledge.

## Evaluation Metrics

1. **Retrieval Metrics**:
   - Recall@K: What % of relevant docs are in top-K?
   - MRR (Mean Reciprocal Rank): How high is the first relevant doc?
   - NDCG: Normalized ranking quality

2. **Generation Metrics**:
   - Faithfulness: Does answer match retrieved docs?
   - Relevance: Does answer address the question?
   - Coherence: Is the answer well-structured?

3. **End-to-End**:
   - Human evaluation (gold standard)
   - GPT-4 as judge (surprisingly good correlation)
   - Exact match / F1 for factoid QA

## State of the Art (2026)

- **Perplexity.ai**: Consumer RAG search engine
- **Google SGE**: Search Generative Experience
- **Microsoft Copilot**: RAG over Office documents
- **Open-source**: LangChain, LlamaIndex, Haystack

The trend is toward **agentic RAG** — multiple specialized agents collaborating rather than a single retrieve-and-generate step.

## My Implementation Notes

For my Second Brain project:
- Use ChromaDB for vector storage (simple, persistent)
- Sentence-Transformers for embeddings (free, local)
- Cross-encoder reranking for precision
- Context optimization to stay under token limits
- Semantic memory to cache common queries

Key insight: **Transparency matters**. Show users exactly what was retrieved, how it was ranked, and why a particular answer was generated.
