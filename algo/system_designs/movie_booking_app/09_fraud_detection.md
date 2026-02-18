# ML-Based Fraud Detection System

## Overview
Real-time fraud detection using machine learning to identify and prevent fraudulent bookings, payment fraud, and bot activity.

---

## Fraud Types

```
1. PAYMENT FRAUD
   • Stolen credit cards
   • Card testing (small transactions)
   • Chargeback fraud

2. BOOKING FRAUD
   • Bot reservations (scalpers)
   • Multiple bookings, single payment
   • Fake accounts for free seats

3. PROMO ABUSE
   • Referral code abuse
   • Discount code farming
   • Multi-accounting

4. ACCOUNT TAKEOVER
   • Credential stuffing
   • Phishing attacks
   • Session hijacking
```

---

## ML Model Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                  FRAUD DETECTION PIPELINE                    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Trigger: User attempts booking → BEFORE payment            │
│                                                              │
│  Step 1: Feature Extraction (<10ms)                         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  User Features:                                        │ │
│  │    • account_age_days: 45                             │ │
│  │    • total_bookings_lifetime: 12                      │ │
│  │    • booking_velocity_1h: 5 (suspicious\!)             │ │
│  │    • failed_payments_24h: 2                           │ │
│  │    • email_domain: "temp-mail.com" (red flag\!)        │ │
│  │    • phone_verified: False                            │ │
│  │                                                        │ │
│  │  Device Features:                                      │ │
│  │    • device_fingerprint: hash                         │ │
│  │    • browser: "Chrome 120"                            │ │
│  │    • os: "Windows 11"                                 │ │
│  │    • is_vpn: True (suspicious\!)                       │ │
│  │    • screen_resolution: "1920x1080"                   │ │
│  │                                                        │ │
│  │  Behavioral Features:                                  │ │
│  │    • time_on_site_seconds: 15 (too fast\!)             │ │
│  │    • pages_visited: 2                                 │ │
│  │    • mouse_movements: 0 (bot behavior\!)               │ │
│  │    • booking_time: 3:00 AM (unusual hour)             │ │
│  │                                                        │ │
│  │  Transaction Features:                                 │ │
│  │    • booking_value: $250                              │ │
│  │    • num_seats: 10 (unusual\!)                         │ │
│  │    • different_ip_than_usual: True                    │ │
│  │    • different_location_than_usual: True              │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                   │
│  Step 2: ML Model Inference (<50ms requirement\!)             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Model: Isolation Forest (Anomaly Detection)          │ │
│  │  Alternative: XGBoost (Supervised)                     │ │
│  │                                                        │ │
│  │  Input: 25-30 features                                │ │
│  │  Output: fraud_score ∈ [0, 1]                         │ │
│  │                                                        │ │
│  │  fraud_score = 0.87 (HIGH RISK\!)                      │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ↓                                   │
│  Step 3: Decision Logic                                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  if fraud_score > 0.8:                                │ │
│  │      action = "BLOCK"                                 │ │
│  │      reason = "High fraud risk"                       │ │
│  │                                                        │ │
│  │  elif 0.5 < fraud_score <= 0.8:                       │ │
│  │      action = "VERIFY"                                │ │
│  │      reason = "Require 2FA or ID verification"        │ │
│  │                                                        │ │
│  │  else:                                                 │ │
│  │      action = "ALLOW"                                 │ │
│  │      reason = "Low risk"                              │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Feature Engineering

```python
def extract_fraud_features(user_id, booking_request):
    features = {}

    # User historical features
    user = get_user(user_id)
    features['account_age_days'] = (datetime.now() - user.created_at).days
    features['total_bookings'] = user.booking_count
    features['avg_booking_value'] = user.total_spent / max(user.booking_count, 1)

    # Velocity features (critical\!)
    features['bookings_last_hour'] = count_bookings(user_id, hours=1)
    features['bookings_last_day'] = count_bookings(user_id, hours=24)
    features['failed_payments_24h'] = count_failed_payments(user_id, hours=24)

    # Device fingerprint
    features['is_new_device'] = is_new_device(user_id, booking_request.device_id)
    features['is_vpn'] = detect_vpn(booking_request.ip_address)
    features['device_bot_score'] = bot_detection_score(booking_request)

    # Location anomaly
    user_locations = get_user_historical_locations(user_id)
    features['location_distance_km'] = haversine_distance(
        booking_request.location, user_locations.most_common
    )

    # Email reputation
    features['email_domain_reputation'] = check_email_domain(user.email)
    features['is_disposable_email'] = is_disposable(user.email)

    # Transaction features
    features['booking_value'] = booking_request.total_amount
    features['num_seats'] = len(booking_request.seat_ids)
    features['unusual_hour'] = 1 if 0 <= datetime.now().hour <= 5 else 0

    # Behavioral
    features['time_on_site'] = (datetime.now() - booking_request.session_start).seconds
    features['mouse_movements'] = booking_request.mouse_event_count

    return features
```

---

## Model Training

### Isolation Forest (Unsupervised)
```python
from sklearn.ensemble import IsolationForest

# Load historical data (no labels needed\!)
X_train = load_historical_features()  # Last 6 months

# Train Isolation Forest
model = IsolationForest(
    contamination=0.05,  # Assume 5% are fraudulent
    n_estimators=200,
    max_samples=256,
    random_state=42
)

model.fit(X_train)

# Predict anomaly score
fraud_score = model.decision_function(X_test)
# Normalize to [0, 1]: 0 = normal, 1 = fraud
fraud_score = 1 - (fraud_score - fraud_score.min()) / (fraud_score.max() - fraud_score.min())
```

