# AI/ML-Powered Movie Ticket Booking System (like AMC, BookMyShow)

This directory contains a comprehensive system design for a **next-generation movie ticket booking platform** that combines **traditional reliable architecture** for core booking with **AI/ML intelligence** for enhanced user experience. The design covers all critical aspects typically discussed in system design interviews.

## Overview

A modern movie ticket booking system with **hybrid architecture**:

### Traditional Core (Deterministic, Fast, Reliable)
- Theater and movie catalog management
- Real-time seat selection and booking
- Payment processing with rollback
- Concurrency control (prevent double booking)
- Multi-city, multi-theater operations

### AI/ML Enhancement Layer (Intelligent, Adaptive, Personalized)
- **AI-powered search** with natural language understanding
- **Smart recommendations** using collaborative filtering + deep learning
- **Dynamic pricing** with ML-based demand forecasting
- **Conversational chatbot** for customer support (LLM-powered)
- **Fraud detection** with anomaly detection models
- **Personalization engine** for tailored experiences
- **Predictive analytics** for business insights

## System Design Documents

### Core Architecture
1. **[01_high_level_architecture.md](./01_high_level_architecture.md)** - Overall system architecture and data flow (with AI/ML layer)
2. **[02_core_components.md](./02_core_components.md)** - Key services and their responsibilities
3. **[03_database_design.md](./03_database_design.md)** - Schema design and data modeling
4. **[04_seat_booking_flow.md](./04_seat_booking_flow.md)** - Critical booking flow with concurrency handling
5. **[05_payment_processing.md](./05_payment_processing.md)** - Payment integration and failure handling

### AI/ML Components
6. **[06_ai_search_recommendations.md](./06_ai_search_recommendations.md)** - AI-powered search, NLP, recommendation engine
7. **[07_ml_dynamic_pricing.md](./07_ml_dynamic_pricing.md)** - ML-based pricing optimization and demand forecasting
8. **[08_chatbot_support.md](./08_chatbot_support.md)** - LLM-powered conversational AI for customer support
9. **[09_fraud_detection.md](./09_fraud_detection.md)** - ML-based fraud detection and risk scoring
10. **[10_personalization_engine.md](./10_personalization_engine.md)** - User behavior analysis and personalization

### Infrastructure
11. **[11_caching_strategy.md](./11_caching_strategy.md)** - Multi-level caching for performance
12. **[12_scalability_reliability.md](./12_scalability_reliability.md)** - Scaling strategies and failover
13. **[13_analytics_monitoring.md](./13_analytics_monitoring.md)** - Business metrics and system health

## Scale Estimates (Interview Reference)

### Traffic Estimates
- **Daily Active Users**: 10M
- **Peak booking hours**: 6 PM - 11 PM
- **Concurrent users during peak**: 500K
- **Bookings per day**: 2M
- **Average booking time**: 5 minutes
- **Read:Write ratio**: 100:1 (browsing vs booking)

### Storage Estimates
- **Movies**: ~2,000 active movies
- **Theaters**: ~5,000 theaters (US market)
- **Screens per theater**: 10 average
- **Shows per day per screen**: 6
- **Historical bookings**: 5 years = ~3.6B bookings
- **Total storage**: ~5-10 TB

### QPS Estimates
- **Search/Browse**: 50K QPS (peak)
- **Seat availability checks**: 20K QPS (peak)
- **Booking requests**: 2K QPS (peak)
- **Payment processing**: 1K QPS (peak)

## Key Design Challenges

### 1. Concurrency Control (MOST CRITICAL!)
**Problem**: Multiple users trying to book the same seat simultaneously

**Solutions**:
- Pessimistic locking with row-level locks
- Optimistic locking with version numbers
- Distributed locks (Redis/Zookeeper)
- Seat hold/reservation with TTL
- Idempotency keys for retry safety

### 2. High Availability
**Problem**: System must be available 99.99% of the time

**Solutions**:
- Multi-region deployment
- Read replicas for databases
- Circuit breakers for external services
- Graceful degradation
- Automated failover

### 3. Payment Reliability
**Problem**: Handle payment failures, timeouts, partial failures

**Solutions**:
- Two-phase commit pattern
- Saga pattern for distributed transactions
- Payment status polling
- Webhook callbacks
- Automatic refunds

