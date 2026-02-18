# Diagram 2: Side Rails - Session, Flags, Usage, Observability

## Overview
Supporting services that run alongside the main request path. These handle session management, feature flags, billing/quotas, and observability.

## Architecture Diagram

```
                    ┌─────────────────────┐
                    │    API Gateway      │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                │              │              │
                ▼              ▼              ▼
    ┌───────────────────────────────────────────────────┐
    │                                                   │
    │  ┌─────────────────┐  ┌─────────────────┐        │
    │  │ Session Service │  │ Feature Flags / │        │
    │  │                 │  │  A/B Testing    │        │
    │  └────────┬────────┘  └────────┬────────┘        │
    │           │                    │                 │
    │           ▼                    ▼                 │
    │  ┌─────────────────┐  ┌─────────────────┐        │
    │  │ Conversations   │  │ Experiment      │        │
    │  │ Database        │  │ Store           │        │
    │  │                 │  │                 │        │
    │  │ - chat_id       │  │ - user_id       │        │
    │  │ - user_id       │  │ - experiment_id │        │
    │  │ - messages[]    │  │ - variant       │        │
    │  │ - metadata      │  │ - metrics       │        │
    │  │ - created_at    │  │                 │        │
    │  └────────┬────────┘  └─────────────────┘        │
    │           │                                       │
    │           │ (TTL-based archival)                  │
    │           ▼                                       │
    │  ┌─────────────────┐                             │
    │  │  Cold Storage   │                             │
    │  │  (S3/GCS)       │                             │
    │  │                 │                             │
    │  │  - Partitioned  │                             │
    │  │    by date      │                             │
    │  │  - Compressed   │                             │
    │  │  - Encrypted    │                             │
    │  └─────────────────┘                             │
    │                                                   │
    └───────────────────────────────────────────────────┘

    ┌───────────────────────────────────────────────────┐
    │           Usage Metering Service                  │
    │                                                   │
    │  ┌─────────────────────────────────────────────┐  │
    │  │  Token Counter                              │  │
    │  │  - Input tokens                             │  │
    │  │  - Output tokens                            │  │
    │  │  - Cached tokens                            │  │
    │  └──────────────────┬──────────────────────────┘  │
    │                     │                             │
    │                     ▼                             │
    │  ┌─────────────────────────────────────────────┐  │
    │  │  Billing / Quotas Database                  │  │
    │  │                                             │  │
    │  │  - user_id / org_id                         │  │
    │  │  - tier (free/pro/enterprise)               │  │
    │  │  - tokens_used_this_month                   │  │
    │  │  - requests_today                           │  │
    │  │  - quota_limit                              │  │
    │  │  - overage_allowed                          │  │
    │  └─────────────────────────────────────────────┘  │
    │                     │                             │
    │                     ▼                             │
    │  ┌─────────────────────────────────────────────┐  │
    │  │  Billing Events Queue (Kafka)               │  │
    │  │  → Stripe / Payment Processor               │  │
    │  └─────────────────────────────────────────────┘  │
    └───────────────────────────────────────────────────┘

    ┌───────────────────────────────────────────────────┐
    │          Observability Platform                   │
    │                                                   │
    │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐ │
    │  │   Logging   │  │   Metrics   │  │  Tracing  │ │
    │  │             │  │             │  │           │ │
    │  │ - ELK Stack │  │ - Prometheus│  │ - Jaeger  │ │
    │  │ - Fluent    │  │ - Grafana   │  │ - Zipkin  │ │
    │  │             │  │             │  │           │ │
    │  │ Logs:       │  │ Metrics:    │  │ Traces:   │ │
    │  │ - Requests  │  │ - QPS       │  │ - Req ID  │ │
    │  │ - Errors    │  │ - Latency   │  │ - Spans   │ │
    │  │ - Prompts*  │  │ - GPU util  │  │ - Tags    │ │
    │  │ - Responses*│  │ - Cache hit │  │           │ │
    │  │             │  │ - Error %   │  │           │ │
    │  │ *redacted   │  │             │  │           │ │
    │  └─────────────┘  └─────────────┘  └───────────┘ │
    │                                                   │
    │  ┌─────────────────────────────────────────────┐  │
    │  │  Prompt/Response Store (Audit)              │  │
    │  │  - Full prompts (encrypted)                 │  │
    │  │  - Model outputs (encrypted)                │  │
    │  │  - Safety decisions                         │  │
    │  │  - Feedback (thumbs up/down)                │  │
    │  │  - Used for model improvement & compliance  │  │
    │  └─────────────────────────────────────────────┘  │
    └───────────────────────────────────────────────────┘
```

## Component Details

### 1. Session Service

**Purpose**: Manage conversation state and history

**Responsibilities**:
- Create/retrieve conversation sessions
- Load recent message history
- Manage context window (truncate old messages)
- Handle multi-device sync

**Database Schema** (Conversations DB):
```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    title TEXT,
    model VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    archived BOOLEAN DEFAULT FALSE,
    INDEX idx_user_created (user_id, created_at)
);

CREATE TABLE messages (
    id UUID PRIMARY KEY,
    conversation_id UUID REFERENCES conversations(id),
    role VARCHAR(20), -- 'user', 'assistant', 'system'
    content TEXT,
    tokens INT,
    metadata JSONB, -- tool calls, citations, etc.
    created_at TIMESTAMP,
    INDEX idx_conv_created (conversation_id, created_at)
);
```

