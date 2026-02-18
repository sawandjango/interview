# Diagram 3: Orchestrator Inner Loop (with Tool Use)

## Overview
The orchestrator is the "brain" that decides how to handle each request. It determines whether to use RAG, call tools, or go straight to the LLM. It also handles multi-turn tool calling.

## Architecture Diagram

```
┌───────────────────────────────────────────────────────────┐
│                     ORCHESTRATOR                          │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Step 1: Build Prompt                               │  │
│  │                                                     │  │
│  │  System Message:                                    │  │
│  │    "You are ChatGPT, a helpful assistant..."       │  │
│  │                                                     │  │
│  │  + Conversation History (last N turns):            │  │
│  │    [{"role": "user", "content": "..."},            │  │
│  │     {"role": "assistant", "content": "..."}]       │  │
│  │                                                     │  │
│  │  + Current User Message:                           │  │
│  │    "What's the weather in NYC?"                    │  │
│  │                                                     │  │
│  │  + Tool Definitions (if tools enabled):            │  │
│  │    [{"name": "get_weather", "params": {...}}]      │  │
│  └──────────────────────┬──────────────────────────────┘  │
│                         │                                 │
│                         ▼                                 │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Step 2: Safety Check (Pre-LLM)                     │  │
│  │                                                     │  │
│  │  ┌────────────────────────────────┐                │  │
│  │  │ Checks:                        │                │  │
│  │  │ - Prompt injection             │                │  │
│  │  │ - Jailbreak attempts           │                │  │
│  │  │ - PII in prompt (redact)       │                │  │
│  │  │ - Toxic language               │                │  │
│  │  │ - Policy violations            │                │  │
│  │  └────────────────┬───────────────┘                │  │
│  │                   │                                │  │
│  │         ┌─────────┴─────────┐                      │  │
│  │         │                   │                      │  │
│  │      BLOCK                ALLOW                    │  │
│  │         │                   │                      │  │
│  │         ▼                   ▼                      │  │
│  │  Return error       Continue                       │  │
│  └─────────────────────────┬───────────────────────────┘  │
│                            │                              │
│                            ▼                              │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Step 3: Optional RAG Query                         │  │
│  │                                                     │  │
│  │  Decision Logic:                                    │  │
│  │    if (query_needs_external_knowledge):            │  │
│  │       context = rag_service.retrieve(query)        │  │
│  │                                                     │  │
│  │  ┌──────────────────────────────────────────────┐  │  │
│  │  │ RAG Flow:                                    │  │  │
│  │  │                                              │  │  │
│  │  │  User Query: "What's in the Q3 report?"     │  │  │
│  │  │          │                                   │  │  │
│  │  │          ▼                                   │  │  │
│  │  │  Query Expansion:                           │  │  │
│  │  │    → "Q3 report", "Q3 earnings",            │  │  │
│  │  │      "third quarter results"                │  │  │
│  │  │          │                                   │  │  │
│  │  │          ▼                                   │  │  │
│  │  │  Hybrid Search (Vector DB):                 │  │  │
│  │  │    - Dense embeddings (semantic)            │  │  │
│  │  │    - Sparse BM25 (keyword)                  │  │  │
│  │  │          │                                   │  │  │
│  │  │          ▼                                   │  │  │
│  │  │  Retrieve top 20 candidates                 │  │  │
│  │  │          │                                   │  │  │
│  │  │          ▼                                   │  │  │
│  │  │  Re-ranker (cross-encoder):                 │  │  │
│  │  │    → top 5 chunks                           │  │  │
│  │  │          │                                   │  │  │
│  │  │          ▼                                   │  │  │
│  │  │  Context = chunks + metadata + citations    │  │  │
│  │  └──────────────────────────────────────────────┘  │  │
│  │                                                     │  │
│  │  Append context to prompt:                         │  │
│  │    "Here is relevant information: [context]"       │  │
│  └──────────────────────┬──────────────────────────────┘  │
│                         │                                 │
│                         ▼                                 │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Step 4: LLM Router                                 │  │
│  │                                                     │  │
│  │  Select model based on:                            │  │
│  │    - User tier (free → gpt-3.5, pro → gpt-4)       │  │
│  │    - Query complexity (simple → small model)       │  │
│  │    - Cost budget                                   │  │
│  │    - Latency requirements                          │  │
│  │    - Regional availability                         │  │
│  │                                                     │  │
│  │  Decision:                                          │  │
│  │    model = "gpt-4"                                 │  │
│  │    region = "us-west-2"                            │  │
│  │    max_tokens = 4096                               │  │
│  └──────────────────────┬──────────────────────────────┘  │
│                         │                                 │
│                         ▼                                 │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Step 5: LLM Inference                              │  │
│  │                                                     │  │
│  │  Send to inference pool:                           │  │
│  │    POST /v1/chat/completions                       │  │
│  │    {                                               │  │
│  │      "model": "gpt-4",                             │  │
│  │      "messages": [...],                            │  │
│  │      "stream": true,                               │  │
│  │      "tools": [...]                                │  │
│  │    }                                               │  │
│  │          │                                          │  │
│  │          ▼                                          │  │
│  │  Model generates tokens...                         │  │
│  │          │                                          │  │
│  │          ├────────► Stream to client               │  │
│  │          │                                          │  │
│  │          ▼                                          │  │
│  │  Model emits: function_call?                       │  │
│  │          │                                          │  │
│  │     ┌────┴────┐                                     │  │
│  │     │         │                                     │  │
│  │    YES       NO                                     │  │
│  │     │         │                                     │  │
│  │     │         └──► Continue to Step 6               │  │
│  │     │                                               │  │
│  │     ▼                                               │  │
│  │  ┌────────────────────────────────────────┐         │  │
│  │  │ Tool Call Loop (Multi-turn)            │         │  │
│  │  │                                        │         │  │
│  │  │ Example:                               │         │  │
│  │  │   Model says:                          │         │  │
│  │  │   {                                    │         │  │
│  │  │     "function_call": {                 │         │  │
│  │  │       "name": "get_weather",           │         │  │
│  │  │       "arguments": {                   │         │  │
│  │  │         "location": "NYC"              │         │  │
│  │  │       }                                │         │  │
│  │  │     }                                  │         │  │
│  │  │   }                                    │         │  │
│  │  │          │                             │         │  │
│  │  │          ▼                             │         │  │
│  │  │  ┌─────────────────────────┐           │         │  │
│  │  │  │ Tool Adapter            │           │         │  │
│  │  │  │ - Validate params       │           │         │  │
│  │  │  │ - Execute function      │           │         │  │
│  │  │  │ - Return result         │           │         │  │
│  │  │  └──────────┬──────────────┘           │         │  │
│  │  │             │                          │         │  │
│  │  │             ▼                          │         │  │
│  │  │  Result: "NYC: 72°F, Sunny"            │         │  │
│  │  │             │                          │         │  │
│  │  │             ▼                          │         │  │
│  │  │  Append to messages:                   │         │  │
│  │  │    {"role": "function",                │         │  │
│  │  │     "name": "get_weather",             │         │  │
│  │  │     "content": "72°F, Sunny"}          │         │  │
│  │  │             │                          │         │  │
│  │  │             ▼                          │         │  │
│  │  │  Call LLM again with tool result       │         │  │
│  │  │             │                          │         │  │
│  │  │             ▼                          │         │  │
│  │  │  Model generates final response:       │         │  │
│  │  │    "The weather in NYC is 72°F..."     │         │  │
│  │  └────────────────────────────────────────┘         │  │
│  └─────────────────────────┬───────────────────────────┘  │
│                            │                              │
│                            ▼                              │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Step 6: Safety Check (Post-LLM)                    │  │
│  │                                                     │  │
│  │  Checks:                                            │  │
│  │    - Harmful content (violence, illegal advice)    │  │
│  │    - PII leakage                                   │  │
│  │    - Hallucinations (if RAG was used)              │  │
│  │    - Toxicity                                      │  │
│  │                                                     │  │
│  │  Actions:                                           │  │
│  │    - Block: Return generic "I can't help with..."  │  │
│  │    - Modify: Redact specific parts                 │  │
│  │    - Allow: Deliver as-is                          │  │
│  └──────────────────────┬──────────────────────────────┘  │
│                         │                                 │
│                         ▼                                 │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Step 7: Deliver Response + Log                     │  │
│  │                                                     │  │
│  │  - Stream final tokens to client                   │  │
│  │  - Save conversation turn to DB                    │  │
│  │  - Log metrics:                                    │  │
│  │      - Latency (total, per component)              │  │
│  │      - Tokens (input, output, cached)              │  │
│  │      - Model used                                  │  │
│  │      - RAG used? Tools called?                     │  │
│  │      - Safety decisions                            │  │
│  │  - Emit billing event                              │  │
│  └─────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

## Decision Logic Pseudocode

```python
class Orchestrator:
    def handle_request(self, user_message, conversation_id, user):
        # Step 1: Build prompt
        conversation = load_conversation(conversation_id)
        messages = build_messages(
            system_prompt=get_system_prompt(),
            history=conversation.recent_messages(limit=10),
            user_message=user_message
        )

        # Step 2: Pre-LLM safety
        safety_result = safety_filter.check_input(user_message)
        if safety_result.blocked:
            return {"error": "Your request violates our policies"}
        if safety_result.modified:
            user_message = safety_result.modified_content

        # Step 3: Decide if RAG is needed
        if self.needs_rag(user_message):
            context = rag_service.retrieve(
                query=user_message,
                top_k=5,
                conversation_context=conversation.summary
            )
            messages.append({
                "role": "system",
                "content": f"Context: {context.format_for_llm()}"
            })

        # Step 4: Route to appropriate model
        model_config = llm_router.select_model(
            user_tier=user.tier,
            query_complexity=estimate_complexity(user_message),
            latency_requirement="p95 < 700ms"
        )

        # Step 5: Inference (with tool calling loop)
        response = None
        max_tool_calls = 5
        tool_call_count = 0

        while tool_call_count < max_tool_calls:
            llm_response = inference_client.complete(
                model=model_config.model,
                messages=messages,
                stream=True,
                tools=AVAILABLE_TOOLS if user.tools_enabled else None
            )

            # Stream tokens to client
            for chunk in llm_response.stream():
                yield chunk

            # Check if model wants to call a tool
            if llm_response.finish_reason == "function_call":
                tool_call_count += 1
                tool_result = self.execute_tool(
                    llm_response.function_call.name,
                    llm_response.function_call.arguments
                )

                # Append tool result to messages
                messages.append({
                    "role": "function",
                    "name": llm_response.function_call.name,
                    "content": json.dumps(tool_result)
                })
                # Loop again to let model use the result
                continue
            else:
                response = llm_response
                break

        # Step 6: Post-LLM safety
        safety_result = safety_filter.check_output(response.content)
        if safety_result.blocked:
            return {"error": "I can't provide that information"}

        # Step 7: Save and log
        conversation.add_message("assistant", response.content)
        conversation.save()

        metrics.log({
            "latency_ms": response.metrics.latency,
            "tokens_input": response.usage.input_tokens,
            "tokens_output": response.usage.output_tokens,
            "model": model_config.model,
            "rag_used": context is not None,
            "tools_called": tool_call_count
        })

        billing.emit_event({
            "user_id": user.id,
            "tokens": response.usage.total_tokens,
            "model": model_config.model
        })

        return response

    def needs_rag(self, message):
        # Heuristics or classifier to decide RAG
        triggers = [
            "what does the document say",
            "according to the report",
            "in the knowledge base",
            contains_recent_events(message)  # beyond training cutoff
        ]
        return any(trigger in message.lower() for trigger in triggers)

    def execute_tool(self, tool_name, arguments):
        # Dispatch to appropriate tool adapter
        if tool_name == "get_weather":
            return weather_api.get_current(arguments["location"])
        elif tool_name == "calculator":
            return calculator.evaluate(arguments["expression"])
        elif tool_name == "database_query":
            # Sandboxed SQL execution
            return database.query(arguments["sql"])
        else:
            return {"error": f"Unknown tool: {tool_name}"}
