# Question 7: Model Version Deployment

[← Back to Case Study 1](./README.md)

---

## 🎯 Difficulty: 🟡 Intermediate

## 📝 Question

### Setup

You have an ML model that classifies user queries:
- **Model v1:** 85% accuracy, running in production for 6 months, stable
- **Model v2:** 92% accuracy on test set, but untested in production

You need to deploy v2 **without breaking production** if it fails.

**Scenario:**

If you just swap v1 → v2:
- What if v2 has a bug that crashes on certain inputs?
- What if v2 is slower than expected?
- What if v2's 92% accuracy doesn't hold in production?

**Question:** How do you safely roll out model v2 while being able to instantly rollback if needed?

---

## 🎓 What I'm Looking For

- Understanding of canary deployments
- Shadow mode testing
- A/B testing strategies
- Gradual rollout patterns
- Rollback criteria and triggers

---

## ✅ Good Answer Should Include

### Strategy 1: Shadow Mode (No User Impact)

**Phase 1: Run both models, but only use v1 results**

```python
class ModelRouter:
    def __init__(self):
        self.model_v1 = load_model('model_v1')
        self.model_v2 = load_model('model_v2')  # New model

    def predict(self, query):
        # Production prediction (v1)
        prediction_v1 = self.model_v1.predict(query)

        # Shadow prediction (v2) - runs in background
        Thread(target=self._shadow_predict, args=(query,)).start()

        # Return v1 result to user (safe!)
        return prediction_v1

    def _shadow_predict(self, query):
        """
        Run v2 in background, log results for comparison
        """
        try:
            start_time = time.time()
            prediction_v2 = self.model_v2.predict(query)
            latency = time.time() - start_time

            # Log for analysis
            logger.info({
                "model": "v2",
                "query": query,
                "prediction": prediction_v2,
                "latency_ms": latency * 1000,
                "shadow_mode": True
            })

        except Exception as e:
            # v2 crashed - but doesn't affect user!
            logger.error(f"Model v2 error (shadow): {e}")
```

**Analysis after 1 week:**

```python
# Compare predictions
def analyze_shadow_results():
    v1_predictions = get_predictions(model="v1", days=7)
    v2_predictions = get_predictions(model="v2", days=7, shadow=True)

    # Agreement rate
    agreement = sum(1 for v1, v2 in zip(v1_predictions, v2_predictions)
                    if v1['prediction'] == v2['prediction'])
    agreement_rate = agreement / len(v1_predictions)

    # Latency comparison
    v1_latency = np.percentile([p['latency_ms'] for p in v1_predictions], 95)
    v2_latency = np.percentile([p['latency_ms'] for p in v2_predictions], 95)

    # Error rate
    v2_errors = sum(1 for p in v2_predictions if p.get('error'))
    v2_error_rate = v2_errors / len(v2_predictions)

    print(f"Agreement: {agreement_rate:.1%}")
    print(f"V1 p95 latency: {v1_latency:.0f}ms")
    print(f"V2 p95 latency: {v2_latency:.0f}ms")
    print(f"V2 error rate: {v2_error_rate:.2%}")

    # Decision
    if agreement_rate > 0.8 and v2_latency < 500 and v2_error_rate < 0.01:
        print("✅ Safe to proceed to canary deployment")
    else:
        print("❌ V2 not ready, needs more work")
```

**Pros:**
- ✅ Zero user impact
- ✅ Real production data
- ✅ Catches crashes before rollout

**Cons:**
- ❌ Double compute cost
- ❌ Can't measure actual accuracy (no ground truth)

### Strategy 2: Canary Deployment (1% → 10% → 50% → 100%)

**Phase 2: Route 1% of traffic to v2**

