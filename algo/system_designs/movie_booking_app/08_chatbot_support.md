# LLM-Powered Conversational AI Chatbot

## Overview
AI chatbot using LLMs (GPT-4/Claude) with function calling to handle customer support queries, bookings, and recommendations.

---

## Architecture

```
User: "I want to watch Avengers tonight in IMAX near downtown"
    ↓
┌──────────────────────────────────────────────────────────────┐
│  Chatbot Service (LLM + Function Calling)                    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Step 1: Check Response Cache (Redis)                       │
│    Key: hash(query + user_context)                          │
│    Hit rate: 80% → Instant response (cost savings\!)         │
│                                                              │
│  Step 2: LLM Processing (if cache miss)                     │
│    ┌────────────────────────────────────────────────────┐  │
│    │  LLM (GPT-4 or Claude)                             │  │
│    │                                                     │  │
│    │  System Prompt:                                     │  │
│    │  "You are a movie booking assistant. Help users    │  │
│    │   find movies, check availability, and book        │  │
│    │   tickets. Be concise and helpful."                │  │
│    │                                                     │  │
│    │  Available Functions:                               │  │
│    │    • search_movies(query, city, date, time)        │  │
│    │    • get_showtimes(movie_id, city, date)           │  │
│    │    • check_seat_availability(show_id)              │  │
│    │    • create_booking(show_id, seats)                │  │
│    │    • cancel_booking(booking_id)                    │  │
│    │    • get_booking_status(booking_id)                │  │
│    │    • get_recommendations(user_id)                  │  │
│    └────────────────────────────────────────────────────┘  │
│                                                              │
│  Step 3: Function Execution                                  │
│    LLM decides to call: search_movies(                       │
│      query="Avengers",                                       │
│      city="downtown",                                        │
│      date="tonight",                                         │
│      screen_type="IMAX"                                      │
│    )                                                         │
│                                                              │
│  Step 4: Format Response                                     │
│    "I found 2 IMAX showtimes for Avengers tonight:          │
│     1. AMC Downtown - 7:00 PM ($22)                          │
│     2. Regal Center - 9:30 PM ($24)                          │
│     Which would you like to book?"                           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Cost Optimization

### Without Optimization
```
1M queries/day
500 tokens/query average
GPT-4: $0.03/1K tokens

Cost = 1,000,000 * 500 / 1000 * $0.03 = $15,000/day
     = $450,000/month 💸💸💸
```

### With Optimization
```
1. Response Caching (80% hit rate)
   → Only 200K actual LLM calls
   → Cost: $90K/month

2. Model Tiering
   Simple queries (70%): GPT-3.5-turbo ($0.002/1K)
   Complex queries (30%): GPT-4 ($0.03/1K)
   → Cost: $21K/month

3. Prompt Engineering (reduce tokens)
   Average tokens: 500 → 200
   → Cost: $8K/month

4. Streaming (better UX, same cost)
   → Cost: $8K/month

Final: ~$10K/month (95% savings\!) ✅
```

---

## Function Calling Implementation

```python
# Available functions for LLM
functions = [
    {
        "name": "search_movies",
        "description": "Search for movies by title, genre, location, and time",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Movie title or genre"},
                "city": {"type": "string", "description": "City or area"},
                "date": {"type": "string", "description": "Date (today, tomorrow, YYYY-MM-DD)"},
                "time": {"type": "string", "description": "Time preference (morning, evening, etc.)"},
                "screen_type": {"type": "string", "enum": ["IMAX", "4DX", "Regular"]}
            },
            "required": ["query"]
        }
    },
    {
        "name": "create_booking",
        "description": "Book tickets for a movie show",
        "parameters": {
            "type": "object",
            "properties": {
                "show_id": {"type": "integer"},
                "seat_ids": {"type": "array", "items": {"type": "integer"}},
                "user_id": {"type": "integer"}
            },
            "required": ["show_id", "seat_ids", "user_id"]
        }
    }
    # ... more functions
]

# LLM call with function calling
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ],
    functions=functions,
    function_call="auto"
)

# Check if LLM wants to call a function
if response.choices[0].message.get("function_call"):
    function_name = response.choices[0].message.function_call.name
    function_args = json.loads(response.choices[0].message.function_call.arguments)
    
    # Execute function
    result = execute_function(function_name, function_args)
    
    # Send result back to LLM for final response
    final_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": None, "function_call": response.choices[0].message.function_call},
            {"role": "function", "name": function_name, "content": json.dumps(result)}
        ]
    )
    
    return final_response.choices[0].message.content
```

---

## Multi-Turn Conversation

```python
# Store conversation history in Redis
conversation_key = f"chat:{user_id}:{session_id}"

