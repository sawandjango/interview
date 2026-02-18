# Question 4: Handling Long-Running LLM Requests

[← Back to Case Study 1](./README.md)

---

## 🎯 Difficulty: 🟡 Intermediate

## 📝 Question

### Setup

Your chatbot uses GPT-4 for complex queries. These requests can take **20-30 seconds** to complete. Meanwhile, you also have simple queries that should respond in **< 200ms** (like fetching conversation history).

The problem: **All requests go through the same API**. When a user makes a GPT-4 request, it blocks the server thread for 30 seconds.

**Scenario:**
- 10 users submit GPT-4 queries (30s each)
- User #11 tries to fetch their conversation list (should be instant)
- **User #11 waits 30+ seconds!** ❌

**Question:** How do you architect this system so fast queries stay fast, even when heavy LLM requests are running?

---

## 🎓 What I'm Looking For

- Understanding of head-of-line blocking
- Knowledge of async task queues (Celery, RabbitMQ, Redis Queue)
- API design (sync vs async endpoints)
- Graceful degradation patterns
- User experience considerations

---

## ✅ Good Answer Should Include

### Solution: Separate Sync and Async Paths

**Architecture:**

```
User Request
    ↓
API Gateway
    ↓
  ┌─────────────────────┐
  │  Route by query     │
  │  type               │
  └─────────────────────┘
          ↓
    ┌─────────┴─────────┐
    ↓                   ↓
┌─────────┐      ┌──────────────┐
│ Sync    │      │ Async Queue  │
│ Fast    │      │ (Celery)     │
│ < 500ms │      │              │
└─────────┘      └──────────────┘
    ↓                   ↓
Response          Task ID returned
immediately       User polls for result
```

### Implementation

**Step 1: Create async endpoints**

```python
from celery import Celery
from flask import Flask, jsonify, request

app = Flask(__name__)
celery = Celery('tasks', broker='redis://localhost:6379/0')

# === SYNC ENDPOINTS (Fast queries) ===

@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    """
    Fast query - returns immediately
    """
    user_id = request.headers['X-User-ID']
    conversations = db.conversations.find(
        {"user_id": user_id}
    ).sort("updated_at", -1).limit(20)

    return jsonify({"conversations": list(conversations)}), 200


# === ASYNC ENDPOINTS (LLM queries) ===

@app.route('/api/chat', methods=['POST'])
def submit_chat_query():
    """
    LLM query - returns task ID immediately
    Actual processing happens in background
    """
    user_id = request.headers['X-User-ID']
    query = request.json['query']
    conversation_id = request.json['conversation_id']

    # Submit to Celery queue (returns immediately!)
    task = process_llm_query.delay(user_id, conversation_id, query)

    return jsonify({
        "task_id": task.id,
        "status": "processing",
        "estimated_time_seconds": 30
    }), 202  # 202 = Accepted


@app.route('/api/chat/status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """
    Poll endpoint - check if LLM response is ready
    """
    task = celery.AsyncResult(task_id)

    if task.state == 'PENDING':
        return jsonify({"status": "processing"}), 200

    elif task.state == 'SUCCESS':
        return jsonify({
            "status": "completed",
            "result": task.result
        }), 200

    elif task.state == 'FAILURE':
        return jsonify({
            "status": "failed",
            "error": str(task.info)
        }), 500

    else:
        return jsonify({"status": task.state}), 200


# === CELERY TASK (Background worker) ===

@celery.task(bind=True)
def process_llm_query(self, user_id, conversation_id, query):
    """
    Runs in background worker
    Takes 20-30 seconds
    """
    try:
        # Call GPT-4 (slow!)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": query}],
            timeout=60
        )

        answer = response.choices[0].message.content

        # Save to database
        db.messages.insert_one({
            "conversation_id": conversation_id,
            "sender": "bot",
            "content": answer,
            "timestamp": datetime.now()
        })

        return {
            "answer": answer,
            "conversation_id": conversation_id
        }

    except Exception as e:
        # Retry 3 times with exponential backoff
        raise self.retry(exc=e, countdown=2 ** self.request.retries, max_retries=3)
```

**Step 2: Frontend implementation**

