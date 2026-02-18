# Diagram 7: Reliability and Multi-Region Architecture

## Overview
Multi-region deployment strategy for high availability, disaster recovery, and latency optimization. Includes failover mechanisms and data replication.

## Architecture Diagram

```
╔═══════════════════════════════════════════════════════════════╗
║                 GLOBAL TRAFFIC MANAGEMENT                     ║
╚═══════════════════════════════════════════════════════════════╝

                    ┌──────────────────────┐
                    │   Anycast / GeoDNS   │
                    │  (Cloudflare / R53)  │
                    │                      │
                    │  Routes to nearest   │
                    │  healthy region      │
                    └──────────┬───────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│   Region: US-W  │   │   Region: US-E  │   │   Region: EU    │
│   (Primary)     │   │   (Active)      │   │   (Active)      │
│                 │   │                 │   │                 │
│   AZ-1    AZ-2  │   │   AZ-1    AZ-2  │   │   AZ-1    AZ-2  │
│    │       │    │   │    │       │    │   │    │       │    │
│    ▼       ▼    │   │    ▼       ▼    │   │    ▼       ▼    │
│  [API] [API]    │   │  [API] [API]    │   │  [API] [API]    │
│  [LLM] [LLM]    │   │  [LLM] [LLM]    │   │  [LLM] [LLM]    │
│  [RAG] [RAG]    │   │  [RAG] [RAG]    │   │  [RAG] [RAG]    │
│                 │   │                 │   │                 │
│  ┌───────────┐  │   │  ┌───────────┐  │   │  ┌───────────┐  │
│  │PostgreSQL │  │   │  │PostgreSQL │  │   │  │PostgreSQL │  │
│  │ (Primary) │  │   │  │ (Replica) │  │   │  │ (Replica) │  │
│  └─────┬─────┘  │   │  └─────▲─────┘  │   │  └─────▲─────┘  │
│        │        │   │        │        │   │        │        │
│        └────────┼───┼────────┴────────┼───┼────────┘        │
│                 │   │                 │   │                 │
│  ┌───────────┐  │   │  ┌───────────┐  │   │  ┌───────────┐  │
│  │ Vector DB │  │   │  │ Vector DB │  │   │  │ Vector DB │  │
│  │(Primary)  │  │   │  │ (Synced)  │  │   │  │ (Synced)  │  │
│  └─────┬─────┘  │   │  └─────▲─────┘  │   │  └─────▲─────┘  │
│        │        │   │        │        │   │        │        │
│        └────────┼───┼────────┴────────┼───┼────────┘        │
│                 │   │                 │   │                 │
│  ┌───────────┐  │   │  ┌───────────┐  │   │  ┌───────────┐  │
│  │  Redis    │  │   │  │  Redis    │  │   │  │  Redis    │  │
│  │ (Cache)   │  │   │  │ (Cache)   │  │   │  │ (Cache)   │  │
│  └───────────┘  │   │  └───────────┘  │   │  └───────────┘  │
│                 │   │                 │   │                 │
│  Health: ✓      │   │  Health: ✓      │   │  Health: ✓      │
│  Latency: 50ms  │   │  Latency: 60ms  │   │  Latency: 80ms  │
│  Load: 40%      │   │  Load: 35%      │   │  Load: 25%      │
└─────────────────┘   └─────────────────┘   └─────────────────┘
         │                     │                     │
         │                     │                     │
         └─────────────────────┴─────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  S3 (Global)         │
                    │  - Cross-region      │
                    │    replication       │
                    │  - Versioning        │
                    └──────────────────────┘


╔═══════════════════════════════════════════════════════════════╗
║                    SINGLE REGION DETAIL                       ║
╚═══════════════════════════════════════════════════════════════╝

                      Region: US-West-2
        ┌────────────────────────────────────────────┐
        │                                            │
        │     ┌──────────────┬──────────────┐        │
        │     │   AZ-1       │   AZ-2       │        │
        │     │              │              │        │
        │     │  ┌────────┐  │  ┌────────┐  │        │
        │     │  │  ALB   │  │  │  ALB   │  │        │
        │     │  └───┬────┘  │  └───┬────┘  │        │
        │     │      │       │      │       │        │
        │     │      ▼       │      ▼       │        │
        │     │  ┌────────┐  │  ┌────────┐  │        │
        │     │  │ API    │  │  │ API    │  │        │
        │     │  │Gateway │  │  │Gateway │  │        │
        │     │  └───┬────┘  │  └───┬────┘  │        │
        │     │      │       │      │       │        │
        │     │      ▼       │      ▼       │        │
        │     │  ┌────────┐  │  ┌────────┐  │        │
        │     │  │Orchestr│  │  │Orchestr│  │        │
        │     │  │ -ator  │  │  │ -ator  │  │        │
        │     │  └───┬────┘  │  └───┬────┘  │        │
        │     │      │       │      │       │        │
        │     │      ▼       │      ▼       │        │
        │     │  ┌────────┐  │  ┌────────┐  │        │
        │     │  │  LLM   │  │  │  LLM   │  │        │
        │     │  │  Pods  │  │  │  Pods  │  │        │
        │     │  └────────┘  │  └────────┘  │        │
        │     │              │              │        │
        │     └──────────────┴──────────────┘        │
        │                                            │
        │  Shared Services (Multi-AZ):               │
        │  ┌──────────────────────────────────────┐  │
        │  │ PostgreSQL (RDS Multi-AZ)            │  │
        │  │ - Primary in AZ-1                    │  │
        │  │ - Standby in AZ-2 (sync replication) │  │
        │  │ - Auto-failover: 60-120 seconds      │  │
        │  └──────────────────────────────────────┘  │
        │                                            │
        │  ┌──────────────────────────────────────┐  │
        │  │ Redis Cluster (ElastiCache)          │  │
        │  │ - 3 nodes across AZs                 │  │
        │  │ - Automatic failover                 │  │
        │  └──────────────────────────────────────┘  │
        │                                            │
        │  ┌──────────────────────────────────────┐  │
        │  │ Vector DB (Managed / Self-hosted)    │  │
        │  │ - Replicated across AZs              │  │
        │  └──────────────────────────────────────┘  │
        └────────────────────────────────────────────┘
```

