# Diagram 6: Data Stores and Retention

## Overview
Comprehensive data storage layer for conversations, vectors, billing, experiments, and observability data. Includes retention policies and compliance considerations.

## Architecture Diagram

```
╔════════════════════════════════════════════════════════════════╗
║                    PRIMARY DATA STORES                         ║
╚════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────┐
│  1. Conversations Database (PostgreSQL / DynamoDB)           │
│                                                              │
│  Schema:                                                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Table: conversations                                   │ │
│  │ ─────────────────────────────────────────────────────  │ │
│  │ id               UUID PRIMARY KEY                      │ │
│  │ user_id          UUID NOT NULL                         │ │
│  │ org_id           UUID                                  │ │
│  │ title            TEXT                                  │ │
│  │ model            VARCHAR(50)                           │ │
│  │ created_at       TIMESTAMP                             │ │
│  │ updated_at       TIMESTAMP                             │ │
│  │ archived         BOOLEAN DEFAULT FALSE                 │ │
│  │ metadata         JSONB                                 │ │
│  │                                                        │ │
│  │ Indexes:                                               │ │
│  │ - idx_user_created (user_id, created_at DESC)         │ │
│  │ - idx_org_created (org_id, created_at DESC)           │ │
│  │ - idx_archived (archived, updated_at)                 │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Table: messages                                        │ │
│  │ ─────────────────────────────────────────────────────  │ │
│  │ id               UUID PRIMARY KEY                      │ │
│  │ conversation_id  UUID REFERENCES conversations(id)     │ │
│  │ role             VARCHAR(20)  -- user/assistant/system│ │
│  │ content          TEXT                                  │ │
│  │ tokens           INT                                   │ │
│  │ model_used       VARCHAR(50)                           │ │
│  │ metadata         JSONB  -- citations, tool calls, etc │ │
│  │ created_at       TIMESTAMP                             │ │
│  │                                                        │ │
│  │ Indexes:                                               │ │
│  │ - idx_conv_created (conversation_id, created_at)      │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Access Patterns:                                            │
│  - Read: Load last N messages for conversation (10-50 msgs) │
│  - Write: Append new message after each turn                │
│  - Update: Update conversation title/metadata               │
│  - Delete: Soft delete (archive = true)                     │
│                                                              │
│  Retention:                                                  │
│  - Hot (PostgreSQL): Last 90 days                           │
│  - Warm (PostgreSQL): 90 days - 1 year (compressed)         │
│  - Cold (S3): > 1 year (archived, encrypted)                │
│                                                              │
│  Row-Level Security (RLS):                                   │
│  - Users can only access their own conversations            │
│  - Org admins can access org conversations (if consented)   │
│  - Enforce via: WHERE user_id = current_user_id()           │
│                                                              │
│  Sharding Strategy:                                          │
│  - Shard by user_id hash (consistent hashing)               │
│  - 16 shards initially, can expand to 256                   │
│  - Route queries based on user_id → shard mapping           │
│                                                              │
│  Replication:                                                │
│  - Primary: Write replica (us-west-2)                       │
│  - Read replicas: 3 (load balanced)                         │
│  - Cross-region replica: us-east-1 (DR)                     │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │ (TTL-based archival every 24h)
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  Cold Storage (S3 / Google Cloud Storage)                   │
│                                                              │
│  Structure:                                                  │
│    s3://chatgpt-conversations/                              │
│      ├── year=2024/                                         │
│      │   ├── month=01/                                      │
│      │   │   ├── day=01/                                    │
│      │   │   │   ├── user_123_conv_abc.json.gz             │
│      │   │   │   ├── user_456_conv_def.json.gz             │
│      │   │   ├── day=02/                                    │
│      │   │   │   └── ...                                    │
│      │   ├── month=02/                                      │
│                                                              │
│  Format: JSONL (compressed with gzip)                       │
│  Encryption: AES-256 server-side encryption                 │
│  Access: Rare (user export, compliance audit)               │
│  Lifecycle: Transition to Glacier after 2 years             │
│  Cost: ~$0.023 per GB/month (S3 Standard-IA)                │
└──────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────┐
│  2. Vector Database (Pinecone / Weaviate / Milvus)          │
│                                                              │
│  Purpose: Store embeddings for RAG retrieval                │
│                                                              │
│  Index Structure:                                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Namespace: production                                  │ │
│  │ Dimension: 1536 (text-embedding-ada-002)              │ │
│  │ Metric: Cosine similarity                             │ │
│  │ Index type: HNSW (M=16, ef=200)                       │ │
│  │                                                        │ │
│  │ Vector entry:                                          │ │
│  │ {                                                      │ │
│  │   "id": "doc_123_chunk_5",                            │ │
│  │   "values": [0.023, -0.156, ...],  // 1536 floats    │ │
│  │   "metadata": {                                       │ │
│  │     "text": "Q3 revenue was $5.2B...",               │ │
│  │     "source": "https://...",                         │ │
│  │     "doc_id": "doc_123",                             │ │
│  │     "chunk_index": 5,                                │ │
│  │     "org_id": "org_789",  // access control          │ │
│  │     "created_at": "2024-01-15T10:00:00Z"             │ │
│  │   }                                                   │ │
│  │ }                                                      │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Size: 100M+ vectors (~600 GB)                              │
│  QPS: 10K+ queries per second                               │
│  Latency: p95 < 50ms for top-100 retrieval                  │
│                                                              │
│  Backup Strategy:                                            │
│  - Daily snapshots to S3                                    │
│  - Point-in-time recovery (7 days)                          │
│  - Rebuild from source docs if catastrophic failure         │
│                                                              │
│  Multi-tenancy:                                              │
│  - Metadata filtering: WHERE org_id = 'org_789'             │
│  - Namespaces per tenant (isolation)                        │
│  - Resource quotas per tenant                               │
└──────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────┐
│  3. Blob Store (S3) - Documents & Media                     │
│                                                              │
│  Purpose: Store original documents for RAG                  │
│                                                              │
│  Structure:                                                  │
│    s3://chatgpt-documents/                                  │
│      ├── org_789/                                           │
│      │   ├── doc_123.pdf                                    │
│      │   ├── doc_124.docx                                   │
│      │   ├── image_456.png                                  │
│                                                              │
│  Metadata (in RDS):                                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Table: documents                                       │ │
│  │ ──────────────────────────────────────────────────────│ │
│  │ id              UUID PRIMARY KEY                       │ │
│  │ org_id          UUID                                   │ │
│  │ filename        TEXT                                   │ │
│  │ s3_key          TEXT                                   │ │
│  │ size_bytes      BIGINT                                 │ │
│  │ mime_type       VARCHAR(100)                           │ │
│  │ upload_at       TIMESTAMP                              │ │
│  │ indexed         BOOLEAN  -- embedded in vector DB?     │ │
│  │ index_version   INT                                    │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Access:                                                     │
│  - Upload: Presigned URL (client → S3 direct)               │
│  - Download: Presigned URL (time-limited)                   │
│  - Processing: Lambda / worker pulls from S3                │
│                                                              │
│  Lifecycle:                                                  │
│  - Standard: 90 days                                        │
│  - Standard-IA: 90 days - 1 year                            │
│  - Glacier: > 1 year                                        │
└──────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────┐
│  4. Billing / Quotas Database (PostgreSQL)                  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Table: usage                                           │ │
│  │ ──────────────────────────────────────────────────────│ │
│  │ user_id          UUID                                  │ │
│  │ date             DATE                                  │ │
│  │ requests_count   INT                                   │ │
│  │ input_tokens     BIGINT                                │ │
│  │ output_tokens    BIGINT                                │ │
│  │ cached_tokens    BIGINT                                │ │
│  │ model            VARCHAR(50)                           │ │
│  │ cost_usd         DECIMAL(10, 4)                        │ │
│  │ PRIMARY KEY (user_id, date, model)                     │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Table: quotas                                          │ │
│  │ ──────────────────────────────────────────────────────│ │
│  │ user_id          UUID PRIMARY KEY                      │ │
│  │ tier             VARCHAR(20)  -- free/pro/enterprise  │ │
│  │ requests_per_day INT                                   │ │
│  │ tokens_per_month BIGINT                                │ │
│  │ overage_allowed  BOOLEAN                               │ │
│  │ updated_at       TIMESTAMP                             │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Aggregation:                                                │
│  - Real-time: Redis counters (fast increment)               │
│  - Batch: Hourly job aggregates Redis → PostgreSQL          │
│  - Billing: Monthly job generates invoices                  │
│                                                              │
│  Retention:                                                  │
│  - Current month: Real-time in Redis                        │
│  - Past 24 months: PostgreSQL (detailed)                    │
│  - > 24 months: S3 (aggregated, for audits)                 │
└──────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────┐
│  5. Experiment Store (Redis / PostgreSQL)                   │
│                                                              │
│  Purpose: Track A/B test assignments and metrics            │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Table: experiments                                     │ │
│  │ ──────────────────────────────────────────────────────│ │
│  │ id               UUID PRIMARY KEY                      │ │
│  │ name             TEXT                                  │ │
│  │ start_date       DATE                                  │ │
│  │ end_date         DATE                                  │ │
│  │ variants         JSONB  -- [{name: "A", weight: 50}]  │ │
│  │ status           VARCHAR(20)  -- active/paused/done   │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Table: assignments                                     │ │
│  │ ──────────────────────────────────────────────────────│ │
│  │ experiment_id    UUID                                  │ │
│  │ user_id          UUID                                  │ │
│  │ variant          VARCHAR(50)                           │ │
│  │ assigned_at      TIMESTAMP                             │ │
│  │ PRIMARY KEY (experiment_id, user_id)                   │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Table: experiment_metrics                              │ │
│  │ ──────────────────────────────────────────────────────│ │
│  │ experiment_id    UUID                                  │ │
│  │ variant          VARCHAR(50)                           │ │
│  │ date             DATE                                  │ │
│  │ metric_name      VARCHAR(100)                          │ │
│  │ value            FLOAT                                 │ │
│  │ count            INT                                   │ │
│  │ PRIMARY KEY (experiment_id, variant, date, metric)     │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Example Metrics:                                            │
│  - Latency: avg(response_time_ms) by variant               │
│  - Quality: avg(thumbs_up_rate) by variant                 │
│  - Engagement: avg(messages_per_conversation) by variant    │
└──────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────┐
│  6. Observability Store                                      │
│                                                              │
│  Logs (Elasticsearch):                                       │
│  - Indexed by: timestamp, user_id, request_id, level        │
│  - Retention: 7 days (hot), 30 days (warm), 90 days (cold)  │
│  - Size: ~500 GB/day → 15 TB/month                          │
│                                                              │
│  Metrics (Prometheus):                                       │
│  - Time series DB                                           │
│  - Retention: 15 days (high-res), 90 days (downsampled)     │
│  - Cardinality: ~1M unique series                           │
│                                                              │
│  Traces (Jaeger):                                            │
│  - Spans stored in Cassandra                                │
│  - Retention: 7 days                                        │
│  - Sampling: 1% of requests (adaptive)                      │
│                                                              │
│  Prompt/Response Audit (S3 + Metadata DB):                  │
│  - Full prompts + responses (encrypted)                     │
│  - Metadata in PostgreSQL (searchable)                      │
│  - Retention: 2 years (compliance)                          │
│  - Access: Logged, requires justification                   │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow - Conversation Lifecycle

```
1. User sends message
      ↓
