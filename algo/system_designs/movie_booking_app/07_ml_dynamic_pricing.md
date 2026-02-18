# ML-Based Dynamic Pricing System

## Overview

Dynamic pricing uses machine learning to optimize ticket prices in real-time based on demand, occupancy, time, and other factors to maximize revenue while maintaining customer satisfaction.

---

## Pricing Strategy

### Traditional Pricing (❌ Static)
```
Base price: $15
Weekend: +20% → $18
Evening show: +15% → $17.25
IMAX: +$5 → $20

Problems:
  • Doesn't respond to actual demand
  • Misses revenue opportunities (high demand)
  • Leaves seats empty (low demand)
  • One-size-fits-all approach
```

### Dynamic Pricing (✅ ML-Based)
```
Factors considered:
  ✓ Current occupancy rate
  ✓ Historical demand patterns
  ✓ Time until showtime
  ✓ Competitor pricing
  ✓ Weather forecast
  ✓ Special events nearby
  ✓ Movie popularity
  ✓ User willingness to pay

Result: Optimal price that maximizes revenue
```

---

## ML Model Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  DYNAMIC PRICING PIPELINE                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Input Features (Feature Store)                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Show Features:                                       │  │
│  │    • current_occupancy: 45%                          │  │
│  │    • time_to_show: 6 hours                           │  │
│  │    • theater_capacity: 200 seats                     │  │
│  │    • screen_type: "IMAX" | "Regular" | "4DX"        │  │
│  │                                                       │  │
│  │  Temporal Features:                                   │  │
│  │    • day_of_week: Monday-Sunday                      │  │
│  │    • hour_of_day: 0-23                               │  │
│  │    • is_weekend: boolean                             │  │
│  │    • is_holiday: boolean                             │  │
│  │    • month: 1-12                                     │  │
│  │                                                       │  │
│  │  Movie Features:                                      │  │
│  │    • popularity_score: 0-100                         │  │
│  │    • imdb_rating: 1-10                               │  │
│  │    • genre: action, comedy, etc.                     │  │
│  │    • is_opening_weekend: boolean                     │  │
│  │    • days_since_release: integer                     │  │
│  │                                                       │  │
│  │  External Features:                                   │  │
│  │    • weather: sunny, rainy, snowy                    │  │
│  │    • temperature: degrees                            │  │
│  │    • competitor_avg_price: $15-$25                   │  │
│  │    • nearby_events: boolean                          │  │
│  │                                                       │  │
│  │  Historical Features:                                 │  │
│  │    • same_show_last_week_price: $18                  │  │
│  │    • same_time_avg_occupancy: 65%                    │  │
│  │    • similar_movies_avg_price: $17                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  ML Model (XGBoost / Neural Network)                 │  │
│  │                                                       │  │
│  │  Model Type: Gradient Boosting (XGBoost)             │  │
│  │  Input: 20-30 features                               │  │
│  │  Output: Predicted optimal price                     │  │
│  │                                                       │  │
│  │  Training:                                            │  │
│  │    • Historical data: 6 months of bookings          │  │
│  │    • Target: Revenue per seat                        │  │
│  │    • Loss: Custom revenue loss function             │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Business Constraints                                 │  │
│  │                                                       │  │
│  │  • min_price = base_price * 0.7                      │  │
│  │  • max_price = base_price * 2.0                      │  │
│  │  • max_change_per_hour = 10%                         │  │
│  │  • competitor_price_threshold: ±15%                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                   │
│  Final Optimized Price: $17.50                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Model Training

### Data Collection
```sql
-- Training dataset query
SELECT
    s.id as show_id,
    s.datetime as show_datetime,
    s.theater_capacity,
    s.screen_type,
    m.title,
    m.genre,
    m.popularity_score,
    m.release_date,
    -- Aggregated booking data
    COUNT(b.id) as total_bookings,
    SUM(b.price) as total_revenue,
    AVG(b.price) as avg_price,
    -- Time-series features
    COUNT(CASE WHEN b.booked_at < show_datetime - INTERVAL '24 hours'
          THEN 1 END) as bookings_24h_before,
    COUNT(CASE WHEN b.booked_at < show_datetime - INTERVAL '1 hour'
          THEN 1 END) as bookings_1h_before,
    -- Target variable
    SUM(b.price) / s.theater_capacity as revenue_per_seat
FROM shows s
JOIN movies m ON s.movie_id = m.id
LEFT JOIN bookings b ON s.id = b.show_id
WHERE s.datetime BETWEEN '2024-01-01' AND '2024-06-30'
GROUP BY s.id, m.id
```

