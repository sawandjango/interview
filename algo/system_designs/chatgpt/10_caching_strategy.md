# Diagram 10: Caching Strategy

## Overview
Multi-level caching strategy to reduce latency, cost, and load on backend services. Caching at API, session, embedding, KV (attention), and result levels.

## Architecture Diagram

```
╔═══════════════════════════════════════════════════════════════╗
║                   MULTI-LEVEL CACHE HIERARCHY                 ║
╚═══════════════════════════════════════════════════════════════╝

                        ┌──────────────┐
                        │  Client      │
                        └──────┬───────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│  Level 1: CDN / Edge Cache                                   │
│  (Cloudflare, Fastly)                                        │
│                                                              │
│  - Static assets (JS, CSS, images)                          │
│  - API responses (very rare, only for public endpoints)     │
│  - TTL: 1 hour - 7 days                                     │
│  - Hit rate: 95%+ for static assets                         │
│  - Latency: 10-50ms (geographic proximity)                  │
│                                                              │
│  Cache-Control headers:                                      │
│    Cache-Control: public, max-age=3600, s-maxage=86400      │
└──────────────────────┬───────────────────────────────────────┘
                       │ (cache miss)
                       ▼
┌──────────────────────────────────────────────────────────────┐
│  Level 2: API Response Cache (Redis)                         │
│  Regional deployment                                         │
│                                                              │
│  Purpose: Cache common/repeated queries                     │
│                                                              │
│  Cache key pattern:                                          │
│    cache:response:{hash(prompt + model + params)}           │
│                                                              │
│  Example:                                                    │
│    Key: cache:response:abc123def456                         │
│    Value: {                                                  │
│      "response": "Paris is the capital of France...",       │
│      "model": "gpt-3.5-turbo",                              │
│      "tokens": 25,                                          │
│      "cached_at": "2024-01-15T10:00:00Z"                    │
│    }                                                         │
│    TTL: 1 hour (for deterministic queries)                  │
│                                                              │
│  When to cache:                                              │
│    - temperature = 0 (deterministic)                        │
│    - Factual queries (e.g., "What is 2+2?")                 │
│    - Public information lookups                             │
│                                                              │
│  Hit rate: 15-25% (surprisingly high for common queries)    │
│  Latency: 1-5ms                                             │
│  Savings: $0.002 per cached response (vs. LLM call)         │
└──────────────────────┬───────────────────────────────────────┘
                       │ (cache miss)
                       ▼
┌──────────────────────────────────────────────────────────────┐
│  Level 3: Session / Conversation Cache (Redis)               │
│                                                              │
│  Purpose: Cache recent conversation context                 │
│                                                              │
│  Cache key: session:{conversation_id}                       │
│  Value: {                                                    │
│    "messages": [last 20 messages],                          │
│    "user_id": "usr_123",                                    │
│    "model": "gpt-4",                                        │
│    "updated_at": "2024-01-15T10:30:00Z"                     │
│  }                                                           │
│  TTL: 1 hour (sliding window on access)                     │
│                                                              │
│  Benefits:                                                   │
│    - Avoid DB read on every turn (50ms → 5ms)               │
│    - Write-through cache (update on new message)            │
│    - Eviction: LRU (least recently used)                    │
│                                                              │
│  Hit rate: 70-80% (most conversations are recent)           │
│  Latency: 2-5ms (vs. 20-50ms DB read)                       │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│  Level 4: Embedding Cache (Redis + Disk)                    │
│                                                              │
│  Purpose: Cache query embeddings for RAG                    │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ A. Query Embedding Cache (Redis)                       │ │
│  │                                                        │ │
│  │  Cache key: embedding:query:{hash(text)}              │ │
│  │  Value: [0.023, -0.156, 0.089, ...]  (1536 floats)   │ │
│  │  TTL: 24 hours                                         │ │
│  │                                                        │ │
│  │  Hit rate: 40-50% (common queries)                    │ │
│  │  Latency: 2ms (vs. 50ms API call)                     │ │
│  │  Savings: $0.0001 per cache hit                       │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ B. Document Embedding Cache (Disk / SSD)              │ │
│  │                                                        │ │
│  │  For RAG pipeline:                                     │ │
│  │    Hash(chunk_text) → embedding vector                │ │
│  │                                                        │ │
│  │  Stored in local SSD on workers                       │ │
│  │  Persistent (rebuilt only when docs change)           │ │
│  │  Size: ~100GB per worker                              │ │
│  │                                                        │ │
│  │  Benefits:                                             │ │
│  │    - Avoid re-embedding same chunks                   │ │
│  │    - Incremental updates (only new chunks)            │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│  Level 5: KV Cache (GPU Memory)                              │
│  In-memory cache for LLM attention                           │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ A. Prefix Caching                                      │ │
│  │                                                        │ │
│  │  System prompt: "You are ChatGPT, a helpful..."       │ │
│  │  Cached Keys/Values for this prefix (all layers)      │ │
│  │                                                        │ │
│  │  Benefits:                                             │ │
│  │    - System prompt: ~50-100 tokens                    │ │
│  │    - Reused across ALL conversations                  │ │
│  │    - Saves ~20-30ms per request                       │ │
│  │    - Reduces compute by 10-15%                        │ │
│  │                                                        │ │
│  │  Storage: ~2GB for system prompt (GPT-4 scale)        │ │
│  │  Eviction: Never (pinned in memory)                   │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ B. Multi-Turn Conversation KV Cache                   │ │
│  │                                                        │ │
│  │  Conversation ID → KV tensors for past tokens         │ │
│  │                                                        │ │
│  │  Example:                                              │ │
│  │    Turn 1: User says "Hi" → cache KV for "Hi"         │ │
│  │    Turn 2: User says "How are you?"                   │ │
│  │            → reuse KV from turn 1, extend with turn 2 │ │
│  │                                                        │ │
│  │  Benefits:                                             │ │
│  │    - Avoid recomputing past tokens                    │ │
│  │    - Only compute new tokens                          │ │
│  │    - Huge speedup for long conversations              │ │
│  │                                                        │ │
│  │  Storage: ~4-5GB per request (at max context)         │ │
│  │  Eviction: LRU when GPU memory full                   │ │
│  │            (PagedAttention for efficient paging)       │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ C. Shared Prefix Optimization (vLLM)                  │ │
│  │                                                        │ │
│  │  If multiple requests share prefix:                   │ │
│  │    Request A: "Translate to French: Hello"            │ │
│  │    Request B: "Translate to French: Goodbye"          │ │
│  │                                                        │ │
│  │  Shared prefix: "Translate to French: "               │ │
│  │  Cache KV for prefix, compute only suffix             │ │
│  │                                                        │ │
│  │  Implementation: Radix tree (prefix trie)             │ │
│  │  Savings: 20-40% compute for batched similar requests │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘


╔═══════════════════════════════════════════════════════════════╗
║                CACHE INVALIDATION STRATEGIES                  ║
╚═══════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────┐
│  1. Time-Based (TTL)                                         │
│                                                              │
│  Most common, simplest approach:                            │
│  - CDN: 1 hour - 7 days                                     │
│  - API responses: 1 hour                                    │
│  - Session data: 1 hour (sliding)                           │
│  - Embeddings: 24 hours                                     │
│                                                              │
│  Pros: Simple, predictable                                  │
│  Cons: May serve stale data until expiry                    │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  2. Event-Based Invalidation                                │
│                                                              │
│  Invalidate when underlying data changes:                   │
│                                                              │
│  User updates profile:                                       │
│    → Invalidate session:{user_id}                           │
│    → Broadcast to all regions (Pub/Sub)                     │
│                                                              │
│  Document updated in RAG:                                    │
│    → Re-embed chunks                                        │
│    → Update vector DB                                       │
│    → Invalidate embedding cache for affected chunks         │
│                                                              │
│  Model updated:                                              │
│    → Clear all KV caches                                    │
│    → Warm up with common prefixes                           │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  3. LRU Eviction                                             │
│                                                              │
│  When cache full, evict least recently used:               │
│                                                              │
│  Redis (session cache):                                      │
│    maxmemory-policy: allkeys-lru                            │
│    maxmemory: 50GB                                          │
│                                                              │
│  GPU KV cache:                                               │
│    PagedAttention: Page out old KVs to CPU/disk            │
│    Prefetch likely-to-be-used KVs back to GPU               │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  4. Cache Stampede Prevention                                │
│                                                              │
│  Problem: Many requests for same key during invalidation    │
│           → All miss, all hit backend                       │
│                                                              │
│  Solution: Locking / Request Coalescing                     │
│                                                              │
│  Pseudocode:                                                 │
│    if cache.get(key) is None:                              │
│      lock = distributed_lock(f"lock:{key}")                │
│      if lock.acquire(timeout=5s):                          │
│        value = expensive_compute()                         │
│        cache.set(key, value, ttl=3600)                     │
│        lock.release()                                       │
│      else:                                                  │
│        # Another process is computing, wait                │
│        wait_and_retry(key)                                 │
│                                                              │
│  Alternative: Probabilistic early expiration                │
│    Expire cache slightly before TTL (stagger refreshes)    │
└──────────────────────────────────────────────────────────────┘
```