2. Save to PostgreSQL (conversations.messages table)
      ↓
3. [After 90 days] Archive job runs
      ↓
4. Export to S3 (compressed JSON)
      ↓
5. Soft delete from PostgreSQL (or hard delete if desired)
      ↓
6. [After 2 years] Move S3 Standard-IA → Glacier
      ↓
7. [After 7 years] Delete (GDPR compliance)
```

## Compliance & Security

### GDPR Right to Deletion
```sql
-- User requests deletion
DELETE FROM messages WHERE conversation_id IN (
    SELECT id FROM conversations WHERE user_id = 'user_123'
);
DELETE FROM conversations WHERE user_id = 'user_123';

-- Also delete from cold storage
aws s3 rm s3://chatgpt-conversations/ --recursive \
  --exclude "*" --include "*user_123*"

-- Mark vectors for deletion (async cleanup)
UPDATE document_chunks SET deleted = true WHERE user_id = 'user_123';
```

### Encryption
- **At rest**: AES-256 (all databases and storage)
- **In transit**: TLS 1.3
- **Field-level**: Sensitive metadata encrypted separately
- **Key management**: AWS KMS, rotated quarterly

### Access Control
- **Row-level security**: Users can only see their data
- **API tokens**: Scoped permissions (read/write/admin)
- **Audit logging**: All access logged with justification

## Backup & Disaster Recovery

### PostgreSQL
- **Continuous backup**: WAL archiving to S3
- **Point-in-time recovery**: Last 30 days
- **Cross-region replica**: us-east-1 (5min lag)
- **RTO**: 1 hour, **RPO**: 5 minutes

### Vector Database
- **Daily snapshots**: Full index to S3
- **Recovery**: Restore from snapshot (2-4 hours)
- **Fallback**: Rebuild from source docs (12-24 hours)

### S3
- **Versioning**: Enabled
- **Cross-region replication**: Automatic
- **Immutable**: Object lock for compliance

## Cost Breakdown (Monthly, at scale)

| Store | Size | Monthly Cost |
|-------|------|--------------|
| PostgreSQL (RDS) | 5 TB | $10K |
| PostgreSQL Replicas (3x) | 15 TB | $25K |
| S3 Cold Storage | 100 TB | $2.3K |
| Vector DB (Pinecone) | 600 GB | $15K |
| S3 Documents | 50 TB | $1.2K |
| Redis (usage counters) | 100 GB | $500 |
| Elasticsearch (logs) | 15 TB | $20K |
| Prometheus (metrics) | 500 GB | $1K |
| **Total** | - | **$75K** |

## Sharding Strategy (PostgreSQL)

```python
# Consistent hashing
def get_shard(user_id):
    hash_value = hashlib.md5(user_id.encode()).hexdigest()
    shard_num = int(hash_value, 16) % NUM_SHARDS
    return f"shard_{shard_num}"

# Routing
shard = get_shard(user_id)
connection = connection_pool[shard]
result = connection.execute("SELECT * FROM conversations WHERE user_id = %s", user_id)
```

**Expansion**: Double shards (16 → 32) with consistent hashing, minimal resharding

## Interview Talking Points

**Q: How do you handle hot users (celebrities)?**
- Detect via usage metrics
- Dedicated shard or read replica
- Cache conversations in Redis
- Rate limit if abusive

**Q: How do you ensure data consistency?**
- PostgreSQL transactions (ACID)
- Write to primary, read from replicas (eventual consistency ok)
- Critical writes (billing): Synchronous replication

**Q: What if database goes down?**
- Automatic failover to read replica (promoted to primary)
- RTO: 1 hour, RPO: 5 minutes
- Degrade gracefully: serve from cache, queue writes

**Q: How do you handle user data export (GDPR)?**
- Async job: Export all conversations to JSON
- Upload to S3 with presigned URL
- Email user link (expires in 7 days)
