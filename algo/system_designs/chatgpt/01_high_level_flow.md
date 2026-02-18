# Diagram 1: High-Level Request Flow

## Overview
This diagram shows the complete end-to-end flow of a user request from the client to the LLM and back.

## Architecture Diagram

```
┌─────────────────────────┐
│ Client (Web/Mobile/API) │
└───────────┬─────────────┘
            │
            │ HTTPS (SSE / WebSocket)
            │ Authorization: Bearer <token>
            ▼
┌───────────────────────────────────────────────────────────┐
│               API Gateway + Auth Layer                     │
│  - SSL Termination                                         │
│  - JWT Validation                                          │
│  - Request Signing                                         │
└───────────┬───────────────────────────────────────────────┘
            │
            ▼
┌───────────────────────────────────────────────────────────┐
│               Rate Limiter + Quotas                        │
│  - Token bucket per user/org                               │
│  - Redis-based distributed limiting                        │
│  - Tier-based quotas (free/pro/enterprise)                 │
└───────────┬───────────────────────────────────────────────┘
            │
            ▼
┌───────────────────────────────────────────────────────────┐
│                   Request Router                           │
│  - Route to region based on latency                        │
│  - Load balancing across AZs                               │
│  - Request deduplication                                   │
└───────────┬───────────────────────────────────────────────┘
            │
            ▼
┌───────────────────────────────────────────────────────────┐
│            Orchestrator / Planner Service                  │
│  - Conversation context loading                            │
│  - Request decomposition                                   │
│  - Execution planning (RAG? Tools? Direct LLM?)            │
└───┬───────┬───────────────────────────────────────────┬───┘
    │       │                                           │
    │       │                                           │
    ▼       ▼                                           ▼
┌─────────────┐  ┌─────────────────────┐  ┌──────────────────────┐
│   Safety    │  │    RAG Service      │  │ Tool/Function Calls  │
│  Filters    │  │                     │  │                      │
│ (Pre-LLM)   │  │  ┌───────────────┐  │  │  ┌────────────────┐  │
│             │  │  │  Query        │  │  │  │ Tool Adapters  │  │
│ - Prompt    │  │  │  Expansion    │  │  │  │ - Web Search   │  │
│   Injection │  │  └───────┬───────┘  │  │  │ - Calculator   │  │
│ - PII       │  │          │          │  │  │ - Database     │  │
│   Detection │  │          ▼          │  │  │ - API Calls    │  │
│ - Toxic     │  │  ┌───────────────┐  │  │  └────────────────┘  │
│   Content   │  │  │  Retriever    │  │  │                      │
└──────┬──────┘  │  │  (Hybrid)     │  │  └──────────┬───────────┘
       │         │  └───────┬───────┘  │             │
       │         │          │          │             │
       │         │          ▼          │             │
       │         │  ┌───────────────┐  │             │
       │         │  │  Vector DB    │  │             │
       │         │  │  + Re-ranker  │  │             │
       │         │  └───────┬───────┘  │             │
       │         │          │          │             │
       │         │          ▼          │             │
       │         │  ┌───────────────┐  │             │
       │         │  │ Context       │  │             │
       │         │  │ (k chunks)    │  │             │
       │         │  └───────────────┘  │             │
       │         └─────────┬───────────┘             │
       │                   │                         │
       └───────────────────┴─────────────────────────┘
                           │
                           ▼
            ┌──────────────────────────┐
            │      LLM Router          │
            │  - Model selection       │
            │  - Region selection      │
            │  - Cost optimization     │
            └──────────┬───────────────┘
                       │
                       ▼
    ┌──────────────────────────────────────────┐
    │       Model Serving Fleet                │
    │                                           │
    │  ┌────────────────────────────────────┐  │
    │  │      GPU Inference Pods            │  │
    │  │  - vLLM / TensorRT-LLM             │  │
    │  │  - Continuous batching             │  │
    │  │  - KV cache (attention reuse)      │  │
    │  └────────────────────────────────────┘  │
    └──────────────────┬───────────────────────┘
                       │
                       │ Stream tokens
                       ▼
            ┌──────────────────────────┐
            │   Safety Filter (Post)   │
            │  - Content moderation    │
            │  - Harmful output detect │
            └──────────┬───────────────┘
                       │
                       │ SSE/WebSocket
                       ▼
            ┌──────────────────────────┐
            │    Client (streaming)    │
            └──────────────────────────┘
```

