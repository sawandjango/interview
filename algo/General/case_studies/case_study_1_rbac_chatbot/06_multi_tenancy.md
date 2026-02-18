# Question 6: Multi-Tenancy & Data Isolation

[← Back to Case Study 1](./README.md)

---

## 🎯 Difficulty: 🔴 Advanced

## 📝 Question

### Setup

Your chatbot is a **SaaS product**. 100 companies use it, all sharing the same database. Each company's data MUST be completely isolated:

- Company A should NEVER see Company B's conversations
- No accidental leaks via bugs, SQL injection, or misconfigured queries
- Compliance requirement: Pass SOC 2 audit

**Scenario:**

A developer writes this code:

```python
@app.route('/api/conversations')
def get_conversations():
    user_id = request.headers['X-User-ID']
    # BUG: No tenant_id check!
    conversations = db.conversations.find({"user_id": user_id})
    return jsonify(list(conversations))
```

**Problem:** If User ID "123" exists in both Company A and Company B, this returns conversations from BOTH companies! ❌

**Questions:**

1. How do you architect the system to prevent this class of bugs?
2. How do you test data isolation?
3. How do you handle shared resources (rate limits, quotas)?

---

## 🎓 What I'm Looking For

- Understanding of multi-tenancy patterns
- Database isolation strategies
- Row-level security (RLS)
- Testing for data leaks
- Compliance awareness (SOC 2, GDPR)

---

## ✅ Good Answer Should Include

### Strategy 1: Tenant ID in Every Query (Manual)

```python
# Middleware extracts tenant_id from JWT
from functools import wraps

def get_tenant_id():
    """Extract tenant ID from authenticated request"""
    token = request.headers.get('Authorization').replace('Bearer ', '')
    claims = jwt.decode(token, SECRET_KEY)
    return claims['tenant_id']


def require_tenant(f):
    """Decorator ensuring tenant_id is always passed"""
    @wraps(f)
    def decorated(*args, **kwargs):
        # Inject tenant_id into kwargs
        kwargs['tenant_id'] = get_tenant_id()
        return f(*args, **kwargs)
    return decorated


@app.route('/api/conversations')
@require_tenant
def get_conversations(tenant_id):
    """
    tenant_id automatically injected by decorator
    """
    user_id = request.headers['X-User-ID']

    # MUST include tenant_id in every query
    conversations = db.conversations.find({
        "tenant_id": tenant_id,  # CRITICAL!
        "user_id": user_id
    })

    return jsonify(list(conversations))
```

**Pros:**
- ✅ Simple to understand
- ✅ Works with any database

**Cons:**
- ❌ Easy to forget tenant_id
- ❌ No enforcement at database level
- ❌ Vulnerable to bugs

### Strategy 2: Database Row-Level Security (PostgreSQL)

```sql
-- Enable row-level security
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their tenant's data
CREATE POLICY tenant_isolation ON conversations
    USING (tenant_id = current_setting('app.tenant_id')::int);

-- Grant SELECT to app user
GRANT SELECT ON conversations TO app_user;
```

```python
# Set tenant_id for this connection
def query_with_tenant(tenant_id, query_func):
    """
    Execute query with tenant context
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Set tenant context for this session
        cursor.execute(f"SET app.tenant_id = {tenant_id}")

        # Execute query - RLS automatically filters by tenant
        result = query_func(cursor)

        return result
    finally:
        cursor.execute("RESET app.tenant_id")
        cursor.close()


# Usage
@app.route('/api/conversations')
@require_tenant
def get_conversations(tenant_id):
    def query(cursor):
        cursor.execute("""
            SELECT * FROM conversations
            WHERE user_id = %s
            -- No need to add tenant_id - RLS handles it!
        """, (user_id,))
        return cursor.fetchall()

    return query_with_tenant(tenant_id, query)
```

**Pros:**
- ✅ Enforced at database level
- ✅ Impossible to accidentally leak data
- ✅ Works even with buggy queries

**Cons:**
- ❌ PostgreSQL-specific
- ❌ Performance overhead (small)
- ❌ Complex to debug

### Strategy 3: Separate Databases Per Tenant

```python
# Connection pool manager
class TenantDatabaseManager:
    def __init__(self):
        self.connections = {}

    def get_db(self, tenant_id):
        """
        Get database connection for specific tenant
        """
        if tenant_id not in self.connections:
            # Each tenant has separate database
            db_name = f"tenant_{tenant_id}_db"
            self.connections[tenant_id] = pymongo.MongoClient()[db_name]

        return self.connections[tenant_id]


db_manager = TenantDatabaseManager()


@app.route('/api/conversations')
@require_tenant
def get_conversations(tenant_id):
    # Get tenant-specific database
    db = db_manager.get_db(tenant_id)

    user_id = request.headers['X-User-ID']

    # No tenant_id needed - physically separate databases!
    conversations = db.conversations.find({"user_id": user_id})

    return jsonify(list(conversations))
```

