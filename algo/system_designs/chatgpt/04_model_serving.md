# Diagram 4: Model Serving Fleet

## Overview
The LLM inference infrastructure that handles tokenization, batching, GPU scheduling, and KV cache management for efficient token generation.

## Architecture Diagram

```
                    ┌──────────────────────┐
                    │     LLM Router       │
                    │                      │
                    │  Decision Logic:     │
                    │  - Model selection   │
                    │  - Load balancing    │
                    │  - Cost optimization │
                    │  - Health checks     │
                    └──────────┬───────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
    ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
    │ Inference     │ │ Inference     │ │ Inference     │
    │ Pool A        │ │ Pool B        │ │ Pool C        │
    │               │ │               │ │               │
    │ Model: GPT-4  │ │ Model: GPT-3.5│ │ Model: Custom │
    │ GPU: 8xA100   │ │ GPU: 4xA100   │ │ CPU/GPU Mixed │
    │ Region: US-W  │ │ Region: US-E  │ │ Region: EU    │
    └───────┬───────┘ └───────┬───────┘ └───────┬───────┘
            │                 │                 │
            └─────────────────┴─────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────┐
        │      Single Inference Pod Detail            │
        │                                             │
        │  ┌───────────────────────────────────────┐  │
        │  │  1. Request Queue (Redis/RabbitMQ)   │  │
        │  │                                       │  │
        │  │  Incoming requests buffered here     │  │
        │  │  Priority: premium > standard > free │  │
        │  │  Queue depth monitoring for scaling  │  │
        │  └─────────────────┬─────────────────────┘  │
        │                    │                         │
        │                    ▼                         │
        │  ┌───────────────────────────────────────┐  │
        │  │  2. Request Preprocessor             │  │
        │  │                                       │  │
        │  │  - Tokenization (BPE/SentencePiece)  │  │
        │  │  - Input validation                  │  │
        │  │  - Truncation if exceeds limit       │  │
        │  │  - Batching compatible requests      │  │
        │  └─────────────────┬─────────────────────┘  │
        │                    │                         │
        │                    ▼                         │
        │  ┌───────────────────────────────────────┐  │
        │  │  3. Dynamic Batch Scheduler           │  │
        │  │     (Continuous Batching)             │  │
        │  │                                       │  │
        │  │  ┌─────────────────────────────────┐  │  │
        │  │  │ Batch 1: [Req1, Req2, Req3]    │  │  │
        │  │  │ - Total tokens: 2048            │  │  │
        │  │  │ - Iteration: 15                 │  │  │
        │  │  └─────────────────────────────────┘  │  │
        │  │                                       │  │
        │  │  ┌─────────────────────────────────┐  │  │
        │  │  │ Batch 2: [Req4, Req5]           │  │  │
        │  │  │ - Total tokens: 1024            │  │  │
        │  │  │ - Iteration: 8                  │  │  │
        │  │  └─────────────────────────────────┘  │  │
        │  │                                       │  │
        │  │  Strategy:                            │  │
        │  │  - Requests finish at different times│  │
        │  │  - New requests join existing batch  │  │
        │  │  - Maximize GPU utilization          │  │
        │  └─────────────────┬─────────────────────┘  │
        │                    │                         │
        │                    ▼                         │
        │  ┌───────────────────────────────────────┐  │
        │  │  4. KV Cache Manager                 │  │
        │  │                                       │  │
        │  │  ┌────────────────────────────────┐   │  │
        │  │  │ Cache Structure:               │   │  │
        │  │  │                                │   │  │
        │  │  │ Request ID → KV Tensors        │   │  │
        │  │  │   req_123 → {                  │   │  │
        │  │  │     layer_0: [K, V],           │   │  │
        │  │  │     layer_1: [K, V],           │   │  │
        │  │  │     ...                        │   │  │
        │  │  │     layer_n: [K, V]            │   │  │
        │  │  │   }                            │   │  │
        │  │  │                                │   │  │
        │  │  │ Memory: 24GB HBM (A100)        │   │  │
        │  │  │ Eviction: LRU                  │   │  │
        │  │  └────────────────────────────────┘   │  │
        │  │                                       │  │
        │  │  Benefits:                            │  │
        │  │  - Reuse past computations           │  │
        │  │  - Multi-turn conversations          │  │
        │  │  - Prefix caching (system prompt)    │  │
        │  └─────────────────┬─────────────────────┘  │
        │                    │                         │
        │                    ▼                         │
        │  ┌───────────────────────────────────────┐  │
        │  │  5. GPU Execution Engine             │  │
        │  │                                       │  │
        │  │  ┌────────────────────────────────┐   │  │
        │  │  │ Tensor Cores (A100/H100)       │   │  │
        │  │  │                                │   │  │
        │  │  │ Operations per decode step:    │   │  │
        │  │  │  1. Attention (Q @ K^T)        │   │  │
        │  │  │  2. Softmax                    │   │  │
        │  │  │  3. Attention @ V              │   │  │
        │  │  │  4. Feed-forward layers        │   │  │
        │  │  │  5. Layer norms                │   │  │
        │  │  │                                │   │  │
        │  │  │ Optimizations:                 │   │  │
        │  │  │  - Flash Attention             │   │  │
        │  │  │  - Fused kernels               │   │  │
        │  │  │  - BF16/FP16 precision         │   │  │
        │  │  │  - Quantization (INT8/INT4)    │   │  │
        │  │  └────────────────────────────────┘   │  │
        │  │                                       │  │
        │  │  Output: Logits for next token       │  │
        │  └─────────────────┬─────────────────────┘  │
        │                    │                         │
        │                    ▼                         │
        │  ┌───────────────────────────────────────┐  │
        │  │  6. Sampling & Decoding              │  │
        │  │                                       │  │
        │  │  Strategies:                          │  │
        │  │  - Greedy (argmax)                    │  │
        │  │  - Top-k sampling                     │  │
        │  │  - Top-p (nucleus) sampling           │  │
        │  │  - Temperature scaling                │  │
        │  │  - Repetition penalty                 │  │
        │  │                                       │  │
        │  │  Stop conditions:                     │  │
        │  │  - EOS token                          │  │
        │  │  - Max tokens reached                 │  │
        │  │  - Stop sequences matched             │  │
        │  └─────────────────┬─────────────────────┘  │
        │                    │                         │
        │                    ▼                         │
        │  ┌───────────────────────────────────────┐  │
        │  │  7. Response Streaming               │  │
        │  │                                       │  │
        │  │  Token → Detokenize → UTF-8 string   │  │
        │  │         ↓                             │  │
        │  │    Send to client (SSE/WebSocket)    │  │
        │  │                                       │  │
        │  │  Latency:                             │  │
        │  │  - Time to first token (TTFT): ~100ms│  │
        │  │  - Inter-token latency: ~10-20ms     │  │
        │  └───────────────────────────────────────┘  │
        └─────────────────────────────────────────────┘
```

