# Chatbot Backend Case Study - Interview Questions
## Practical & Interview-Friendly Version

---

## Case Study 1: Secure Chatbot API Platform with Role-Based Access Control

---

### Question 1: JWT Token Security - The Nightmare Scenario

**Setup:**
It's 2 PM on Friday. Your security team just called - someone leaked your JWT secret key on GitHub. There are potentially 50,000 active user tokens out there, and attackers are using them right now.

**Part A: You DON'T have Redis (stateless JWT only)**

Tell me step-by-step, what do you do in the next 30 minutes?

**What I'm looking for:**
- Do you understand that rotating the secret invalidates ALL tokens (including good users)?
- How do you handle the deployment without downtime?
- What's your communication plan for users?

**Good answer should cover:**
```
1. Immediate action:
   - Generate new JWT secret
   - Deploy to all servers (blue-green deployment)
   - Old secret works for 5-minute grace period
   - Force re-login for all users

2. Why this is painful:
   - Everyone gets logged out (bad UX)
   - Mobile apps might break
   - Deployment takes time

3. Better long-term fix:
   - Add token versioning
   - Implement short-lived tokens (15 min)
   - Use refresh tokens
```

**Follow-up:** "What if you can't log everyone out because it's Black Friday and that would cost millions in lost sales?"

---

**Part B: NOW you have Redis**

Same scenario, but you have Redis. How does this change your answer?

**What I'm looking for:**
- Understanding of denylist/allowlist patterns
- Performance implications (every request hits Redis now)
- Thinking about Redis as a single point of failure

**Good answer should cover:**
```
With Redis, much better options:

Option 1 - Denylist (my preference):
- Store compromised token IDs in Redis
- Check on every request: "Is this token revoked?"
- Only affects compromised tokens
- Users stay logged in

Implementation:
redis.set("revoked:token_abc123", "1", ex=86400)  # expires in 24h

Pros: Simple, surgical
Cons: Redis lookup on every request (+2ms latency)

Option 2 - Allowlist:
- Store ALL valid tokens in Redis
- If not in Redis = invalid
- Can invalidate by deleting from Redis

Pros: Full control
Cons: Redis becomes critical path, expensive

My choice: Denylist because...
```

**Follow-up:** "Redis just crashed. Do you fail open (let everyone in, security risk) or fail closed (block everyone, availability risk)?"

---

### Question 2: Rate Limiting Across Multiple Servers

**Setup:**
Your chatbot has 5 API servers. A user can hit any server (load balancer distributes randomly).

You need to enforce: **100 requests per minute per user**.

Problem: How do you track "100 requests" when they're spread across 5 different servers?

**What I'm looking for:**
- Understanding of distributed systems challenges
- Knowledge of rate limiting algorithms
- Practical trade-offs

**Bad answer:**
"Just put a counter in memory on each server"
- Why bad? User gets 500 requests/min (100 per server × 5 servers)

**Good answer:**
```
Need centralized counter. Options:

1. Redis counter (my choice):
   key = "ratelimit:user123:2024-11-02-14:05"  # per minute
   redis.incr(key)
   redis.expire(key, 60)

   if redis.get(key) > 100:
       return "Rate limited"

2. Token bucket in Redis:
   - More sophisticated
   - Allows bursts
   - Better user experience

Trade-offs:
- Redis adds 1-2ms latency
- Redis is now in critical path
- Need Redis cluster for HA

Alternative: Sticky sessions
- Same user always hits same server
- Can use local counters
- Problem: Uneven load distribution
```

**Follow-up:** "User hits rate limit at 10:59:59 AM. At 11:00:00 AM, can they make requests immediately or do they wait a full minute?"

*Hint: Testing if they understand sliding window vs fixed window*

---

### Question 3: Database Design for Conversation History

**Setup:**
Users have conversations with the chatbot. A conversation can have:
- Hundreds of messages
- Branching (user tries different follow-up questions)
- Attachments (images, files)
- Metadata (which LLM model was used, tokens consumed, etc.)

**Question:** MongoDB or PostgreSQL? Defend your choice.

**What I'm looking for:**
- Understanding of document vs relational trade-offs
- Thinking about query patterns
- Consideration of scale

**If they say MongoDB:**
```
Good points to mention:
- Natural fit for nested documents
- One conversation = one document
- No joins needed
- Flexible schema

Concerns I'll probe:
"What about the 16MB document limit?"
"How do you query: 'Find all messages containing X across all conversations'?"
"What if I need analytics: 'Average messages per conversation by user role'?"
```