## Data Replication Strategy

### 1. PostgreSQL (Conversations)
```
┌────────────────────────────────────────────────────────┐
│                                                        │
│  US-West (Primary)                                     │
│    │                                                   │
│    ├──> US-East (Read Replica, Async)                 │
│    │    - Replication lag: ~5 seconds                 │
│    │    - Read-only queries                           │
│    │                                                   │
│    └──> EU (Read Replica, Async)                      │
│         - Replication lag: ~10 seconds                │
│         - Data residency compliance                   │
│                                                        │
│  Failover:                                             │
│    1. Health check detects primary failure            │
│    2. Promote US-East replica to primary (manual)     │
│    3. Update DNS to point to new primary              │
│    4. Total time: 5-15 minutes (RTO)                  │
│    5. Data loss: Last ~5 seconds (RPO)                │
└────────────────────────────────────────────────────────┘
```

### 2. Vector Database
```
┌────────────────────────────────────────────────────────┐
│                                                        │
│  US-West (Primary)                                     │
│    │                                                   │
│    ├──> Daily snapshot to S3                          │
│    │                                                   │
│    ├──> Async replication to US-East                  │
│    │    - Delta sync every 1 hour                     │
│    │    - Full sync every 24 hours                    │
│    │                                                   │
│    └──> Async replication to EU                       │
│         - Delta sync every 4 hours                    │
│                                                        │
│  Failover:                                             │
│    - Point queries to US-East (may be slightly stale) │
│    - Rebuild from S3 snapshot if needed (2-4 hours)   │
└────────────────────────────────────────────────────────┘
```

### 3. S3 (Documents, Cold Storage)
```
┌────────────────────────────────────────────────────────┐
│                                                        │
│  S3 Cross-Region Replication (CRR)                    │
│                                                        │
│  US-West bucket                                        │
│    │                                                   │
│    ├──> US-East bucket (automatic, <15 min)           │
│    │                                                   │
│    └──> EU bucket (automatic, <15 min)                │
│                                                        │
│  Replication: Near real-time                          │
│  Consistency: Eventual (typically <1 minute)          │
│  Versioning: Enabled (protect against accidental delete)│
└────────────────────────────────────────────────────────┘
```

## Failure Scenarios & Mitigation

### Scenario 1: Single AZ Failure
```
Problem: AZ-1 in US-West goes down

Impact:
- 50% of API/LLM capacity in region lost
- PostgreSQL auto-fails to AZ-2 standby (60s)
- Redis cluster rebalances (30s)

Mitigation:
- Load balancer routes all traffic to AZ-2
- Auto-scaling adds capacity in AZ-2
- Total disruption: ~2 minutes (mostly routing)
- User impact: Minimal (automatic retry succeeds)

Recovery:
- AZ-1 comes back online
- Gradual drain traffic back to AZ-1
- No manual intervention needed
```

### Scenario 2: Full Region Failure
```
Problem: US-West region completely unavailable

Impact:
- All US-West traffic must reroute
- PostgreSQL primary unavailable
- Vector DB primary unavailable

Mitigation:
1. GeoDNS detects health check failures (30s)
2. Route traffic to US-East (becomes new primary)
3. Promote US-East PostgreSQL replica to primary (manual, 5 min)
4. Point Vector DB queries to US-East (stale by ~1 hour)
5. S3 traffic automatically served from US-East

Total RTO: 10-15 minutes
RPO: 5 seconds (PostgreSQL), 1 hour (Vector DB)

User impact:
- Brief 503 errors during DNS switch (~1 min)
- Increased latency for West Coast users (routing to East)
- Slightly stale RAG results (1 hour lag)

Recovery:
- US-West comes back online
- Resync data from US-East
- Gradual traffic shift back to US-West
- Total recovery time: 2-4 hours
```