```

## Tool Call Example Flow

**User**: "What's 25% of 480, and what's the weather in that result's zip code (if it's in NYC)?"

1. **LLM Call 1**: Model emits `function_call: calculator("25% of 480")`
2. **Tool Execution**: Calculator returns `120`
3. **LLM Call 2**: Model receives result, emits `function_call: get_weather("10120")`
   (Note: 10120 is not a valid NYC zip, model might correct or ask)
4. **Tool Execution**: Weather API returns error or data
5. **LLM Call 3**: Model generates final natural language response

**Total latency**: 3 LLM calls + 2 tool executions ≈ 2-3 seconds

## Key Optimizations

1. **RAG Query Expansion**: Improves recall
   - "Q3 report" → ["Q3", "third quarter", "quarterly report"]

2. **Hybrid Search**: Combines semantic + keyword
   - Dense vectors: Understand "cheap flights" ≈ "affordable travel"
   - Sparse BM25: Exact match for product codes, names

3. **Re-ranker**: Cross-encoder for final ranking
   - More accurate than bi-encoder but slower
   - Only re-rank top 20 → top 5 (manageable compute)

4. **Tool Call Budget**: Prevent infinite loops
   - Max 5 tool calls per request
   - Timeout after 10 seconds total

5. **Streaming**: Start sending tokens ASAP
   - Don't wait for full response
   - Better perceived latency

## Failure Modes

| Failure | Impact | Mitigation |
|---------|--------|------------|
| Safety filter timeout | Slow response | Timeout after 100ms, fail open |
| RAG service down | No context | Degrade gracefully, use LLM alone |
| Tool execution error | Incomplete response | Return error to model, let it explain |
| LLM timeout | No response | Retry once, fallback to cached response |
| Infinite tool loop | Wasted compute | Hard limit of 5 calls, timeout |

## Metrics to Track

- **Per-step latency**: Safety (pre/post), RAG, LLM, tools
- **Decision rates**: % requests using RAG, % using tools
- **Tool success rate**: % tool calls that succeed
- **Safety block rate**: % requests blocked pre/post
- **Model utilization**: Distribution of model usage (GPT-4 vs 3.5)
