# ChatGPT System Design - Quick Reference Guide

## For System Design Interviews

### Time Allocation (45-60 min interview)

1. **Requirements & Scope (5 min)**
   - Clarify: ChatGPT-like conversational AI
   - Scale: 100M+ DAU, 1M+ QPS
   - Latency: p95 TTFT < 700ms
   - Features: Multi-turn chat, RAG, tool calling, streaming

2. **High-Level Design (10 min)**
   - Start with Diagram 1 (High-Level Flow)
   - Client → API Gateway → Orchestrator → LLM → Stream back
   - Mention key components: Rate limiting, Safety, RAG, Model serving

3. **Deep Dive (20 min)**
   - Pick 2-3 areas based on interviewer interest:
     - **Orchestrator** (Diagram 3): Tool calling, RAG integration, safety
     - **Model Serving** (Diagram 4): GPU batching, KV cache, quantization
     - **RAG** (Diagram 5): Hybrid search, re-ranking, embedding cache
     - **Reliability** (Diagram 7): Multi-region, failover, replication

4. **Bottlenecks & Optimizations (10 min)**
   - Latency Budget (Diagram 8): Break down 660ms → 400ms optimizations
   - Caching (Diagram 10): Session, embedding, KV, response caching
   - Cost optimization: Model routing, quantization, prefix caching

5. **Q&A / Follow-ups (5 min)**
   - Security (Diagram 9): Auth, RBAC, API keys
   - Data stores (Diagram 6): Retention, compliance, sharding
   - Monitoring: Metrics, SLOs, alerting

---

## Component Summary (1-liner each)

| Component | One-Liner |
|-----------|-----------|
| **API Gateway** | SSL termination, auth, rate limiting, routing |
| **Orchestrator** | Decides RAG/tools/direct-LLM, manages multi-turn execution |
| **Safety Filter** | Pre/post moderation, PII detection, policy enforcement |
| **RAG Service** | Retrieves relevant docs via hybrid search + re-ranking |
| **LLM Router** | Selects model/region based on cost/latency/complexity |
| **Model Serving** | GPU inference with batching, KV cache, streaming |
| **Session Service** | Loads conversation history, manages context window |
| **Billing/Quotas** | Tracks token usage, enforces limits, generates invoices |
| **Vector DB** | Stores embeddings for semantic search (RAG) |
| **PostgreSQL** | Conversations, users, metadata (multi-AZ, replicated) |
| **Redis** | Caching (sessions, embeddings, rate limits) |
| **S3** | Cold storage for archived conversations, documents |

---

## Numbers to Remember

### Scale
- **DAU**: 100M+
- **QPS**: 1M+ at peak
- **Conversations**: 10B+ total, 1B active
- **Messages**: 100B+ stored
- **Tokens/day**: 10T+ generated

### Latency (p95 TTFT)
- **Target**: <700ms
- **Actual (optimized)**: ~400ms
- **Breakdown**: Network 80ms + Gateway 15ms + Session 20ms + Orchestrator 20ms + Safety 35ms + RAG 70ms + Queue 50ms + LLM 80ms + Response 30ms

### Capacity
- **LLM pods**: 50-100 per region
- **GPU**: 8xA100 per pod (GPT-4 scale)
- **Concurrent requests per pod**: 15-20 (with PagedAttention)
- **Throughput**: 50-100 tokens/sec per request

### Costs (Monthly)
- **Compute (LLM)**: $600K (multi-region)
- **Database**: $120K (PostgreSQL + replicas)
- **Storage**: $80K (S3, vector DB, Redis)
- **Networking**: $100K (cross-region, CDN)
- **Total**: ~$900K/month

### Hit Rates (Caching)
- **CDN**: 95%+ (static assets)
- **Session cache**: 70-80%
- **Embedding cache**: 40-50%
- **API response cache**: 15-25%
- **KV prefix cache**: 100% (system prompt)

---

## Common Interview Questions & Answers

### Scalability

**Q: How do you scale to 1M QPS?**
- Horizontal scaling: 1000s of stateless pods
- LLM pods: Auto-scale based on queue depth
- Database: Sharding by user_id, read replicas
- Multi-region: Route to nearest healthy region

**Q: What's the bottleneck at scale?**
- GPU availability (most expensive, hardest to scale)
- Mitigation: Model routing (simple → GPT-3.5, complex → GPT-4), quantization, speculative decoding

### Performance

**Q: How do you achieve <700ms TTFT?**
- See Diagram 8 (Latency Budget)
- Key optimizations: Caching (session, embedding, KV), edge deployment, continuous batching, prefix caching

**Q: How do you reduce inter-token latency?**
- Flash Attention (2-4x faster attention)
- Quantization (INT8, less memory transfer)
- Continuous batching (high GPU utilization)
- KV cache (reuse past computations)

### Reliability

