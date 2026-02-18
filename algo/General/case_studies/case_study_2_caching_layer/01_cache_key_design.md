# Question 1: Cache Key Design for Complex Queries

[← Back to Case Study 2](./README.md)

---

## 🎯 Difficulty: 🟢 Core Concept

## 📝 Question

### Setup

Your chatbot allows users to query sales data with complex filters:

**Example query:**
```
"Show me sales for:
- Products: ['iPhone', 'iPad', 'MacBook']
- Regions: ['North America', 'Europe']
- Time period: '2024-Q1'
- Metric: 'revenue'
- Breakdown by: 'month'"
```

You need to cache these results in Redis. Each unique query combination needs a unique cache key.

**The Challenge:**

If you just concatenate:
```python
cache_key = f"sales:{products}:{regions}:{time}:{metric}:{breakdown}"
# Result: "sales:['iPhone','iPad','MacBook']:['North America','Europe']:2024-Q1:revenue:month"
```

**Problems:**
- Key too long (Redis key limit: 512MB but long keys are slow)
- Order matters: `['iPhone', 'iPad']` ≠ `['iPad', 'iPhone']` (but should be same cache!)
- Special characters cause issues
- Keys aren't readable

**Question:** How do you design cache keys that are:
1. Unique (different queries → different keys)
2. Consistent (same query → same key, regardless of parameter order)
3. Short (fast Redis lookups)
4. Debuggable (human-readable)

---

## 🎓 What I'm Looking For

- Hash function design
- Key normalization strategies
- Collision handling
- Trade-offs between readability and performance

---

## ✅ Good Answer Should Include

### Strategy 1: Normalized Hash Keys (Recommended)

```python
import hashlib
import json

def generate_cache_key(query_params):
    """
    Generate consistent, short cache key from query parameters
    """
    # Step 1: Normalize parameters
    normalized = normalize_params(query_params)

    # Step 2: Create stable JSON representation
    canonical_json = json.dumps(normalized, sort_keys=True)

    # Step 3: Hash to fixed-length key
    hash_value = hashlib.sha256(canonical_json.encode()).hexdigest()[:16]

    # Step 4: Human-readable prefix
    prefix = get_query_prefix(query_params)

    # Final key: readable prefix + hash
    cache_key = f"sales:{prefix}:{hash_value}"

    return cache_key


def normalize_params(params):
    """
    Normalize parameters for consistent hashing
    """
    normalized = {}

    # Sort lists
    if 'products' in params:
        normalized['products'] = sorted(params['products'])

    if 'regions' in params:
        normalized['regions'] = sorted(params['regions'])

    # Normalize time format
    if 'time_period' in params:
        normalized['time_period'] = normalize_time(params['time_period'])

    # Lowercase strings
    if 'metric' in params:
        normalized['metric'] = params['metric'].lower()

    if 'breakdown' in params:
        normalized['breakdown'] = params['breakdown'].lower()

    return normalized


def normalize_time(time_str):
    """
    Normalize different time formats to canonical form
    """
    # "Q1 2024", "2024-Q1", "Jan-Mar 2024" → "2024-Q1"
    if 'Q1' in time_str or 'Jan' in time_str:
        return "2024-Q1"
    # ... handle other formats

    return time_str


def get_query_prefix(params):
    """
    Create human-readable prefix for debugging
    """
    metric = params.get('metric', 'unknown')[:4]
    period = params.get('time_period', 'all')[:8]

    return f"{metric}_{period}"


# Example usage:
params = {
    'products': ['iPhone', 'iPad', 'MacBook'],
    'regions': ['Europe', 'North America'],  # Different order!
    'time_period': '2024-Q1',
    'metric': 'Revenue',  # Capital R
    'breakdown': 'month'
}

cache_key = generate_cache_key(params)
print(cache_key)
# Output: "sales:reve_2024-Q1:7f3d8c2b1a5e9f42"

# Same query with different order/case:
params2 = {
    'products': ['MacBook', 'iPad', 'iPhone'],  # Different order
    'regions': ['North America', 'Europe'],      # Different order
    'time_period': 'Q1 2024',                    # Different format
    'metric': 'revenue',                          # Lowercase
    'breakdown': 'MONTH'                          # Uppercase
}

cache_key2 = generate_cache_key(params2)
print(cache_key2)
# Output: "sales:reve_2024-Q1:7f3d8c2b1a5e9f42"  ← Same key!
```

