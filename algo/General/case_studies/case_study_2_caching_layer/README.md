# Case Study 2: Chatbot Caching and Query Optimization Layer

## 📋 Scenario

Design a scalable backend layer for a chatbot that pulls data from a data warehouse (e.g., Redshift or BigQuery) and serves summarized insights. Since real-time querying is expensive, intelligent caching and key-based lookup strategies are required.

## 🎯 Success Metrics

- Reduce redundant data warehouse hits by 80% via Redis caching
- Cache hit ratio above 85% for high-traffic queries
- Less than 1% of stale data served across test queries

## 💻 Technical Requirements

### Core Components
- Redis caching layer with intelligent key generation
- Data warehouse integration (Redshift/BigQuery)
- Cache invalidation mechanism (hourly batch jobs)
- Query intent classifier (ML-based routing)
- Cache warming and preloading system
- Monitoring and metrics dashboard

### Architecture Overview
```
User Query
    ↓
Intent Classifier (ML)
    ↓
    ├──→ Cache Hit? → Return cached data (fast)
    │
    └──→ Cache Miss → Query warehouse (slow)
                     ↓
                   Cache result
                     ↓
                   Return data
```

## 📚 Questions

### 1. [Cache Key Design for Complex Queries](./01_cache_key_design.md) 🟢
**Topic:** Cache Design, Key Generation

**Scenario:** Design cache keys for queries with 5+ filters without key explosion

**Key Skills Tested:**
- Hash function design
- Collision handling
- Key normalization
- Uniqueness vs readability

---

### 2. [Semantic Query Matching](./02_semantic_matching.md) 🔴
**Topic:** NLP, Cache Optimization

**Scenario:** "Q1 sales" and "Jan-Mar revenue" should hit same cache

---

### 3. [Partial Cache Hits](./03_partial_cache.md) 🟡
**Topic:** Cache Strategies

**Scenario:** User asks for 10 products, 7 cached, 3 not

---

### 4. [Cache Stampede Prevention](./04_cache_stampede.md) 🟡
**Topic:** Distributed Systems, Locking

**Scenario:** Popular cache expires, 1000 requests hit warehouse

---

### 5. [Redis Memory Management](./05_redis_memory.md) 🟢
**Topic:** Redis, Eviction Policies

**Scenario:** Redis hits memory limit, need eviction strategy

---

### 6. [Cache Warming Strategy](./06_cache_warming.md) 🟡
**Topic:** Preloading, Performance

**Scenario:** Warm top 100 queries before peak traffic

---

### 7. [Stale Data Handling](./07_stale_data.md) 🟡
**Topic:** Consistency, TTL

**Scenario:** Data updates hourly, prevent serving stale data

---

### 8. [ML-Based Cache Routing](./08_ml_routing.md) 🔴
**Topic:** ML Integration

**Scenario:** ML decides which queries to cache vs skip

---

### 9. [Redis High Availability](./09_redis_ha.md) 🔴
**Topic:** HA, Failover

**Scenario:** Design Redis cluster for zero downtime

---

### 10. [Cache Monitoring & Metrics](./10_monitoring.md) 🟢
**Topic:** Observability

**Scenario:** Build monitoring dashboard for cache performance

---

## 🎯 Learning Path

**Recommended Order:**
1. Start with 1, 5, 10 (fundamentals)
2. Then 4, 6, 7 (common patterns)
3. Finally 2, 8, 9 (advanced)

---

## 💡 Key Concepts Covered

- **Caching:** TTL, Eviction, Warming, Stampede prevention
- **Redis:** Architecture, Clustering, HA, Memory management
- **Consistency:** Invalidation, Staleness, Eventually consistent
- **Performance:** Hit ratio optimization, Latency reduction
- **ML:** Query classification, Semantic matching
- **Monitoring:** Metrics, Alerting, Dashboards

---

[← Back to Main README](../README.md)