**If they say PostgreSQL:**
```
Good points to mention:
- Relational integrity
- Complex queries with JOINs
- JSONB for flexibility
- No size limits

Concerns I'll probe:
"How do you efficiently fetch a complete conversation with 500 messages?"
"Show me the schema for branching conversations"
"What about horizontal scaling?"
```

**The "great" answer (hybrid):**
```
Primary: PostgreSQL
- conversations table (metadata)
- messages table (individual messages)
- Strong consistency, analytics

Cache layer: Redis
- Cache full conversation JSON
- TTL: 1 hour
- Invalidate on new message

Best of both worlds:
- Fast reads from cache
- Complex queries on Postgres
- Analytics capability
```

**Follow-up:** "A conversation has 10,000 messages. User opens the chat. How do you load it without killing the browser?"

---

### Question 4: Handling Long-Running LLM Requests

**Setup:**
Your chatbot uses GPT-4. Some requests take 30 seconds. You're using Celery for async processing.

**Problem:** You have 10 Celery workers. If 10 users ask slow questions, all workers are blocked. User #11 waits forever even for a fast query.

How do you fix this?

**What I'm looking for:**
- Understanding of head-of-line blocking
- Queue management strategies
- Graceful degradation

**Good answer should include:**
```
Problem: Head-of-line blocking

Solution 1: Multiple queues (my preference)
- Fast queue: 8 workers (for quick queries)
- Slow queue: 2 workers (for LLM queries)
- Classify queries before routing

celery -A app worker -Q fast_queue -c 8
celery -A app worker -Q slow_queue -c 2

Pros: Fast queries never blocked
Cons: Need to classify queries upfront

Solution 2: Task timeouts
- Set max execution time: 30 seconds
- Kill and retry if exceeded
- Alert if happening too much

@celery.task(time_limit=30, soft_time_limit=25)
def process_llm_query(query):
    # Do work

Pros: Simple
Cons: Might kill legitimate slow queries

Solution 3: Auto-scaling workers
- Monitor queue depth
- Scale workers up/down based on load
- AWS ECS/Lambda can help

My choice: Combination of 1 + 2
```

**Follow-up:** "User submits query, closes browser, comes back 10 min later. How do they get the result?"

---

### Question 5: Cache Invalidation Strategy

**Setup:**
Your chatbot queries a data warehouse (slow, expensive). You cache results in Redis.

Data warehouse updates **every hour at :00 minutes** (1:00, 2:00, 3:00, etc.).

**Question:** How do you keep cache fresh without serving stale data?