**Pros:**
- ✅ Consistent (same query always produces same key)
- ✅ Short (hash is fixed length)
- ✅ Fast lookups

**Cons:**
- ❌ Hash collisions (rare but possible)
- ❌ Less debuggable (need to log params separately)

### Strategy 2: Hierarchical Keys (Better Debugging)

```python
def generate_hierarchical_key(params):
    """
    Create hierarchical key structure for better organization
    """
    # Group by metric and time period
    metric = params.get('metric', 'unknown')
    time_period = params.get('time_period', 'all')

    # Sort and abbreviate lists
    products = '_'.join(sorted(params.get('products', []))[:3])  # Max 3
    regions = '_'.join(sorted(params.get('regions', []))[:2])     # Max 2

    # Build hierarchical key
    key = f"sales:{metric}:{time_period}:{products}:{regions}"

    # If too long (> 100 chars), hash the last part
    if len(key) > 100:
        products_regions = f"{products}:{regions}"
        hashed = hashlib.md5(products_regions.encode()).hexdigest()[:8]
        key = f"sales:{metric}:{time_period}:{hashed}"

    return key


# Example:
cache_key = generate_hierarchical_key(params)
# Output: "sales:revenue:2024-Q1:iPad_iPhone_MacBook:Europe_NorthAmerica"

# Can query by pattern:
all_revenue_keys = redis.keys("sales:revenue:*")
q1_keys = redis.keys("sales:*:2024-Q1:*")
```