def handle_message(user_id, session_id, message):
    # Fetch conversation history
    history = redis.get(conversation_key) or []
    
    # Add user message
    history.append({"role": "user", "content": message})
    
    # Call LLM with full history
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            *history  # Unpack all previous messages
        ],
        functions=functions,
        function_call="auto"
    )
    
    # Add assistant response to history
    assistant_message = response.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_message})
    
    # Save history (TTL: 30 minutes)
    redis.setex(conversation_key, 1800, json.dumps(history))
    
    return assistant_message
```

---

## Fallback to Human Agent

```python
def should_escalate(conversation_history, user_sentiment):
    """
    Decide if conversation should be escalated to human
    """
    # Escalate if:
    # 1. User explicitly asks for human
    if any("human" in msg or "agent" in msg for msg in conversation_history):
        return True
    
    # 2. Conversation too long (>10 turns)
    if len(conversation_history) > 20:  # 10 turns = 20 messages
        return True
    
    # 3. Negative sentiment detected
    if user_sentiment < 0.3:  # Sentiment analysis score
        return True
    
    # 4. Payment issues
    if any("payment" in msg and "failed" in msg for msg in conversation_history):
        return True
    
    return False

# In chatbot handler
if should_escalate(history, sentiment):
    return {
        "message": "I'll connect you with a human agent who can better assist you.",
        "action": "escalate_to_agent",
        "queue": "general_support"
    }
```

---

## Example Conversations

### Conversation 1: Movie Search & Booking
```
User: "I want to watch something funny tonight"

Bot: "I found several comedies playing tonight. Here are the top picks:
     1. Barbie (Comedy) - AMC Downtown, 7:30 PM, 9:45 PM
     2. The Hangover (Comedy) - Regal Cinema, 8:00 PM
     Which interests you?"

User: "Barbie at 7:30 sounds good"

Bot: "Great\! Barbie at AMC Downtown, 7:30 PM. How many tickets?"

User: "2 tickets"

Bot: "Perfect\! 2 tickets for Barbie at 7:30 PM. Total: $28.
     Would you like to select your seats?"

User: "Yes"

Bot: [Shows seat map] "Please select 2 seats."

User: [Selects A5, A6]

Bot: "You selected A5 and A6. Proceeding to payment...
     Your total is $28. Please enter your payment details."

User: [Completes payment]

Bot: "✅ Booking confirmed\! Your confirmation code is ABC123.
     Check your email for tickets. Enjoy the movie\! 🎬"
```

### Conversation 2: Booking Status
```
User: "What's my booking status for tonight?"

Bot: [Calls get_user_bookings(user_id)]
     "You have 1 booking for tonight:
     • Avengers at AMC Downtown, 8:00 PM
     • Seats: B7, B8
     • Status: Confirmed
     • Confirmation: XYZ789"

User: "Can I cancel that?"

Bot: "I can help you cancel your booking for Avengers tonight.
     You'll receive a full refund of $36. Confirm cancellation?"

User: "Yes cancel it"

Bot: [Calls cancel_booking(booking_id)]
     "✅ Booking cancelled. Refund of $36 will be processed in 3-5 days."
```

---

## Monitoring Metrics

```
LLM Performance:
  • Average response time: 1.8s (target: <2s)
  • Cache hit rate: 79% (target: >75%)
  • Token usage per query: 220 (target: <300)
  • Cost per query: $0.01 (target: <$0.02)

User Experience:
  • User satisfaction: 4.2/5.0 (thumbs up/down)
  • Resolution rate: 82% (no human needed)
  • Escalation rate: 12% (target: <15%)
  • Average conversation length: 4.2 turns

Business Impact:
  • Support ticket reduction: 65%
  • Booking conversion from chat: 18%
  • Cost savings vs human agents: $150K/month
```

---

## Interview Q&A

**Q: How do you handle LLM hallucinations?**
```
1. Function calling: LLM can't make up data, must call functions
2. Constrained responses: System prompt specifies exact format
3. Validation: Check LLM output against business rules
4. Fallback: If response seems wrong, ask for clarification
5. Human in the loop: Escalate if uncertain
```

**Q: What if OpenAI API is down?**
```
Fallback chain:
1. Try alternative LLM (Anthropic Claude)
2. If all LLMs down → simple rule-based chatbot
3. Display: "Chat temporarily limited, showing FAQ"
4. Always offer: "Talk to human agent" button
```

**Q: How do you prevent prompt injection attacks?**
```
1. Input sanitization: Remove special characters
2. System prompt protection: Mark system prompts as immutable
3. Function validation: Validate all function arguments
4. Rate limiting: Max 10 messages/minute per user
5. Monitoring: Alert on suspicious patterns
```

---

**Implementation: 4-6 weeks**
**Cost: $10K/month (vs $50K for human agents)**
**ROI: 5x cost savings + 24/7 availability** 🚀