**Pros:**
- ✅ Complete physical isolation
- ✅ Easy to migrate single tenant
- ✅ Better performance (smaller datasets)

**Cons:**
- ❌ Expensive (100 databases!)
- ❌ Complex schema migrations
- ❌ Hard to do cross-tenant analytics

### Strategy 4: Hybrid (Schema-based in PostgreSQL)

```python
# Each tenant gets separate PostgreSQL schema
# One database, multiple schemas

def get_schema_name(tenant_id):
    return f"tenant_{tenant_id}"


def query_tenant_schema(tenant_id, query_func):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        schema = get_schema_name(tenant_id)

        # Set search_path to tenant schema
        cursor.execute(f"SET search_path TO {schema}")

        result = query_func(cursor)

        return result
    finally:
        cursor.execute("SET search_path TO public")
        cursor.close()


# Table exists in each schema
# tenant_1.conversations
# tenant_2.conversations
# tenant_3.conversations
```

**Pros:**
- ✅ Physical isolation within one database
- ✅ Easier management than separate DBs
- ✅ Good performance

**Cons:**
- ❌ PostgreSQL-specific
- ❌ Schema migration complexity

---

## 🔴 Common Mistakes to Avoid

### Mistake 1: Relying only on application logic

```python
# ❌ Bad: One bug = data leak
def get_conversations(tenant_id, user_id):
    return db.conversations.find({
        "tenant_id": tenant_id,  # What if developer forgets this?
        "user_id": user_id
    })

# ✅ Good: Defense in depth
# 1. Application layer (tenant_id required)
# 2. Database layer (row-level security)
# 3. Automated tests (verify isolation)
```

### Mistake 2: Shared User IDs across tenants

```python
# ❌ Bad: User ID 123 exists in multiple tenants
{
    "user_id": "123",  # Collision!
    "tenant_id": "tenant_A"
}

# ✅ Good: Globally unique user IDs
{
    "user_id": "tenant_A_123",  # Unique across all tenants
    "tenant_id": "tenant_A"
}

# Or use UUIDs
{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "tenant_id": "tenant_A"
}
```

### Mistake 3: No monitoring for cross-tenant queries

```python
# ❌ Bad: No detection
db.conversations.find({"user_id": user_id})  # Accidental cross-tenant query

# ✅ Good: Monitor and alert
def query_conversations(tenant_id, user_id):
    results = db.conversations.find({
        "tenant_id": tenant_id,
        "user_id": user_id
    })

    # Log query for audit
    audit_log.info({
        "action": "query_conversations",
        "tenant_id": tenant_id,
        "user_id": user_id,
        "result_count": len(results)
    })

    return results


# Alert on suspicious patterns
# Example: User accessing data from multiple tenants
```

---

## 🤔 Follow-Up Questions

### Q1: "How do you test data isolation?"

**Good Answer:**
```python
# Test 1: Basic isolation
def test_tenant_isolation():
    # Create data for tenant A
    tenant_a_conv = create_conversation(tenant_id="tenant_a", user_id="user123")

    # Create data for tenant B (same user_id!)
    tenant_b_conv = create_conversation(tenant_id="tenant_b", user_id="user123")

    # Query as tenant A - should only see tenant A data
    with tenant_context("tenant_a"):
        results = get_conversations(user_id="user123")
        assert len(results) == 1
        assert results[0]['id'] == tenant_a_conv['id']
        assert results[0]['id'] != tenant_b_conv['id']


# Test 2: SQL injection attempt
def test_sql_injection_tenant_bypass():
    # Attacker tries to bypass tenant filter
    malicious_user_id = "123' OR tenant_id != 'tenant_a' --"

    with tenant_context("tenant_a"):
        results = get_conversations(user_id=malicious_user_id)
        # Should return empty (no user with that ID)
        assert len(results) == 0


# Test 3: Pagination doesn't leak
def test_pagination_isolation():
    # Create 100 conversations for each tenant
    for i in range(100):
        create_conversation(tenant_id="tenant_a", user_id=f"user{i}")
        create_conversation(tenant_id="tenant_b", user_id=f"user{i}")

    # Paginate tenant A - should never see tenant B
    with tenant_context("tenant_a"):
        for page in range(1, 11):  # 10 pages
            results = get_conversations(page=page, per_page=10)
            for conv in results:
                assert conv['tenant_id'] == "tenant_a"


# Test 4: Performance - ensure indexes work per-tenant
def test_tenant_query_performance():
    with tenant_context("tenant_a"):
        start = time.time()
        results = get_conversations(user_id="user123")
        duration = time.time() - start

        # Should be fast even with millions of rows across all tenants
        assert duration < 0.1  # 100ms
```