```python
class ModelRouter:
    def __init__(self):
        self.model_v1 = load_model('model_v1')
        self.model_v2 = load_model('model_v2')
        self.canary_percent = self._get_canary_percent()

    def _get_canary_percent(self):
        # Read from config (can update without deploy)
        return int(redis_client.get('model_v2_canary_percent') or 0)

    def predict(self, query, user_id):
        # Deterministic routing (same user always gets same model)
        user_hash = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        user_bucket = user_hash % 100  # 0-99

        canary_percent = self._get_canary_percent()

        if user_bucket < canary_percent:
            # User in canary group
            return self._predict_with_monitoring(query, "v2")
        else:
            # User in control group
            return self._predict_with_monitoring(query, "v1")

    def _predict_with_monitoring(self, query, model_version):
        model = self.model_v2 if model_version == "v2" else self.model_v1

        start_time = time.time()
        try:
            prediction = model.predict(query)
            latency = time.time() - start_time

            # Log prediction
            logger.info({
                "model": model_version,
                "prediction": prediction,
                "latency_ms": latency * 1000,
                "success": True
            })

            # Track metrics
            metrics.histogram(f"model_{model_version}_latency", latency * 1000)
            metrics.increment(f"model_{model_version}_success")

            return prediction

        except Exception as e:
            latency = time.time() - start_time
            logger.error({
                "model": model_version,
                "error": str(e),
                "latency_ms": latency * 1000
            })

            metrics.increment(f"model_{model_version}_error")

            # Fallback to v1 if v2 fails
            if model_version == "v2":
                logger.warning("Model v2 failed, falling back to v1")
                return self.model_v1.predict(query)
            else:
                raise
```

**Gradual rollout schedule:**

```python
# Day 1: 1% canary
redis_client.set('model_v2_canary_percent', 1)

# Day 3: If metrics good, increase to 10%
redis_client.set('model_v2_canary_percent', 10)

# Day 5: 25%
redis_client.set('model_v2_canary_percent', 25)

# Day 7: 50%
redis_client.set('model_v2_canary_percent', 50)

# Day 10: 100% (full rollout)
redis_client.set('model_v2_canary_percent', 100)


# Automated rollback if errors spike
def monitor_and_rollback():
    """
    Runs every 5 minutes
    """
    v1_error_rate = get_error_rate(model="v1", minutes=5)
    v2_error_rate = get_error_rate(model="v2", minutes=5)

    if v2_error_rate > v1_error_rate * 2:  # V2 errors 2x higher
        logger.critical("Model v2 error rate too high, rolling back!")
        redis_client.set('model_v2_canary_percent', 0)
        alert_on_call_engineer("Model v2 rollback triggered")
```

### Strategy 3: A/B Testing with Metrics

**Track business metrics, not just technical metrics**

```python
# Track user satisfaction by model version
def log_user_feedback(user_id, query_id, feedback):
    """
    User clicks thumbs up/down on chatbot response
    """
    # Find which model served this query
    query_log = db.query_logs.find_one({"query_id": query_id})
    model_version = query_log['model_version']

    db.feedback.insert_one({
        "user_id": user_id,
        "query_id": query_id,
        "model_version": model_version,
        "feedback": feedback,  # "positive" or "negative"
        "timestamp": datetime.now()
    })


# Analyze after 1 week
def compare_user_satisfaction():
    v1_feedback = db.feedback.find({"model_version": "v1"})
    v2_feedback = db.feedback.find({"model_version": "v2"})

    v1_positive_rate = sum(1 for f in v1_feedback if f['feedback'] == 'positive') / v1_feedback.count()
    v2_positive_rate = sum(1 for f in v2_feedback if f['feedback'] == 'positive') / v2_feedback.count()

    print(f"V1 satisfaction: {v1_positive_rate:.1%}")
    print(f"V2 satisfaction: {v2_positive_rate:.1%}")

    # Statistical significance test
    p_value = stats.chi2_contingency(...)  # Chi-square test

    if p_value < 0.05 and v2_positive_rate > v1_positive_rate:
        print("✅ V2 is statistically better")
    else:
        print("❌ No significant improvement")
```

---

## 🔴 Common Mistakes to Avoid

### Mistake 1: No rollback plan

```python
# ❌ Bad: Hard-coded model version
model = load_model('model_v2')

# ✅ Good: Config-driven
model_version = config.get('active_model_version', 'v1')
model = load_model(f'model_{model_version}')

# Instant rollback via config change (no deploy needed)
```

### Mistake 2: Non-deterministic routing

```python
# ❌ Bad: Random routing
if random.random() < 0.1:  # 10% canary
    use_v2()
# Problem: Same user gets different models each request!

# ✅ Good: Deterministic by user_id
user_hash = hash(user_id) % 100
if user_hash < 10:  # 10% canary
    use_v2()
# Same user always gets same model (consistent experience)
```

### Mistake 3: Not monitoring business metrics

