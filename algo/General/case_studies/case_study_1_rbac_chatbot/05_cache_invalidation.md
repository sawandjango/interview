# Question 5: Cache Invalidation Strategy

[← Back to Case Study 1](./README.md)

---

## 🎯 Difficulty: 🟡 Intermediate

## 📝 Question

### Setup

Your chatbot pulls sales data from a data warehouse (Redshift). Warehouse queries are **expensive** (2-5 seconds, high cost). You cache results in Redis with TTL.

**The Problem:**

- Data warehouse updates **every hour** (on the hour: 9:00, 10:00, 11:00...)
- User asks "Q1 sales?" at 9:05 AM → Cache miss → Query warehouse → Cache for 1 hour
- At 10:00 AM, warehouse updates with new data
- **At 10:30 AM, user still sees stale 9:05 data!** ❌

**Questions:**

1. How do you ensure users see fresh data after warehouse updates?
2. How do you prevent **cache stampede** (1000 users hitting warehouse at 10:00:01)?
3. How do you handle **partial updates** (some tables update, others don't)?

---

## 🎓 What I'm Looking For

- Knowledge of cache invalidation strategies
- Understanding of cache stampede problem
- TTL vs event-based invalidation
- Graceful degradation patterns
- Production thinking (what if invalidation fails?)

---

## ✅ Good Answer Should Include

### Strategy 1: Time-Based TTL (Simple but imperfect)

```python
import redis
from datetime import datetime, timedelta

redis_client = redis.Redis()

def get_sales_data(query):
    cache_key = f"sales:{hash(query)}"

    # Check cache
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # Cache miss - query warehouse
    data = query_warehouse(query)

    # Calculate TTL to next hour boundary
    now = datetime.now()
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    ttl_seconds = int((next_hour - now).total_seconds())

    # Cache until next hour
    redis_client.setex(cache_key, ttl_seconds, json.dumps(data))

    return data
```

**Pros:**
- ✅ Simple to implement
- ✅ No external dependencies

**Cons:**
- ❌ Not precise (user at 9:59:59 gets 1-second cache)
- ❌ Doesn't handle early/delayed warehouse updates
- ❌ Cache stampede at hour boundary

### Strategy 2: Event-Based Invalidation (Recommended)

```python
# === Warehouse Update Job (runs hourly) ===

def warehouse_update_complete():
    """
    Called after warehouse ETL finishes
    Publishes event to invalidate caches
    """
    # Publish to Redis pub/sub
    redis_client.publish('warehouse_updated', json.dumps({
        'timestamp': datetime.now().isoformat(),
        'tables': ['sales', 'inventory', 'customers']
    }))

    # Also set a flag in Redis
    redis_client.set('warehouse_last_update', time.time())


# === API Server (subscribes to updates) ===

from threading import Thread

def start_cache_invalidation_listener():
    """
    Background thread listening for warehouse updates
    """
    pubsub = redis_client.pubsub()
    pubsub.subscribe('warehouse_updated')

    for message in pubsub.listen():
        if message['type'] == 'message':
            logger.info("Warehouse updated, invalidating caches")
            invalidate_all_sales_caches()


def invalidate_all_sales_caches():
    """
    Delete all sales-related cache keys
    """
    # Get all matching keys
    keys = redis_client.keys('sales:*')

    # Delete in batches (don't block Redis)
    batch_size = 1000
    for i in range(0, len(keys), batch_size):
        batch = keys[i:i + batch_size]
        redis_client.delete(*batch)

    logger.info(f"Invalidated {len(keys)} cache entries")


# Start listener on app startup
Thread(target=start_cache_invalidation_listener, daemon=True).start()
```

**Pros:**
- ✅ Immediate invalidation (no stale data)
- ✅ Works with irregular update schedules
- ✅ Can invalidate selectively by table

**Cons:**
- ❌ Requires pub/sub infrastructure
- ❌ What if message is lost?
- ❌ Cache stampede still possible

### Strategy 3: Cache Stampede Prevention

**Problem:** At 10:00 AM, 1000 users' caches expire. All 1000 hit warehouse simultaneously!

**Solution 1: Probabilistic Early Expiration**

```python
import random

def get_sales_data(query):
    cache_key = f"sales:{hash(query)}"

    cached_data = redis_client.get(cache_key)
    if cached_data:
        # Probabilistic early refresh
        # As cache gets older, higher chance of refresh
        cache_age = redis_client.ttl(cache_key)
        max_age = 3600  # 1 hour

        # Probability increases as expiry approaches
        refresh_probability = 1 - (cache_age / max_age)

        if random.random() < refresh_probability:
            # Refresh cache in background
            Thread(target=refresh_cache, args=(cache_key, query)).start()

        return json.loads(cached_data)

    # Cache miss - query warehouse
    return query_and_cache(query)
```

**Solution 2: Locking (One request queries, others wait)**

```python
def get_sales_data(query):
    cache_key = f"sales:{hash(query)}"
    lock_key = f"lock:{cache_key}"

    # Check cache
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # Try to acquire lock
    lock_acquired = redis_client.set(lock_key, '1', nx=True, ex=10)  # 10s timeout

    if lock_acquired:
        # This request won the race - query warehouse
        try:
            data = query_warehouse(query)
            redis_client.setex(cache_key, 3600, json.dumps(data))
            return data
        finally:
            redis_client.delete(lock_key)
    else:
        # Another request is already querying - wait for result
        for _ in range(50):  # Wait up to 5 seconds
            time.sleep(0.1)
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

        # Timeout - fallback to querying anyway
        logger.warning(f"Lock timeout for {cache_key}, querying anyway")
        return query_warehouse(query)
```

**Solution 3: Stale-While-Revalidate (Best UX)**

```python
def get_sales_data(query):
    cache_key = f"sales:{hash(query)}"

    # Check cache
    cached_data = redis_client.get(cache_key)
    cache_timestamp = redis_client.get(f"{cache_key}:timestamp")

    if cached_data and cache_timestamp:
        age_seconds = time.time() - float(cache_timestamp)

        # Serve stale data if less than 2 hours old
        if age_seconds < 7200:  # 2 hours
            # If older than 1 hour, refresh in background
            if age_seconds > 3600:
                Thread(target=refresh_cache_async, args=(cache_key, query)).start()

            return json.loads(cached_data)

    # No cache or too old - query synchronously
    data = query_warehouse(query)
    redis_client.setex(cache_key, 7200, json.dumps(data))
    redis_client.setex(f"{cache_key}:timestamp", 7200, str(time.time()))

    return data


def refresh_cache_async(cache_key, query):
    """
    Background cache refresh
    """
    try:
        data = query_warehouse(query)
        redis_client.setex(cache_key, 7200, json.dumps(data))
        redis_client.setex(f"{cache_key}:timestamp", 7200, str(time.time()))
    except Exception as e:
        logger.error(f"Background cache refresh failed: {e}")
        # Don't crash - old cache still valid
```

### Strategy 4: Versioned Caching

```python
def get_sales_data(query):
    # Get current warehouse version
    warehouse_version = redis_client.get('warehouse_version')
    if not warehouse_version:
        warehouse_version = query_warehouse_version()  # e.g., "20241102-10:00"

    cache_key = f"sales:{warehouse_version}:{hash(query)}"

    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # Cache miss
    data = query_warehouse(query)
    redis_client.setex(cache_key, 3600, json.dumps(data))

    return data


# Warehouse update job
def after_warehouse_update():
    # Increment version
    new_version = f"{datetime.now().strftime('%Y%m%d-%H:%M')}"
    redis_client.set('warehouse_version', new_version)

    # Old caches automatically invalid (different version in key)
    # Will expire naturally via TTL
```

---

## 🔴 Common Mistakes to Avoid

### Mistake 1: Synchronous cache invalidation in hot path

```python
# ❌ Bad: Blocks user request
@app.route('/api/invalidate')
def invalidate_caches():
    keys = redis_client.keys('sales:*')  # Can take seconds!
    redis_client.delete(*keys)  # Blocks Redis!
    return "OK"

# ✅ Good: Async invalidation
@app.route('/api/invalidate')
def invalidate_caches():
    Thread(target=invalidate_caches_async).start()
    return "Invalidation started"
```

### Mistake 2: Not handling invalidation failures

```python
# ❌ Bad: No fallback
def get_data(query):
    cache_key = f"sales:{hash(query)}"
    return redis_client.get(cache_key)  # What if Redis is down?

# ✅ Good: Graceful degradation
def get_data(query):
    try:
        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
    except redis.ConnectionError:
        logger.warning("Redis down, querying warehouse directly")

    return query_warehouse(query)
```

### Mistake 3: redis.keys() in production

```python
# ❌ Bad: Blocks entire Redis instance
keys = redis_client.keys('sales:*')  # O(N) operation!

# ✅ Good: Use SCAN (iterative, non-blocking)
def delete_pattern(pattern):
    cursor = 0
    while True:
        cursor, keys = redis_client.scan(cursor, match=pattern, count=100)
        if keys:
            redis_client.delete(*keys)
        if cursor == 0:
            break
```

---

## 🤔 Follow-Up Questions

### Q1: "What if warehouse update fails midway? Some tables updated, others not."

**Good Answer:**
```python
# Use warehouse transaction log

def check_warehouse_consistency():
    """
    Called before cache invalidation
    Verifies all tables updated successfully
    """
    expected_tables = ['sales', 'inventory', 'customers']
    update_log = query_warehouse("SELECT table_name, last_updated FROM update_log")

    current_hour = datetime.now().replace(minute=0, second=0)

    for table in expected_tables:
        last_updated = update_log.get(table)
        if last_updated < current_hour:
            logger.error(f"Table {table} not updated yet!")
            return False  # Don't invalidate cache yet

    return True  # Safe to invalidate


def warehouse_update_complete():
    if check_warehouse_consistency():
        redis_client.publish('warehouse_updated', '...')
    else:
        logger.warning("Warehouse update incomplete, skipping cache invalidation")
```

### Q2: "How do you test cache invalidation in staging?"

**Good Answer:**
```python
# Manual trigger endpoint (protected)

@app.route('/admin/trigger-invalidation', methods=['POST'])
@require_admin
def trigger_invalidation():
    """
    Testing endpoint - simulates warehouse update
    """
    if not app.config['ENV'] in ['staging', 'development']:
        return {"error": "Not allowed in production"}, 403

    redis_client.publish('warehouse_updated', json.dumps({
        'timestamp': datetime.now().isoformat(),
        'test': True
    }))

    return {"status": "Invalidation triggered"}, 200


# Automated tests
def test_cache_invalidation():
    # Seed cache
    redis_client.set('sales:test_key', 'old_data', ex=3600)

    # Trigger invalidation
    client.post('/admin/trigger-invalidation')

    time.sleep(0.5)  # Wait for async invalidation

    # Verify cache cleared
    assert redis_client.get('sales:test_key') is None
```

---

## 💡 Key Takeaways

1. **Event-based > Time-based**
   - Immediate invalidation
   - Handles irregular schedules
   - Requires pub/sub infrastructure

2. **Prevent cache stampede**
   - Locking (one queries, others wait)
   - Stale-while-revalidate (serve old, refresh background)
   - Probabilistic early expiration

3. **Version cache keys**
   - Include warehouse version in key
   - Natural expiration of old caches

4. **Graceful degradation**
   - Fallback to warehouse if Redis down
   - Serve stale data if warehouse slow

5. **Monitor everything**
   - Cache hit ratio
   - Invalidation lag time
   - Stampede incidents

---

## 🔗 Related Questions

- [Question 2: Rate Limiting Across Multiple Servers](./02_rate_limiting.md)
- [Question 4: Handling Long-Running LLM Requests](./04_async_processing.md)

---

[← Back to Case Study 1](./README.md) | [Next Question →](./06_multi_tenancy.md)