## Continuous Batching in Detail

### Traditional Static Batching
```
Batch 1: [Req1 (50 tokens), Req2 (100 tokens), Req3 (150 tokens)]

Problem: Must wait for longest request (150 tokens)
GPU idle time while Req1, Req2 finish early
Throughput: ~3 requests / (150 * 20ms) = 1 req/sec
```

### Continuous Batching (vLLM style)
```
Time 0ms:    Batch = [Req1, Req2, Req3]
Time 1000ms: Req1 finishes → Batch = [Req2, Req3, Req4] (new!)
Time 2000ms: Req2 finishes → Batch = [Req3, Req4, Req5] (new!)
Time 3000ms: Req3 finishes → Batch = [Req4, Req5, Req6] (new!)

Benefit: GPU always fully utilized
Throughput: 2-3x higher than static batching
```

## KV Cache Memory Layout

```
Model: GPT-4 (170B params, estimated)
Layers: 96
Heads: 96
Head dim: 128
Sequence length: 2048 tokens

Per-request KV cache:
  = 2 (K and V) × 96 layers × 2048 tokens × 96 heads × 128 dim × 2 bytes (FP16)
  = ~4.7 GB per request at max length

A100 (80GB):
  - Model weights: ~340 GB (need 4-8 GPUs with tensor parallelism)
  - Available for KV cache: ~60 GB
  - Concurrent requests: ~12-15 at max length

Optimization: PagedAttention (vLLM)
  - Store KV cache in pages (like virtual memory)
  - Share pages for common prefixes (system prompt)
  - Reduce fragmentation
  - Support 2-4x more concurrent requests
```

## Model Parallelism Strategies

### 1. Tensor Parallelism
```
Split model layers across GPUs horizontally

GPU 0: First 1/4 of each layer's weights
GPU 1: Second 1/4 of each layer's weights
GPU 2: Third 1/4 of each layer's weights
GPU 3: Fourth 1/4 of each layer's weights

All GPUs process same batch in parallel
High communication overhead (need NVLink)
```