### 4. Real-time Updates
**Problem**: Show seat availability in real-time to all users

**Solutions**:
- WebSocket connections for live updates
- Server-Sent Events (SSE)
- Short polling with caching
- Event-driven architecture

## Technology Stack (Example)

### Backend (Traditional Services)
- **API Gateway**: Kong / AWS API Gateway
- **Services**: Java/Spring Boot or Node.js/Express
- **Orchestration**: Kubernetes (EKS/GKE)
- **Service Mesh**: Istio (optional)

### AI/ML Infrastructure (NEW!)
- **ML Platform**: SageMaker / Vertex AI / Azure ML
- **Model Serving**: TensorFlow Serving / TorchServe / Seldon Core
- **Feature Store**: Feast / Tecton / Hopsworks
- **LLM Provider**: OpenAI API / Anthropic Claude / Azure OpenAI
- **Vector Database**: Pinecone / Weaviate / Milvus (for embeddings)
- **ML Orchestration**: Kubeflow / MLflow / Airflow
- **Real-time ML**: Apache Flink / Spark Streaming
- **Model Monitoring**: Evidently AI / Arize / WhyLabs

### Databases
- **Primary DB**: PostgreSQL (ACID compliance for bookings)
- **Read Replicas**: PostgreSQL replicas for queries
- **Cache**: Redis (seat availability, session data)
- **Search**: Elasticsearch (movie search, autocomplete)
- **Graph DB**: Neo4j (user relationships, social recommendations)
- **Time-series DB**: InfluxDB / TimescaleDB (user behavior tracking)
- **Analytics**: ClickHouse / BigQuery

### Message Queue
- **Queue**: Kafka (event streaming)
- **Task Queue**: RabbitMQ / AWS SQS (notifications, emails)

### Storage
- **Object Storage**: S3 (movie posters, images)
- **CDN**: CloudFront / Cloudflare (static assets)

### External Services
- **Payment Gateway**: Stripe / PayPal / Square
- **SMS**: Twilio
- **Email**: SendGrid / AWS SES
- **Push Notifications**: Firebase Cloud Messaging

### Monitoring & Observability
- **Metrics**: Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Tracing**: Jaeger / Zipkin
- **APM**: Datadog / New Relic
- **Alerts**: PagerDuty

## Interview Flow Guide

### Step 1: Requirements Clarification (5 mins)
**Functional Requirements (Traditional)**:
- Users can search movies by city, theater, time
- Users can view seat layout and availability
- Users can select seats and make payment
- Users receive booking confirmation
- Users can cancel bookings with refund
- Theater admins can add/update shows

**Functional Requirements (AI/ML-Enhanced)**:
- Users get personalized movie recommendations
- Natural language search ("action movies near me tonight")
- AI chatbot for customer support
- Dynamic pricing based on demand
- Fraud detection for suspicious bookings
- Predictive analytics for theater operators

**Non-Functional Requirements**:
- High availability (99.99%)
- Low latency (<200ms for seat availability, <1s for AI features)
- Strong consistency for bookings (no double booking)
- Eventually consistent for other operations
- Scalable to 10M DAU
- Secure payment processing
- ML model latency <100ms (for real-time features)

### Step 2: Back-of-Envelope Calculations (5 mins)
- Calculate QPS, storage, bandwidth
- Identify bottlenecks (booking service, database)

### Step 3: High-Level Design (10 mins)
- Draw client → API Gateway → Services → Databases
- Identify core services (Movie, Theater, Booking, Payment, Notification)
- **Add AI/ML layer** (Recommendation, Chatbot, Pricing, Fraud Detection)
- Show data flow for key operations
- Explain why hybrid architecture (traditional + AI/ML)

### Step 4: Deep Dive (25 mins)
Focus on these areas based on interviewer interest:

**A. Seat Booking with Concurrency Control (CRITICAL!)**
- Explain locking mechanisms
- Handle race conditions
- Timeout and cleanup strategy

**B. Database Schema**
- Tables: Users, Movies, Theaters, Shows, Seats, Bookings
- Indexing strategy
- Partitioning strategy

**C. Payment Processing**
- Two-phase booking (reserve → pay → confirm)
- Failure handling and rollback
- Idempotency

**D. AI/ML Components (NEW!)**

