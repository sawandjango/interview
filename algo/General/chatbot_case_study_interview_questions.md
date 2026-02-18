# Hard Interview Questions for Chatbot Backend Case Studies

---

## Case Study 1: Secure Chatbot API Platform with Role-Based Access Control

### Architecture & Design Questions

1. **RBAC Implementation Deep Dive**
   - How would you handle hierarchical roles (e.g., senior analyst inherits analyst permissions)? Walk me through your data model.
   - If a user has multiple roles simultaneously, how do you resolve conflicting permissions? What's your precedence strategy?
   - How would you implement attribute-based access control (ABAC) on top of RBAC for fine-grained permissions (e.g., "analyst can only see their region's data")?

2. **API Security & Authentication**
   - Your JWT tokens are stolen and being used by attackers. How do you invalidate all active tokens without a central token store? What about if you DO have Redis?
   - Explain the difference between stateless JWT and stateful session tokens. When would you choose one over the other for this chatbot platform?
   - How do you prevent privilege escalation attacks where a guest user tries to modify their JWT claims to become admin?
   - Implement refresh token rotation. What happens if a refresh token is compromised mid-rotation?

3. **Database & Conversation History**
   - You chose MongoDB/PostgreSQL for conversation history. Defend your choice. What are the trade-offs for storing nested conversation trees with branching?
   - Design the indexing strategy for a query like: "Get all conversations for user X in the last 7 days where role was 'analyst' and query type was 'sales summary'". Show me the indexes.
   - Conversation history grows to 500GB. How do you partition/shard this data while maintaining fast retrieval for recent conversations?
   - How do you handle GDPR "right to be forgotten" requests where you must delete all conversation history for a user, including from backups?

4. **Async Task Processing & LLM Integration**
   - Your Celery workers are processing LLM requests, but some tasks take 30+ seconds and block other tasks. How do you prevent head-of-line blocking?
   - How do you handle the scenario where a user submits a query, closes their browser, and comes back 10 minutes later expecting the result?
   - A Celery worker dies mid-LLM request (after 15 seconds of a 20-second task). How do you handle retry logic without duplicate processing?
   - How do you implement circuit breaking for the LLM service when it becomes slow or starts timing out?

5. **Rate Limiting & Performance**
   - Design a distributed rate limiter that works across multiple API servers. How do you handle clock skew between servers?
   - An admin user should have higher rate limits than guests. How do you implement tiered rate limiting?
   - What happens when a user hits the rate limit exactly at midnight when limits reset? How do you prevent thundering herd?
   - How would you implement rate limiting at multiple levels: per-user, per-IP, per-role, and global?

6. **Audit Logging & Compliance**
   - You need 100% audit logging coverage, but logging to database synchronously would slow down your API. How do you ensure no logs are lost while maintaining performance?
   - How do you make your audit logs tamper-proof and verifiable by external auditors?
   - Design a query to detect anomalous access patterns (e.g., guest user suddenly accessing 1000x more queries than usual).
   - Your audit logs grow to 10TB annually. Design an archival and retrieval strategy with cost optimization.

7. **ML Integration (Sentence Classification)**
   - Your sentence classifier has 85% accuracy. How do you handle the 15% misclassification rate without degrading user experience?
   - The ML model takes 200ms to classify. This violates your 500ms p95 latency budget. How do you optimize?
   - How do you handle model versioning and A/B testing when routing queries to different workflows?
   - The model was trained on English data but users are sending queries in Spanish. How do you handle this gracefully?

8. **Failure Scenarios & Edge Cases**
   - Database goes down for 30 seconds. How do you handle in-flight requests and queued async tasks?
   - A malicious admin creates a role with contradictory permissions. How do you validate and prevent this?
   - An analyst user's role is changed from 'analyst' to 'guest' while they have 5 active conversations. What happens to those conversations?
   - Your Redis cache (used for sessions/rate limiting) gets wiped. How does your system recover?