### 2. Pipeline Parallelism
```
Split model layers vertically

GPU 0: Layers 1-24
GPU 1: Layers 25-48
GPU 2: Layers 49-72
GPU 3: Layers 73-96

Sequential processing, pipeline bubbles
Lower communication overhead
```

### 3. Data Parallelism
```
Each GPU has full model copy
Process different batches

GPU 0: Batch 1
GPU 1: Batch 2
GPU 2: Batch 3
GPU 3: Batch 4

Simple, but requires each GPU to hold full model
Only works for smaller models
```

**GPT-4 uses**: Tensor + Pipeline parallelism (estimated)

## Performance Optimizations

### 1. Flash Attention
- Fused attention kernel (no intermediate writes to HBM)
- I/O-aware algorithm
- 2-4x speedup, lower memory

### 2. Quantization
- **FP16**: 50% memory reduction, minimal quality loss
- **INT8**: 75% memory reduction, slight quality loss
- **INT4**: 87.5% memory reduction, noticeable quality loss (use for smaller models)

### 3. Speculative Decoding
```
Small model (GPT-3.5): Generate 5 tokens quickly
Large model (GPT-4): Verify in parallel
  - If correct: Accept all 5 (5x speedup!)
  - If wrong: Reject, generate 1 token normally

Average speedup: 2-3x for simpler queries
```

### 4. Prefix Caching
```
System prompt: "You are ChatGPT, a helpful assistant..."
  ↓
Cache KV for this prefix
Reuse across all conversations
Saves ~50-100 tokens of compute per request
```

## Autoscaling Logic

```python
# Metrics to monitor
queue_depth = redis.llen("inference_queue_gpt4")
avg_latency_p95 = prometheus.query("p95_latency_ms")
gpu_utilization = prometheus.query("avg_gpu_util_percent")

# Scaling rules
if queue_depth > 100 or avg_latency_p95 > 700:
    scale_up(target_pods = current_pods + 2)
elif queue_depth < 20 and gpu_utilization < 40:
    scale_down(target_pods = max(1, current_pods - 1))

# Scale-up time: ~2-3 minutes (model loading)
# Scale-down: Graceful drain (finish in-flight requests)
```

## Failure Handling

| Failure | Detection | Mitigation |
|---------|-----------|------------|
| GPU OOM | CUDA error | Reject request, reduce batch size |
| GPU crash | Health check timeout | Move requests to another pod, restart |
| Slow request | Timeout (30s) | Cancel, return partial response |
| Model load failure | Init error | Retry 3x, alert on-call |
| KV cache corruption | Checksum mismatch | Evict cache, recompute |

## Cost Breakdown (Per Million Tokens)

| Model | Hardware | Cost | Latency (TTFT) |
|-------|----------|------|----------------|
| GPT-4 | 8xA100 | $30 | ~100ms |
| GPT-3.5 | 4xA100 | $2 | ~50ms |
| Custom (distilled) | 2xT4 | $0.50 | ~80ms |

**Optimization**: Route simple queries to GPT-3.5, complex to GPT-4
- Estimated cost savings: 60-70%

## Monitoring Metrics

### Infrastructure
- GPU utilization (%)
- GPU memory usage (GB)
- GPU temperature (°C)
- PCIe bandwidth (GB/s)
- NVLink bandwidth (GB/s)

### Application
- Requests per second (QPS)
- Queue depth (backlog)
- TTFT (p50, p95, p99)
- Inter-token latency (ms)
- Throughput (tokens/sec)
- Batch size (avg, max)

### Cost
- Tokens generated per GPU-hour
- Cost per token (by model)
- Idle GPU time (%)

## Interview Talking Points

**Q: How do you reduce TTFT?**
- Prefix caching (system prompt)
- Speculative decoding
- Smaller models for routing layer
- Edge deployment (geographically close to user)

**Q: How do you increase throughput?**
- Continuous batching (vLLM)
- Larger batch sizes
- KV cache optimization (PagedAttention)
- Quantization (fit more in memory)

**Q: How do you handle large models?**
- Tensor parallelism (split across GPUs)
- Pipeline parallelism (split layers)
- Offloading to CPU memory (slow, last resort)

**Q: What if GPU crashes mid-request?**
- Health checks detect failure (5-10s)
- Request automatically retried on healthy pod
- Client sees slight delay, no data loss
