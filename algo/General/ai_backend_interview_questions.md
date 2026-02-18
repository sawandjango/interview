# AI & Backend Interview Questions (Super Hard)

## System Design & Architecture

1. Design a distributed training system for large language models (like GPT) that can handle petabytes of data across thousands of GPUs. How do you handle fault tolerance, gradient synchronization, and model checkpointing?
   **→ [📝 Detailed Answer](#question-1-distributed-training-system-for-large-language-models)**

2. Design a real-time recommendation system that serves 100 million users with sub-100ms latency. How do you handle cold start, model updates, and A/B testing at scale?

3. Design a vector database that can perform similarity search on billions of high-dimensional embeddings (1536 dimensions) with <10ms p99 latency.

4. Build a distributed inference system for serving multiple large language models (70B+ parameters) with dynamic batching, model parallelism, and auto-scaling.

5. Design a feature store for ML systems that handles real-time feature computation, historical feature retrieval, and ensures training-serving consistency.

## ML/AI Deep Dive

6. Explain the mathematical derivation of backpropagation for a transformer architecture. How do you compute gradients for multi-head attention?

7. You have a model that performs well on validation data but poorly in production. Walk through your debugging process considering data drift, label noise, and distribution shift.

8. Design a training pipeline for a multi-modal model (text + image + audio). How do you handle different modality learning rates, alignment, and fusion strategies?

9. Implement gradient checkpointing for memory-efficient training of very deep networks. What's the time-memory trade-off?

10. How would you implement Ring-AllReduce for distributed data parallel training? Explain the algorithm and bandwidth complexity.

## Distributed Systems & Scalability

11. Design a globally distributed cache system with strong consistency guarantees. Handle network partitions, cache invalidation, and thundering herd problems.

12. Implement a distributed transaction system across multiple databases with ACID guarantees. Explain 2-phase commit, 3-phase commit, and their failure modes.

13. Design a rate limiting system that works across multiple data centers with eventual consistency. Handle clock skew and DDoS attacks.

14. Build a distributed lock manager (like Google's Chubby or Apache ZooKeeper) from scratch. Handle split-brain scenarios and leader election.

15. Design a log aggregation system that processes 10 million events per second from 100,000 servers with exactly-once delivery semantics.

## Database & Storage

16. Design a time-series database optimized for write-heavy workloads (1M writes/sec) with efficient time-range queries and downsampling.

17. Implement a LSM tree from scratch. Explain compaction strategies, bloom filters, and write amplification trade-offs.

18. Design sharding strategy for a multi-tenant SaaS database with 1M tenants where tenant sizes vary by 5 orders of magnitude.

19. How would you migrate a 100TB production database with zero downtime? Handle schema changes, data validation, and rollback strategies.

20. Design a graph database query optimizer for traversal queries. How do you handle index selection and join ordering?

## Concurrency & Performance

21. Implement a lock-free queue with ABA problem handling. Explain memory ordering and compare-and-swap operations.

22. Debug a production system with 99th percentile latency spikes every 30 minutes. Walk through your investigation including GC pauses, kernel scheduling, and network issues.

23. Implement a thread pool with work stealing. How do you prevent contention and ensure fair scheduling?

24. Design a memory allocator optimized for ML workloads with large tensor allocations. Handle fragmentation and buddy allocation.

25. Explain false sharing in multi-core systems and how to detect/prevent it in a high-performance computing application.

## Advanced Backend Concepts

26. Design an API gateway that handles authentication, rate limiting, request routing, and circuit breaking for 10,000 microservices.

27. Implement a consensus algorithm (Raft or Paxos) from scratch. Handle log replication, leader election, and membership changes.

28. Design a message queue system (like Kafka) with partitioning, replication, and exactly-once semantics.

29. Build a service mesh from scratch. Handle service discovery, load balancing, retry logic, and distributed tracing.

30. Design a deployment system that can safely roll out changes to 100,000 servers with automatic rollback on anomaly detection.

## ML Operations & Infrastructure

31. Design an end-to-end ML monitoring system that detects model degradation, data drift, and concept drift in production.

32. Build an automated model retraining pipeline with data versioning, experiment tracking, and model registry.

33. Design a feature engineering pipeline that processes streaming data and batch data with consistent transformation logic.

34. Implement online learning for a production model serving 1M QPS. Handle model updates without downtime.

35. Design a human-in-the-loop labeling system for active learning with quality control and consensus mechanisms.

## Security & Reliability

36. Design a secrets management system for a microservices architecture with rotation, auditing, and zero-trust security.

37. Implement differential privacy for a ML model trained on sensitive user data. What's the privacy-utility trade-off?

38. Design a chaos engineering platform that can safely test failure scenarios in production without impacting users.

39. Build a WAF (Web Application Firewall) using ML to detect zero-day attacks and SQL injection with low false positives.

40. Design a disaster recovery system with RPO < 5 minutes and RTO < 15 minutes for a globally distributed application.

## Optimization & Algorithms

41. Optimize matrix multiplication for transformers on GPU. Explain tiling, memory coalescing, and kernel fusion.

42. Design a hyperparameter optimization system using Bayesian optimization. Handle parallel trials and early stopping.

43. Implement quantization (INT8/INT4) for neural network inference. What's the accuracy-speed trade-off?

44. Design an efficient algorithm for finding top-K items from 1 trillion records distributed across 10,000 machines.

45. Implement flash attention mechanism. Explain the I/O complexity improvements over standard attention.

## Real-World Problem Solving

46. Your model serving infrastructure costs $1M/month. How do you reduce it by 50% without degrading quality or latency?

47. A production model suddenly starts making biased predictions after 6 months. How do you investigate and fix it?

48. Your database is at 90% CPU utilization during peak hours. Walk through your optimization strategy.

49. Design a system to detect and prevent prompt injection attacks in an LLM-powered application.

50. You need to serve a 175B parameter model with 50ms p95 latency on a limited budget. What's your strategy?

---

## Categories by Topic

- **System Design**: 1-5, 11-15, 26-30
- **ML/AI**: 6-10, 31-35, 49-50
- **Database**: 16-20, 48
- **Concurrency**: 21-25
- **Infrastructure**: 26-30, 40
- **Optimization**: 41-45
- **Security**: 36-39, 49
- **Problem Solving**: 46-50

---

## Detailed Answers

### Question 1: Distributed Training System for Large Language Models

**Design a distributed training system for large language models (like GPT) that can handle petabytes of data across thousands of GPUs. How do you handle fault tolerance, gradient synchronization, and model checkpointing?**

---

#### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                   DISTRIBUTED LLM TRAINING SYSTEM                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                         ORCHESTRATION LAYER                              │  │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐            │  │
│  │  │  Kubernetes    │  │  Ray / Horovod │  │  SLURM / PBS   │            │  │
│  │  │  (K8s)         │  │  (ML Framework)│  │  (HPC Scheduler)│           │  │
│  │  └────────────────┘  └────────────────┘  └────────────────┘            │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                    ↓                                            │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                        TRAINING CLUSTER                                  │  │
│  │                                                                          │  │
│  │  Node 1          Node 2          ...         Node N                     │  │
│  │  ┌────────┐      ┌────────┐                 ┌────────┐                 │  │
│  │  │ 8xA100 │      │ 8xA100 │                 │ 8xA100 │                 │  │
│  │  │ GPU    │      │ GPU    │                 │ GPU    │                 │  │
│  │  │        │      │        │                 │        │                 │  │
│  │  │ NVLink │      │ NVLink │                 │ NVLink │                 │  │
│  │  │ 600GB/s│      │ 600GB/s│                 │ 600GB/s│                 │  │
│  │  └────────┘      └────────┘                 └────────┘                 │  │
│  │       ↕               ↕                          ↕                       │  │
│  │  ┌──────────────────────────────────────────────────────────┐          │  │
│  │  │ InfiniBand / RoCE Network (200 Gbps+)                    │          │  │
│  │  │ NCCL (NVIDIA Collective Communications Library)          │          │  │
│  │  └──────────────────────────────────────────────────────────┘          │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                    ↓                                            │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                       PARALLELISM STRATEGIES                             │  │
│  │                                                                          │  │
│  │  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐  │  │
│  │  │ Data Parallelism  │  │ Model Parallelism │  │Pipeline Parallelism│  │
│  │  │                   │  │                   │  │                   │  │  │
│  │  │ Same model copy   │  │ Split model       │  │ Split layers      │  │  │
│  │  │ Different batches │  │ across GPUs       │  │ into stages       │  │  │
│  │  │                   │  │                   │  │                   │  │  │
│  │  │ ZeRO-1/2/3        │  │ Tensor Parallel   │  │ GPipe / PipeDream │  │  │
│  │  │ DDP (PyTorch)     │  │ Megatron-LM       │  │                   │  │  │
│  │  └───────────────────┘  └───────────────────┘  └───────────────────┘  │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                    ↓                                            │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                        DATA PIPELINE                                     │  │
│  │                                                                          │  │
│  │  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐      │  │
│  │  │ Object   │ →   │ Data     │ →   │ Tokenizer│ →   │ DataLoader│     │  │
│  │  │ Storage  │     │ Streaming│     │ (Parallel)│     │ (Prefetch)│     │  │
│  │  │ (S3/GCS) │     │          │     │          │     │          │      │  │
│  │  └──────────┘     └──────────┘     └──────────┘     └──────────┘      │  │
│  │                                                                          │  │
│  │  • WebDataset format (tar shards)                                       │  │
│  │  • Streaming from cloud storage                                         │  │
│  │  • Prefetch 2-3 batches ahead                                           │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                    ↓                                            │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                  FAULT TOLERANCE & CHECKPOINTING                         │  │
│  │                                                                          │  │
│  │  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────┐   │  │
│  │  │ Elastic Training   │  │ Async Checkpoints  │  │ Redundant Save │   │  │
│  │  │ (PyTorch Elastic)  │  │ (Every N steps)    │  │ (3 locations)  │   │  │
│  │  └────────────────────┘  └────────────────────┘  └────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

#### 1. Parallelism Strategies (3D Parallelism)

**A. Data Parallelism (Most Common)**

```python
# Concept: Replicate model on each GPU, different data batches

# Traditional Data Parallel (DDP)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Problem: Each GPU stores full model copy → memory inefficient for large models

import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

# Initialize process group
dist.init_process_group(backend='nccl')

# Wrap model with DDP
model = MyLargeModel()
model = DDP(model, device_ids=[local_rank])

# Training loop
for batch in dataloader:
    loss = model(batch)
    loss.backward()  # Gradient all-reduce happens automatically
    optimizer.step()

# All-Reduce Gradient Synchronization:
# Each GPU computes gradients → All-Reduce → Average → Update weights
```

**ZeRO (Zero Redundancy Optimizer) - Memory Efficient!**

```
ZeRO-1: Optimizer State Partitioning
  • Each GPU stores 1/N of optimizer states
  • Saves 4x memory (Adam has 2 states per param)

ZeRO-2: Optimizer + Gradient Partitioning
  • Each GPU stores 1/N of gradients too
  • Saves 8x memory

ZeRO-3: Optimizer + Gradient + Parameter Partitioning
  • Each GPU stores 1/N of model parameters
  • During forward/backward: all-gather needed params
  • Saves up to 64x memory!
  • Trade-off: More communication

Example: 175B parameter model (GPT-3 scale)
  • Without ZeRO: Needs ~700GB GPU memory (impossible!)
  • With ZeRO-3: Needs ~11GB per GPU with 64 GPUs
```

**Implementation (DeepSpeed ZeRO):**
```python
import deepspeed

# DeepSpeed config
ds_config = {
    "train_batch_size": 512,
    "gradient_accumulation_steps": 16,
    "optimizer": {
        "type": "Adam",
        "params": {"lr": 1e-4}
    },
    "zero_optimization": {
        "stage": 3,  # ZeRO-3
        "offload_optimizer": {
            "device": "cpu"  # Offload to CPU RAM if needed
        },
        "offload_param": {
            "device": "cpu"
        }
    },
    "fp16": {"enabled": True}
}

model_engine, optimizer, _, _ = deepspeed.initialize(
    model=model,
    config=ds_config
)

for batch in dataloader:
    loss = model_engine(batch)
    model_engine.backward(loss)
    model_engine.step()
```

---

**B. Model Parallelism (Tensor Parallelism)**

```python
# Concept: Split model layers/tensors across GPUs
# Used when model doesn't fit on single GPU

# Megatron-LM Style Tensor Parallelism
# Split attention heads across GPUs

class ParallelSelfAttention(nn.Module):
    def __init__(self, hidden_size, num_heads, tensor_parallel_size):
        super().__init__()
        self.num_heads = num_heads
        self.tp_size = tensor_parallel_size

        # Each GPU gets num_heads / tp_size heads
        self.local_num_heads = num_heads // tensor_parallel_size

        # Q, K, V projections (column-parallel)
        self.qkv = ColumnParallelLinear(
            hidden_size,
            3 * hidden_size,
            gather_output=False
        )

        # Output projection (row-parallel)
        self.out = RowParallelLinear(
            hidden_size,
            hidden_size,
            input_is_parallel=True
        )

    def forward(self, x):
        # Q, K, V are split across GPUs
        qkv = self.qkv(x)  # No communication here

        # Local attention computation
        attn_output = self._local_attention(qkv)

        # All-reduce during output projection
        output = self.out(attn_output)  # All-reduce inside

        return output
```

**Communication Pattern:**
```
GPU 0: Heads 0-7    |  GPU 1: Heads 8-15  |  GPU 2: Heads 16-23  |  GPU 3: Heads 24-31

Forward:
  f(x) → g(x) [all-reduce] → output
       ↑                   ↑
  No communication    Communication

Backward:
  Same pattern in reverse
```

---

**C. Pipeline Parallelism**

```python
# Concept: Split model vertically into stages
# Different GPUs handle different layers

# GPipe Style Pipeline Parallelism

# Example: 96-layer transformer
# Stage 0 (GPU 0): Layers 0-23
# Stage 1 (GPU 1): Layers 24-47
# Stage 2 (GPU 2): Layers 48-71
# Stage 3 (GPU 3): Layers 72-95

# Micro-batching to hide pipeline bubbles
# Split batch of 64 into 8 micro-batches of 8

from torch.distributed.pipeline.sync import Pipe

model = nn.Sequential(*layers)  # 96 layers
model = Pipe(model, chunks=8)   # 8 micro-batches

# Training
for batch in dataloader:
    output = model(batch)  # Pipeline automatically handled
    loss = criterion(output, target)
    loss.backward()
```

**Pipeline Schedule (GPipe):**
```
Time →
  Micro-batch: 1   2   3   4   5   6   7   8

GPU 0:  F1  F2  F3  F4  F5  F6  F7  F8  B1  B2  B3  B4  B5  B6  B7  B8
GPU 1:      F1  F2  F3  F4  F5  F6  F7  F8  B1  B2  B3  B4  B5  B6  B7  B8
GPU 2:          F1  F2  F3  F4  F5  F6  F7  F8  B1  B2  B3  B4  B5  B6  B7  B8
GPU 3:              F1  F2  F3  F4  F5  F6  F7  F8  B1  B2  B3  B4  B5  B6  B7

F = Forward pass
B = Backward pass

Bubble: ~12.5% of time (GPUs idle)
Trade-off: Reduce bubbles by increasing micro-batches (but more memory)
```

---

#### 2. Gradient Synchronization (Communication Primitives)

**A. Ring-AllReduce (Bandwidth-Optimal)**

```
Algorithm: Each GPU sends/receives from neighbors in a ring

Setup: N GPUs, each has gradient tensor of size M

Step 1: Scatter-Reduce (N-1 steps)
  • Each GPU sends chunk to next GPU, receives from previous
  • Reduces (adds) received chunk with local chunk

Step 2: All-Gather (N-1 steps)
  • Each GPU sends reduced chunk to next GPU
  • Now all GPUs have complete reduced gradients

Example: 4 GPUs, 4 chunks (A, B, C, D)

Initial:
  GPU 0: [A0, B0, C0, D0]
  GPU 1: [A1, B1, C1, D1]
  GPU 2: [A2, B2, C2, D2]
  GPU 3: [A3, B3, C3, D3]

After Scatter-Reduce:
  GPU 0: [A_sum, B0, C0, D0]
  GPU 1: [A1, B_sum, C1, D1]
  GPU 2: [A2, B2, C_sum, D2]
  GPU 3: [A3, B3, C3, D_sum]

After All-Gather:
  GPU 0: [A_sum, B_sum, C_sum, D_sum]
  GPU 1: [A_sum, B_sum, C_sum, D_sum]
  GPU 2: [A_sum, B_sum, C_sum, D_sum]
  GPU 3: [A_sum, B_sum, C_sum, D_sum]

Complexity:
  • Data sent per GPU: 2M(N-1)/N ≈ 2M (optimal!)
  • Bandwidth optimal: Doesn't depend on number of GPUs
  • Latency: O(N) steps
```

**Implementation (NCCL):**
```python
import torch.distributed as dist

# NCCL (NVIDIA Collective Communications Library) handles this automatically
# Optimized for GPU-to-GPU communication

# All-Reduce
dist.all_reduce(tensor, op=dist.ReduceOp.SUM)

# NCCL automatically chooses best algorithm:
# - Ring-AllReduce for large tensors
# - Tree-AllReduce for small tensors
# - 2D-AllReduce for very large clusters
```

**B. Gradient Compression (Reduce Communication)**

```python
# Technique 1: Gradient Sparsification
# Only send top-K gradients

def sparsify_gradients(gradients, top_k_ratio=0.01):
    """
    Only send top 1% of gradients by magnitude
    Saves 99% bandwidth!
    """
    flat_grad = torch.cat([g.flatten() for g in gradients])
    k = int(len(flat_grad) * top_k_ratio)

    # Get top-K indices
    _, indices = torch.topk(flat_grad.abs(), k)

    # Sparse tensor: (indices, values)
    sparse_grad = (indices, flat_grad[indices])

    return sparse_grad

# Technique 2: Quantization (FP32 → FP16 or INT8)
def quantize_gradient(gradient):
    # FP32 (4 bytes) → FP16 (2 bytes) = 50% savings
    return gradient.half()

# Technique 3: PowerSGD (Low-Rank Approximation)
# Approximate gradient matrix G ≈ P × Q^T
# Send P and Q instead of G (much smaller!)
```

---

#### 3. Fault Tolerance

**A. Checkpoint Strategies**

```python
# Strategy 1: Synchronous Checkpointing
# All GPUs save simultaneously (simple but slow)

def synchronous_checkpoint(model, optimizer, step):
    if step % CHECKPOINT_INTERVAL == 0:
        # Block all GPUs until checkpoint completes
        checkpoint = {
            'model': model.state_dict(),
            'optimizer': optimizer.state_dict(),
            'step': step,
            'rng_state': torch.get_rng_state()
        }

        # Save to distributed filesystem
        torch.save(checkpoint, f'/shared/checkpoint_{step}.pt')

        # Problem: Stops training for 30-60 seconds!

# Strategy 2: Asynchronous Checkpointing (BETTER!)
# Save to CPU memory first, then async write to disk

from threading import Thread

def async_checkpoint(model, optimizer, step):
    if step % CHECKPOINT_INTERVAL == 0:
        # Copy state dicts to CPU (fast: ~1 second)
        checkpoint = {
            'model': {k: v.cpu() for k, v in model.state_dict().items()},
            'optimizer': {k: v.cpu() for k, v in optimizer.state_dict().items()},
            'step': step
        }

        # Async write to disk (doesn't block training!)
        thread = Thread(target=save_checkpoint, args=(checkpoint, step))
        thread.start()

        # Training continues immediately!

def save_checkpoint(checkpoint, step):
    torch.save(checkpoint, f'/shared/checkpoint_{step}.pt')
    # Also upload to S3 for durability
    upload_to_s3(f'/shared/checkpoint_{step}.pt', f's3://checkpoints/{step}.pt')
```

**Strategy 3: Redundant Checkpointing**
```python
# Save to multiple locations for reliability

CHECKPOINT_LOCATIONS = [
    '/local/ssd/checkpoints',      # Fast local SSD
    '/shared/nfs/checkpoints',     # Shared NFS
    's3://bucket/checkpoints'      # Cloud storage (most durable)
]

def redundant_checkpoint(checkpoint, step):
    for location in CHECKPOINT_LOCATIONS:
        save_to_location(checkpoint, location, step)

    # Keep last N checkpoints, delete older ones
    cleanup_old_checkpoints(keep_last=5)
```

**B. Elastic Training (Handle Node Failures)**

```python
# PyTorch Elastic Training
# Automatically handles GPU/node failures

import torch.distributed.elastic as elastic

@elastic.train
def train_loop():
    # Training code here
    for epoch in range(num_epochs):
        for batch in dataloader:
            # If node fails during training:
            # 1. Elastic agent detects failure
            # 2. Remaining nodes regroup
            # 3. Load last checkpoint
            # 4. Resume training with fewer nodes

            loss = model(batch)
            loss.backward()
            optimizer.step()

# Run with:
# torchrun --nnodes=1:128 --nproc_per_node=8 train.py
#          ↑ min:max nodes (elastic range)
```

**C. Failure Detection & Recovery**

```python
class FaultTolerantTrainer:
    def __init__(self, model, optimizer):
        self.model = model
        self.optimizer = optimizer
        self.step = 0

    def train(self):
        while self.step < MAX_STEPS:
            try:
                # Training step
                loss = self.train_step()

                # Heartbeat: Check if all ranks alive
                if self.step % 100 == 0:
                    self.health_check()

                # Checkpoint
                if self.step % CHECKPOINT_INTERVAL == 0:
                    self.save_checkpoint()

                self.step += 1

            except RuntimeError as e:
                if "NCCL" in str(e) or "communication" in str(e):
                    # Communication failure detected
                    self.handle_failure()
                else:
                    raise

    def health_check(self):
        # All-reduce barrier: If any rank fails, this will hang/error
        dummy = torch.tensor([1.0]).cuda()
        dist.all_reduce(dummy)

    def handle_failure(self):
        # 1. Log failure
        logger.error(f"Node failure at step {self.step}")

        # 2. Wait for elastic agent to regroup
        time.sleep(30)

        # 3. Re-initialize process group
        dist.destroy_process_group()
        dist.init_process_group(backend='nccl')

        # 4. Load latest checkpoint
        self.load_checkpoint()

        # 5. Resume training
        logger.info(f"Resumed from step {self.step}")
```

---

#### 4. Data Pipeline (Petabyte Scale)

**A. Data Storage & Format**

```python
# WebDataset: Streaming-friendly format
# Store data as tar shards (each ~1GB)

# Directory structure:
# s3://training-data/
#   ├── shard-000000.tar (1GB, ~10K samples)
#   ├── shard-000001.tar
#   ├── ...
#   └── shard-099999.tar (100K shards = 100TB total)

# Each tar contains:
#   sample_000000.txt      (raw text)
#   sample_000000.json     (metadata)
#   ...

import webdataset as wds

# Streaming dataset (doesn't download everything!)
dataset = (
    wds.WebDataset("s3://training-data/shard-{000000..099999}.tar")
    .shuffle(1000)  # Shuffle within buffer
    .decode()       # Decode tar files
    .to_tuple("txt", "json")  # Extract text and metadata
    .batched(64)    # Batch size
)

# DataLoader with prefetching
dataloader = torch.utils.data.DataLoader(
    dataset,
    batch_size=None,  # Already batched
    num_workers=4,    # Parallel data loading
    prefetch_factor=2 # Prefetch 2 batches ahead
)
```

**B. Efficient Data Loading**

```python
# Problem: Data loading can be bottleneck
# Solution: Multi-process data loading + prefetching

class PrefetchDataLoader:
    """
    Prefetch next batch to GPU while training current batch
    """
    def __init__(self, dataloader, device):
        self.dataloader = dataloader
        self.device = device
        self.stream = torch.cuda.Stream()
        self.preload()

    def preload(self):
        try:
            self.next_batch = next(self.loader)
        except StopIteration:
            self.next_batch = None
            return

        # Async copy to GPU
        with torch.cuda.stream(self.stream):
            self.next_batch = {
                k: v.to(self.device, non_blocking=True)
                for k, v in self.next_batch.items()
            }

    def __iter__(self):
        self.loader = iter(self.dataloader)
        self.preload()
        return self

    def __next__(self):
        torch.cuda.current_stream().wait_stream(self.stream)
        batch = self.next_batch
        if batch is None:
            raise StopIteration
        self.preload()
        return batch

# Usage
dataloader = PrefetchDataLoader(dataloader, device='cuda')

for batch in dataloader:
    # Batch already on GPU!
    # Next batch loading in background
    loss = model(batch)
```

---

#### 5. Monitoring & Debugging

```python
# Comprehensive monitoring for distributed training

import wandb
from torch.profiler import profile, ProfilerActivity

class DistributedMonitor:
    def __init__(self, rank):
        self.rank = rank
        if rank == 0:
            wandb.init(project='llm-training')

    def log_metrics(self, step, metrics):
        if self.rank == 0:
            # Only rank 0 logs to avoid duplicates
            wandb.log({
                'step': step,
                'loss': metrics['loss'],
                'lr': metrics['lr'],
                'tokens_per_sec': metrics['throughput'],

                # GPU metrics
                'gpu_memory_used': torch.cuda.max_memory_allocated() / 1e9,
                'gpu_utilization': self.get_gpu_util(),

                # Communication metrics
                'comm_time_ms': metrics.get('comm_time', 0),
                'comp_time_ms': metrics.get('comp_time', 0),

                # Gradient stats
                'grad_norm': metrics.get('grad_norm', 0),
            })

    def profile_step(self, model, batch):
        """Profile single training step"""
        with profile(
            activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
            record_shapes=True,
            profile_memory=True
        ) as prof:
            loss = model(batch)
            loss.backward()

        # Print profiling results
        print(prof.key_averages().table(sort_by="cuda_time_total"))

        # Identify bottlenecks:
        # - High CUDA memory? → Reduce batch size or use ZeRO
        # - High communication time? → Gradient compression
        # - Low GPU util? → Data loading bottleneck

# Critical metrics to monitor:
METRICS = {
    'throughput': 'tokens/sec per GPU',
    'mfu': 'Model FLOPs Utilization (%)',  # Should be >40%
    'loss': 'Training loss',
    'grad_norm': 'Gradient norm (detect exploding gradients)',
    'comm_time': 'Communication time (should be <10% of step time)',
    'gpu_memory': 'GPU memory usage',
    'cpu_memory': 'CPU memory usage',
}
```

---

#### 6. Putting It All Together (Production Setup)

**Complete Training Script:**

```python
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
import deepspeed
import wandb

def main():
    # 1. Initialize distributed training
    dist.init_process_group(backend='nccl')
    local_rank = int(os.environ['LOCAL_RANK'])
    torch.cuda.set_device(local_rank)

    # 2. Create model (175B parameters)
    config = GPTConfig(
        n_layer=96,
        n_head=96,
        n_embd=12288,
        vocab_size=50257
    )
    model = GPT(config)

    # 3. DeepSpeed (ZeRO-3 for memory efficiency)
    ds_config = {
        "train_batch_size": 512,
        "gradient_accumulation_steps": 16,
        "zero_optimization": {"stage": 3},
        "fp16": {"enabled": True},
        "activation_checkpointing": {
            "partition_activations": True,
            "cpu_checkpointing": True
        }
    }

    model_engine, optimizer, _, lr_scheduler = deepspeed.initialize(
        model=model,
        config=ds_config
    )

    # 4. Data pipeline
    dataset = create_webdataset()  # Streaming from S3
    dataloader = create_dataloader(dataset, local_rank)

    # 5. Training loop
    step = 0
    for epoch in range(NUM_EPOCHS):
        for batch in dataloader:
            # Forward + backward
            loss = model_engine(batch)
            model_engine.backward(loss)
            model_engine.step()

            # Logging
            if step % 100 == 0 and local_rank == 0:
                wandb.log({'loss': loss.item(), 'step': step})

            # Checkpointing
            if step % 5000 == 0:
                model_engine.save_checkpoint('/checkpoints', tag=f'step_{step}')

            step += 1

if __name__ == '__main__':
    main()
```

**Launch Command:**

```bash
# Launch on 128 nodes × 8 GPUs = 1024 GPUs total

torchrun \
    --nnodes=128 \
    --nproc_per_node=8 \
    --rdzv_backend=c10d \
    --rdzv_endpoint=$MASTER_ADDR:$MASTER_PORT \
    train.py
```

---

#### 7. Cost & Performance Optimization

```
Training GPT-3 (175B parameters):

Hardware: 1024 × A100 GPUs (80GB each)
  • Cost: $2.50/GPU/hour
  • Total: $2,560/hour

Training time: ~34 days
  • Total cost: ~$2.1M

Optimizations:
  1. Mixed Precision (FP16): 2x speedup
  2. Gradient Checkpointing: 3x memory savings
  3. ZeRO-3: 64x memory savings
  4. Flash Attention: 2-4x speedup
  5. Optimized kernel fusion: 1.5x speedup

With optimizations:
  • Training time: ~10 days
  • Total cost: ~$600K (71% savings!)

Key metrics:
  • MFU (Model FLOPs Utilization): 45-50%
  • Throughput: 150K tokens/sec/GPU
  • Communication overhead: <8%
```

---

#### Interview Talking Points Summary

**1. Parallelism:**
- Use 3D parallelism: Data + Model + Pipeline
- ZeRO for memory efficiency
- Choose based on model size and cluster size

**2. Communication:**
- Ring-AllReduce is bandwidth-optimal
- NCCL library handles most optimization
- Gradient compression for slow networks

**3. Fault Tolerance:**
- Async checkpointing every N steps
- Redundant storage (local + shared + cloud)
- Elastic training for node failures
- Always keep last 3-5 checkpoints

**4. Data Pipeline:**
- WebDataset for streaming
- Prefetch to GPU asynchronously
- Multi-process data loading

**5. Monitoring:**
- Track GPU utilization, memory, communication time
- Profile regularly to find bottlenecks
- Alert on anomalies (grad explosions, NaN losses)

**Trade-offs:**
- Memory vs Speed: ZeRO trades communication for memory
- Checkpointing frequency: Too often → slow, Too rare → lose progress
- Batch size: Larger → faster, but needs more GPUs for same learning dynamics

---

*Note: These questions require deep expertise in multiple domains. Prepare to discuss trade-offs, edge cases, and production challenges.*