9. **Scalability & Load**
   - You need to scale from 1000 users to 1 million users. What are the bottlenecks in your current design?
   - How do you handle the scenario where 10,000 users all ask the same question simultaneously?
   - Design auto-scaling policies for your Celery workers based on queue depth and task latency.

10. **Security Deep Dive**
    - How do you prevent timing attacks on your authentication endpoint?
    - Explain how you'd protect against CSRF, XSS, SQL injection, and NoSQL injection in your API.
    - How do you secure secrets (API keys, DB passwords) in your deployment? Walk me through your secrets management strategy.

---

## Case Study 2: Chatbot Caching and Query Optimization Layer for Fast API Responses

### Architecture & Design Questions

11. **Cache Key Design & Strategy**
    - Show me your cache key generation algorithm for a query with 5 filters (time range, product category, region, customer segment, metric type). How do you ensure uniqueness while avoiding key explosion?
    - Two queries are semantically identical but phrased differently: "sales in Q1 2024" vs "revenue from Jan-Mar 2024". How do you ensure cache hits for both?
    - How do you handle partial cache hits? For example, user asks for data for 10 products, and 7 are cached but 3 are not.
    - Design a cache key versioning strategy so you can invalidate all cache entries when your data warehouse schema changes.

12. **Cache Invalidation & Consistency**
    - Your data warehouse updates hourly. Design a cache invalidation strategy that minimizes stale data exposure while maximizing cache hit ratio.
    - How do you handle the scenario where a cache invalidation job fails halfway through (50% of keys invalidated)?
    - Implement cache-aside vs write-through vs write-behind patterns. Which would you choose for this use case and why?
    - A user modifies data in the warehouse via a different system. How does your cache know to invalidate without polling?

13. **Redis Architecture & Performance**
    - Your Redis instance hits memory limits. Walk me through your eviction strategy. Which eviction policy would you use and why?
    - Design a Redis cluster architecture for high availability. How do you handle failover without losing cache data?
    - How do you prevent cache stampede when a popular query's cache expires and 1000 users request it simultaneously?
    - Explain the difference between Redis Cluster, Redis Sentinel, and standalone Redis. When would you use each?

14. **Query Intent Classification (ML)**
    - Your ML classifier determines which queries should hit cache vs database. What features would you use for this classification?
    - How do you handle cold start? A new query type arrives that the model has never seen before.
    - The classifier has a 10% false negative rate (says "don't cache" but should cache). How does this affect your success metrics?
    - How would you continuously retrain this model based on cache hit/miss patterns in production?

15. **Cache Warming & Preloading**
    - Design a cache warming strategy for the top 100 most frequent queries. How do you identify these queries?
    - You warm the cache at 6 AM, but data updates at 7 AM. How do you prevent serving stale warmed data?
    - How do you prioritize which cache entries to warm when you have limited time/resources?

16. **Data Warehouse Integration**
    - Your BigQuery/Redshift queries take 5-30 seconds. How do you prevent these from blocking your API responses?
    - Design a query result pagination strategy for large datasets (10M rows). How does caching work with pagination?
    - How do you handle data warehouse connection pooling and prevent connection exhaustion?
    - What if the data warehouse is temporarily unavailable? Design your fallback strategy.

17. **Monitoring & Observability**
    - How do you measure cache hit ratio in real-time? What metrics would you track?
    - Design an alerting strategy for when cache hit ratio drops below 85%.
    - How would you debug a scenario where cache hit ratio suddenly drops from 90% to 60%?
    - Show me how you'd calculate the cost savings from caching (reduced warehouse queries).

18. **Edge Cases & Failure Modes**
    - A cache entry is corrupted (contains invalid JSON). How do you detect and handle this?
    - What happens if Redis becomes slower than the data warehouse due to network issues?
    - How do you handle timezone differences when caching time-based queries across global users?
    - A user's query returns 1GB of data. Do you cache it? What's your maximum cache entry size policy?

19. **Optimization & Performance**
    - You're achieving only 60% cache hit ratio. Walk me through your debugging and optimization process.
    - How would you implement cache compression to store more entries in Redis?
    - Design a multi-tier caching strategy (L1: in-memory, L2: Redis, L3: warehouse).
    - How do you handle cache coherency across multiple API servers?

