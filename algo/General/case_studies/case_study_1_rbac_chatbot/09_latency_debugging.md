# Question 9: Debugging Production Latency

[← Back to Case Study 1](./README.md)

---

## 🎯 Difficulty: 🟢 Core Concept

## 📝 Question

### Setup

It's Monday morning. Users are complaining that the chatbot is "slow". You check the metrics:

- **p50 (median) latency:** 200ms ✅ (normal)
- **p95 latency:** 5000ms ❌ (terrible! should be < 500ms)
- **p99 latency:** 12000ms ❌ (12 seconds!)

**The mystery:** Most requests are fast, but 5% are extremely slow.

**Your dashboard shows:**
- Database: Healthy
- Redis: Healthy
- CPU: 30% (plenty of capacity)
- Memory: 50% (not an issue)

**Question:** How do you systematically debug this latency issue? Walk me through your process step-by-step.

---

## 🎓 What I'm Looking For

- Systematic debugging approach
- Knowledge of distributed tracing
- Understanding of percentiles
- Database query optimization
- Common production issues

---

## ✅ Good Answer Should Include

### Step 1: Reproduce the Issue

```python
# First, identify WHICH requests are slow
# Log response time for every request

from time import time

@app.before_request
def start_timer():
    request.start_time = time()


@app.after_request
def log_request(response):
    latency = (time() - request.start_time) * 1000  # milliseconds

    logger.info({
        "method": request.method,
        "path": request.path,
        "latency_ms": latency,
        "status": response.status_code,
        "user_id": request.headers.get('X-User-ID'),
        "query_params": dict(request.args)
    })

    # Alert on slow requests
    if latency > 5000:
        logger.warning(f"Slow request detected: {request.path} took {latency}ms")

    return response


# Query logs for slow requests
def find_slow_requests():
    # Get last 1000 slow requests
    slow_requests = query_logs(latency_ms__gt=5000, limit=1000)

    # Group by endpoint
    by_endpoint = defaultdict(list)
    for req in slow_requests:
        by_endpoint[req['path']].append(req)

    # Find pattern
    for path, requests in by_endpoint.items():
        print(f"\n{path}: {len(requests)} slow requests")
        print(f"  Avg latency: {sum(r['latency_ms'] for r in requests) / len(requests):.0f}ms")
        print(f"  Example query_params: {requests[0].get('query_params')}")
```

### Step 2: Add Distributed Tracing

```python
# Instrument code with detailed timing
from functools import wraps

def trace(operation_name):
    """Decorator to track operation timing"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            start = time()
            try:
                result = f(*args, **kwargs)
                duration = (time() - start) * 1000

                logger.info({
                    "operation": operation_name,
                    "duration_ms": duration,
                    "trace_id": request.trace_id
                })

                return result
            except Exception as e:
                duration = (time() - start) * 1000
                logger.error({
                    "operation": operation_name,
                    "duration_ms": duration,
                    "error": str(e),
                    "trace_id": request.trace_id
                })
                raise
        return wrapper
    return decorator


# Instrument the endpoint
@app.route('/api/conversations/<conversation_id>')
@trace("get_conversation")
def get_conversation(conversation_id):
    # Trace each operation
    user_id = _get_user_id()  # Traced

    conversation = _fetch_conversation(conversation_id)  # Traced

    messages = _fetch_messages(conversation_id)  # Traced

    permissions = _check_permissions(user_id, conversation_id)  # Traced

    return jsonify({"conversation": conversation, "messages": messages})


@trace("get_user_id")
def _get_user_id():
    token = request.headers.get('Authorization')
    return jwt.decode(token, SECRET_KEY)['user_id']


@trace("fetch_conversation")
def _fetch_conversation(conversation_id):
    return db.conversations.find_one({"_id": conversation_id})


@trace("fetch_messages")
def _fetch_messages(conversation_id):
    return list(db.messages.find({"conversation_id": conversation_id}))


@trace("check_permissions")
def _check_permissions(user_id, conversation_id):
    # This might be slow!
    return db.permissions.find_one({
        "user_id": user_id,
        "conversation_id": conversation_id
    })


# Example trace output for slow request:
"""
{
  "trace_id": "abc123",
  "total_duration_ms": 5200,
  "operations": [
    {"operation": "get_user_id", "duration_ms": 50},
    {"operation": "fetch_conversation", "duration_ms": 80},
    {"operation": "fetch_messages", "duration_ms": 4800},  ← CULPRIT!
    {"operation": "check_permissions", "duration_ms": 270}
  ]
}
"""
```

