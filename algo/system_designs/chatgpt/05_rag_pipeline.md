# Diagram 5: RAG Data Pipeline (Offline → Online)

## Overview
Retrieval Augmented Generation (RAG) enhances LLM responses with external knowledge. This involves offline data ingestion and online retrieval.

## Architecture Diagram

```
╔═══════════════════════════════════════════════════════════════╗
║                   OFFLINE INGESTION PIPELINE                  ║
╚═══════════════════════════════════════════════════════════════╝

┌─────────────────┐
│  Source Data    │
│                 │
│ - PDFs          │
│ - Web pages     │
│ - Docs          │
│ - Databases     │
│ - APIs          │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  1. Document Ingestion                                  │
│                                                         │
│  - Crawlers / Connectors                               │
│  - Format conversion (PDF→text, HTML→markdown)         │
│  - Metadata extraction (title, author, date, URL)      │
│  - Deduplication (hash-based)                          │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  2. Preprocessing                                       │
│                                                         │
│  - Text cleaning (remove HTML tags, special chars)     │
│  - Language detection                                  │
│  - Quality filtering (gibberish, low-content pages)    │
│  - PII redaction (emails, phone numbers, SSN)          │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  3. Chunking Strategy                                   │
│                                                         │
│  Options:                                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │ A. Fixed-size chunking                           │  │
│  │    - 512 tokens per chunk                        │  │
│  │    - 50 token overlap (preserve context)         │  │
│  │    Pro: Simple, consistent                       │  │
│  │    Con: May split mid-sentence                   │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ B. Semantic chunking                             │  │
│  │    - Split on paragraph boundaries               │  │
│  │    - Use sentence embeddings to find breaks      │  │
│  │    - Target ~500 tokens, flexible               │  │
│  │    Pro: Preserves semantic units                 │  │
│  │    Con: Variable chunk sizes                     │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ C. Hierarchical chunking                         │  │
│  │    - Document → Sections → Paragraphs           │  │
│  │    - Store relationships in metadata             │  │
│  │    - Retrieve parent if child is relevant        │  │
│  │    Pro: Rich context, flexible retrieval         │  │
│  │    Con: Complex, higher storage                  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  **Choice: Semantic chunking (B)**                     │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  4. Embedding Generation                                │
│                                                         │
│  Model: text-embedding-ada-002 (OpenAI)                │
│         OR custom BERT/Sentence-BERT                    │
│                                                         │
│  Input:  Chunk text (512 tokens)                       │
│  Output: Dense vector (1536 dimensions)                │
│                                                         │
│  Batching: 100 chunks per API call (reduce latency)    │
│  Caching: Hash chunk → embedding (avoid re-compute)    │
│                                                         │
│  Throughput: 1M chunks/hour (parallelized)             │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  5. Vector Database Upsert                              │
│                                                         │
│  Database: Pinecone / Weaviate / Milvus / Qdrant       │
│                                                         │
│  Schema:                                                │
│  {                                                      │
│    "id": "doc123_chunk5",                              │
│    "vector": [0.023, -0.15, ...],  // 1536 dims       │
│    "metadata": {                                       │
│      "text": "original chunk text...",                │
│      "source": "https://...",                         │
│      "title": "Q3 Earnings Report",                   │
│      "date": "2024-01-15",                            │
│      "author": "CFO",                                 │
│      "section": "Revenue",                            │
│      "chunk_index": 5,                                │
│      "total_chunks": 20                               │
│    }                                                   │
│  }                                                      │
│                                                         │
│  Indexing:                                              │
│  - HNSW (Hierarchical Navigable Small World)           │
│  - IVF (Inverted File Index)                           │
│  - Product Quantization (compression)                  │
│                                                         │
│  Index build time: Minutes to hours (depending on size)│
└────────┬────────────────────────────────────────────────┘
         │
         ▼
    [Vector DB]
    100M+ vectors
    ~200 GB storage


╔═══════════════════════════════════════════════════════════════╗
║                     ONLINE RETRIEVAL FLOW                     ║
╚═══════════════════════════════════════════════════════════════╝

┌─────────────────┐
│   User Query    │
│                 │
│ "What were the │
│  Q3 revenues?"  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  1. Query Understanding & Expansion                     │
│                                                         │
│  Original: "Q3 revenues"                               │
│            ↓                                            │
│  Expanded: [                                            │
│    "Q3 revenues",                                      │
│    "third quarter revenue",                            │
│    "quarterly earnings Q3",                            │
│    "revenue Q3 2024"                                   │
│  ]                                                      │
│                                                         │
│  Techniques:                                            │
│  - Synonym expansion (WordNet, custom)                 │
│  - Query rewriting (LLM-based)                         │
│  - Acronym expansion (Q3 → third quarter)              │
│  - Temporal context (Q3 → recent if not specified)     │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  2. Hybrid Search (Dense + Sparse)                      │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Dense Vector Search (Semantic)                  │  │
│  │                                                  │  │
│  │  Query → Embedding model → vector                │  │
│  │  "What were the Q3 revenues?"                    │  │
│  │         ↓                                         │  │
│  │  [0.12, -0.34, 0.56, ...]  (1536 dims)          │  │
│  │         ↓                                         │  │
│  │  Vector DB: cosine similarity search             │  │
│  │         ↓                                         │  │
│  │  Top 50 candidates                               │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Sparse Keyword Search (BM25)                    │  │
│  │                                                  │  │
│  │  Query: "Q3 revenues"                            │  │
│  │  Tokens: ["q3", "revenues"]                      │  │
│  │         ↓                                         │  │
│  │  Inverted index lookup                           │  │
│  │         ↓                                         │  │
│  │  Top 50 candidates (ranked by BM25)              │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  Fusion:                                                │
│  - Reciprocal Rank Fusion (RRF)                        │
│  - Score = 1/(rank_dense + k) + 1/(rank_sparse + k)    │
│  - Combine to get top 20 candidates                    │
│                                                         │
│  Why hybrid?                                            │
│  - Dense: "cheap flights" ≈ "affordable travel"        │
│  - Sparse: Exact match for IDs, codes, names           │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  3. Re-ranking (Cross-Encoder)                          │
│                                                         │
│  Why?                                                   │
│  - Bi-encoder (used above): Fast but less accurate     │
│  - Cross-encoder: Slower but much more accurate        │
│                                                         │
│  For top 20 candidates:                                │
│    Input: [query, chunk_text] → Cross-encoder model    │
│    Output: Relevance score (0.0 to 1.0)                │
│                                                         │
│  Example:                                               │
│    Query: "Q3 revenues"                                │
│    Chunk: "In Q3 2024, revenues reached $5.2B..."      │
│           → Score: 0.94 (highly relevant)              │
│                                                         │
│  Model: MiniLM-L12 (small, fast), BERT-large (slower)  │
│  Latency: ~50ms for 20 chunks                          │
│                                                         │
│  Select top 5 chunks after re-ranking                  │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  4. Context Construction                                │
│                                                         │
│  Format for LLM:                                        │
│                                                         │
│  Context:                                               │
│  ---                                                    │
│  [1] Q3 2024 Earnings Report (Source: investor.co)     │
│      "In Q3 2024, revenues reached $5.2B, up 15%..."   │
│                                                         │
│  [2] CFO Statement, Oct 2024 (Source: blog.co)         │
│      "We are pleased to report strong Q3 results..."    │
│                                                         │
│  [3] Revenue Breakdown (Source: internal)               │
│      "Q3 revenue by segment: Cloud $3B, Ads $2.2B..."  │
│  ---                                                    │
│                                                         │
│  Token budget: ~1500 tokens (fits in context window)   │
│  Citations: Embedded for LLM to reference              │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  5. Return to Orchestrator                              │
│                                                         │
│  Response:                                              │
│  {                                                      │
│    "context": "...",                                   │
│    "citations": [                                      │
│      {"id": 1, "source": "https://...", "title": "..."},│
│      {"id": 2, "source": "https://...", "title": "..."},│
│      {"id": 3, "source": "https://...", "title": "..."} │
│    ],                                                   │
│    "latency_ms": 180                                   │
│  }                                                      │
└─────────────────────────────────────────────────────────┘
```