**Archival Strategy**:
- Conversations older than 90 days → Cold Storage (S3)
- Compressed with gzip
- Partitioned by year/month/day
- Indexed in metadata DB for retrieval

**Scalability**:
- Read replicas for conversation loading
- Sharding by user_id hash
- Caching recent conversations in Redis (TTL 1 hour)

---

### 2. Feature Flags / A/B Testing

**Purpose**: Control feature rollouts and run experiments

**Use Cases**:
- Gradual model rollout (10% → 50% → 100%)
- A/B test new prompts, system messages
- Regional feature enablement
- Kill switch for problematic features

**Implementation**:
```python
# Example: Check if user should get new model
if feature_flag_service.is_enabled("gpt4_turbo", user_id):
    model = "gpt-4-turbo"
else:
    model = "gpt-3.5-turbo"
```

**Experiment Store**:
- User ID → Experiment variant mapping
- Consistent hashing (same user always gets same variant)
- Metrics collection per variant

**Tools**:
- LaunchDarkly, Optimizely, or custom service
- Real-time flag updates (no redeployment)

---

### 3. Usage Metering & Billing

**Purpose**: Track usage, enforce quotas, generate bills

**Metering Flow**:
1. Count tokens (input + output)
2. Write to Kafka/Kinesis stream
3. Aggregate in time windows (hourly/daily)
4. Update quota database
5. Emit billing events

**Quota Enforcement**:
- **Free Tier**: 10 requests/day, 100K tokens/month
- **Pro Tier**: Unlimited requests, pay-per-token
- **Enterprise**: Custom quotas, reserved capacity

**Database Schema**:
```sql
CREATE TABLE usage (
    user_id UUID,
    date DATE,
    requests_count INT,
    input_tokens BIGINT,
    output_tokens BIGINT,
    cached_tokens BIGINT,
    cost_usd DECIMAL(10,4),
    PRIMARY KEY (user_id, date)
);
```

**Billing Integration**:
- Monthly aggregation → Stripe invoice
- Real-time overage alerts
- Budget caps to prevent runaway costs

---

### 4. Observability Platform

**Purpose**: Monitor system health, debug issues, improve models

#### Logging (ELK Stack)
- **What to log**:
  - Request IDs, user IDs (hashed), conversation IDs
  - Model used, latency, token counts
  - Error messages, stack traces
  - Redacted prompts/responses (for debugging)

- **Retention**:
  - Hot logs: 7 days (Elasticsearch)
  - Warm logs: 30 days (S3 + Athena)
  - Cold logs: 1 year (Glacier)

#### Metrics (Prometheus + Grafana)
- **Infrastructure**:
  - GPU utilization, memory, temperature
  - CPU, network I/O
  - Pod health, restarts

- **Application**:
  - QPS, latency (p50/p95/p99)
  - Error rates (4xx, 5xx)
  - Cache hit ratio (KV cache, embedding cache)
  - Queue depth (inference queue)

- **Business**:
  - Active users, new signups
  - Revenue (tokens × price)
  - Model usage distribution

#### Tracing (Jaeger)
- End-to-end request tracing
- Spans: Gateway → Orchestrator → RAG → LLM → Response
- Helps identify bottlenecks

#### Prompt/Response Store
- **Purpose**: Audit, compliance, model improvement
- **Storage**: Encrypted at rest (AES-256)
- **Access**: Role-based, logged
- **Retention**: 2 years (compliance requirement)
- **Usage**:
  - RLHF training data
  - Safety model fine-tuning
  - Quality audits

---

## Integration Points

### API Gateway → Session Service
```
1. User requests conversation history
2. Gateway validates auth token
3. Calls Session Service with user_id
4. Session Service loads last N messages from DB
5. Returns to Gateway → Client
```

### Orchestrator → Feature Flags
```
1. Orchestrator receives request
2. Checks feature flag: "use_rag_for_queries"
3. If enabled → call RAG service
4. If disabled → skip to LLM
```

### LLM → Usage Metering
```
1. LLM completes generation
2. Count tokens (input: 150, output: 300)
3. Emit event to Kafka: {user_id, tokens, model, timestamp}
4. Metering service aggregates hourly
5. Update quota DB, check limits
```

### All Components → Observability
```
- Every service logs to stdout → Fluent → Elasticsearch
- Every service exposes /metrics → Prometheus scrapes
- Every request has trace_id → Jaeger collects spans
```

---

## Failure Handling

| Component | Failure Mode | Fallback |
|-----------|--------------|----------|
| Session DB | Down | Use cached sessions, limit to 1 turn |
| Feature Flags | Unavailable | Default to off (safe mode) |
| Usage Metering | Queue full | Buffer locally, retry async |
| Billing DB | Write failure | Log to disk, replay later |
| Logging | Elasticsearch down | Buffer in-memory, alert ops |

---

## Security & Privacy

- **PII Redaction**: Prompts/responses redacted before logging
- **Encryption**: At rest (AES-256), in transit (TLS 1.3)
- **Access Control**: RBAC for internal tools
- **Audit Logs**: Who accessed what data, when
- **GDPR Compliance**: User data export/deletion APIs
- **Data Residency**: EU users → EU region only

---

## Costs

| Component | Monthly Cost (at scale) |
|-----------|-------------------------|
| Conversations DB | $50K (RDS Multi-AZ) |
| Cold Storage | $10K (S3 Standard-IA) |
| Feature Flags | $5K (LaunchDarkly) |
| Usage Metering | $20K (Kafka, workers) |
| Observability | $100K (ELK, Prometheus, storage) |
| **Total** | **$185K/month** |