### Feature Engineering
```python
def engineer_features(show_data):
    features = {}

    # Occupancy rate
    features['occupancy_rate'] = show_data['bookings'] / show_data['capacity']

    # Time to show (hours)
    features['time_to_show'] = (
        show_data['show_datetime'] - datetime.now()
    ).total_seconds() / 3600

    # Temporal features
    dt = show_data['show_datetime']
    features['day_of_week'] = dt.weekday()  # 0-6
    features['hour_of_day'] = dt.hour  # 0-23
    features['is_weekend'] = 1 if dt.weekday() >= 5 else 0
    features['is_evening'] = 1 if 18 <= dt.hour <= 22 else 0

    # Movie age
    features['days_since_release'] = (
        datetime.now() - show_data['release_date']
    ).days

    # Velocity features
    features['booking_velocity'] = (
        show_data['bookings_last_hour'] / 1.0  # Bookings per hour
    )

    # Categorical encoding
    features['screen_type_imax'] = 1 if show_data['screen_type'] == 'IMAX' else 0
    features['genre_action'] = 1 if 'action' in show_data['genre'] else 0

    return features
```

### Model Training (XGBoost)
```python
import xgboost as xgb

# Load training data
X_train, y_train = load_training_data()  # Features, revenue_per_seat

# XGBoost parameters
params = {
    'objective': 'reg:squarederror',
    'max_depth': 6,
    'learning_rate': 0.05,
    'n_estimators': 500,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'reg_alpha': 0.1,  # L1 regularization
    'reg_lambda': 1.0,  # L2 regularization
}

# Train model
model = xgb.XGBRegressor(**params)
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    early_stopping_rounds=50,
    verbose=10
)

# Save model
model.save_model('pricing_model_v1.json')
```

### Custom Loss Function (Revenue Optimization)
```python
def revenue_loss(y_true, y_pred, bookings, price):
    """
    Custom loss that considers:
    - Higher price → more revenue per booking
    - But higher price → fewer bookings (price elasticity)
    """
    # Predicted revenue = predicted_price * predicted_bookings
    predicted_bookings = bookings * elasticity_function(price)
    predicted_revenue = y_pred * predicted_bookings

    # True revenue
    true_revenue = y_true * bookings

    # Loss = MSE on revenue
    return (true_revenue - predicted_revenue) ** 2
```

---

## Real-Time Pricing Updates

### Batch Mode (Every 10 minutes)
```python
def batch_update_prices():
    """
    Updates prices for all upcoming shows
    Runs every 10 minutes via cron job
    """
    # Get all shows in next 7 days
    shows = db.query("""
        SELECT * FROM shows
        WHERE datetime BETWEEN NOW() AND NOW() + INTERVAL '7 days'
        AND datetime > NOW()
    """)

    updated_count = 0

    for show in shows:
        # Extract features
        features = feature_store.get_features(show.id)

        # Predict optimal price
        predicted_price = pricing_model.predict([features])[0]

        # Apply business constraints
        final_price = apply_constraints(
            predicted_price,
            show.base_price,
            show.current_price
        )

        # Update if price changed significantly
        if abs(final_price - show.current_price) > 0.50:  # $0.50 threshold
            db.execute("""
                UPDATE shows
                SET current_price = %s, updated_at = NOW()
                WHERE id = %s
            """, (final_price, show.id))

            # Invalidate cache
            cache.delete(f"show:{show.id}:price")

            # Publish event
            kafka.produce('price.updated', {
                'show_id': show.id,
                'old_price': show.current_price,
                'new_price': final_price,
                'reason': 'ml_prediction'
            })

            updated_count += 1

    logger.info(f"Updated {updated_count} show prices")
```