**D1. Recommendation Engine**
- Collaborative filtering (user-user, item-item similarity)
- Deep learning (neural collaborative filtering)
- Feature engineering (user demographics, watch history, ratings)
- Real-time vs batch predictions
- Cold start problem handling

**D2. Dynamic Pricing**
- Features: occupancy rate, time to show, historical demand, day of week
- Model: Gradient Boosting (XGBoost/LightGBM) or Neural Network
- Online learning vs batch retraining
- A/B testing for pricing strategies
- Constraints: min/max price, surge limits

**D3. AI Chatbot**
- Architecture: LLM (GPT-4/Claude) + Function calling
- Tools: search_movies(), check_availability(), get_booking_status()
- Context management for multi-turn conversations
- Fallback to human agent
- Cost optimization (caching, smaller models for simple queries)

**D4. Fraud Detection**
- Features: booking velocity, payment failures, device fingerprint, location anomalies
- Model: Isolation Forest / Autoencoder for anomaly detection
- Real-time scoring (<50ms)
- Feedback loop for model improvement
- False positive handling

**E. Scalability**
- Horizontal scaling of services
- Database sharding strategy
- Caching layers
- CDN for static content
- ML model serving at scale (multiple replicas, load balancing)

**F. Reliability**
- Multi-AZ deployment
- Database replication
- Circuit breakers
- Rate limiting
- ML model fallbacks (rule-based system if ML fails)

### Step 5: Trade-offs & Extensions (5 mins)

**Traditional System Trade-offs:**
- SQL vs NoSQL for different components
- Synchronous vs asynchronous processing
- Strong vs eventual consistency
- Pessimistic vs optimistic locking

**AI/ML Trade-offs:**
- **Online vs Batch predictions**: Real-time ML adds latency, batch is stale
- **Model complexity vs latency**: Complex models (deep learning) slower than simple models
- **Accuracy vs cost**: GPT-4 more accurate but expensive vs GPT-3.5-turbo
- **Cold start handling**: Random recommendations vs popularity-based
- **Feature freshness**: Real-time features expensive, batch features stale

**Possible Extensions:**
- Loyalty programs
- Social features (watch with friends)
- Virtual reality seat preview
- Multi-language support with AI translation
- Voice booking with speech recognition
- Accessibility features (AI-powered audio descriptions)

## Critical Interview Talking Points

### 1. Seat Booking Race Condition
```
PROBLEM: User A and User B both try to book Seat 5 at same time

SOLUTION OPTIONS:

Option 1: Database Row Lock
  BEGIN TRANSACTION
  SELECT * FROM seats WHERE id = 5 FOR UPDATE  -- Lock row
  UPDATE seats SET status = 'BOOKED', user_id = A
  COMMIT

Option 2: Optimistic Locking
  SELECT version FROM seats WHERE id = 5
  UPDATE seats SET status = 'BOOKED', version = version + 1
  WHERE id = 5 AND version = <old_version>
  -- If rows affected = 0, retry

Option 3: Distributed Lock
  Redis: SET lock:seat:5 user_A NX EX 300  -- Lock with TTL
  If success, proceed with booking
  Release lock after booking
```

### 2. Booking State Machine
```
AVAILABLE → LOCKED → PAYMENT_PENDING → CONFIRMED
    ↓          ↓            ↓
  (none)   (timeout)    (failed)
    ↓          ↓            ↓
AVAILABLE  AVAILABLE    AVAILABLE
```

### 3. Database Partitioning Strategy
```
Partition by: city_id + date
Reason: Most queries are city-specific and date-specific
Benefits: Better query performance, easier archival
```

## Common Interview Questions

### Traditional System Questions
1. **How do you prevent double booking?**
   - Discuss locking strategies, transaction isolation levels

2. **How do you handle payment failures?**
   - Timeout handling, retry logic, rollback mechanism

3. **How would you scale to 100M users?**
   - Horizontal scaling, database sharding, caching

4. **What if payment gateway is down?**
   - Circuit breaker pattern, fallback to alternative gateway

5. **How do you ensure seat availability is accurate?**
   - Real-time updates, cache invalidation, websockets

6. **How to handle flash sales (Avengers opening)?**
   - Queue-based booking, rate limiting, virtual waiting room

### AI/ML Specific Questions (NEW!)

