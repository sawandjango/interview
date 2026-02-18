# AI-Powered Search & Recommendation Engine

## Overview

This document covers the AI/ML-powered search and recommendation system for the movie booking platform, including natural language search, semantic understanding, and personalized recommendations.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│              AI SEARCH & RECOMMENDATION SYSTEM                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Query: "Show me action movies like John Wick tonight"    │
│       ↓                                                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Search Service                                           │  │
│  │  ┌────────────────┐  ┌────────────────┐                 │  │
│  │  │ Traditional    │  │ AI-Powered     │                 │  │
│  │  │ Search         │  │ Search (NLP)   │                 │  │
│  │  │                │  │                │                 │  │
│  │  │ • Elasticsearch│  │ • Semantic     │                 │  │
│  │  │ • Keyword match│  │   understanding│                 │  │
│  │  │ • Filters      │  │ • Entity       │                 │  │
│  │  │ • Autocomplete │  │   extraction   │                 │  │
│  │  └────────────────┘  │ • Intent       │                 │  │
│  │                      │   recognition  │                 │  │
│  │                      └────────────────┘                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│       ↓                         ↓                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Recommendation Engine                                    │  │
│  │                                                           │  │
│  │  ┌─────────────────┐  ┌─────────────────┐              │  │
│  │  │ Collaborative   │  │ Content-Based   │              │  │
│  │  │ Filtering       │  │ Filtering       │              │  │
│  │  │                 │  │                 │              │  │
│  │  │ • User-User     │  │ • Movie metadata│              │  │
│  │  │ • Item-Item     │  │ • Genre, cast   │              │  │
│  │  │ • Matrix Factor │  │ • Plot keywords │              │  │
│  │  └─────────────────┘  └─────────────────┘              │  │
│  │           ↓                    ↓                         │  │
│  │  ┌──────────────────────────────────────────┐           │  │
│  │  │ Hybrid Recommendation Model              │           │  │
│  │  │ (Neural Collaborative Filtering)         │           │  │
│  │  │                                           │           │  │
│  │  │ • Deep learning model                     │           │  │
│  │  │ • User embeddings (256D)                 │           │  │
│  │  │ • Movie embeddings (256D)                │           │  │
│  │  │ • Context features                        │           │  │
│  │  └──────────────────────────────────────────┘           │  │
│  └──────────────────────────────────────────────────────────┘  │
│       ↓                                                         │
│  Personalized Results + Ranking                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component 1: AI-Powered Search

### 1.1 Natural Language Understanding

**User Query Examples:**
```
❌ Traditional search struggles with:
  • "Show me something like Inception"
  • "Action movies similar to John Wick tonight"
  • "Funny movies for kids near downtown"

✅ AI-powered search understands:
  • Intent: search, filter, recommendation
  • Entities: genre, movie name, location, time
  • Similarity: "like", "similar to"
  • Context: "tonight", "near me", "for kids"
```

### 1.2 Implementation

**Architecture:**
```python
# Pseudocode for AI Search Pipeline

def ai_powered_search(query, user_context):
    # Step 1: Query understanding with NLP
    intent, entities = extract_intent_entities(query)
    # Uses: spaCy or transformer model (BERT)

    # Step 2: Semantic search
    query_embedding = encode_query(query)              # 768D vector
    similar_movies = vector_db.search(query_embedding, top_k=100)

    # Step 3: Apply extracted filters
    filtered = apply_filters(similar_movies, entities)

    # Step 4: Personalized ranking
    ranked = recommendation_model.rerank(
        movies=filtered,
        user_id=user_context.user_id,
        context=user_context
    )

    # Step 5: Return top results
    return ranked[:10]
```

**NLP Pipeline:**
```
User Query: "Show me action movies like John Wick tonight"
    ↓
┌─────────────────────────────────────────────────────────┐
│ Step 1: Intent Classification                          │
│   Model: BERT fine-tuned on movie queries             │
│   Output: Intent = "search_similar"                    │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│ Step 2: Entity Extraction (NER)                        │
│   Model: spaCy or custom NER                           │
│   Output:                                               │
│     - Genre: "action"                                   │
│     - Reference Movie: "John Wick"                     │
│     - Time: "tonight"                                   │
│     - Location: user's current location                │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│ Step 3: Query Expansion                                 │
│   Expand "John Wick" to similar movies:                │
│     - Keanu Reeves films                               │
│     - Gun-fu action movies                             │
│     - Neo-noir thrillers                               │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│ Step 4: Semantic Search                                 │
│   Vector DB query with combined constraints             │
│   Returns: Top 100 candidate movies                     │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│ Step 5: Personalized Reranking                         │
│   ML model considers user history                       │
│   Final output: Top 10 personalized results            │
└─────────────────────────────────────────────────────────┘
```