**Pros:**
- ✅ Debuggable (can see what's cached)
- ✅ Pattern matching (`sales:revenue:*`)
- ✅ Good for analytics

**Cons:**
- ❌ Keys can be long
- ❌ Need careful normalization

### Strategy 3: Hybrid (Best of Both)

```python
def generate_hybrid_key(params):
    """
    Hybrid approach: readable prefix + hash suffix
    Store full params in separate key
    """
    # Generate hash key
    normalized = normalize_params(params)
    canonical_json = json.dumps(normalized, sort_keys=True)
    hash_value = hashlib.sha256(canonical_json.encode()).hexdigest()[:12]

    # Human-readable prefix
    metric = params.get('metric', 'unknown')[:6]
    period = params.get('time_period', 'all').replace('-', '')[:8]
    num_products = len(params.get('products', []))
    num_regions = len(params.get('regions', []))

    # Final key
    cache_key = f"sales:{metric}:{period}:p{num_products}r{num_regions}:{hash_value}"

    # Store mapping for debugging
    redis.setex(
        f"cache_metadata:{hash_value}",
        86400,  # 24 hours
        json.dumps(params)
    )

    return cache_key


# Example:
cache_key = generate_hybrid_key(params)
# Output: "sales:revenu:2024Q1:p3r2:7f3d8c2b1a5e"

# For debugging, can lookup:
params_debug = redis.get("cache_metadata:7f3d8c2b1a5e")
print(params_debug)
# {"products": ["iPad", "iPhone", "MacBook"], ...}
```

---

## 🔴 Common Mistakes to Avoid

### Mistake 1: Not normalizing order

```python
# ❌ Bad: Different order = different keys
key1 = f"sales:{['iPhone', 'iPad']}"    # "sales:['iPhone', 'iPad']"
key2 = f"sales:{['iPad', 'iPhone']}"    # "sales:['iPad', 'iPhone']"
# These are different! Cache miss!

# ✅ Good: Sort before hashing
products = sorted(['iPhone', 'iPad'])
key = f"sales:{products}"  # Always same order
```

### Mistake 2: Case sensitivity

```python
# ❌ Bad: Case matters
key1 = f"sales:Revenue"  # "sales:Revenue"
key2 = f"sales:revenue"  # "sales:revenue"
# Different keys!

# ✅ Good: Normalize case
metric = params['metric'].lower()
key = f"sales:{metric}"
```

### Mistake 3: Not handling special characters

```python
# ❌ Bad: Special characters cause issues
product = "iPhone 13 Pro Max (256GB)"
key = f"sales:{product}"
# Redis key contains spaces, parentheses!

# ✅ Good: URL-encode or hash
product_encoded = urllib.parse.quote(product)
# OR
product_hash = hashlib.md5(product.encode()).hexdigest()[:8]
```

### Mistake 4: Collision-prone short hashes

```python
# ❌ Bad: 4-character hash → high collision rate
hash_value = hashlib.sha256(data.encode()).hexdigest()[:4]
# Only 65,536 possible values!

# ✅ Good: 12-16 character hash → negligible collision rate
hash_value = hashlib.sha256(data.encode()).hexdigest()[:16]
# 2^64 possible values (collision extremely unlikely)
```

---

## 🤔 Follow-Up Questions

### Q1: "How do you handle hash collisions?"

**Good Answer:**
```python
def get_cached_result(query_params):
    """
    Handle potential hash collisions
    """
    cache_key = generate_cache_key(query_params)

    # Get cached data
    cached_data = redis.get(cache_key)

    if cached_data:
        data = json.loads(cached_data)

        # Verify this is actually the right query (collision check)
        if data.get('query_params') == query_params:
            return data['result']
        else:
            # Hash collision detected!
            logger.warning(f"Cache key collision detected: {cache_key}")
            # Fall through to query warehouse
            return None

    return None


def cache_result(query_params, result):
    """
    Store result with original params for collision detection
    """
    cache_key = generate_cache_key(query_params)

    cached_data = {
        'query_params': query_params,  # Store original params
        'result': result,
        'cached_at': time.time()
    }

    redis.setex(cache_key, 3600, json.dumps(cached_data))
```

### Q2: "How do you debug cache misses?"

**Good Answer:**
```python
# Add logging to track cache keys and params

def get_with_logging(query_params):
    cache_key = generate_cache_key(query_params)

    # Log cache attempt
    logger.info({
        "action": "cache_lookup",
        "cache_key": cache_key,
        "query_params": query_params
    })

    result = redis.get(cache_key)

    if result:
        logger.info({
            "action": "cache_hit",
            "cache_key": cache_key
        })
    else:
        logger.info({
            "action": "cache_miss",
            "cache_key": cache_key,
            "reason": "key_not_found"
        })

        # Store params for debugging
        redis.setex(
            f"debug:miss:{cache_key}",
            300,  # 5 minutes
            json.dumps(query_params)
        )

    return result


# Dashboard: Show top cache misses
def analyze_cache_misses():
    miss_keys = redis.keys("debug:miss:*")

    for key in miss_keys:
        params = json.loads(redis.get(key))
        print(f"Cache miss: {params}")
```

---

## 💡 Key Takeaways

1. **Always normalize**
   - Sort lists (products, regions)
   - Lowercase strings
   - Standardize time formats

2. **Hash for consistency**
   - Use SHA-256 (12-16 chars)
   - Avoid short hashes (collisions)
   - Include params in cached value (collision detection)

3. **Human-readable prefixes**
   - `sales:revenue:2024Q1:{hash}`
   - Helps debugging
   - Enables pattern matching

4. **Store metadata separately**
   - Map hash → original params
   - Useful for debugging
   - TTL can be shorter than cache

5. **Test normalization**
   - Same query, different order → same key
   - Different case → same key
   - Different time format → same key

---

## 🔗 Related Questions

- [Question 2: Semantic Query Matching](./02_semantic_matching.md)
- [Question 4: Cache Stampede Prevention](./04_cache_stampede.md)

---

[← Back to Case Study 2](./README.md) | [Next Question →](./02_semantic_matching.md)