```javascript
// Option 1: Polling
async function askChatbot(query) {
  // Submit query
  const response = await fetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ query, conversation_id: 'conv123' })
  });

  const { task_id } = await response.json();

  // Poll every 2 seconds
  return new Promise((resolve, reject) => {
    const pollInterval = setInterval(async () => {
      const statusResponse = await fetch(`/api/chat/status/${task_id}`);
      const status = await statusResponse.json();

      if (status.status === 'completed') {
        clearInterval(pollInterval);
        resolve(status.result);
      } else if (status.status === 'failed') {
        clearInterval(pollInterval);
        reject(status.error);
      }
      // Continue polling if still processing
    }, 2000);
  });
}

// Option 2: WebSockets (better UX)
const socket = new WebSocket('ws://api.example.com/ws');

function askChatbot(query) {
  socket.send(JSON.stringify({
    type: 'chat_query',
    query: query,
    conversation_id: 'conv123'
  }));
}

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.type === 'chat_response') {
    displayAnswer(data.answer);  // Show result
  } else if (data.type === 'progress') {
    showProgress(data.percent);  // Show progress bar
  }
};
```

---

## 🔴 Common Mistakes to Avoid

### Mistake 1: Not separating fast and slow queries

```python
# ❌ Bad: All queries in same endpoint
@app.route('/api/query', methods=['POST'])
def handle_query(query):
    # Fast query waits behind slow query!
    if is_llm_query(query):
        return call_gpt4(query)  # 30 seconds
    else:
        return fetch_from_db(query)  # 50ms

# ✅ Good: Separate endpoints
@app.route('/api/chat', methods=['POST'])  # Async
@app.route('/api/conversations', methods=['GET'])  # Sync
```

### Mistake 2: No timeout on LLM calls

```python
# ❌ Bad: No timeout
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[...]
    # Hangs forever if OpenAI is down!
)

# ✅ Good: Set timeout
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[...],
    timeout=60  # Fail after 60 seconds
)
```

### Mistake 3: Not handling queue overload

```python
# ❌ Bad: Unlimited queue growth
task = process_llm_query.delay(query)
# Queue grows to 10,000 tasks → Redis OOM!

# ✅ Good: Check queue size first
from celery.app.control import Inspect

def submit_query(query):
    inspector = Inspect(app=celery)
    active_tasks = inspector.active()

    # Count total tasks
    total = sum(len(tasks) for tasks in active_tasks.values())

    if total > 1000:
        return {"error": "System overloaded, try again later"}, 503

    task = process_llm_query.delay(query)
    return {"task_id": task.id}, 202
```

### Mistake 4: No retry logic

```python
# ❌ Bad: One failure = permanent failure
@celery.task
def process_llm_query(query):
    return openai.ChatCompletion.create(...)
    # Fails permanently if OpenAI has 1-second hiccup

# ✅ Good: Retry with exponential backoff
@celery.task(bind=True, max_retries=3)
def process_llm_query(self, query):
    try:
        return openai.ChatCompletion.create(...)
    except Exception as e:
        # Retry after 2^n seconds (2s, 4s, 8s)
        raise self.retry(exc=e, countdown=2 ** self.request.retries)
```

---

## 🤔 Follow-Up Questions

### Q1: "How do you show progress to the user while LLM is processing?"

**Good Answer:**
```python
# Use Celery task.update_state() to send progress

@celery.task(bind=True)
def process_llm_query(self, query):
    # Step 1: Preprocessing
    self.update_state(state='PROGRESS', meta={'percent': 10, 'status': 'Analyzing query...'})
    time.sleep(2)

    # Step 2: Calling LLM
    self.update_state(state='PROGRESS', meta={'percent': 30, 'status': 'Generating response...'})
    response = openai.ChatCompletion.create(...)

    # Step 3: Post-processing
    self.update_state(state='PROGRESS', meta={'percent': 80, 'status': 'Formatting...'})
    formatted = format_response(response)

    # Step 4: Done
    self.update_state(state='PROGRESS', meta={'percent': 100, 'status': 'Complete'})
    return formatted

# Frontend polls and shows progress bar
async function pollStatus(task_id) {
  const response = await fetch(`/api/chat/status/${task_id}`);
  const data = await response.json();

  if (data.status === 'PROGRESS') {
    updateProgressBar(data.meta.percent);  // 10%, 30%, 80%, 100%
    showMessage(data.meta.status);  // "Analyzing query..."
  }
}
```

