# Case Study 1: Secure Chatbot API Platform with RBAC

## 📋 Scenario

Build the backend architecture for an enterprise chatbot platform that supports multiple user roles (admin, analyst, guest) and offers tailored access to AI-generated insights. The chatbot assists users with querying sales data, generating summaries, and triggering workflow actions (like generating reports).

## 🎯 Success Metrics

- 99% of access violations prevented by RBAC checks
- 95th percentile API response time under 500ms (excluding async LLM tasks)
- 100% audit logging coverage for user interactions and access patterns

## 💻 Technical Requirements

### Core Components
- REST/GraphQL API for chatbot interaction
- Role-Based Access Control (RBAC) system
- Conversation history storage (PostgreSQL or MongoDB)
- Async task processing (Celery + Redis)
- Token-based authentication (JWT or OAuth2)
- ML sentence classification model for query routing
- Rate limiting and audit logging

### Architecture Overview
```
User Request
    ↓
API Gateway (Auth + Rate Limit)
    ↓
RBAC Layer (Permission Check)
    ↓
┌─────────────┬──────────────┐
│ Sync API    │  Async Queue │
│ (Fast)      │  (LLM/Heavy) │
└─────────────┴──────────────┘
    ↓                ↓
Database         Celery Workers
(Conversations)   (LLM Processing)
    ↓
Audit Logs
```

## 📚 Questions

### 1. [JWT Token Security & Breach Response](./01_jwt_security.md) 🟢
**Topic:** Authentication, Security, Incident Response

**Scenario:** JWT secret key leaked on GitHub. 50,000 active tokens compromised.

**Key Skills Tested:**
- Token invalidation strategies
- Stateless vs stateful sessions
- Redis integration
- Incident response planning

---

### 2. [Rate Limiting Across Multiple Servers](./02_rate_limiting.md) 🟡
**Topic:** Distributed Systems, Rate Limiting

**Scenario:** Enforce 100 req/min per user across 5 load-balanced API servers.

**Key Skills Tested:**
- Distributed counters
- Redis patterns
- Clock skew handling
- Sliding vs fixed windows

---

### 3. [Database Design for Conversations](./03_database_design.md) 🟢
**Topic:** Database Design, Data Modeling

**Scenario:** Design database schema for conversations with branching, attachments, metadata.

**Key Skills Tested:**
- MongoDB vs PostgreSQL trade-offs
- Schema design for nested data
- Query optimization
- Horizontal scaling

---

### 4. [Handling Long-Running LLM Requests](./04_async_processing.md) 🟡
**Topic:** Async Processing, Task Queues

**Scenario:** GPT-4 requests take 30s. Prevent blocking fast queries.

**Key Skills Tested:**
- Head-of-line blocking
- Queue management
- Celery configuration
- Graceful degradation

---

### 5. [Cache Invalidation Strategy](./05_cache_invalidation.md) 🟡
**Topic:** Caching, Consistency

**Scenario:** Data warehouse updates hourly. Keep cache fresh without staleness.

**Key Skills Tested:**
- TTL strategies
- Event-based invalidation
- Cache stampede prevention
- Version-based caching

---

### 6. [Multi-Tenancy & Data Isolation](./06_multi_tenancy.md) 🔴
**Topic:** Security, Multi-Tenancy

**Scenario:** 100 companies sharing one database. Ensure Company A never sees Company B's data.

**Key Skills Tested:**
- Tenant isolation patterns
- Row-level security
- Testing strategies
- Compliance

---

### 7. [Model Version Deployment](./07_model_deployment.md) 🟡
**Topic:** ML Ops, A/B Testing

**Scenario:** Deploy model v2 (92% accuracy) safely without breaking v1 (85% accuracy).

**Key Skills Tested:**
- Canary deployments
- Shadow mode testing
- Gradual rollout
- Rollback criteria

---

### 8. [GDPR Right to be Forgotten](./08_gdpr_deletion.md) 🔴
**Topic:** Compliance, Data Privacy

**Scenario:** User requests deletion of all data. Must purge from database, backups, logs, cache.

**Key Skills Tested:**
- GDPR compliance
- Backup handling
- Soft vs hard delete
- Audit trails

---

### 9. [Debugging Production Latency](./09_latency_debugging.md) 🟢
**Topic:** Performance, Debugging

**Scenario:** p95 latency spikes to 5000ms. p50 is fine at 200ms.

**Key Skills Tested:**
- Distributed tracing
- Performance profiling
- Database query optimization
- Systematic debugging

---

### 10. [Circuit Breaker Implementation](./10_circuit_breaker.md) 🟡
**Topic:** Resilience, Fault Tolerance

**Scenario:** OpenAI API sometimes goes down. Prevent cascading failures.

**Key Skills Tested:**
- Circuit breaker pattern
- State management
- Fallback strategies
- Graceful degradation

---

## 🎯 Learning Path

**Recommended Order:**
1. Start with Question 1, 3, 9 (fundamentals)
2. Then 2, 4, 5, 10 (intermediate patterns)
3. Finally 6, 7, 8 (advanced topics)

**Time Estimate:** 2-3 hours to work through all questions

---

## 💡 Key Concepts Covered

- **Security:** JWT, RBAC, ABAC, OAuth2, Token management
- **Databases:** Schema design, Indexing, Sharding, MongoDB vs PostgreSQL
- **Caching:** Redis, Invalidation, TTL, Stampede prevention
- **Async:** Celery, Task queues, Head-of-line blocking
- **Scalability:** Load balancing, Distributed systems, Multi-tenancy
- **Observability:** Logging, Tracing, Monitoring, Debugging
- **Compliance:** GDPR, Audit logs, Data privacy
- **ML Integration:** Model deployment, A/B testing, Versioning
- **Resilience:** Circuit breakers, Fallbacks, Graceful degradation

---

## 📖 Additional Resources

- [Martin Fowler - Circuit Breaker](https://martinfowler.com/bliki/CircuitBreaker.html)
- [GDPR Developer Guide](https://gdpr.eu/developer-guide/)
- [Redis Best Practices](https://redis.io/docs/manual/patterns/)
- [Celery Documentation](https://docs.celeryproject.org/)

---

[← Back to Main README](../README.md)