**What I'm looking for:**
- Understanding of cache invalidation (one of CS's hardest problems)
- TTL strategies
- Consistency vs performance trade-offs

**Approaches to discuss:**

```
Approach 1: TTL-based (simple but flawed)
redis.set("sales_Q3", data, ex=3600)  # 1 hour TTL

Problem:
- If data updates at 2:00, cache expires at 2:30
- Serve stale data for 30 min!

Approach 2: Event-based invalidation (better)
1. Data warehouse update triggers event
2. Event listener deletes relevant cache keys
3. Next request rebuilds cache

Pros: Always fresh
Cons: Needs event infrastructure

Approach 3: Cache with version (my choice)
Key format: "sales_Q3:v2024110214"  # includes update hour

When data updates:
1. Increment version number
2. Old cache entries naturally expire
3. New requests use new version

Pros: Gradual rollover, no stampede
Cons: More complex key management

Approach 4: Refresh-ahead
Before TTL expires, background job refreshes cache

Pros: Always warm cache, no latency spike
Cons: Complexity, might refresh unused keys
```

**Follow-up:** "1000 users request the same query RIGHT when cache expires. What happens?"

*Testing if they know about cache stampede*

---

### Question 6: Multi-Tenancy & Data Isolation

**Setup:**
Your chatbot serves 100 companies. Each company has 1000 users. Company A's users must NEVER see Company B's data.

**Question:** How do you ensure data isolation in your database and API?

**What I'm looking for:**
- Security-first thinking
- Understanding of multi-tenancy patterns
- Testing strategies

**Approaches to discuss:**

```
Approach 1: Separate databases per tenant
Database: company_a_db, company_b_db, ...

Pros:
- Perfect isolation
- Easy to backup/restore per customer
- Can migrate tenants easily

Cons:
- Management nightmare (100 databases!)
- Expensive
- Schema changes = 100 migrations

Approach 2: Shared database, tenant_id column
conversations table:
| id | tenant_id | user_id | message |
|----|-----------|---------|---------|

EVERY query MUST include:
WHERE tenant_id = 'company_a'

Pros: Simple, cost-effective
Cons:
- One missing WHERE = data leak!!
- No physical isolation

Approach 3: Shared database, Row-Level Security (my choice)
PostgreSQL RLS:

CREATE POLICY tenant_isolation ON conversations
  USING (tenant_id = current_setting('app.current_tenant'));

SET app.current_tenant = 'company_a';
-- Now all queries automatically filtered!

Pros:
- Enforced at DB level
- Can't forget WHERE clause
- Auditable

Cons:
- DB-specific feature
- Performance overhead
```

**How to prevent mistakes:**
```
1. Code review checklist:
   ☐ All queries filtered by tenant_id?
   ☐ Unit tests with cross-tenant data?
   ☐ Integration tests attempt data leak?

2. Automated testing:
   def test_cannot_access_other_tenant_data():
       # Login as Company A user
       response = client.get('/conversations')
       # Verify NO Company B data in response

3. DB constraints:
   ALTER TABLE conversations
   ADD CONSTRAINT check_tenant_match
   CHECK (user_id LIKE tenant_id || '_%');
```

**Follow-up:** "A developer writes a query and forgets tenant_id filter. How do you catch this before production?"

---

### Question 7: Handling Model Version Updates

**Setup:**
You use a sentence classification model to route queries:
- v1: 85% accuracy
- v2: 92% accuracy (just released)

You want to deploy v2 safely without breaking existing users.

**Question:** What's your deployment strategy?

**What I'm looking for:**
- A/B testing understanding
- Gradual rollout strategies
- Monitoring and rollback plans

**Good answer includes:**

```
Phase 1: Shadow mode (1 week)
- Run v2 in parallel with v1
- v1 makes decisions (production)
- v2 runs but results are logged
- Compare outputs, measure drift

if v1_prediction != v2_prediction:
    log_difference(query, v1_result, v2_result)

Metrics to watch:
- Agreement rate (should be >80%)
- v2 error rate on production queries
- Latency difference

Phase 2: Canary deployment (1 week)
- 5% of traffic → v2
- 95% of traffic → v1

Monitor:
- Error rates
- User feedback
- Latency
- Routing accuracy

Phase 3: Gradual rollout
- Day 1: 10%
- Day 3: 25%
- Day 7: 50%
- Day 14: 100%

Rollback criteria:
- Error rate > 2% higher than v1
- Latency > 1.5x of v1
- Negative user feedback spike
```

**Follow-up:** "v2 performs WORSE for a specific query type (Spanish queries). How do you handle this?"

---

### Question 8: GDPR "Right to be Forgotten"

**Setup:**
User requests deletion of all their data. You must:
- Delete conversation history
- Delete from database backups
- Delete from logs
- Delete from cache

All within 30 days, and prove it's done.

**Question:** Walk me through your implementation.

**What I'm looking for:**
- Understanding of GDPR requirements
- Practical challenges with backups
- Audit trail thinking

**Good answer:**

```
Step 1: Soft delete (immediate)
UPDATE users SET deleted_at = NOW() WHERE id = 'user123';
UPDATE conversations SET deleted_at = NOW() WHERE user_id = 'user123';

Why soft delete first?
- Immediate response to user
- Can rollback if accidental
- Gives time for backup handling

Step 2: Purge from live systems (within 24 hours)
1. Database: Hard delete after 24h grace period
2. Redis cache: Invalidate all keys with user_id
3. Elasticsearch logs: Delete by user_id
4. Object storage: Delete user files

Step 3: Backup handling (hardest part)
Problem: You have 30 days of rolling backups

Option 1: Keep deletion log
deletions table:
| user_id | deleted_at | reason |
|---------|------------|--------|

On backup restore:
1. Restore from backup
2. Replay deletion log
3. Re-delete users

Option 2: Backup exclusion (better)
- Custom backup script excludes deleted users
- Backups never contain deleted data
- More complex but cleaner

Step 4: Proof of deletion
Generate deletion certificate:
{
  "user_id": "user123",
  "deletion_requested": "2024-11-02",
  "deletion_completed": "2024-11-15",
  "systems_purged": [
    "postgres_main",
    "redis_cache",
    "s3_uploads",
    "elasticsearch_logs",
    "backup_system"
  ],
  "signed_by": "data_protection_officer",
  "signature": "..."
}
```

**Edge cases to discuss:**
- User data in logs: How to redact without deleting entire log files?
- User data in analytics: Anonymize instead of delete?
- Legal hold: What if user is part of an investigation?

**Follow-up:** "User requests deletion. 5 days later, they want their data back. What do you do?"

---

### Question 9: Debugging a Production Latency Issue

**Setup:**
Users complain that API is slow. Your monitoring shows:
- p50 latency: 200ms (normal)
- p95 latency: 5000ms (BAD, should be <500ms)
- p99 latency: 15000ms (TERRIBLE)

5% of requests are really slow. Where do you start?

**What I'm looking for:**
- Systematic debugging approach
- Knowledge of monitoring tools
- Understanding of latency sources

**Good debugging flow:**

```
Step 1: Add detailed tracing
Use distributed tracing (Datadog, New Relic, etc.)

Sample slow request breakdown:
Total: 5000ms
├─ Auth check: 50ms
├─ Database query: 4800ms ← PROBLEM!
├─ LLM call: 100ms
└─ Response serialization: 50ms

Aha! Database is slow.

Step 2: Check database
- Query explain plan
- Missing indexes?
- Lock contention?
- Connection pool exhausted?

EXPLAIN ANALYZE
SELECT * FROM conversations
WHERE user_id = 'user123'
AND created_at > NOW() - INTERVAL '7 days';

Result: Seq Scan on conversations (slow!)
Missing index on (user_id, created_at)

Step 3: Fix
CREATE INDEX CONCURRENTLY idx_user_created
ON conversations(user_id, created_at DESC);

Step 4: Verify
Monitor p95 latency for 1 hour
Should drop from 5000ms → <500ms
```

**Other common causes to discuss:**
```
1. Garbage collection pauses (Java/Python)
   - Check GC logs
   - Tune GC settings

2. Network issues
   - Check cross-region latency
   - Check DNS resolution time

3. Rate limiting / backpressure
   - Downstream service slow
   - Queues backing up

4. Cold starts (serverless)
   - Lambda/Cloud Function warm-up time

5. Cache misses
   - Redis down
   - Cache invalidation storm
```

**Follow-up:** "You find the slow queries are only for a specific user. What could cause that?"

---

### Question 10: Designing Circuit Breaker for LLM Service

**Setup:**
Your chatbot calls OpenAI API. Sometimes OpenAI is slow or down. You notice:
- When OpenAI is down, requests queue up
- All Celery workers blocked waiting
- Users wait 60+ seconds for timeout

**Question:** Implement a circuit breaker. Explain your logic.

**What I'm looking for:**
- Understanding of circuit breaker pattern
- Graceful degradation
- User experience thinking

**Circuit breaker states:**

```
States:
1. CLOSED (normal)
   - All requests go through
   - Track failure rate

2. OPEN (broken)
   - All requests fail immediately
   - Don't call LLM at all
   - Return cached/fallback response

3. HALF-OPEN (testing)
   - Allow few requests through
   - If succeed → CLOSED
   - If fail → OPEN again

Implementation:
class CircuitBreaker:
    def __init__(self):
        self.state = "CLOSED"
        self.failure_count = 0
        self.failure_threshold = 5
        self.timeout = 30  # seconds
        self.last_failure_time = None

    def call_llm(self, prompt):
        if self.state == "OPEN":
            # Check if timeout expired
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF-OPEN"
            else:
                # Fail fast!
                return self.fallback_response()

        try:
            response = openai.chat(prompt, timeout=10)

            if self.state == "HALF-OPEN":
                self.state = "CLOSED"  # Recovery!
                self.failure_count = 0

            return response

        except Exception as e:
            self.failure_count += 1

            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                self.last_failure_time = time.time()

            return self.fallback_response()

    def fallback_response(self):
        return {
            "message": "Service temporarily unavailable. Please try again.",
            "cached": True
        }
```

**Better fallback strategies:**
```
1. Return cached response
   - Previous similar query
   - "Sorry, I can't help with that right now"

2. Degrade gracefully
   - Use smaller, faster model
   - Return partial results

3. Queue for later
   - "We'll email you when ready"
   - Process when service recovers
```

**Follow-up:** "How do you decide the right timeout and failure threshold values?"

---

## Summary: What Makes a Great Answer?

1. **Start with understanding**
   - Repeat the problem back
   - Ask clarifying questions
   - "What's the scale? How many users?"

2. **Provide multiple options**
   - "I see 3 approaches here..."
   - Explain trade-offs
   - Pick one and defend it

3. **Show real-world thinking**
   - "I've seen this fail in production when..."
   - Mention monitoring, alerting, rollback
   - Think about edge cases

4. **Be specific**
   - Give actual numbers (not "fast" but "< 100ms")
   - Name specific tools (Redis, PostgreSQL, not "a database")
   - Show code snippets

5. **Think end-to-end**
   - Not just the happy path
   - What if Redis crashes?
   - What if the database is slow?
   - How do you monitor this?

---

Good luck! 🚀