## Request Flow Steps

1. **Client Request**
   - User sends message via HTTPS
   - Connection upgraded to SSE/WebSocket for streaming
   - Includes: conversation_id, message, model preference, settings

2. **API Gateway**
   - SSL termination
   - JWT validation (user identity)
   - Request logging and correlation ID generation

3. **Rate Limiting**
   - Check user quota (requests/day, tokens/month)
   - Apply token bucket algorithm
   - Return 429 if limit exceeded

4. **Request Router**
   - Geographic routing (latency-based)
   - Load balancing across availability zones
   - Health check-based routing

5. **Orchestrator**
   - Load conversation history from DB
   - Determine execution plan:
     - Need RAG? (based on knowledge cutoff, user request)
     - Need tools? (based on intent detection)
     - Direct LLM call?

6. **Parallel Execution** (if needed)
   - **Safety Filter**: Check prompt for violations
   - **RAG**: Retrieve relevant context from knowledge base
   - **Tools**: Execute function calls (search, calculate, etc.)

7. **LLM Router**
   - Select appropriate model (GPT-4, GPT-3.5, custom)
   - Route to least-loaded region
   - Consider cost vs. quality trade-offs

8. **Inference**
   - Queue request in inference pool
   - Batch with compatible requests
   - Generate tokens with KV cache
   - Stream tokens back to client

9. **Post-processing**
   - Safety check on generated content
   - Citation formatting (if RAG was used)
   - Token counting for billing

10. **Response**
    - Stream tokens to client in real-time
    - Save conversation turn to database
    - Log metrics (latency, tokens, model used)

## Key Design Choices

### Why SSE/WebSocket?
- Real-time streaming of tokens
- Better UX (user sees response as it's generated)
- Reduces perceived latency

### Why Pre and Post Safety?
- **Pre-LLM**: Prevent malicious prompts, save compute
- **Post-LLM**: Catch model hallucinations, harmful outputs

### Why LLM Router?
- Cost optimization (route simple queries to cheaper models)
- Load balancing across regions
- A/B testing different models

### Why Orchestrator?
- Central decision point for complex workflows
- Simplifies client (client doesn't need to know about RAG/tools)
- Enables sophisticated multi-step reasoning

## Failure Modes

| Failure | Impact | Mitigation |
|---------|--------|------------|
| API Gateway down | All requests fail | Multi-region deployment, health checks |
| Rate limiter unavailable | Can't enforce limits | Fail open with logging, cache limits locally |
| Orchestrator crash | Request fails | Retry with backoff, circuit breaker |
| RAG timeout | Slow response | Timeout after 200ms, proceed without context |
| LLM pod crash | Request fails | Auto-scaling, health checks, retry |
| Safety filter timeout | Slow response | Fail open (allow) or fail closed (block) based on risk |

## Scalability

- **API Gateway**: Horizontal scaling, 10K+ RPS per instance
- **Rate Limiter**: Distributed Redis cluster, millions of keys
- **Orchestrator**: Stateless, scale to 1000s of instances
- **LLM Fleet**: Add GPU pods on demand, 100+ pods per model
- **Safety**: Edge-deployed models, <50ms latency

## Metrics to Monitor

- **Latency**: p50, p95, p99 per component
- **Throughput**: QPS per endpoint
- **Error Rate**: 4xx, 5xx by component
- **Quota**: Usage per user/org
- **Cost**: Tokens generated per model, compute cost