## Cache Metrics & Monitoring

### Key Metrics
```python
# Cache hit rate (by level)
cache_hit_rate = {
    'cdn': 95.2%,              # Static assets
    'api_response': 18.3%,     # Repeated queries
    'session': 76.5%,          # Conversation context
    'embedding': 43.8%,        # Query embeddings
    'kv_prefix': 100%,         # System prompt (always hit)
    'kv_conversation': 85.2%,  # Multi-turn cache
}

# Latency impact
latency_with_cache = {
    'session_load': 5ms,       # vs. 50ms DB
    'embedding': 2ms,          # vs. 50ms API
    'response': 3ms,           # vs. 500ms LLM
}

# Cost savings
cost_savings_per_day = {
    'api_response_cache': '$500',  # Avoided LLM calls
    'embedding_cache': '$200',     # Avoided embedding API
    'kv_cache': '$5000',           # Reduced GPU compute
}
```

### Monitoring Dashboards
```yaml
# Grafana panels
panels:
  - title: "Cache Hit Rate by Level"
    query: "rate(cache_hits) / rate(cache_requests)"
    breakdown: [cdn, api, session, embedding, kv]

  - title: "Cache Memory Usage"
    query: "cache_memory_bytes"
    breakdown: [redis, gpu_kv, disk]

  - title: "Cache Evictions"
    query: "rate(cache_evictions)"
    alert_threshold: 1000/sec  # Too many evictions = undersized cache

  - title: "Latency Improvement from Caching"
    query: "p95(latency_with_cache) vs p95(latency_without_cache)"
```