### Q2: "How do you handle shared resources like rate limits?"

**Good Answer:**
```python
# Option 1: Per-tenant rate limits
RATE_LIMITS = {
    "basic": 100,      # 100 req/min
    "premium": 1000,   # 1000 req/min
    "enterprise": None # Unlimited
}

def check_rate_limit(tenant_id, user_id):
    # Get tenant's plan
    tenant = db.tenants.find_one({"tenant_id": tenant_id})
    limit = RATE_LIMITS[tenant['plan']]

    if limit is None:  # Unlimited
        return True

    # Rate limit per tenant
    key = f"ratelimit:{tenant_id}:{current_minute}"
    count = redis.incr(key)

    if count == 1:
        redis.expire(key, 60)

    if count > limit:
        raise RateLimitExceeded(f"Tenant limit: {limit}/min")

    return True


# Option 2: Per-user within tenant
def check_user_rate_limit(tenant_id, user_id):
    # Each user gets their own limit
    key = f"ratelimit:{tenant_id}:{user_id}:{current_minute}"
    count = redis.incr(key)

    if count == 1:
        redis.expire(key, 60)

    user_limit = 10  # 10 req/min per user
    if count > user_limit:
        raise RateLimitExceeded("User limit: 10/min")

    # Also check tenant-wide limit
    tenant_key = f"ratelimit_tenant:{tenant_id}:{current_minute}"
    tenant_count = redis.incr(tenant_key)

    tenant = db.tenants.find_one({"tenant_id": tenant_id})
    tenant_limit = RATE_LIMITS[tenant['plan']]

    if tenant_count > tenant_limit:
        raise RateLimitExceeded(f"Tenant limit reached: {tenant_limit}/min")

    return True
```

### Q3: "How do you handle tenant-specific configurations?"

**Good Answer:**
```python
# Tenant configuration stored in database
class TenantConfig:
    def __init__(self, tenant_id):
        self.tenant_id = tenant_id
        self._config = self._load_config()

    def _load_config(self):
        # Load from database
        tenant = db.tenants.find_one({"tenant_id": self.tenant_id})
        return tenant.get('config', {})

    def get(self, key, default=None):
        return self._config.get(key, default)


# Usage
@app.route('/api/chat', methods=['POST'])
@require_tenant
def chat(tenant_id):
    config = TenantConfig(tenant_id)

    # Tenant-specific settings
    max_tokens = config.get('max_tokens', 1000)
    temperature = config.get('temperature', 0.7)
    model = config.get('model', 'gpt-4')

    # Custom prompt prefix
    system_prompt = config.get('system_prompt', 'You are a helpful assistant.')

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.json['query']}
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )

    return jsonify({"answer": response.choices[0].message.content})
```

---

## 📊 Multi-Tenancy Strategy Comparison

| Strategy | Isolation | Cost | Complexity | Best For |
|----------|-----------|------|------------|----------|
| **Shared DB + tenant_id** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | Small tenants, high count |
| **Row-Level Security** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Medium security needs |
| **Separate schemas** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | Moderate tenant count |
| **Separate databases** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | Large enterprises |

**My Recommendation:**
- **Start with:** Row-level security (good isolation, reasonable cost)
- **Upgrade to:** Separate schemas for large tenants (> 1M records)
- **Reserve:** Separate databases for enterprise customers (contractual requirement)

---

## 💡 Key Takeaways

1. **Defense in depth**
   - Application layer (decorators, middleware)
   - Database layer (RLS, schemas)
   - Testing layer (automated isolation tests)

2. **Never trust application logic alone**
   - Bugs happen
   - Use database-enforced isolation

3. **Globally unique identifiers**
   - User IDs, conversation IDs should be unique across ALL tenants
   - Use UUIDs or tenant-prefixed IDs

4. **Test, test, test**
   - Automated tests for data isolation
   - Penetration testing
   - SQL injection attempts

5. **Monitor cross-tenant access**
   - Audit logs
   - Alerts for suspicious patterns
   - Regular compliance audits

---

## 🔗 Related Questions

- [Question 1: JWT Token Security & Breach Response](./01_jwt_security.md)
- [Question 8: GDPR Right to be Forgotten](./08_gdpr_deletion.md)

---

[← Back to Case Study 1](./README.md) | [Next Question →](./07_model_deployment.md)