20. **API Design for Cache Management**
    - Design RESTful endpoints for viewing, invalidating, and warming cache entries. Show me the request/response schemas.
    - How do you secure these admin endpoints? Who should have access to cache invalidation?
    - How do you implement bulk cache invalidation by pattern (e.g., invalidate all entries for product category "electronics")?

---

## Case Study 3: Real-Time Moderation and Compliance Engine for AI Chatbot

### Architecture & Design Questions

21. **Middleware Architecture & Interception**
    - How do you ensure 100% interception of responses? What happens if the middleware crashes?
    - Design the middleware as both a synchronous interceptor and an async event-driven system. Which is better for <100ms latency?
    - How do you handle streaming responses from the LLM (token-by-token generation)? Do you wait for the full response or moderate in real-time?
    - What if the chatbot response is 10,000 words? How do you moderate efficiently while meeting latency requirements?

22. **ML Model Integration (Toxicity/PII Detection)**
    - Your toxicity detection model has 95% precision and 90% recall. How do these metrics impact user experience?
    - How do you handle multi-language toxicity detection when your model is only trained on English?
    - Design an ensemble approach using multiple models (toxicity, PII, hate speech). How do you combine their outputs?
    - The ML model inference takes 80ms. You have 20ms left in your 100ms budget for everything else. How do you architect this?

23. **Region-Specific Rules & Configuration**
    - Design a rule engine that supports GDPR (EU), HIPAA (US), and LGPD (Brazil) simultaneously. Show me the data model.
    - How do you determine which region's rules to apply for a VPN user whose IP is in US but account is registered in EU?
    - A compliance team updates rules for EU. How do you ensure these changes are applied immediately across all servers without downtime?
    - How do you handle rule conflicts? E.g., EU rule blocks term "X" but US rule allows it for the same user (dual citizenship).

24. **Dynamic Rule Updates Without Redeployment**
    - Design an API for compliance teams to add/update keyword patterns or regex rules in real-time.
    - How do you validate user-submitted regex patterns to prevent ReDoS (Regular Expression Denial of Service) attacks?
    - Your rule update API is called, but the change shouldn't affect in-flight requests. How do you handle versioning?
    - How would you implement a rule testing/preview mode so compliance teams can test rules before activating them?

25. **Audit Logging & Compliance Reporting**
    - You must log every flagged response with full metadata. How do you do this without violating the same PII rules you're enforcing?
    - Design an audit log query system for compliance teams to investigate "all blocked responses containing term X in last 90 days".
    - How do you ensure audit logs are immutable and tamper-proof for legal purposes?
    - Generate a compliance report showing: block rate by rule type, by region, by time period, and by false positive rate.

26. **Fallback & Error Handling**
    - A response is blocked. Design a user-friendly error message that doesn't reveal internal moderation logic.
    - What if the ML model becomes unavailable? Do you fail open (allow all) or fail closed (block all)? Defend your choice.
    - How do you handle partial moderation failures? E.g., PII detection passes but toxicity detection service is down.
    - Design a manual review queue for edge cases where automated moderation is uncertain.

27. **Performance & Latency Optimization**
    - You're hitting 150ms latency instead of target <100ms. Walk me through your optimization strategy.
    - How would you implement request batching for the ML model to improve throughput while maintaining low latency?
    - Design a multi-tier moderation strategy: fast keyword filters (5ms) → ML model (80ms) → complex rule engine (15ms).
    - How do you handle the latency vs accuracy trade-off? Would you use a faster but less accurate model?

28. **False Positives & Model Tuning**
    - You're getting 2% false positives (blocking legitimate responses). How do you reduce this to <0.1%?
    - Design a feedback loop where users can report false positives, which then retrain your model.
    - How do you measure false negative rate (toxic content that passed moderation)? This is harder to detect.
    - Implement a shadow mode where new rules run in parallel without blocking, allowing you to measure impact before activation.

