# Question 10: Circuit Breaker Implementation

[← Back to Case Study 1](./README.md)

---

## 🎯 Difficulty: 🟡 Intermediate

## 📝 Question

### Setup

Your chatbot calls OpenAI's API for every query. Normally this works great.

**The Problem (Friday, 2 PM):**

OpenAI API starts having issues:
- 50% of requests timeout (> 60 seconds)
- Your servers keep retrying
- All your threads/workers get blocked waiting
- **Your entire application goes down** even though your servers are healthy!

**Cascading Failure:**

```
OpenAI slow → Your workers blocked → Queue fills up → New requests timeout → Users can't even fetch old conversations!
```

**Question:** How do you prevent OpenAI's failures from taking down your entire system?

---

## 🎓 What I'm Looking For

- Understanding of circuit breaker pattern
- State management (closed, open, half-open)
- Fallback strategies
- Graceful degradation
- Real-world implementation details

---

## ✅ Good Answer Should Include

### Core Concept: Circuit Breaker Pattern

**Three States:**

```
┌─────────────┐
│   CLOSED    │  Normal operation
│  (healthy)  │  Requests go through
└──────┬──────┘
       │
       │ Too many failures
       ↓
┌─────────────┐
│    OPEN     │  Failing
│  (broken)   │  Requests blocked immediately
└──────┬──────┘  Return error or fallback
       │
       │ After timeout
       ↓
┌─────────────┐
│ HALF-OPEN   │  Testing
│  (testing)  │  Allow 1 request to test
└──────┬──────┘
       │
       ├─ Success → CLOSED
       └─ Failure → OPEN
```

### Implementation

```python
import time
from enum import Enum
from threading import Lock

class CircuitState(Enum):
    CLOSED = "closed"      # Healthy
    OPEN = "open"          # Broken
    HALF_OPEN = "half_open"  # Testing


class CircuitBreaker:
    def __init__(
        self,
        failure_threshold=5,       # Open after 5 failures
        timeout=60,                # Stay open for 60 seconds
        expected_exception=Exception
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self.lock = Lock()

    def call(self, func, *args, **kwargs):
        """
        Execute function with circuit breaker protection
        """
        with self.lock:
            if self.state == CircuitState.OPEN:
                # Check if timeout elapsed
                if time.time() - self.last_failure_time >= self.timeout:
                    # Move to HALF_OPEN (test if service recovered)
                    self.state = CircuitState.HALF_OPEN
                    logger.info("Circuit breaker moving to HALF_OPEN")
                else:
                    # Still broken - fail fast
                    raise CircuitBreakerOpenError("Circuit breaker is OPEN")

        # Execute function
        try:
            result = func(*args, **kwargs)

            # Success!
            with self.lock:
                if self.state == CircuitState.HALF_OPEN:
                    # Test passed - close circuit
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
                    logger.info("Circuit breaker CLOSED (service recovered)")

            return result

        except self.expected_exception as e:
            # Failure
            with self.lock:
                self.failure_count += 1
                self.last_failure_time = time.time()

                if self.state == CircuitState.HALF_OPEN:
                    # Test failed - reopen circuit
                    self.state = CircuitState.OPEN
                    logger.warning("Circuit breaker reopened (test failed)")

                elif self.failure_count >= self.failure_threshold:
                    # Too many failures - open circuit
                    self.state = CircuitState.OPEN
                    logger.error(f"Circuit breaker OPENED after {self.failure_count} failures")

            raise


class CircuitBreakerOpenError(Exception):
    pass


# Usage
circuit_breaker = CircuitBreaker(
    failure_threshold=5,  # Open after 5 failures
    timeout=60,           # Stay open 60 seconds
    expected_exception=(requests.Timeout, requests.ConnectionError)
)


def call_openai_with_circuit_breaker(query):
    """
    Call OpenAI API with circuit breaker protection
    """
    try:
        return circuit_breaker.call(call_openai_api, query)
    except CircuitBreakerOpenError:
        # Circuit is open - return fallback
        logger.warning("Circuit breaker open, using fallback")
        return get_fallback_response(query)


def call_openai_api(query):
    """
    Actual OpenAI API call
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": query}],
        timeout=30  # Fail fast
    )
    return response.choices[0].message.content
```