### Q2: "What if Celery workers crash? How do you prevent lost tasks?"

**Good Answer:**
```python
# Option 1: Task acknowledgment AFTER completion
celery.conf.task_acks_late = True
celery.conf.worker_prefetch_multiplier = 1

# Task stays in queue until worker confirms completion
# If worker crashes, task goes back to queue

# Option 2: Result backend (Redis/Database)
celery.conf.result_backend = 'redis://localhost:6379/1'

# Task results persisted, can be retrieved even after restart

# Option 3: Dead letter queue
from celery.signals import task_failure

@task_failure.connect
def handle_task_failure(sender=None, task_id=None, exception=None, **kwargs):
    # Log failed task
    logger.error(f"Task {task_id} failed: {exception}")

    # Store in database for manual retry
    db.failed_tasks.insert_one({
        "task_id": task_id,
        "exception": str(exception),
        "timestamp": datetime.now()
    })
```

### Q3: "How do you handle cancellation? User closes browser mid-query."

**Good Answer:**
```python
# Option 1: Revoke task
@app.route('/api/chat/cancel/<task_id>', methods=['POST'])
def cancel_task(task_id):
    celery.control.revoke(task_id, terminate=True)
    return {"status": "cancelled"}, 200

# Option 2: Timeout for abandoned tasks
@celery.task(bind=True, time_limit=300, soft_time_limit=290)
def process_llm_query(self, query):
    # Hard limit: 300s (5 min)
    # Soft limit: 290s (gives 10s to cleanup)
    try:
        return openai.ChatCompletion.create(...)
    except SoftTimeLimitExceeded:
        # Cleanup before hard kill
        cleanup()
        raise

# Option 3: Heartbeat check
@celery.task(bind=True)
def process_llm_query(self, user_id, query):
    # Check if user still waiting
    if not redis.exists(f"active_session:{user_id}"):
        logger.info(f"User {user_id} disconnected, aborting task")
        return None

    return openai.ChatCompletion.create(...)

# Frontend sends heartbeat
setInterval(() => {
  redis.setex(`active_session:${user_id}`, 60, '1');
}, 30000);  // Every 30 seconds
```

---

## 📊 Architecture Comparison

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| **Sync (blocking)** | Simple | Blocks threads | Fast queries only |
| **Threading** | Easy to implement | GIL in Python, memory overhead | I/O-bound tasks |
| **Async (asyncio)** | Efficient | Complex code | Many concurrent requests |
| **Celery queue** | Scalable, robust | Infrastructure overhead | Long-running tasks |
| **Serverless (Lambda)** | Auto-scaling | Cold starts, 15min limit | Bursty workloads |

**My Recommendation: Celery + Redis**
- Proven at scale (used by Instagram, Reddit)
- Great tooling and monitoring
- Easy to add more workers

---

## 💡 Key Takeaways

1. **Separate fast and slow paths**
   - Fast queries: Sync endpoints (< 500ms)
   - Slow queries: Async with task queue (> 1s)

2. **Return task ID immediately**
   - Don't make user wait for 30 seconds
   - Return 202 Accepted with task_id
   - Let them poll or use WebSockets

3. **Always set timeouts**
   - On external API calls
   - On Celery tasks
   - On database queries

4. **Handle failures gracefully**
   - Retry with exponential backoff
   - Dead letter queue for persistent failures
   - Show helpful error messages

5. **Monitor queue health**
   - Queue depth (alert if > 1000)
   - Worker count (auto-scale)
   - Task duration (detect slowdowns)

---

## 🔗 Related Questions

- [Question 5: Cache Invalidation Strategy](./05_cache_invalidation.md)
- [Question 10: Circuit Breaker Implementation](./10_circuit_breaker.md)

---

[← Back to Case Study 1](./README.md) | [Next Question →](./05_cache_invalidation.md)
