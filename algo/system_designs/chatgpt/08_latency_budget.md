# Diagram 8: Latency Budget & Performance

## Overview
Detailed breakdown of latency at each stage of request processing. Identifies bottlenecks and optimization strategies to meet p95 TTFT (Time To First Token) < 700ms target.

## Latency Budget Diagram

```
╔═══════════════════════════════════════════════════════════════╗
║              END-TO-END LATENCY BREAKDOWN                     ║
║              Target: p95 TTFT < 700ms                         ║
╚═══════════════════════════════════════════════════════════════╝

Client Request
     │
     │  ┌─────────────────────────────────────────────────┐
     └─►│ 1. Network (Client → API Gateway)               │
        │    - DNS resolution: 10-30ms                    │
        │    - TLS handshake: 50-100ms (reuse: ~0ms)     │
        │    - Geographic latency: 20-80ms               │
        │    ─────────────────────────────────────────── │
        │    Subtotal: 80-210ms (p50: 100ms, p95: 150ms) │
        └────────────┬────────────────────────────────────┘
                     │
                     │  ┌──────────────────────────────────────┐
                     └─►│ 2. API Gateway + Auth                │
                        │    - Load balancing: 5-10ms          │
                        │    - JWT validation: 5-10ms          │
                        │    - Request parsing: 5-10ms         │
                        │    ────────────────────────────────  │
                        │    Subtotal: 15-30ms (p95: 30ms)     │
                        └──────────┬───────────────────────────┘
                                   │
                     ┌─────────────┴─────────────┐
                     │                           │
                     ▼                           ▼
        ┌──────────────────────┐    ┌──────────────────────┐
        │ 3a. Session Load     │    │ 3b. Rate Limit Check │
        │    (if existing conv)│    │    (Redis lookup)    │
        │    - DB query: 20-50ms│   │    - 2-5ms           │
        │    - Cache hit: 5-10ms│   │                      │
        └──────────┬───────────┘    └──────────┬───────────┘
                   │                           │
                   └───────────┬───────────────┘
                               │
                               │  ┌──────────────────────────────────────┐
                               └─►│ 4. Orchestrator Routing              │
                                  │    - Decision logic: 10-20ms         │
                                  │    - Feature flag lookup: 5ms        │
                                  │    ────────────────────────────────  │
                                  │    Subtotal: 15-25ms (p95: 20ms)     │
                                  └──────────┬───────────────────────────┘
                                             │
                               ┌─────────────┴─────────────┐
                               │                           │
                               ▼                           ▼
                  ┌────────────────────────┐  ┌────────────────────────┐
                  │ 5a. Safety Check (Pre) │  │ 5b. RAG Retrieval      │
                  │    - Model inference:  │  │    (if needed)         │
                  │      30-50ms           │  │    - Query expansion:  │
                  │    - PII detection:    │  │      5-10ms            │
                  │      10-20ms           │  │    - Vector search:    │
                  │    ──────────────────  │  │      30-60ms           │
                  │    Subtotal: 40-70ms   │  │    - Re-ranking:       │
                  │    (p95: 60ms)         │  │      40-60ms           │
                  └────────────┬───────────┘  │    - Context build:    │
                               │              │      5-10ms            │
                               │              │    ──────────────────  │
                               │              │    Subtotal: 80-140ms  │
                               │              │    (p95: 120ms)        │
                               │              └────────────┬───────────┘
                               │                           │
                               └───────────┬───────────────┘
                                           │
                                           │  ┌──────────────────────────────────────┐
                                           └─►│ 6. Request Queuing                   │
                                              │    - Wait for inference slot         │
                                              │    - p50: 10ms (low load)            │
                                              │    - p95: 150ms (high load)          │
                                              │    - p99: 500ms (peak)               │
                                              │    ────────────────────────────────  │
                                              │    Target: 50-150ms (p95: 100ms)     │
                                              └──────────┬───────────────────────────┘
                                                         │
                                                         │  ┌──────────────────────────────────────┐
                                                         └─►│ 7. LLM First Decode                  │
                                                            │    - Tokenization: 5-10ms            │
                                                            │    - Prompt processing: 20-40ms      │
                                                            │    - First token generation: 50-80ms │
                                                            │    ────────────────────────────────  │
                                                            │    Subtotal: 75-130ms (p95: 120ms)   │
                                                            └──────────┬───────────────────────────┘
                                                                       │
                                                                       │  ┌──────────────────────────────────────┐
                                                                       └─►│ 8. Response (First Token to Client)  │
                                                                          │    - Detokenization: 2-5ms           │
                                                                          │    - Network (server→client): 20-50ms│
                                                                          │    ────────────────────────────────  │
                                                                          │    Subtotal: 22-55ms (p95: 50ms)     │
                                                                          └──────────────────────────────────────┘

═════════════════════════════════════════════════════════════════════════════
TOTAL TIME TO FIRST TOKEN (TTFT):

Best Case (p50):  100 + 30 + 20 + 20 + 60 + 50 + 120 + 50 = 450ms ✓
Typical (p95):    150 + 30 + 20 + 20 + 120 + 150 + 120 + 50 = 660ms ✓
Worst Case (p99): 210 + 40 + 30 + 30 + 150 + 500 + 180 + 80 = 1220ms ✗

Target: p95 < 700ms ✓ (with margin: 660ms)
═════════════════════════════════════════════════════════════════════════════


╔═══════════════════════════════════════════════════════════════╗
║           SUBSEQUENT TOKEN GENERATION (STREAMING)             ║
╚═══════════════════════════════════════════════════════════════╝

After first token:
     │
     │  ┌──────────────────────────────────────────────┐
     └─►│ Per-Token Generation Loop                    │
        │                                              │
        │  For each token (until EOS or max_tokens):  │
        │                                              │
        │  1. Decode step (GPU): 8-15ms                │
        │     - Attention calculation: 5-10ms          │
        │     - Feed-forward: 2-4ms                    │
        │     - Sampling: 1ms                          │
        │                                              │
        │  2. Send to client: 5-10ms                   │
        │     - Network latency: 5-10ms                │
        │                                              │
        │  ───────────────────────────────────────────│
        │  Inter-token latency: 13-25ms                │
        │  (p95: 20ms)                                 │
        │                                              │
        │  For 100-token response:                     │
        │  - TTFT: 660ms (p95)                         │
        │  - Subsequent: 100 tokens × 20ms = 2000ms    │
        │  - Total: 2660ms (~2.7 seconds)              │
        └──────────────────────────────────────────────┘
```