### 1.3 Technical Stack

```
┌──────────────────────────────────────────────────────┐
│  NLP Models:                                         │
│    • Query Understanding: BERT / RoBERTa             │
│    • Entity Extraction: spaCy / Custom NER           │
│    • Semantic Encoding: Sentence-BERT                │
│                                                      │
│  Vector Database:                                    │
│    • Pinecone / Weaviate / Milvus                    │
│    • Movie embeddings: 768D                          │
│    • Fast ANN search (<50ms)                         │
│                                                      │
│  Traditional Search:                                 │
│    • Elasticsearch for keyword matching              │
│    • BM25 scoring                                    │
│    • Filters, facets, aggregations                   │
│                                                      │
│  Hybrid Approach:                                    │
│    • Combine semantic + keyword scores               │
│    • Score = 0.6 * semantic + 0.4 * keyword          │
└──────────────────────────────────────────────────────┘
```

---

## Component 2: Recommendation Engine

### 2.1 Multiple Recommendation Strategies

**1. Collaborative Filtering (User-Based)**
```
Concept: "Users similar to you also liked..."

Algorithm: Matrix Factorization (SVD)
  • User-Movie rating matrix: R (sparse)
  • Factorize: R ≈ U × V^T
  • U: user embeddings (100K users × 128D)
  • V: movie embeddings (5K movies × 128D)

Prediction:
  rating(user_i, movie_j) = U[i] · V[j]

Pros: Discovers hidden patterns, serendipity
Cons: Cold start problem for new users
```

**2. Content-Based Filtering**
```
Concept: "You liked X, here's similar Y"

Features per movie:
  • Genre: [action, thriller, drama]
  • Cast: [actor1, actor2, ...]
  • Director: name
  • Keywords: [revenge, assassin, gun-fu, ...]
  • Plot embedding: 768D vector from BERT

Similarity:
  sim(movie_i, movie_j) = cosine(features_i, features_j)

Pros: No cold start, explainable
Cons: Limited diversity, filter bubble
```

**3. Neural Collaborative Filtering (NCF)**
```
Deep Learning Approach (BEST!)

Architecture:
┌───────────────────────────────────────────────────┐
│  Input Layer                                      │
│    • user_id → Embedding(100K, 256)              │
│    • movie_id → Embedding(5K, 256)               │
│    • context features (time, device, ...)        │
└───────────────────────────────────────────────────┘
         ↓
┌───────────────────────────────────────────────────┐
│  Hidden Layers                                    │
│    • Dense(512, ReLU)                             │
│    • BatchNorm + Dropout(0.3)                     │
│    • Dense(256, ReLU)                             │
│    • BatchNorm + Dropout(0.3)                     │
│    • Dense(128, ReLU)                             │
└───────────────────────────────────────────────────┘
         ↓
┌───────────────────────────────────────────────────┐
│  Output Layer                                     │
│    • Dense(1, Sigmoid)                            │
│    • Predicted rating: [0, 1]                     │
└───────────────────────────────────────────────────┘

Training:
  • Loss: Binary Cross-Entropy (implicit feedback)
  • Optimizer: Adam
  • Batch size: 1024
  • Negative sampling: 4 negatives per positive

Performance:
  • Training: 1M examples/sec on V100 GPU
  • Inference: <5ms per user
```

### 2.2 Two-Stage Recommendation Pipeline

**Why Two-Stage?**
- Can't run expensive model on entire catalog (5K movies)
- Need fast candidate generation + precise ranking

```
Stage 1: CANDIDATE GENERATION (Fast, Broad)
═══════════════════════════════════════════════════
Goal: Reduce 5K movies → Top 100 candidates
Method: Vector similarity search (ANN)
Latency: <50ms

user_embedding = get_user_embedding(user_id)         # 256D
candidates = vector_db.search(
    query=user_embedding,
    top_k=100,
    filters={"in_theaters": True, "city": user_city}
)

Cost: Cheap (CPU-based ANN)
Recall@100: ~95% (covers most relevant movies)


Stage 2: PRECISE RANKING (Slower, Accurate)
═══════════════════════════════════════════════════
Goal: Rank top 100 → Final top 10
Method: Neural network with rich features
Latency: <100ms

for movie in candidates:
    features = extract_features(user, movie, context)
    score = ncf_model.predict(features)

top_10 = sort(candidates, by=score, descending=True)[:10]

Cost: Moderate (GPU inference)
NDCG@10: 0.85 (very accurate ranking)


Total Latency: 50ms + 100ms = 150ms ✅
```