7. **How would you implement personalized recommendations?**
   - Collaborative filtering matrix factorization
   - Neural collaborative filtering (NCF)
   - Hybrid approach: content + collaborative
   - Cold start: popularity-based fallback
   - Real-time: feature store + cached embeddings

8. **Explain dynamic pricing ML model**
   - **Features**: occupancy_rate, time_to_show, day_of_week, movie_popularity, weather, nearby_events
   - **Model**: XGBoost or Neural Network
   - **Training**: Historical booking data, revenue optimization
   - **Serving**: Batch predictions (hourly) or real-time
   - **Constraints**: min_price, max_price, max_surge_multiplier (2x)
   - **A/B testing**: Test pricing strategies before full rollout

9. **How does the AI chatbot work?**
   - **Architecture**: LLM (Claude/GPT-4) + Function calling
   - **Tools**: search_movies(), check_seats(), book_tickets(), cancel_booking()
   - **Context**: Store conversation history in Redis (TTL: 30 min)
   - **Fallback**: If LLM fails or user requests, route to human agent
   - **Cost optimization**: Use smaller model (GPT-3.5) for simple queries, cache common questions

10. **How do you detect fraudulent bookings?**
    - **Features**: booking_velocity, failed_payments, device_fingerprint, location_anomaly, time_patterns
    - **Model**: Isolation Forest (unsupervised) or XGBoost (supervised if labeled data)
    - **Real-time scoring**: <50ms latency requirement
    - **Action**: High risk (>0.8) → block, Medium (0.5-0.8) → require verification
    - **Feedback loop**: Analysts label flagged bookings → retrain model weekly

11. **How do you handle ML model failures?**
    - **Graceful degradation**: Fallback to rule-based system
    - **Recommendations**: Fall back to popularity-based
    - **Pricing**: Use default pricing table
    - **Fraud**: Use simple threshold rules
    - **Monitoring**: Alert if model latency > 200ms or error rate > 1%

12. **How do you keep recommendations fresh?**
    - **Batch**: Retrain collaborative filtering model daily
    - **Real-time**: Update user embeddings on each interaction
    - **Feature store**: Real-time + batch features combined
    - **Online learning**: Incremental model updates for trending movies

13. **How do you measure recommendation quality?**
    - **Offline metrics**: Precision@K, Recall@K, NDCG, AUC
    - **Online metrics**: Click-through rate (CTR), Conversion rate, Revenue per user
    - **A/B testing**: Control vs treatment groups
    - **Business metrics**: Booking increase, user engagement time

## Performance Optimizations

### Traditional Optimizations
1. **Caching Layers**
   - CDN: Static assets (images, CSS, JS)
   - Redis: Seat availability, movie details
   - Application cache: Theater locations, pricing

2. **Database Optimizations**
   - Indexing on commonly queried fields
   - Read replicas for queries
   - Connection pooling
   - Query optimization

3. **API Optimizations**
   - GraphQL for flexible queries
   - Response compression
   - Pagination
   - Batch operations

### ML/AI Specific Optimizations (NEW!)

4. **Model Serving Optimizations**
   - **Model quantization**: FP32 → INT8 (4x faster, minimal accuracy loss)
   - **Batch inference**: Group predictions to utilize GPU efficiently
   - **Model caching**: Cache embeddings for frequently accessed items
   - **A/B testing infrastructure**: Shadow mode, canary deployments

5. **Feature Engineering Optimizations**
   - **Feature store**: Tecton/Feast for online + offline features
   - **Pre-computed features**: Batch compute expensive features
   - **Feature caching**: Redis cache for user/movie embeddings
   - **Sparse features**: Use hashing for categorical features

6. **LLM Cost Optimizations**
   - **Prompt caching**: Cache responses for common questions (80% hit rate)
   - **Model tiering**: GPT-3.5 for simple, GPT-4 for complex queries
   - **Streaming responses**: Better perceived performance
   - **Function calling**: Reduce token usage vs prompt engineering

7. **Recommendation System Optimizations**
   - **Approximate nearest neighbors**: FAISS/Annoy for similarity search
   - **Two-stage ranking**: Fast candidate generation → precise reranking
   - **Personalization at scale**: Pre-compute top-K for each user segment

## Security Considerations

1. **Authentication & Authorization**
   - JWT tokens for session management
   - OAuth2 for social login
   - RBAC for admin operations