29. **Scalability & High Availability**
    - Your system must handle 10,000 requests/second. How do you scale the moderation middleware?
    - Design a circuit breaker pattern for when the ML service becomes overloaded.
    - How do you ensure no single point of failure in your moderation pipeline?
    - What's your disaster recovery plan if your moderation service goes down completely?

30. **Security & Adversarial Attacks**
    - Users are trying to bypass your filter by using l33t speak ("h3ll0" instead of "hello"). How do you handle this?
    - How do you prevent prompt injection attacks where users trick the chatbot into revealing blocked content?
    - Design rate limiting specifically for users who repeatedly trigger moderation blocks (potential abuse).
    - How do you handle obfuscation techniques like zero-width characters, homoglyphs, or base64 encoding?

31. **Advanced Compliance Scenarios**
    - You need to moderate based on user context (e.g., financial advice allowed for premium users only). How does this change your architecture?
    - Implement time-based rules: certain terms are only blocked during business hours for EU users.
    - How do you handle chained conversations where context from message 1 makes message 5 non-compliant?
    - Design a reputation system where trusted users get lighter moderation, while flagged users get stricter checks.

32. **Testing & Validation**
    - How do you test that you're achieving 100% interception without gaps?
    - Design a test suite for your moderation engine with adversarial examples.
    - How do you simulate production load (10K req/sec) to validate your 100ms latency SLA?
    - Create a dataset of edge cases for regression testing after rule updates.

33. **Cost Optimization**
    - ML model inference costs $0.001 per request. At 10M requests/day, that's $10K/day. How do you reduce this?
    - Would you use a smaller, faster, cheaper model for pre-filtering before the expensive accurate model?
    - How do you optimize Redis/database costs for storing audit logs at scale?

34. **Integration & API Design**
    - Should this be a middleware, a sidecar, or a separate microservice? Defend your architectural choice.
    - Design the API contract between the chatbot service and moderation service. Show me request/response schemas.
    - How do you version your moderation API so chatbot clients can upgrade gradually?

35. **Monitoring & Alerting**
    - What are the top 5 metrics you'd monitor for this system? Design your dashboard.
    - Design alerts for: latency SLA violations, false positive rate spikes, rule update failures, ML model degradation.
    - How would you debug a production incident where 50% of legitimate responses are being blocked?

---

## Cross-Cutting Questions (Applicable to All Case Studies)

36. **Observability & Debugging**
    - How do you implement distributed tracing across your microservices?
    - Design a logging strategy that doesn't violate PII regulations but still allows debugging.
    - How would you debug a production issue where 1% of requests fail intermittently?

37. **DevOps & Deployment**
    - Design a CI/CD pipeline for zero-downtime deployments.
    - How do you handle database migrations in production without downtime?
    - What's your rollback strategy if a deployment introduces a critical bug?

38. **Cost & Resource Management**
    - Calculate the total infrastructure cost for 1M daily active users. Where would you optimize?
    - How do you implement auto-scaling that balances cost with performance?

39. **Disaster Recovery**
    - Your primary database fails. Walk me through your failover process.
    - Design a backup strategy with RPO < 1 hour and RTO < 15 minutes.

40. **Team & Process**
    - How would you split this system across a team of 5 backend engineers?
    - What documentation would you create for this system?
    - How do you ensure code quality and prevent regressions?

---

## Evaluation Rubric

### Excellent Answer Indicators
- Discusses trade-offs explicitly
- Provides specific numbers and calculations
- Mentions edge cases and failure scenarios
- References real-world production experience
- Proposes monitoring and alerting strategies
- Considers cost implications
- Thinks about security proactively
- Designs for scale from the start

### Red Flags
- "Just use library X" without understanding internals
- No consideration of failure modes
- Ignores performance/cost trade-offs
- Overly complex solutions without justification
- No mention of monitoring or observability
- Security as an afterthought
- "It will just work" without proof

---

*Use these questions to probe depth of understanding, architectural thinking, and production experience. Adjust difficulty based on candidate's seniority level.*