### Fallback Strategies

**Strategy 1: Cached Responses**

```python
def get_fallback_response(query):
    """
    Return cached response for similar queries
    """
    # Find similar queries in cache
    cache_key = f"query_cache:{hash(query)}"
    cached = redis_client.get(cache_key)

    if cached:
        return {
            "answer": cached,
            "source": "cache",
            "message": "Using cached response (OpenAI unavailable)"
        }

    # Find semantically similar query
    similar_query = find_similar_query(query)
    if similar_query:
        return {
            "answer": similar_query['answer'],
            "source": "similar_query",
            "message": "Using response from similar query"
        }

    # No cache - return graceful error
    return {
        "answer": None,
        "source": "error",
        "message": "AI service temporarily unavailable. Please try again later."
    }
```

**Strategy 2: Degraded Mode (Simpler Model)**

```python
def call_openai_with_fallback(query):
    try:
        # Try primary (GPT-4)
        return circuit_breaker_gpt4.call(call_gpt4, query)
    except CircuitBreakerOpenError:
        logger.info("GPT-4 unavailable, falling back to GPT-3.5")
        try:
            # Fallback to GPT-3.5 (faster, cheaper)
            return circuit_breaker_gpt3.call(call_gpt3_5, query)
        except CircuitBreakerOpenError:
            # Both unavailable
            return get_cached_response(query)
```

**Strategy 3: Queue for Later**

```python
def handle_query_with_fallback(query, user_id):
    try:
        # Try immediate response
        answer = circuit_breaker.call(call_openai_api, query)
        return {"answer": answer, "status": "completed"}

    except CircuitBreakerOpenError:
        # OpenAI down - queue for later
        task_id = queue_for_later.delay(query, user_id)

        return {
            "answer": None,
            "status": "queued",
            "task_id": task_id,
            "message": "Your query has been queued. We'll email you when ready."
        }


@celery.task
def queue_for_later(query, user_id):
    """
    Process query when OpenAI recovers
    """
    # Wait for circuit to close
    while True:
        try:
            answer = circuit_breaker.call(call_openai_api, query)

            # Success! Send email
            send_email(user_id, f"Your answer: {answer}")
            return answer

        except CircuitBreakerOpenError:
            # Still open - wait 1 minute
            time.sleep(60)
```

---

## 🔴 Common Mistakes to Avoid

### Mistake 1: Not failing fast

```python
# ❌ Bad: Wait 60 seconds for timeout
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[...],
    timeout=60  # Blocks for 60 seconds!
)
# When OpenAI is down, every request waits 60s

# ✅ Good: Fail fast (10 seconds max)
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[...],
    timeout=10  # Fail after 10 seconds
)
```

### Mistake 2: Circuit breaker per instance (not shared)

```python
# ❌ Bad: Each server has separate circuit breaker
circuit_breaker = CircuitBreaker()  # In-memory

# Problem: Server 1 opens circuit, but Server 2-5 keep hammering OpenAI!


# ✅ Good: Shared circuit breaker (Redis)
class SharedCircuitBreaker:
    def __init__(self, redis_client, service_name):
        self.redis = redis_client
        self.service_name = service_name

    def is_open(self):
        state = self.redis.get(f"circuit:{self.service_name}:state")
        return state == "open"

    def open(self):
        self.redis.setex(f"circuit:{self.service_name}:state", 60, "open")

    def close(self):
        self.redis.delete(f"circuit:{self.service_name}:state")
```

### Mistake 3: No observability

```python
# ❌ Bad: Silent failures
if circuit_breaker.is_open():
    return fallback()

# ✅ Good: Log and alert
if circuit_breaker.is_open():
    logger.error("Circuit breaker OPEN for OpenAI")
    metrics.increment("circuit_breaker.open", tags=["service:openai"])
    alert_on_call("OpenAI circuit breaker opened")
    return fallback()
```