## Data Flow Example

### Offline: Ingest "Q3 Earnings Report"
```
1. PDF file uploaded (50 pages)
2. Convert to text, extract metadata
3. Clean & filter → 45 pages of quality content
4. Chunk into 120 chunks (~400 tokens each)
5. Generate embeddings → 120 vectors
6. Upsert to vector DB with metadata
7. Build/update index

Total time: ~5 minutes
```

### Online: Retrieve for "What were Q3 revenues?"
```
1. Query expansion (5ms)
   → ["Q3 revenues", "third quarter revenue", ...]

2. Hybrid search (100ms)
   - Dense: 50 candidates from vector DB
   - Sparse: 50 candidates from keyword index
   - Fusion: Top 20

3. Re-ranking (50ms)
   - Cross-encoder: Top 5 chunks

4. Context construction (10ms)
   - Format with citations

5. Return to orchestrator (165ms total)
```

## Embedding Cache Strategy

```python
# Cache structure
embedding_cache = {
    hash("What were the Q3 revenues?"): [0.12, -0.34, ...],
    hash("Q3 revenue numbers"): [0.11, -0.35, ...],
    ...
}

# On query:
query_hash = hash(normalize(query))
if query_hash in embedding_cache:
    vector = embedding_cache[query_hash]  # Cache hit! (0ms)
else:
    vector = embedding_model.encode(query)  # Cache miss (50ms)
    embedding_cache[query_hash] = vector

# TTL: 1 hour (redis)
# Size: ~100K most common queries
# Hit rate: 40-60% (significant latency savings)
```