```python
# ❌ Bad: Only technical metrics
# "V2 has 50ms lower latency!"
# But users hate the results...

# ✅ Good: Track user satisfaction
# - Thumbs up/down rate
# - Follow-up question rate (indicates bad answer)
# - Session abandonment rate
# - Query reformulation rate
```

### Mistake 4: Deploying on Friday

```python
# ❌ Bad: Deploy v2 on Friday afternoon
# If it breaks, you're working the weekend!

# ✅ Good: Deploy Tuesday morning
# Gives you Wed-Thu-Fri to monitor and fix issues
```

---

## 🤔 Follow-Up Questions

### Q1: "How do you test model inference time in production?"

**Good Answer:**
```python
# Load testing before rollout
def load_test_model_v2():
    """
    Simulate production load
    """
    # Sample 1000 recent queries
    queries = db.query_logs.find().sort("timestamp", -1).limit(1000)

    latencies = []
    errors = 0

    for query in queries:
        start = time.time()
        try:
            model_v2.predict(query['text'])
            latency = time.time() - start
            latencies.append(latency * 1000)
        except Exception as e:
            errors += 1
            logger.error(f"Prediction failed: {e}")

    print(f"P50: {np.percentile(latencies, 50):.0f}ms")
    print(f"P95: {np.percentile(latencies, 95):.0f}ms")
    print(f"P99: {np.percentile(latencies, 99):.0f}ms")
    print(f"Error rate: {errors / len(queries):.1%}")

    # Requirements
    assert np.percentile(latencies, 95) < 500, "P95 too high!"
    assert errors / len(queries) < 0.01, "Error rate too high!"
```

### Q2: "How do you version models in storage?"

**Good Answer:**
```python
# Model artifacts stored with version tags
MODEL_PATHS = {
    "v1": "s3://models/query-classifier-v1/model.pkl",
    "v2": "s3://models/query-classifier-v2/model.pkl",
    "v2.1": "s3://models/query-classifier-v2.1/model.pkl"
}

# Metadata stored in database
{
    "model_id": "v2",
    "created_at": "2024-11-01",
    "trained_on": "2024-10-15 to 2024-10-30",
    "training_samples": 50000,
    "test_accuracy": 0.92,
    "features": ["query_length", "keyword_count", ...],
    "hyperparameters": {"learning_rate": 0.001, ...},
    "model_path": "s3://models/query-classifier-v2/model.pkl"
}

# Never delete old models (might need to rollback!)
```

###Q3: "What if v2 is much slower but more accurate?"

**Good Answer:**
```python
# Option 1: Hybrid routing (slow queries → v2, fast queries → v1)
def predict(query):
    query_complexity = estimate_complexity(query)

    if query_complexity > 0.7:  # Complex query
        # Use v2 (slow but accurate)
        return model_v2.predict(query)
    else:  # Simple query
        # Use v1 (fast but less accurate)
        return model_v1.predict(query)


# Option 2: Async processing for v2
def predict(query):
    if estimated_latency_v2 > 1000:  # > 1 second
        # Return v1 immediately, compute v2 in background
        task_id = compute_v2_async.delay(query)
        return {
            "prediction": model_v1.predict(query),  # Fast but less accurate
            "task_id": task_id,  # User can poll for better result
            "upgrade_available": True
        }
    else:
        return {"prediction": model_v2.predict(query)}


# Option 3: Infrastructure upgrade
# Add more powerful servers / GPUs for v2
# Accept higher cost for better accuracy
```

---

## 💡 Key Takeaways

1. **Shadow mode first**
   - Test with real production data
   - Zero user impact
   - Catch crashes and latency issues

2. **Gradual rollout**
   - 1% → 10% → 25% → 50% → 100%
   - Monitor at each stage
   - Pause if metrics degrade

3. **Deterministic routing**
   - Same user always gets same model
   - Consistent experience
   - Easier to debug issues

4. **Auto-rollback triggers**
   - Error rate > 2x baseline
   - Latency > 500ms p95
   - User satisfaction drop > 5%

5. **Business metrics > technical metrics**
   - Track user satisfaction
   - Monitor downstream conversions
   - Don't optimize latency at cost of accuracy

---

## 🔗 Related Questions

- [Question 4: Handling Long-Running LLM Requests](./04_async_processing.md)
- [Question 10: Circuit Breaker Implementation](./10_circuit_breaker.md)

---

[← Back to Case Study 1](./README.md) | [Next Question →](./08_gdpr_deletion.md)