---

## 🤔 Follow-Up Questions

### Q1: "How do you test circuit breaker in staging?"

**Good Answer:**
```python
# Chaos engineering - simulate failures

def test_circuit_breaker():
    # Inject failures
    with inject_failure(openai.ChatCompletion, error=requests.Timeout):
        # First 5 requests should fail and count toward threshold
        for i in range(5):
            try:
                call_openai_with_circuit_breaker("test query")
            except Exception:
                pass

        # Circuit should now be OPEN
        assert circuit_breaker.state == CircuitState.OPEN

        # Next request should fail immediately (not call OpenAI)
        start = time.time()
        try:
            call_openai_with_circuit_breaker("test query")
        except CircuitBreakerOpenError:
            pass
        duration = time.time() - start

        # Should fail instantly (not wait for timeout)
        assert duration < 0.1

    # Remove failure injection
    # Wait for timeout
    time.sleep(61)

    # Circuit should move to HALF_OPEN and test
    result = call_openai_with_circuit_breaker("test query")

    # Should succeed and close circuit
    assert circuit_breaker.state == CircuitState.CLOSED
```

### Q2: "Should you have one circuit breaker for all external services or one per service?"

**Good Answer:**
```
One per service (recommended):
──────────────────────────────
circuit_breaker_openai = CircuitBreaker(...)
circuit_breaker_stripe = CircuitBreaker(...)
circuit_breaker_sendgrid = CircuitBreaker(...)

Why:
✓ Independent failures (Stripe down ≠ OpenAI down)
✓ Different thresholds (critical vs non-critical services)
✓ Different fallback strategies
✓ Better observability (know which service is failing)


Example:
if circuit_breaker_openai.is_open():
    # OpenAI down - use fallback
    return cached_response()

if circuit_breaker_stripe.is_open():
    # Stripe down - queue payment for later
    return queue_payment()

if circuit_breaker_sendgrid.is_open():
    # SendGrid down - log email, retry later
    return log_email_for_retry()
```

### Q3: "How do you prevent thundering herd when circuit reopens?"

**Good Answer:**
```python
# Problem: Circuit opens → 1000 queued requests → Circuit closes → All 1000 hammer service at once!

# Solution: Gradual recovery
class GradualCircuitBreaker(CircuitBreaker):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recovery_percentage = 0

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.HALF_OPEN:
            # Only allow recovery_percentage of requests through
            if random.random() > self.recovery_percentage:
                raise CircuitBreakerOpenError("Gradual recovery in progress")

        result = super().call(func, *args, **kwargs)

        # Gradually increase allowed traffic
        if self.state == CircuitState.HALF_OPEN:
            self.recovery_percentage = min(1.0, self.recovery_percentage + 0.1)

        return result


# Phase 1: 10% traffic
# Phase 2: 20% traffic
# ...
# Phase 10: 100% traffic (fully recovered)
```

---

## 💡 Key Takeaways

1. **Fail fast**
   - Set aggressive timeouts (10s, not 60s)
   - Don't let slow services block your app
   - Circuit breaker prevents cascading failures

2. **Three states**
   - CLOSED: Normal (requests go through)
   - OPEN: Broken (fail fast, use fallback)
   - HALF_OPEN: Testing (try one request)

3. **Shared state in distributed systems**
   - Use Redis for circuit breaker state
   - All servers see same circuit status
   - Prevent thundering herd

4. **Always have fallback**
   - Cached responses
   - Degraded mode (simpler model)
   - Queue for later
   - Graceful error message

5. **Monitor and alert**
   - Log circuit state changes
   - Alert when circuit opens
   - Track fallback usage
   - Dashboard for observability

---

## 🔗 Related Questions

- [Question 4: Handling Long-Running LLM Requests](./04_async_processing.md)
- [Question 7: Model Version Deployment](./07_model_deployment.md)

---

[← Back to Case Study 1](./README.md)