### Event-Driven Updates (Real-Time)
```python
# When user books seats → trigger price update
@event_listener('booking.confirmed')
def on_booking_confirmed(event):
    show_id = event['show_id']

    # Recompute occupancy
    occupancy = compute_occupancy(show_id)

    # If occupancy crossed threshold, update price
    if occupancy > 0.7:  # 70% full
        # Trigger immediate price update
        update_show_price(show_id, reason='high_demand')
```

---

## Price Elasticity Modeling

**Concept:** How does demand change with price?

```
Price Elasticity = % change in demand / % change in price

Example:
  • Price increases 10% ($15 → $16.50)
  • Demand decreases 15% (100 bookings → 85 bookings)
  • Elasticity = -15% / 10% = -1.5 (elastic)
```

### Implementation
```python
def estimate_elasticity(movie_id, theater_id):
    """
    Estimate price elasticity from historical data
    """
    # Get historical shows with price variations
    data = db.query("""
        SELECT price, COUNT(*) as bookings
        FROM bookings b
        JOIN shows s ON b.show_id = s.id
        WHERE s.movie_id = %s
        AND s.theater_id = %s
        GROUP BY price
        ORDER BY price
    """, (movie_id, theater_id))

    # Fit demand curve: bookings = a * price^b
    # Log transform: log(bookings) = log(a) + b * log(price)
    # Elasticity = b

    prices = [row['price'] for row in data]
    bookings = [row['bookings'] for row in data]

    # Linear regression on log-log scale
    model = LinearRegression()
    model.fit(
        np.log(prices).reshape(-1, 1),
        np.log(bookings)
    )

    elasticity = model.coef_[0]  # slope = elasticity
    return elasticity
```

---

## A/B Testing Framework

```
┌───────────────────────────────────────────────────────┐
│  A/B Test: ML Pricing vs Rule-Based Pricing          │
├───────────────────────────────────────────────────────┤
│                                                       │
│  Control Group (50% of shows):                        │
│    • Rule-based pricing                              │
│    • Base price + simple rules                       │
│    • Weekend: +20%, Evening: +15%                    │
│                                                       │
│  Treatment Group (50% of shows):                      │
│    • ML-based dynamic pricing                        │
│    • XGBoost model predictions                       │
│    • Updates every 10 minutes                        │
│                                                       │
│  Metrics:                                             │
│    Primary: Revenue per seat                         │
│    Secondary: Occupancy rate, booking velocity       │
│                                                       │
│  Duration: 4 weeks                                    │
│  Sample size: 10K shows                              │
│  Statistical significance: p < 0.05                  │
│                                                       │
│  Results:                                             │
│    • Revenue per seat: +12% (ML wins!)              │
│    • Occupancy rate: +8%                            │
│    • Customer complaints: -5%                        │
│                                                       │
└───────────────────────────────────────────────────────┘
```

### Implementation
```python
def assign_pricing_strategy(show_id):
    """
    Randomly assign show to control or treatment
    """
    # Hash-based assignment (consistent)
    hash_val = hashlib.md5(str(show_id).encode()).hexdigest()
    variant = int(hash_val, 16) % 2  # 0 or 1

    if variant == 0:
        return 'control'  # Rule-based
    else:
        return 'treatment'  # ML-based

def compute_price(show):
    variant = assign_pricing_strategy(show.id)

    if variant == 'control':
        # Rule-based pricing
        price = show.base_price
        if show.is_weekend:
            price *= 1.2
        if show.is_evening:
            price *= 1.15
        return price
    else:
        # ML-based pricing
        features = extract_features(show)
        return pricing_model.predict([features])[0]
```

---

## Business Constraints