**Q: How do you handle failures?**
- Multi-AZ: Auto-failover within region (60s)
- Multi-region: Manual failover across regions (10-15 min)
- Stateless services: Auto-restart, health checks
- Database: Synchronous replication (primary-standby)

**Q: What if a region goes down?**
- GeoDNS detects health check failures (30s)
- Route to backup region
- Promote replica to primary (PostgreSQL)
- RTO: 10-15 min, RPO: 5 seconds

### Cost Optimization

**Q: How do you reduce costs?**
- Model routing: Use GPT-3.5 for 60% of queries (10x cheaper)
- Caching: API responses, embeddings (save API calls)
- KV cache: Prefix caching saves 10-15% compute
- Quantization: INT8 models use 2x less memory → smaller GPUs

**Q: What's the cost per 1000 tokens?**
- GPT-4: $0.03 (input) + $0.06 (output)
- GPT-3.5: $0.0015 (input) + $0.002 (output)
- Our cost (infrastructure): $0.01-0.02 (with optimizations)

### Data & Privacy

**Q: How do you handle GDPR?**
- Right to deletion: Cascade delete from all stores
- Right to access: Export API (JSON format)
- Data residency: EU users → EU region only
- Encryption: AES-256 at rest, TLS 1.3 in transit

**Q: How long do you keep data?**
- Hot (PostgreSQL): 90 days
- Cold (S3): 2 years
- Audit logs: 2 years (compliance)
- After retention: Permanent deletion

### RAG (if applicable)

**Q: How do you implement RAG?**
- Offline: Ingest docs → chunk → embed → vector DB
- Online: Query → expand → hybrid search → re-rank → context
- See Diagram 5 for details

**Q: How do you keep RAG data fresh?**
- Incremental updates (daily crawl)
- Event-based invalidation (doc updated)
- Metadata: last_updated timestamp, filter by recency

---

## Drawing Tips (Whiteboard)

### Start Simple
```
[Client] → [API] → [Orchestrator] → [LLM] → [Client]
                         ↓
                      [RAG]
                      [Safety]
                      [Tools]
```

### Add Detail Gradually
- First: Request path (happy path)
- Second: Data stores (DB, cache, vector DB)
- Third: Failure handling (replicas, failover)
- Fourth: Monitoring (metrics, logs)

### Use Layers
- Layer 1: Client, CDN, load balancer
- Layer 2: API gateway, auth, rate limit
- Layer 3: Business logic (orchestrator, RAG, tools)
- Layer 4: Model serving (LLM inference)
- Layer 5: Data layer (DB, cache, storage)

---

## Red Flags to Avoid

❌ Don't say "just use a load balancer" without explaining HOW
❌ Don't ignore cost (GPU inference is $$$ at scale)
❌ Don't hand-wave latency ("it'll be fast")
❌ Don't forget monitoring/observability
❌ Don't ignore security (auth, rate limiting, PII)
❌ Don't over-engineer (start simple, iterate)

✅ Do ask clarifying questions
✅ Do state assumptions explicitly
✅ Do discuss trade-offs (cost vs. latency vs. complexity)
✅ Do mention numbers (QPS, latency, cost)
✅ Do think about failure modes
✅ Do consider the user experience (streaming, latency)

---

## Follow-up Topics (If Time Permits)

- **Multimodal**: Adding image/audio input (vision models, speech-to-text)
- **Fine-tuning**: Custom model training pipeline (data collection, RLHF)
- **Plugins**: Sandboxed execution of user code (Docker, WebAssembly)
- **Code Interpreter**: Stateful Python runtime (Jupyter kernel)
- **Compliance**: SOC 2, ISO 27001, HIPAA
- **A/B Testing**: Experiment framework (feature flags, metrics)
- **Abuse Prevention**: Rate limiting, content filters, ban evasion
- **Mobile**: Offline support, sync, push notifications

---

## Recommended Interview Flow

### Act 1: Requirements (5 min)
- "Can you clarify the requirements?"
- "What's the expected scale? Latency targets?"
- "Are we building the full product or focusing on inference?"

### Act 2: High-Level (10 min)
- Draw Diagram 1 on whiteboard
- Walk through request flow
- Identify key components

### Act 3: Deep Dive (20 min)
- Interviewer picks 2-3 areas
- Common: Model serving, RAG, reliability
- Show trade-offs, numbers, optimizations

### Act 4: Bottlenecks (10 min)
- "What are the main bottlenecks?"
- Latency: Queuing, LLM decode, RAG
- Cost: GPU compute
- Scale: Database writes, vector search

### Act 5: Wrap-up (5 min)
- Monitoring, alerting, SLOs
- Failure modes, recovery
- Future improvements

---

## Good Luck! 🚀

Remember:
1. **Think out loud** - Explain your reasoning
2. **Ask questions** - Clarify ambiguities
3. **Start simple** - Add complexity incrementally
4. **Show trade-offs** - There's no perfect solution
5. **Be honest** - Say "I don't know" if you don't, then reason through it
6. **Have fun** - System design is creative problem-solving!