## Cache Sizing & Capacity Planning

### Redis (Session + Embedding + API Response)
```
Conversations:
  - Avg size per conversation: 10KB (20 messages)
  - Active conversations (1 hour window): 500K
  - Memory: 500K × 10KB = 5GB

Embeddings:
  - Avg size per embedding: 6KB (1536 floats × 4 bytes)
  - Cache 100K common queries
  - Memory: 100K × 6KB = 600MB

API Responses:
  - Avg size per response: 1KB
  - Cache 50K recent responses
  - Memory: 50K × 1KB = 50MB

Total: 5GB + 600MB + 50MB ≈ 6GB
Provision: 12GB (2x for headroom)
Cost: $100/month (ElastiCache)
```

### GPU KV Cache
```
Per-request KV cache (GPT-4 scale):
  - Layers: 96
  - Context: 2048 tokens
  - Memory: ~4.7GB per request at max context

A100 GPU (80GB):
  - Model weights: ~40GB (8-way tensor parallelism)
  - Available for KV: ~40GB
  - Concurrent requests: ~8-10 at full context
  - With PagedAttention: ~15-20 (better packing)

Optimization: Prefix caching
  - System prompt KV: 2GB (shared across all)
  - Per-request: 2.7GB (reduced from 4.7GB)
  - Concurrent requests: ~14 → ~20 (40% improvement)
```

## Cache Warm-up Strategies

### System Startup
```python
# On deployment, warm up critical caches
def warm_up_caches():
    # 1. System prompt KV (LLM)
    llm.prefill("You are ChatGPT, a helpful assistant...")

    # 2. Common embeddings
    common_queries = [
        "What is AI?",
        "How do I...",
        "Explain...",
    ]
    for query in common_queries:
        embedding = embedding_model.encode(query)
        redis.set(f"embedding:query:{hash(query)}", embedding, ttl=86400)

    # 3. Feature flags
    feature_flags = load_feature_flags_from_db()
    redis.set("feature_flags", feature_flags, ttl=3600)

    print("Caches warmed up")
```

## Trade-offs & Considerations

### Consistency vs. Performance
| Scenario | Strategy | Trade-off |
|----------|----------|-----------|
| User profile updates | Write-through cache | Consistent but slower writes |
| Conversation history | Cache-aside (lazy load) | Fast but may be stale briefly |
| Model outputs (temp=0) | Aggressive caching | Perfect consistency (deterministic) |
| RAG documents | Event-based invalidation | Eventual consistency ok |

### Memory vs. Cost
- **More cache = less backend load** (cheaper LLM/DB calls)
- **But more cache = higher Redis/GPU cost**
- **Sweet spot**: Cache high-frequency items (80/20 rule)

### Staleness Tolerance
- **Session data**: 1 hour stale ok (user won't notice)
- **RAG documents**: 4 hours stale ok (knowledge doesn't change often)
- **API responses**: 1 hour max (factual queries)
- **User settings**: <1 min stale (update immediately)

## Interview Talking Points

**Q: How do you decide what to cache?**
- High-frequency reads (session data, common queries)
- Expensive to compute (LLM outputs, embeddings)
- Low write frequency (static data, configuration)
- Deterministic (temperature=0 responses)

**Q: How do you handle cache invalidation?**
- TTL for most caches (simple, predictable)
- Event-based for critical data (user settings)
- LRU eviction when full
- Cache stampede prevention (locks, request coalescing)

**Q: What's the impact of caching on latency?**
- Session cache: 50ms → 5ms (10x faster)
- Embedding cache: 50ms → 2ms (25x faster)
- KV cache: Enables multi-turn (otherwise prohibitive)
- Overall: p95 TTFT 660ms → 400ms (with all caches)

**Q: How do you size caches?**
- Monitor hit rates (target >70% for high-value caches)
- Monitor eviction rates (high evictions = undersized)
- Cost-benefit: Cache cost vs. savings (LLM calls)
- Start conservative, scale up based on data