2. **Payment Security**
   - PCI DSS compliance
   - Tokenization of card details
   - HTTPS/TLS for all communications
   - 3D Secure for card payments

3. **Rate Limiting**
   - Per-user rate limits
   - IP-based rate limits
   - Bot detection

4. **Data Privacy**
   - GDPR compliance
   - PII encryption
   - Right to be forgotten
   - Audit logs

## Monitoring & Alerts

### Traditional System Metrics
**Key Metrics to Track**:
- Booking success rate
- Payment success rate
- API response times (p50, p95, p99)
- Error rates (5xx, 4xx)
- Seat lock timeout rate
- Database connection pool usage
- Cache hit ratio

**Critical Alerts**:
- Payment gateway failure
- Database connection issues
- High booking failure rate
- Seat locking issues
- Unusual traffic spikes

### ML/AI Specific Metrics (NEW!)

**ML Model Performance**:
- Model inference latency (p50, p95, p99)
- Model error rate
- Feature computation time
- Batch prediction lag
- Model staleness (time since last training)

**Recommendation Quality**:
- Click-through rate (CTR) - Target: >5%
- Conversion rate (clicked → booked) - Target: >15%
- Recommendation diversity score
- Coverage (% of catalog recommended)
- Cold start fallback rate

**Dynamic Pricing**:
- Average ticket price
- Revenue per seat
- Price adjustment frequency
- Surge pricing incidents
- Price optimization vs rule-based (A/B test)

**LLM Chatbot**:
- Query latency - Target: <2s for simple, <5s for complex
- Tokens consumed per query (cost tracking)
- Function call success rate
- Escalation to human agent rate - Target: <10%
- User satisfaction score (thumbs up/down)

**Fraud Detection**:
- Fraud detection latency - Target: <50ms
- True positive rate (actual fraud caught)
- False positive rate - Target: <2%
- Manual review queue size
- Model drift (prediction distribution changes)

**ML Infrastructure**:
- GPU utilization
- Model server CPU/memory
- Feature store latency
- Vector DB query time
- Model deployment pipeline health

**Critical ML Alerts**:
- Model inference latency > 200ms
- Model error rate > 1%
- Fraud model unavailable (fallback activated)
- Recommendation CTR drops >20%
- LLM API rate limit hit
- Feature store lag > 5 minutes
- Model prediction drift detected

## Related System Designs