## Challenges & Solutions

### 1. Stale Data
**Problem**: Knowledge base outdated

**Solution**:
- Incremental updates (daily crawl)
- Versioning (track doc versions)
- Metadata: `last_updated` timestamp
- Filter by recency in retrieval

### 2. Hallucination / Irrelevant Retrieval
**Problem**: LLM uses low-quality context

**Solution**:
- Higher re-ranking threshold (>0.7 relevance)
- LLM prompt: "Only use provided context, say 'I don't know' if unsure"
- Confidence scoring

### 3. Long Documents
**Problem**: User asks about 500-page manual

**Solution**:
- Hierarchical retrieval (section → paragraph)
- Two-stage search (find section, then drill down)
- Summarization of long sections

### 4. Multilingual
**Problem**: Docs in multiple languages

**Solution**:
- Multilingual embedding models (mE5, LaBSE)
- Translate query to doc language
- Language-specific indexes

### 5. Security / Access Control
**Problem**: User shouldn't see private docs

**Solution**:
- Metadata: `user_id`, `org_id`, `access_level`
- Filter at query time: `WHERE org_id = user.org_id`
- Row-level security (RLS) in vector DB

## Metrics to Monitor

### Offline Pipeline
- **Ingestion rate**: Docs/hour
- **Embedding generation**: Tokens/sec
- **Index build time**: Minutes
- **Storage used**: GB
- **Deduplication rate**: % duplicates caught

### Online Retrieval
- **Latency**: p50, p95 (target: <200ms)
- **Recall@5**: Are relevant docs in top 5?
- **Precision@5**: What % of top 5 are relevant?
- **Cache hit rate**: % queries served from cache
- **Re-ranking improvement**: % better than dense alone

## Costs

| Component | Cost (per 1M queries) |
|-----------|-----------------------|
| Embedding API (OpenAI) | $100 |
| Vector DB (Pinecone) | $70 (storage + compute) |
| Re-ranker (self-hosted) | $20 (GPU time) |
| Storage (S3) | $5 |
| **Total** | **$195** |

**Optimization**: Self-host embedding model → save $100

## Interview Talking Points

**Q: Why hybrid search?**
- Dense: Good for semantic similarity ("fast car" ≈ "quick vehicle")
- Sparse: Good for exact matches (product IDs, names)
- Combined: Best of both worlds

**Q: Why re-ranking?**
- Bi-encoder fast but less accurate (independent encoding)
- Cross-encoder slow but accurate (joint encoding)
- Two-stage: Fast first pass, accurate final selection

**Q: How to handle updates?**
- Incremental: Only re-index changed docs
- Soft deletes: Mark old versions, filter at query time
- Versioning: Keep multiple versions, let user choose

**Q: How to improve relevance?**
- Better chunking (preserve semantic units)
- Query expansion (synonyms, related terms)
- User feedback (thumbs up/down → fine-tune ranking)
- A/B test retrieval strategies
