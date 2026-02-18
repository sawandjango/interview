# Question 2: Rate Limiting Across Multiple Servers

[← Back to Case Study 1](./README.md)

---

## 🎯 Difficulty: 🟡 Intermediate

## 📝 Question

### Setup

Your chatbot has **5 API servers** behind a load balancer. Requests are distributed randomly across all servers.

You need to enforce: **100 requests per minute per user**

### The Problem

If each server tracks its own counter, User A could make:
- 100 requests to Server 1
- 100 requests to Server 2
- 100 requests to Server 3
- ... etc.

**Total: 500 requests/min instead of 100!** ❌

**Question:** How do you accurately enforce 100 req/min across all 5 servers?

---

## 🎓 What I'm Looking For

- Understanding of distributed systems challenges
- Knowledge of rate limiting algorithms
- Redis usage patterns
- Clock synchronization issues
- Trade-offs between accuracy and performance

---

## ✅ Good Answer Should Include

### Solution 1: Centralized Counter in Redis (Recommended)

```
Strategy: Use Redis as single source of truth for all servers

Implementation:
────────────────
Key format: "ratelimit:{user_id}:{timestamp_minute}"
Example: "ratelimit:user123:2024-11-02-14:05"

On each request:
1. Increment counter in Redis
2. If counter > 100, reject
3. Set TTL = 60 seconds (auto cleanup)

Code:
def check_rate_limit(user_id):
    current_minute = datetime.now().strftime("%Y-%m-%d-%H:%M")
    key = f"ratelimit:{user_id}:{current_minute}"

    # Increment counter
    count = redis.incr(key)

    # Set TTL on first request of the minute
    if count == 1:
        redis.expire(key, 60)

    # Check limit
    if count > 100:
        return False  # Rate limited!

    return True  # Allow request
```

**Pros:**
- ✅ Accurate (single source of truth)
- ✅ Simple to implement
- ✅ Auto cleanup (TTL)
- ✅ Works across any number of servers

**Cons:**
- ❌ Redis becomes critical path (+1-2ms per request)
- ❌ Redis is now a SPOF
- ❌ Need Redis cluster for high availability

### Solution 2: Token Bucket Algorithm

```
Better for user experience (allows bursts)

Concept:
────────
- User has a "bucket" with 100 tokens
- Each request consumes 1 token
- Bucket refills at rate of 100 tokens/minute

Implementation in Redis:
key = f"bucket:{user_id}"
value = {
    "tokens": 100,
    "last_refill": timestamp
}

def check_token_bucket(user_id):
    key = f"bucket:{user_id}"
    bucket = redis.get(key)

    if not bucket:
        # First request
        bucket = {"tokens": 100, "last_refill": time.time()}

    # Calculate refill
    now = time.time()
    time_passed = now - bucket["last_refill"]
    refill_tokens = (time_passed / 60) * 100  # 100 tokens per minute

    # Update tokens (max 100)
    bucket["tokens"] = min(100, bucket["tokens"] + refill_tokens)
    bucket["last_refill"] = now

    # Try to consume token
    if bucket["tokens"] >= 1:
        bucket["tokens"] -= 1
        redis.set(key, bucket, ex=3600)  # 1 hour TTL
        return True
    else:
        return False  # Rate limited
```

**Pros:**
- ✅ Allows bursts (better UX)
- ✅ Smoother rate limiting
- ✅ More forgiving for bursty traffic

**Cons:**
- ❌ More complex
- ❌ Need atomic operations (Lua script)

### Solution 3: Sliding Window

```
More accurate than fixed windows

Problem with fixed window:
User makes 100 requests at 10:59:59
User makes 100 requests at 11:00:01
→ 200 requests in 2 seconds! (but in different minutes)

Sliding window solution:
Count requests in last 60 seconds (not current minute)

Implementation:
Redis Sorted Set (score = timestamp)

def sliding_window_rate_limit(user_id, limit=100, window=60):
    key = f"ratelimit:{user_id}"
    now = time.time()
    window_start = now - window

    # Remove old entries
    redis.zremrangebyscore(key, 0, window_start)

    # Count requests in window
    count = redis.zcard(key)

    if count >= limit:
        return False  # Rate limited

    # Add current request
    redis.zadd(key, {str(now): now})
    redis.expire(key, window)

    return True
```

**Pros:**
- ✅ Most accurate
- ✅ No "edge of minute" problem
- ✅ Fair distribution

**Cons:**
- ❌ More memory (stores timestamps)
- ❌ More Redis operations

---

## 🔴 Common Mistakes to Avoid

### Mistake 1: Not handling Redis failures

```python
# ❌ Bad
def check_rate_limit(user_id):
    count = redis.incr(key)  # Crashes if Redis down!
    if count > 100:
        return False
    return True

# ✅ Good
def check_rate_limit(user_id):
    try:
        count = redis.incr(key, timeout=0.1)
        if count > 100:
            return False
        return True
    except redis.TimeoutError:
        logger.error("Redis timeout")
        return True  # Fail open (or closed, depending on requirements)
    except redis.ConnectionError:
        logger.error("Redis connection failed")
        return True  # Fail open
```

### Mistake 2: Not setting TTL

```python
# ❌ Bad (memory leak!)
redis.incr(key)  # Key never expires!

# ✅ Good
count = redis.incr(key)
if count == 1:  # Only set TTL once
    redis.expire(key, 60)
```