### Scenario 3: Database Split Brain
```
Problem: Network partition causes both regions to think they're primary

Prevention:
- Use consensus (Raft/Paxos) for leader election
- Require quorum (majority of replicas agree)
- Fencing: Old primary shut down before promoting new

Detection:
- Monitor replication lag
- Alert if lag > 30 seconds
- Auto-page on-call if lag > 2 minutes

Resolution:
- Automated: Quorum-based leader election
- Manual fallback: DBA promotes correct primary
```

### Scenario 4: LLM Inference Pod Crash
```
Problem: GPU OOM or hardware failure

Detection:
- Kubernetes liveness probe fails (3 consecutive checks)
- Pod marked unhealthy (<10s)

Mitigation:
- In-flight requests: Retry on healthy pod
- Queue: Reroute to other pods
- Auto-scaling: New pod spins up (2-3 min for model load)

User impact:
- Single request may see 5-10s delay (retry)
- Overall throughput reduced by ~10% (1 pod out of 10)

Recovery:
- Automatic pod restart
- Model reloaded from shared storage
- No data loss (stateless inference)
```

## Health Checks & Monitoring

### Regional Health Metrics
```python
# Health check endpoint (called every 10s)
@app.route('/health')
def health():
    checks = {
        'database': check_db_connection(),  # < 100ms
        'redis': check_redis_connection(),  # < 50ms
        'llm': check_llm_ready(),           # < 200ms
        'vector_db': check_vector_db(),     # < 100ms
    }

    if all(checks.values()):
        return {'status': 'healthy'}, 200
    else:
        return {'status': 'unhealthy', 'checks': checks}, 503

# GeoDNS uses this to route traffic
# If 3 consecutive failures → remove region from rotation
```

### SLO-based Alerts
```yaml
alerts:
  - name: HighErrorRate
    expr: error_rate_5m > 1%  # More than 1% errors
    action: Page on-call

  - name: HighLatency
    expr: p95_latency > 700ms  # p95 TTFT > 700ms
    action: Slack alert, investigate

  - name: RegionDown
    expr: health_check_failures > 3
    action: Auto-failover to backup region, page on-call

  - name: DatabaseLagHigh
    expr: replication_lag_seconds > 30
    action: Alert DBA
```

## Geographic Routing Logic

```python
# GeoDNS routing logic
def route_request(client_ip):
    client_location = geoip_lookup(client_ip)

    # Preferred regions by client location
    region_preferences = {
        'US-West': ['us-west-2', 'us-east-1', 'eu-central-1'],
        'US-East': ['us-east-1', 'us-west-2', 'eu-central-1'],
        'Europe': ['eu-central-1', 'us-east-1', 'us-west-2'],
        'Asia': ['ap-southeast-1', 'us-west-2', 'us-east-1'],
    }

    for region in region_preferences[client_location]:
        if is_region_healthy(region):
            return region

    # Fallback: Any healthy region
    return get_any_healthy_region()
```

## Capacity Planning

### Target Metrics
- **QPS per region**: 500K at peak
- **LLM pods**: 50-100 per region (autoscale)
- **Database**: 10K connections, 50K QPS
- **Cache**: 1M keys, 100K ops/sec

### Autoscaling Rules
```yaml
# LLM pods
autoscaling:
  min_replicas: 10
  max_replicas: 100
  metrics:
    - type: queue_depth
      target: 20  # avg queue depth < 20
    - type: gpu_utilization
      target: 80%  # keep GPUs busy

# API Gateway
autoscaling:
  min_replicas: 5
  max_replicas: 50
  metrics:
    - type: cpu
      target: 70%
    - type: requests_per_second
      target: 1000
```

## Cost Optimization

### Multi-Region Cost
| Component | Single Region | Multi-Region (3x) | Delta |
|-----------|---------------|-------------------|-------|
| Compute | $200K | $600K | +$400K |
| Database | $50K | $120K | +$70K (replicas) |
| Networking | $20K | $100K | +$80K (cross-region) |
| **Total** | **$270K** | **$820K** | **+$550K (2x)** |

**Trade-off**: 2x cost for 99.9% → 99.99% availability

### Smart Routing (Cost Optimization)
- Route simple queries to cheaper models (GPT-3.5 in US-East)
- Route complex queries to best model (GPT-4 in US-West)
- Cache common queries in CDN edge locations

## Interview Talking Points

**Q: How do you ensure high availability?**
- Multi-AZ within region (automatic failover)
- Multi-region deployment (manual failover)
- Redundancy at every layer (LB, API, DB, cache)
- Target: 99.9% uptime (43 min downtime/month)

**Q: What's the trade-off between consistency and latency?**
- Writes: Synchronous to primary, async to replicas
- Reads: Eventually consistent (5-10s lag acceptable for conversations)
- Critical data (billing): Synchronous replication

**Q: How do you handle network partitions?**
- Quorum-based consensus (Raft/Paxos)
- Prefer availability over consistency (AP in CAP)
- Manual intervention for split-brain scenarios

**Q: How do you test failover?**
- Chaos engineering (terminate random pods)
- Regular DR drills (quarterly)
- Synthetic monitoring (continuous failover tests)