### 2.3 Cold Start Problem Solutions

**Problem:** New user with no history

**Solutions:**

**1. Popularity-Based Fallback**
```python
if user.num_ratings == 0:
    return top_movies_by_popularity(user.location)
```

**2. Demographic Signals**
```python
if user.age and user.gender:
    similar_users = find_users_by_demographics(user.age, user.gender)
    return collaborative_filter(similar_users)
```

**3. Quick Onboarding Quiz**
```
"Help us personalize your experience!"
  • Select your favorite genres: [Action, Comedy, Drama, ...]
  • Rate these popular movies: [Avengers, Inception, ...]

After 3-5 ratings → cold start solved!
```

**4. Content-Based (No History Needed)**
```python
# User selected genre: "Action"
return content_based_filter(
    genre="action",
    sort_by="popularity",
    limit=10
)
```

### 2.4 Real-Time vs Batch Recommendations

**Batch Recommendations (Offline)**
```
Frequency: Daily (every night at 2 AM)
Process:
  1. Train collaborative filtering on all historical data
  2. Generate top-50 recommendations for ALL users
  3. Store in Redis: user_id → [movie1, movie2, ...]

Pros:
  • Fast serving (<1ms, just cache lookup)
  • Can use expensive models
  • Consistent results

Cons:
  • Stale (up to 24 hours old)
  • Doesn't adapt to recent actions

Use case: Homepage recommendations
```

**Real-Time Recommendations (Online)**
```
Trigger: Every user action (click, search, booking)
Process:
  1. Fetch user's recent actions (last 1 hour)
  2. Update user embedding in real-time
  3. Re-rank batch recommendations with new signal

Latency: <100ms

Pros:
  • Fresh, adapts immediately
  • Captures trending content

Cons:
  • Higher compute cost
  • More complex infrastructure

Use case: "Because you just booked...", trending movies
```

**Hybrid Approach (BEST!):**
```python
def get_recommendations(user_id):
    # Get batch recommendations (cached)
    batch_recs = redis.get(f"recs:batch:{user_id}")     # Fast!

    # Get real-time signals (fresh)
    recent_actions = get_recent_actions(user_id, hours=1)

    if recent_actions:
        # Re-rank with real-time signal
        scores = model.predict_batch(
            movies=batch_recs,
            user_embedding=get_user_embedding(user_id),
            recent_actions=recent_actions
        )
        return rerank(batch_recs, scores)
    else:
        # Just return batch recs
        return batch_recs
```

### 2.5 Diversity & Exploration

**Problem:** Recommendations too similar (filter bubble)

**Solution: Diversification Strategies**

**1. Genre Diversity**
```python
# Ensure at least 3 different genres in top-10
top_10 = []
genres_seen = set()

for movie in ranked_movies:
    if len(genres_seen) < 3 or movie.genre in genres_seen:
        top_10.append(movie)
        genres_seen.add(movie.genre)
    if len(top_10) == 10:
        break
```

**2. Exploration vs Exploitation (ε-greedy)**
```python
epsilon = 0.2  # 20% exploration

if random() < epsilon:
    # EXPLORE: Show unexpected/new movies
    return sample_random_popular_movies(n=10)
else:
    # EXPLOIT: Show personalized recommendations
    return ncf_model.recommend(user_id, n=10)
```

**3. Thompson Sampling (MAB)**
```python
# Multi-armed bandit for A/B testing recommendations

for movie in candidates:
    # Sample from posterior distribution
    estimated_ctr = beta_distribution(
        alpha=movie.clicks + 1,
        beta=movie.impressions - movie.clicks + 1
    ).sample()

# Show movies with highest sampled CTR
```

---

## Feature Engineering

### User Features
```python
user_features = {
    # Demographic
    "age": user.age,
    "gender": user.gender,
    "location_city": user.city,

    # Behavioral
    "total_bookings": user.booking_count,
    "avg_rating": user.avg_rating,
    "favorite_genres": user.top_3_genres,
    "booking_frequency": bookings_per_month,

    # Temporal
    "preferred_day": most_common_booking_day,
    "preferred_time": most_common_booking_time,

    # Embedding
    "user_embedding": user_embedding_256d,  # From NCF model
}
```