### Mistake 3: Race condition on TTL

```python
# ❌ Bad (race condition)
count = redis.incr(key)
redis.expire(key, 60)  # What if request #2 happens here?
                       # TTL gets reset!

# ✅ Good (atomic)
lua_script = """
local count = redis.call('INCR', KEYS[1])
if count == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
end
return count
"""
count = redis.eval(lua_script, 1, key, 60)
```

---

## 🤔 Follow-Up Questions

### Q1: "User hits rate limit at 10:59:59. At 11:00:00, can they make requests immediately?"

**Depends on algorithm:**

```
Fixed Window:
10:59:59 - Request #100 (limit hit)
11:00:00 - NEW MINUTE → Counter reset → Request allowed ✓

Problem: Can get 200 requests in 1 second!

Sliding Window:
10:59:59 - Request #100
11:00:00 - Check last 60 seconds → Still 100 requests → BLOCKED ✗
11:00:59 - Check last 60 seconds → 99 requests → ALLOWED ✓

Better behavior!
```

### Q2: "How do you handle different rate limits for different user roles?"

```python
# Good Answer:

RATE_LIMITS = {
    "guest": 10,      # 10 req/min
    "user": 100,      # 100 req/min
    "premium": 1000,  # 1000 req/min
    "admin": None     # Unlimited
}

def check_rate_limit(user_id, role):
    limit = RATE_LIMITS.get(role)

    if limit is None:  # Admin - no limit
        return True

    current_minute = datetime.now().strftime("%Y-%m-%d-%H:%M")
    key = f"ratelimit:{user_id}:{current_minute}"

    count = redis.incr(key)
    if count == 1:
        redis.expire(key, 60)

    return count <= limit

# Better: Include limit in response headers
response.headers['X-RateLimit-Limit'] = str(limit)
response.headers['X-RateLimit-Remaining'] = str(max(0, limit - count))
response.headers['X-RateLimit-Reset'] = str(next_minute_timestamp)
```

### Q3: "How do you prevent clock skew issues between servers?"

**Good Answer:**
```
Problem: If servers have different times, counters don't align

Server 1 thinks it's 10:00:05
Server 2 thinks it's 10:00:58
→ Different Redis keys!

Solutions:

1. NTP Synchronization (must-have)
   - All servers sync with same NTP server
   - Monitor clock drift

2. Use Redis time (better)
   lua_script = """
   local now = redis.call('TIME')
   local timestamp = now[1]  -- Redis server time
   local minute = math.floor(timestamp / 60)
   local key = 'ratelimit:' .. ARGV[1] .. ':' .. minute
   -- ... rest of logic
   """

3. Longer windows to absorb skew
   - Instead of 1 minute, use 65 seconds
   - Add 5-second buffer for clock skew
```

### Q4: "What if you need rate limiting at multiple levels: per-user, per-IP, global?"

```python
def multi_level_rate_limit(user_id, ip_address):
    # Check global limit first (cheapest to fail fast)
    if not check_global_limit():
        return {"error": "System overloaded"}, 503

    # Check IP limit (prevent DDoS)
    if not check_ip_limit(ip_address):
        return {"error": "Too many requests from your IP"}, 429

    # Check user limit
    if not check_user_limit(user_id):
        return {"error": "Too many requests"}, 429

    # All checks passed
    return None

def check_global_limit():
    key = f"global:{current_minute}"
    count = redis.incr(key)
    if count == 1:
        redis.expire(key, 60)
    return count <= 10000  # 10k req/min globally

def check_ip_limit(ip):
    key = f"ip:{ip}:{current_minute}"
    count = redis.incr(key)
    if count == 1:
        redis.expire(key, 60)
    return count <= 1000  # 1k req/min per IP

def check_user_limit(user_id):
    key = f"user:{user_id}:{current_minute}"
    count = redis.incr(key)
    if count == 1:
        redis.expire(key, 60)
    return count <= 100  # 100 req/min per user
```

---

## 📊 Algorithm Comparison

| Algorithm | Accuracy | Memory | Complexity | Burst Handling |
|-----------|----------|--------|------------|----------------|
| Fixed Window | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ |
| Sliding Window | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Token Bucket | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Leaky Bucket | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ❌ |

**My Recommendation:**
- Start with **Fixed Window** (simple, good enough)
- Upgrade to **Token Bucket** if you need burst handling
- Use **Sliding Window** for strict accuracy requirements

---

## 💡 Key Takeaways

1. **Centralized state is required**
   - Can't track distributed counters accurately
   - Redis is the standard solution

2. **Handle Redis failures gracefully**
   - Circuit breaker pattern
   - Fail open vs fail closed decision
   - Cache locally with best-effort

3. **Return helpful headers**
   ```
   X-RateLimit-Limit: 100
   X-RateLimit-Remaining: 42
   X-RateLimit-Reset: 1699000000
   ```

4. **Use Lua scripts for atomicity**
   - Avoid race conditions
   - Reduce round trips

5. **Monitor and alert**
   - Track rate limit hit rate
   - Alert if >5% of requests rate limited
   - May indicate attack or incorrect limits

---

## 🔗 Related Questions

- [Question 1: JWT Token Security](./01_jwt_security.md)
- [Question 5: Cache Invalidation Strategy](./05_cache_invalidation.md)

---

[← Back to Case Study 1](./README.md) | [Next Question →](./03_database_design.md)