## Component-Level Optimization Strategies

### 1. Network (100-150ms target)
**Current**: 150ms (p95)

**Optimizations**:
- **CDN/Edge deployment**: Terminate TLS at edge (save 50-100ms)
- **HTTP/3 (QUIC)**: Faster connection setup (save 20-50ms)
- **Connection pooling**: Reuse TLS connections (save 50-100ms on subsequent requests)
- **Optimized routing**: GeoDNS routes to nearest region (save 30-80ms)

**Result**: 150ms → **80ms** (p95)

---

### 2. Gateway + Auth (30ms target)
**Current**: 30ms (p95)

**Optimizations**:
- **JWT caching**: Cache decoded JWTs in Redis (save 5-10ms)
- **Async logging**: Don't block on log writes (save 5ms)
- **Lightweight validation**: Lazy load user profile (save 5ms)

**Result**: 30ms → **15ms** (p95)

---

### 3. Session Load (20-50ms)
**Current**: 50ms (p95)

**Optimizations**:
- **Redis caching**: Cache recent conversations (hit rate 70%)
  - Cache hit: 5ms
  - Cache miss: 50ms
  - Weighted avg: 0.7 × 5 + 0.3 × 50 = **18.5ms**
- **Lazy loading**: Only load last 10 messages, not full history
- **Compression**: Compress cached data (smaller network transfer)

**Result**: 50ms → **20ms** (p95)

---

### 4. Orchestrator (20ms target)
**Current**: 20ms (p95)

**Optimizations**:
- **In-memory feature flags**: Sync every 60s, not per-request (save 5ms)
- **Parallel execution**: Run safety + RAG + routing in parallel (already optimized)

**Result**: Already optimal at **20ms**

---

### 5a. Safety Check (60ms target)
**Current**: 60ms (p95)

**Optimizations**:
- **Edge deployment**: Run small safety models at edge (save 20ms network)
- **Model quantization**: INT8 models, 2x faster (save 15ms)
- **Caching**: Hash prompt → safety result (hit rate 20%)
  - Weighted avg: 0.2 × 5 + 0.8 × 45 = **37ms**

**Result**: 60ms → **35ms** (p95)

---

### 5b. RAG Retrieval (120ms target)
**Current**: 120ms (p95)

**Optimizations**:
- **Embedding cache**: Cache query embeddings (hit rate 40%)
  - Without cache: 50ms for embedding
  - With cache: 50ms → 5ms (save 45ms on 40% of queries)
  - Weighted: 0.4 × 5 + 0.6 × 50 = **32ms** for embedding step
- **Approximate NN**: Use HNSW with lower recall for speed (save 15ms)
- **Parallel re-ranking**: GPU batch inference (save 20ms)
- **Reduced top-k**: Re-rank 10 instead of 20 (save 10ms)

**Result**: 120ms → **70ms** (p95)

---

### 6. Request Queuing (100ms target)
**Current**: 150ms (p95)

**Optimizations**:
- **Continuous batching**: Pack requests dynamically (better GPU utilization)
- **Priority queues**: Premium users get priority (reduce wait)
- **Auto-scaling**: Add pods when queue depth > 20 (reduce wait)
- **Speculative execution**: Start processing while waiting (overlap time)

**Result**: 150ms → **50ms** (p95)

---

### 7. LLM First Decode (120ms target)
**Current**: 120ms (p95)

