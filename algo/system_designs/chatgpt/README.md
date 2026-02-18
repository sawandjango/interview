# ChatGPT System Design

This directory contains a comprehensive system design for a ChatGPT-like conversational AI platform. The design is broken down into multiple layers and components for better understanding during interviews or architectural discussions.

## Overview

ChatGPT is a large-scale conversational AI system that handles:
- Real-time streaming responses
- Multi-turn conversations with context
- RAG (Retrieval Augmented Generation) for knowledge enhancement
- Tool/Function calling capabilities
- High availability and low latency (p95 TTFT ~500-700ms)
- Rate limiting, quotas, and billing
- Safety and content moderation

## Diagrams

1. **[01_high_level_flow.md](./01_high_level_flow.md)** - End-to-end request flow from client to LLM
2. **[02_side_rails.md](./02_side_rails.md)** - Session management, feature flags, billing, observability
3. **[03_orchestrator_loop.md](./03_orchestrator_loop.md)** - Orchestrator inner logic with tool use
4. **[04_model_serving.md](./04_model_serving.md)** - LLM inference fleet architecture
5. **[05_rag_pipeline.md](./05_rag_pipeline.md)** - RAG data ingestion and retrieval
6. **[06_data_stores.md](./06_data_stores.md)** - Database and storage layer
7. **[07_reliability_regions.md](./07_reliability_regions.md)** - Multi-region deployment and failover
8. **[08_latency_budget.md](./08_latency_budget.md)** - Latency breakdown and SLOs
9. **[09_authentication_authorization.md](./09_authentication_authorization.md)** - Auth and security layer
10. **[10_caching_strategy.md](./10_caching_strategy.md)** - Caching at multiple levels

## Key Design Decisions

### Scale Numbers (Interview Reference)
- **Users**: 100M+ DAU
- **Requests**: 1M+ QPS at peak
- **Latency**: p95 TTFT < 700ms, p99 < 1s
- **Availability**: 99.9% uptime SLO
- **Models**: Multiple (GPT-4, GPT-3.5, fine-tuned variants)
- **Data**: Petabyte-scale conversation history

### Technology Stack (Example)
- **API Gateway**: Kong / Envoy
- **Load Balancer**: GeoDNS + L7 LB
- **Orchestration**: Kubernetes
- **Inference**: vLLM / TensorRT-LLM on A100/H100 GPUs
- **Vector DB**: Pinecone / Weaviate / Milvus
- **Primary DB**: PostgreSQL (conversations, users)
- **Cache**: Redis (KV cache, session state)
- **Message Queue**: Kafka (async processing)
- **Object Storage**: S3 (docs, cold storage)
- **Observability**: Prometheus, Grafana, Jaeger, ELK

## Interview Talk Track

### How to Present (Step-by-step)
1. Start with **Diagram 1** - Overall flow (5 min)
2. Deep dive into **Orchestrator** (Diagram 3) - Core logic (5 min)
3. Explain **Model Serving** (Diagram 4) - How LLMs scale (5 min)
4. Discuss **RAG** if asked (Diagram 5) - Knowledge retrieval (3 min)
5. Cover **Reliability** (Diagram 7) - Multi-region, failover (3 min)
6. Show **Latency Budget** (Diagram 8) - Performance optimization (2 min)
7. Q&A on side rails (sessions, billing, safety) as needed

### Common Interview Questions

**Q: How do you handle rate limiting?**
- Token bucket algorithm per user/organization
- Distributed rate limiter (Redis)
- Tiered quotas (free, pro, enterprise)

**Q: How do you reduce latency?**
- KV cache reuse across requests
- Speculative decoding
- Model distillation for faster variants
- Edge deployment for routing
- Continuous batching

**Q: How do you handle long conversations?**
- Context window management (truncation strategies)
- Summarization of old messages
- Sliding window with importance scoring

**Q: How do you ensure safety?**
- Pre-moderation (before LLM)
- Post-moderation (after LLM, before user)
- RLHF/RLAIF trained models
- Prompt injection detection
- PII redaction

**Q: How do you scale inference?**
- Horizontal scaling: more GPU pods
- Model parallelism: split model across GPUs
- Request batching: batch compatible requests
- Auto-scaling based on queue depth

**Q: How do you handle failures?**
- Circuit breakers
- Graceful degradation (fallback to smaller model)
- Multi-region failover
- Request retry with backoff
- Dead letter queues

**Q: How do you monitor?**
- Request tracing (Jaeger)
- Metrics (latency, throughput, error rate)
- Logging (redacted prompts/responses)
- Alerting (SLO violations)
- A/B experiment analytics

## Bottlenecks and Optimizations

| Component | Bottleneck | Solution |
|-----------|------------|----------|
| LLM Inference | GPU compute | Batching, KV cache, quantization |
| RAG Retrieval | Vector search latency | Approximate NN, caching, indexing |
| Database | Write throughput | Sharding, async writes, batching |
| Network | Token streaming | SSE/WebSocket, CDN edge termination |
| Memory | KV cache size | Paging, eviction policies |

## Extensions and Advanced Topics

- **Plugin System**: Sandboxed execution of user plugins
- **Code Interpreter**: Secure Python runtime with stateful sessions
- **Multimodal**: Image/audio input processing pipeline
- **Fine-tuning**: Custom model training pipeline
- **Compliance**: GDPR, data residency, audit logs
- **Cost Optimization**: Model routing based on complexity, caching, prompt compression