```python
def apply_constraints(predicted_price, base_price, current_price):
    """
    Apply business rules to ML predictions
    """
    # Constraint 1: Min/Max bounds
    min_price = base_price * 0.7  # No lower than 70% of base
    max_price = base_price * 2.0  # No higher than 200% of base
    price = clip(predicted_price, min_price, max_price)

    # Constraint 2: Max change per update (avoid shocking customers)
    max_change = current_price * 0.10  # 10% max change
    if abs(price - current_price) > max_change:
        if price > current_price:
            price = current_price + max_change
        else:
            price = current_price - max_change

    # Constraint 3: Competitor pricing (stay competitive)
    competitor_avg = get_competitor_avg_price()
    if price > competitor_avg * 1.15:  # Don't exceed by >15%
        price = competitor_avg * 1.15

    # Constraint 4: Round to nearest $0.50
    price = round(price * 2) / 2

    return price
```

---

## Monitoring & Alerting

### Key Metrics
```
Model Performance:
  • MAPE (Mean Absolute Percentage Error): 8.2% (target: <10%)
  • R²: 0.78 (target: >0.75)
  • Prediction vs actual revenue correlation: 0.85

Business Metrics:
  • Average ticket price: $17.20 (baseline: $15.50)
  • Revenue per seat: $14.80 (baseline: $13.10) → +13%
  • Occupancy rate: 72% (baseline: 68%)
  • Bookings per show: 144 (baseline: 136)

Operational:
  • Price updates per hour: 600
  • Model inference latency: p95 = 25ms
  • Feature fetch latency: p95 = 15ms
```

### Alerts
```
🚨 Critical Alerts:
  • Model prediction out of bounds (>$50 or <$5)
  • Feature store lag > 10 minutes
  • Price update failures > 5% of attempts
  • Revenue per seat drops >10% week-over-week

⚠️  Warning Alerts:
  • MAPE increases >15%
  • Competitor price divergence >25%
  • Occupancy rate drops suddenly
  • Customer complaints about pricing spike
```

---

## Interview Q&A

**Q1: How do you handle surge pricing for blockbuster movies?**
```
ML model automatically detects:
  • High booking velocity
  • Low availability (seats filling fast)
  • Opening weekend signal

Applies gradual price increase:
  • Hour 1: +5%
  • Hour 2: +10%
  • Hour 3: +15%
  • Max surge: 2x base price

Monitors customer complaints, adjusts if needed.
```

**Q2: What if your ML model predicts an unrealistic price?**
```
Multiple safety mechanisms:
  1. Business constraints (min/max bounds)
  2. Rate of change limits (10% per hour)
  3. Sanity checks (if price > $100, alert!)
  4. Fallback to rule-based if model fails
  5. Human oversight dashboard for approval
```

**Q3: How do you measure success?**
```
A/B test for 4 weeks:
  • Control: Rule-based pricing
  • Treatment: ML-based pricing

Metrics:
  • Primary: Revenue per seat (+12%)
  • Secondary: Occupancy (+8%), Customer satisfaction (-2% complaints)

Statistical significance: p < 0.01 (highly significant)
Decision: Roll out ML pricing to 100% of shows
```

**Q4: How often do you retrain the model?**
```
Frequency: Weekly
Reason: Capture seasonal trends, new movies, changing demand

Process:
  1. Fetch last 6 months of data
  2. Feature engineering
  3. Train XGBoost model
  4. Offline evaluation (MAPE, R²)
  5. Shadow mode testing (1 day)
  6. If metrics good → deploy
  7. Monitor for 24 hours

Fallback: If new model performs worse, auto-rollback
```

**Q5: How do you handle competitor pricing?**
```
Web scraping pipeline:
  • Scrape competitor sites every hour
  • Extract prices for same movies/times
  • Store in feature store

ML model uses as feature:
  • competitor_avg_price
  • competitor_min_price

Business constraint:
  • Stay within ±15% of competitor average
  • Alert if we're consistently more expensive
```

---

## Implementation Timeline

**Week 1-2:** Data collection, feature engineering
**Week 3-4:** Model training, offline evaluation
**Week 5:** A/B test infrastructure
**Week 6-9:** Run A/B test (4 weeks)
**Week 10:** Analysis, decision
**Week 11-12:** Full rollout, monitoring

**Total:** 12 weeks (3 months)
**Team:** 2 ML engineers, 1 data engineer, 1 PM
**Expected ROI:** +10-15% revenue increase 💰