**Optimizations**:
- **Prefix caching**: Cache system prompt KV (save 20-30ms)
- **Speculative decoding**: Generate 3-5 tokens speculatively (perceived speedup)
- **Quantization**: Use INT8/INT4 weights (save 15-20ms)
- **Flash Attention**: Optimized attention kernels (save 10ms)
- **Smaller models for routing**: Use GPT-3.5 for simple queries (50% faster)

**Result**: 120ms → **80ms** (p95)

---

### 8. Response to Client (50ms target)
**Current**: 50ms (p95)

**Optimizations**:
- **Edge termination**: Stream from nearest edge location (save 20ms)
- **WebSocket reuse**: Keep connection open (save 10ms on subsequent requests)

**Result**: 50ms → **30ms** (p95)

---

## Optimized Latency Budget

| Component | Before (p95) | After (p95) | Savings |
|-----------|--------------|-------------|---------|
| Network | 150ms | 80ms | 70ms |
| Gateway | 30ms | 15ms | 15ms |
| Session | 50ms | 20ms | 30ms |
| Orchestrator | 20ms | 20ms | 0ms |
| Safety | 60ms | 35ms | 25ms |
| RAG | 120ms | 70ms | 50ms |
| Queuing | 150ms | 50ms | 100ms |
| LLM Decode | 120ms | 80ms | 40ms |
| Response | 50ms | 30ms | 20ms |
| **Total** | **750ms** | **400ms** | **350ms** |

**Result**: p95 TTFT = **400ms** (target: <700ms) ✓✓

---

## Monitoring Latency

### Metrics to Track
```python
# Per-component latency (tagged by component)
histogram('request.latency', tags=['component:network'])
histogram('request.latency', tags=['component:gateway'])
histogram('request.latency', tags=['component:rag'])
histogram('request.latency', tags=['component:llm_decode'])

# Percentiles
gauge('request.latency.p50')
gauge('request.latency.p95')
gauge('request.latency.p99')

# SLO compliance
gauge('slo.ttft.p95_under_700ms', value=99.2%)  # 99.2% of requests meet SLO
```

### Alerting
```yaml
alerts:
  - name: HighP95Latency
    condition: p95(request.latency) > 700ms for 5min
    action: Slack alert, investigate

  - name: SLOBreach
    condition: slo.ttft.p95_under_700ms < 99%
    action: Page on-call

  - name: ComponentSlow
    condition: p95(request.latency, component=rag) > 150ms
    action: Investigate RAG service
```

---

## A/B Testing for Latency

```python
# Test: Does prefix caching reduce latency?
experiment = {
    'name': 'prefix_caching_v1',
    'variants': [
        {'name': 'control', 'weight': 50},    # No prefix caching
        {'name': 'treatment', 'weight': 50},  # With prefix caching
    ],
    'metrics': ['ttft', 'accuracy', 'cost'],
}

# Results after 1 week:
results = {
    'control': {'ttft_p95': 660ms, 'cost_per_1k_tokens': $0.03},
    'treatment': {'ttft_p95': 580ms, 'cost_per_1k_tokens': $0.025},
}

# Winner: Treatment (12% faster, 17% cheaper) → Roll out to 100%
```

---

## Cost vs. Latency Trade-offs

| Optimization | Latency Savings | Cost Impact |
|--------------|-----------------|-------------|
| Edge deployment | -70ms | +30% (more PoPs) |
| Prefix caching | -25ms | -15% (fewer tokens) |
| Speculative decoding | -40ms (perceived) | +20% (more compute) |
| Smaller models (GPT-3.5) | -50ms | -90% (much cheaper) |
| Quantization (INT8) | -20ms | -30% (smaller GPUs) |
| Auto-scaling (more pods) | -100ms (queue) | +50% (idle capacity) |

**Sweet spot**: Prefix caching + Quantization + Smart routing (smaller models for simple queries)
- **Latency**: 660ms → 450ms (32% improvement)
- **Cost**: -40% (due to smaller models + caching)

---

## Interview Talking Points

**Q: How do you reduce latency?**
1. Measure everything (per-component tracing)
2. Identify bottlenecks (queuing, RAG, LLM decode)
3. Optimize hot path (caching, edge deployment, faster models)
4. A/B test changes (measure impact)
5. Set SLOs and alert on violations

**Q: What's the biggest latency bottleneck?**
- **Queuing** (150ms at p95) → Fix with auto-scaling and continuous batching
- **RAG** (120ms) → Fix with embedding caching and approximate search
- **LLM decode** (120ms) → Fix with prefix caching and quantization

**Q: How do you balance cost vs. latency?**
- Use smaller/faster models for simple queries (router logic)
- Cache aggressively (embeddings, safety results, prefixes)
- Trade compute for latency (speculative decoding uses 2x compute for 2x speed)

**Q: How do you ensure latency doesn't regress?**
- Continuous monitoring (p50/p95/p99 dashboards)
- SLO alerts (page if p95 > 700ms)
- Load testing before deploys
- Gradual rollouts with canary analysis