### XGBoost (Supervised, if labels available)
```python
import xgboost as xgb

# Load labeled data
X_train, y_train = load_labeled_fraud_data()  # 0 = legit, 1 = fraud

# Handle class imbalance (fraud is rare\!)
scale_pos_weight = len(y_train[y_train == 0]) / len(y_train[y_train == 1])

# Train XGBoost
model = xgb.XGBClassifier(
    max_depth=6,
    learning_rate=0.05,
    n_estimators=500,
    scale_pos_weight=scale_pos_weight,  # Balance classes
    eval_metric='aucpr'  # Precision-Recall AUC
)

model.fit(X_train, y_train)

# Predict fraud probability
fraud_prob = model.predict_proba(X_test)[:, 1]  # Probability of fraud
```

---

## Real-Time Scoring

```python
@app.route('/api/fraud/check', methods=['POST'])
def check_fraud():
    """
    Real-time fraud check (MUST be <50ms\!)
    """
    start_time = time.time()

    # Extract features (target: <10ms)
    features = extract_fraud_features(
        user_id=request.json['user_id'],
        booking_request=request.json['booking']
    )

    # Model inference (target: <30ms)
    fraud_score = fraud_model.predict([list(features.values())])[0]

    # Decision
    if fraud_score > 0.8:
        action, reason = "BLOCK", "High fraud risk"
    elif fraud_score > 0.5:
        action, reason = "VERIFY", "Additional verification required"
    else:
        action, reason = "ALLOW", "Low risk"

    # Log for monitoring
    latency_ms = (time.time() - start_time) * 1000
    logger.info(f"Fraud check: {action}, score={fraud_score:.2f}, latency={latency_ms:.1f}ms")

    # Alert if high risk
    if fraud_score > 0.8:
        alert_fraud_team(user_id, features, fraud_score)

    return {
        "action": action,
        "fraud_score": fraud_score,
        "reason": reason,
        "latency_ms": latency_ms
    }
```

---

## Feedback Loop

```
┌───────────────────────────────────────────────────────┐
│  Continuous Learning (Weekly Retraining)              │
├───────────────────────────────────────────────────────┤
│                                                       │
│  Day 1-7: Model makes predictions                     │
│    • Block high-risk bookings                        │
│    • Flag medium-risk for review                     │
│                                                       │
│  Fraud Analyst Reviews:                               │
│    • Reviews 200 flagged cases/week                  │
│    • Labels: TRUE_FRAUD or FALSE_POSITIVE            │
│    • Feedback stored in database                     │
│                                                       │
│  Sunday Night: Automated Retraining                   │
│    1. Fetch labeled data from last week              │
│    2. Combine with historical labels                 │
│    3. Retrain XGBoost model                          │
│    4. Offline evaluation (AUC, Precision, Recall)    │
│    5. If metrics good → deploy new model             │
│    6. Monitor for 24 hours                           │
│                                                       │
│  Result: Model continuously improves\!                 │
│                                                       │
└───────────────────────────────────────────────────────┘
```

---

## Metrics & Monitoring

### Model Performance
```
Precision: 85% (of flagged fraud, 85% actually fraud)
Recall: 78% (caught 78% of all fraud)
False Positive Rate: 2.1% (acceptable: <3%)
True Positive Rate: 78%
AUC: 0.92 (excellent\!)

Latency:
  • p50: 28ms ✅
  • p95: 45ms ✅
  • p99: 62ms ⚠️ (target: <50ms)
```

### Business Impact
```
Fraud prevented: $2.4M/month
False positives: 420/month (legitimate users blocked)
Customer complaints: 15/month
Manual reviews required: 800/month

Cost savings: $2.4M - $50K (operations) = $2.35M/month ROI
```

---

## Interview Q&A

**Q: How do you balance false positives vs false negatives?**
```
Threshold tuning:
  • High threshold (0.9): Fewer false positives, more fraud slips through
  • Low threshold (0.5): Catch more fraud, but annoy legitimate users

Solution: Three-tier system
  • 0.8-1.0: BLOCK (high confidence)
  • 0.5-0.8: VERIFY (ask for 2FA, not block)
  • 0.0-0.5: ALLOW (low risk)

Monitor customer complaints, adjust thresholds weekly.
```

**Q: What if fraud model fails?**
```
Fallback to rule-based system:
  • booking_velocity > 10/hour → BLOCK
  • failed_payments > 5/day → BLOCK
  • VPN + disposable email → VERIFY
  • Known blacklist IPs → BLOCK

Graceful degradation: System still works, just less accurate.
```

**Q: How do you handle new fraud patterns?**
```
1. Anomaly detection (Isolation Forest) catches unknown patterns
2. Weekly retraining adapts to new fraud types
3. Feature engineering: Add new features as fraud evolves
4. Human analysts identify patterns → add to model
```

---

**ROI: $2.35M/month fraud prevention**
**Implementation: 8-10 weeks**
**Team: 2 ML engineers + 1 fraud analyst** 🛡️