### Step 3: Identify the Slow Operation

**Finding: `fetch_messages` is taking 4.8 seconds!**

**Next: Profile the database query**

```python
# Enable MongoDB profiling
db.set_profiling_level(2, slow_ms=1000)  # Log queries > 1 second

# Check slow queries
slow_queries = db.system.profile.find({
    "millis": {"$gt": 1000}
}).sort("millis", -1).limit(10)

for query in slow_queries:
    print(f"Query: {query['command']}")
    print(f"Duration: {query['millis']}ms")
    print(f"Docs examined: {query['docsExamined']}")
    print(f"Docs returned: {query['nreturned']}")
    print()

# Example output:
"""
Query: find conversations.messages {"conversation_id": "conv123"}
Duration: 4850ms
Docs examined: 1000000  ← Scanning 1M documents!
Docs returned: 500      ← Only returning 500

Problem: No index on conversation_id!
"""
```

### Step 4: Fix the Issue

**Problem found: Missing database index!**

```python
# Check current indexes
print(db.messages.index_information())
# Output: {'_id_': {...}}  ← Only default _id index!

# Create missing index
db.messages.create_index([
    ("conversation_id", 1),
    ("timestamp", 1)
])

# Verify improvement
def test_query_performance():
    start = time()
    messages = list(db.messages.find({"conversation_id": "conv123"}))
    duration = (time() - start) * 1000

    print(f"Query took {duration:.0f}ms")
    print(f"Returned {len(messages)} messages")

# Before index: 4850ms
# After index: 45ms ← 100x improvement!
```

---

## 🔴 Common Production Latency Issues

### Issue 1: N+1 Query Problem

```python
# ❌ Bad: 1 query to get conversations, then 1 query per conversation for messages
conversations = db.conversations.find({"user_id": user_id})  # 1 query

for conv in conversations:  # 20 conversations
    messages = db.messages.find({"conversation_id": conv['_id']})  # 20 queries!
    # Total: 21 queries!


# ✅ Good: 2 queries total
conversations = list(db.conversations.find({"user_id": user_id}))  # 1 query
conv_ids = [c['_id'] for c in conversations]

messages_by_conv = {}
messages = db.messages.find({"conversation_id": {"$in": conv_ids}})  # 1 query

for msg in messages:
    conv_id = msg['conversation_id']
    if conv_id not in messages_by_conv:
        messages_by_conv[conv_id] = []
    messages_by_conv[conv_id].append(msg)

# Total: 2 queries (10x faster!)
```

### Issue 2: Unbounded Queries

```python
# ❌ Bad: Fetch all messages (could be 10,000!)
messages = db.messages.find({"conversation_id": conv_id})
# Takes 5 seconds for old conversations with many messages

# ✅ Good: Paginate
messages = db.messages.find({"conversation_id": conv_id}) \
    .sort("timestamp", -1) \
    .limit(50)  # Latest 50 only
# Takes 50ms
```

### Issue 3: External API calls in hot path

```python
# ❌ Bad: Call external API for every request
@app.route('/api/user/profile')
def get_profile(user_id):
    user = db.users.find_one({"user_id": user_id})

    # External API call (500ms)
    avatar_url = fetch_avatar_from_gravatar(user['email'])

    return jsonify({"user": user, "avatar": avatar_url})


# ✅ Good: Cache external data
@app.route('/api/user/profile')
def get_profile(user_id):
    user = db.users.find_one({"user_id": user_id})

    # Check cache first
    cache_key = f"avatar:{user['email']}"
    avatar_url = redis_client.get(cache_key)

    if not avatar_url:
        # Cache miss - fetch from API
        avatar_url = fetch_avatar_from_gravatar(user['email'])
        redis_client.setex(cache_key, 86400, avatar_url)  # Cache 24h

    return jsonify({"user": user, "avatar": avatar_url})
```