- **E-commerce Platform** (similar payment flow)
- **Restaurant Reservation** (similar booking flow)
- **Flight Booking System** (similar seat selection)
- **Event Ticketing** (similar concurrency challenges)
- **Hotel Booking** (similar availability management)

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────────────────┐
│            AI/ML-POWERED MOVIE BOOKING SYSTEM (Hybrid Architecture)         │
├─────────────────────────────────────────────────────────────────────────────┤
│ SCALE: 10M DAU, 2M bookings/day, 2K booking QPS (peak)                     │
│                                                                             │
│ 🎯 CORE SERVICES (Traditional - Deterministic):                            │
│  • Movie Service        • Theater Service     • Booking Service ⭐          │
│  • Payment Service ⭐    • Notification Service                             │
│                                                                             │
│ 🤖 AI/ML SERVICES (Intelligent Enhancement):                               │
│  • Recommendation Engine  • Dynamic Pricing ML   • AI Chatbot (LLM)       │
│  • Fraud Detection ML     • Personalization Engine                         │
│                                                                             │
│ 💾 DATABASES:                                                               │
│  • PostgreSQL (bookings, users) - ACID compliance for booking              │
│  • Redis (cache, distributed locks, session) - <1ms latency                │
│  • Elasticsearch (search, NLP queries)                                      │
│  • Pinecone/Weaviate (vector embeddings) - for recommendations             │
│  • Neo4j (user graph) - for social recommendations                         │
│                                                                             │
│ 🔧 ML/AI INFRASTRUCTURE:                                                    │
│  • Feature Store: Feast/Tecton                                             │
│  • Model Serving: TensorFlow Serving / TorchServe                          │
│  • LLM: OpenAI API / Claude API                                            │
│  • ML Platform: SageMaker / Vertex AI                                      │
│                                                                             │
│ ⚠️  CRITICAL CHALLENGE: Prevent double booking!                            │
│  Solution: Row-level locks OR distributed locks (Redis) with TTL=5min     │
│                                                                             │
│ 📋 BOOKING FLOW (Traditional - Must be reliable!):                         │
│  1. Lock seat (Redis distributed lock, TTL: 5 min)                        │
│  2. Collect payment (Stripe/PayPal)                                       │
│  3. Confirm booking OR release on timeout                                 │
│  4. Send notification (Kafka → Email/SMS)                                 │
│                                                                             │
│ 🤖 AI/ML FEATURES (Optional Enhancement):                                  │
│  • Recommendations: Collaborative filtering + NCF (Neural Collab Filter)  │
│  • Dynamic Pricing: XGBoost model, features: occupancy, time_to_show      │
│  • Chatbot: GPT-4 + function calling (search, book, cancel)               │
│  • Fraud Detection: Isolation Forest, real-time scoring <50ms             │
│                                                                             │
│ 🎚️  ARCHITECTURE DECISION: Why Hybrid?                                     │
│  • Traditional for BOOKING: Needs determinism, low latency (<200ms)       │
│  • AI/ML for UX: Can tolerate latency (1-2s), improves conversion         │
│  • Fallbacks: ML fails → use rule-based system (graceful degradation)     │
│                                                                             │
│ 🔒 CONSISTENCY MODEL:                                                       │
│  • Booking/Payment: STRONG consistency (ACID) - no double booking!         │
│  • Movie catalog: EVENTUAL consistency - slight staleness OK               │
│  • Recommendations: EVENTUAL - batch updates OK                            │
│  • Seat availability: NEAR real-time (30s cache TTL)                      │
│                                                                             │
│ 🚀 LATENCY REQUIREMENTS:                                                    │
│  • Seat lock: <50ms (critical path)                                       │
│  • Payment: <500ms                                                         │
│  • Search: <200ms                                                          │
│  • Recommendations: <1s                                                    │
│  • AI Chatbot: <2s (simple), <5s (complex)                                │
│  • ML fraud check: <50ms (real-time)                                      │
│                                                                             │
│ ⚡ AVAILABILITY: 99.99% uptime                                              │
│  • Multi-region deployment (active-active for reads, active-passive write)│
│  • Read replicas for database                                             │
│  • Circuit breakers for external services (payment, LLM)                  │
│  • Graceful degradation (ML fails → fallback to rules)                    │
│                                                                             │
│ 💰 COST OPTIMIZATION (AI/ML):                                               │
│  • LLM caching: 80% hit rate for common queries                           │
│  • Model tiering: GPT-3.5 (cheap) vs GPT-4 (expensive)                    │
│  • Batch predictions: Group inference requests                            │
│  • Model quantization: FP32 → INT8 (4x faster, minimal accuracy loss)     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Architecture Summary

```
┌──────────────────────────────────────────────────────────────┐
│                  HYBRID ARCHITECTURE                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Layer 1: TRADITIONAL CORE (Must be rock-solid)             │
│  ═══════════════════════════════════════════════════        │
│    → Movie catalog, Theater management                       │
│    → Seat booking with concurrency control ⭐               │
│    → Payment processing ⭐                                   │
│    → Notification system                                     │
│                                                              │
│  Layer 2: AI/ML ENHANCEMENT (Nice to have, can fail)        │
│  ═══════════════════════════════════════════════════        │
│    → Personalized recommendations                            │
│    → Dynamic pricing optimization                            │
│    → Conversational AI chatbot                               │
│    → Real-time fraud detection                               │
│    → Predictive analytics                                    │
│                                                              │
│  ⚖️  Trade-off: Reliability vs Intelligence                 │
│    • Core = 100% uptime, deterministic                       │
│    • AI = 95%+ uptime, probabilistic, fallback to rules     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

**Time to Master**:
- Traditional components: 2-3 hours
- AI/ML components: +2-3 hours
- **Total**: 4-6 hours of focused study

**Interview Success Tips**:
1. Start with traditional architecture (booking flow, concurrency control)
2. Add AI/ML **only if interviewer asks** about UX improvements
3. Explain why hybrid: reliability for core, intelligence for enhancement
4. Always discuss fallbacks: "What if ML model fails?"

**Real-World Complexity**: Very High (combines distributed systems + ML systems)
**Best for**: Senior+ interviews, ML Engineer roles, AI Product companies