### Movie Features
```python
movie_features = {
    # Metadata
    "title": movie.title,
    "genres": movie.genres,
    "cast": movie.cast[:5],  # Top 5 actors
    "director": movie.director,
    "release_year": movie.year,
    "runtime_minutes": movie.runtime,

    # Popularity
    "imdb_rating": movie.imdb_rating,
    "rt_score": movie.rotten_tomatoes,
    "total_bookings": movie.booking_count,
    "trending_score": bookings_last_7_days,

    # Content
    "plot_summary": movie.plot,
    "keywords": movie.keywords,  # ["revenge", "assassin", ...]

    # Embedding
    "movie_embedding": movie_embedding_256d,  # From NCF model
    "plot_embedding": bert_encode(movie.plot),  # 768D
}
```

### Context Features
```python
context_features = {
    # Temporal
    "day_of_week": current_day,  # Mon-Sun
    "time_of_day": current_hour,  # 0-23
    "is_weekend": is_weekend,
    "is_holiday": is_holiday,

    # Session
    "session_duration": minutes_on_site,
    "pages_viewed": page_count,
    "searches_made": search_count,

    # Device
    "device_type": "mobile" | "desktop",
    "browser": user.browser,
}
```

---

## Evaluation Metrics

### Offline Metrics (Model Training)
```
Ranking Metrics:
  • Precision@K: What % of top-K are relevant?
    P@10 = (# relevant in top-10) / 10
    Target: >0.6

  • Recall@K: What % of relevant items in top-K?
    R@10 = (# relevant in top-10) / (total relevant)
    Target: >0.4

  • NDCG@K: Normalized Discounted Cumulative Gain
    Considers position (top results weighted more)
    Target: >0.75

  • Hit Rate@K: Did user interact with ANY in top-K?
    Target: >0.8

Classification Metrics (Implicit Feedback):
  • AUC-ROC: 0.82 (target: >0.80)
  • Log Loss: 0.34 (target: <0.4)
```

### Online Metrics (A/B Testing)
```
User Engagement:
  • Click-Through Rate (CTR): 6.2% (baseline: 5%)
  • Conversion Rate: 18% (clicked → booked)
  • Time to booking: 4.2 min (faster is better)

Business Metrics:
  • Bookings per user: 2.1 (baseline: 1.8)
  • Revenue per user: $42 (baseline: $36)
  • User retention: 78% return within 30 days

Quality Metrics:
  • Diversity score: 0.72 (how diverse are recs?)
  • Coverage: 85% (% of catalog recommended)
  • Novelty: 0.65 (how unexpected are recs?)
```

---

## Interview Questions & Answers

**Q1: How do you handle the cold start problem?**
```
Multi-pronged approach:
1. New users: Popularity-based + quick onboarding quiz
2. New movies: Content-based (metadata, plot similarity)
3. Fallback chain:
   - Try personalized (if >10 ratings)
   - Try demographic-based (if <10 ratings)
   - Use popularity (if new user)
```

**Q2: Explain your two-stage ranking system.**
```
Stage 1: Candidate Generation (ANN search)
  • Input: User embedding (256D)
  • Output: Top 100 candidates
  • Latency: <50ms
  • Recall@100: 95%

Stage 2: Precise Ranking (Neural network)
  • Input: Rich features (user + movie + context)
  • Output: Top 10 recommendations
  • Latency: <100ms
  • NDCG@10: 0.85

Why? Can't afford to run expensive model on 5K movies.
Two-stage balances speed + accuracy.
```

**Q3: How do you ensure recommendation diversity?**
```
1. Genre diversity: Force 3+ genres in top-10
2. Exploration (ε-greedy): 20% random popular movies
3. MMR (Maximal Marginal Relevance):
   - Balance relevance + dissimilarity
4. Position-aware: Don't cluster similar items together
```

**Q4: Real-time vs batch recommendations?**
```
Hybrid approach:
- Batch (daily): Generate top-50 for all users (cached)
- Real-time: Re-rank based on recent actions
- Cost-effective + fresh results
- Latency: <100ms (cache lookup + reranking)
```

**Q5: How do you measure success?**
```
Offline: NDCG@10, Precision@10, AUC
Online: CTR (+1.2%), Conversion (+15%), Revenue (+17%)
A/B test: 2 weeks, 10K users per variant
```

---

## Implementation Checklist

- [x] Vector database setup (Pinecone/Milvus)
- [x] Movie embedding generation (BERT)
- [x] NCF model training pipeline
- [x] Two-stage ranking system
- [x] Cold start handling
- [x] Real-time feature computation
- [x] A/B testing framework
- [x] Offline evaluation metrics
- [x] Online monitoring dashboard
- [x] Model retraining automation

---

**Time to implement: 4-6 weeks**
**Team size: 2-3 ML engineers + 1 backend engineer**
**Complexity: High**
**Impact: +15-20% booking conversion** 🚀