### Issue 4: Slow serialization

```python
# ❌ Bad: Serialize large objects to JSON
@app.route('/api/conversations/<id>')
def get_conversation(id):
    conv = db.conversations.find_one({"_id": id})

    # Conversation has 10,000 messages embedded!
    return jsonify(conv)  # Takes 3 seconds to serialize


# ✅ Good: Project only needed fields
@app.route('/api/conversations/<id>')
def get_conversation(id):
    conv = db.conversations.find_one(
        {"_id": id},
        {
            "title": 1,
            "created_at": 1,
            "message_count": 1,
            "messages": {"$slice": 50}  # Only latest 50 messages
        }
    )

    return jsonify(conv)  # Takes 50ms
```

---

## 🤔 Follow-Up Questions

### Q1: "How do you prevent this issue from happening again?"

**Good Answer:**
```python
# 1. Add query performance monitoring
def monitor_query_performance(collection, operation, duration_ms):
    if duration_ms > 1000:
        alert("Slow query detected", {
            "collection": collection,
            "operation": operation,
            "duration_ms": duration_ms
        })


# 2. Add index monitoring
def check_missing_indexes():
    """
    Run weekly: Analyze slow queries and suggest indexes
    """
    slow_queries = db.system.profile.find({"millis": {"$gt": 1000}})

    for query in slow_queries:
        if query['docsExamined'] > query['nreturned'] * 100:
            print(f"⚠️  Possible missing index:")
            print(f"   Collection: {query['ns']}")
            print(f"   Query: {query['command']}")
            print(f"   Examined: {query['docsExamined']}, Returned: {query['nreturned']}")


# 3. Load testing before deploy
def load_test():
    """
    Simulate production load
    """
    for _ in range(1000):
        response = requests.get('/api/conversations/conv123')
        latency = response.elapsed.total_seconds() * 1000

        if latency > 500:
            print(f"❌ Latency too high: {latency}ms")


# 4. SLO monitoring
# Define SLO: p95 < 500ms
# Alert if SLO violated
```

### Q2: "How do you debug latency in distributed systems (microservices)?"

**Good Answer:**
```python
# Use distributed tracing (Jaeger, Zipkin)

from opentelemetry import trace
from opentelemetry.exporter.jaeger import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Setup tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name='localhost',
    agent_port=6831,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)


# Instrument services
@app.route('/api/chat')
def chat():
    with tracer.start_as_current_span("chat_endpoint"):
        # Span automatically tracks duration

        with tracer.start_as_current_span("call_auth_service"):
            user = call_auth_service()  # Microservice 1

        with tracer.start_as_current_span("call_llm_service"):
            response = call_llm_service(user, query)  # Microservice 2

        with tracer.start_as_current_span("save_to_db"):
            save_conversation(response)  # Database

        return jsonify(response)


# Jaeger UI shows:
"""
chat_endpoint (5.2s)
├── call_auth_service (0.1s)
├── call_llm_service (4.8s)  ← SLOW!
└── save_to_db (0.3s)
"""
```

---

## 💡 Key Takeaways

1. **Percentiles matter**
   - p50 (median) doesn't show outliers
   - Always monitor p95, p99
   - Slowest requests affect user experience most

2. **Systematic approach**
   - Reproduce issue (logs)
   - Isolate slow operation (tracing)
   - Profile database queries
   - Fix root cause

3. **Common culprits**
   - Missing database indexes
   - N+1 query problem
   - Unbounded queries
   - External API calls in hot path

4. **Prevention**
   - Query performance monitoring
   - Load testing before deploy
   - Regular index reviews
   - SLO alerting

5. **Tools**
   - Distributed tracing (Jaeger, Zipkin)
   - Database profiling
   - APM tools (Datadog, New Relic)

---

## 🔗 Related Questions

- [Question 3: Database Design for Conversations](./03_database_design.md)
- [Question 5: Cache Invalidation Strategy](./05_cache_invalidation.md)

---

[← Back to Case Study 1](./README.md) | [Next Question →](./10_circuit_breaker.md)
