# System Performance Basics

## Overview
This document covers fundamental concepts related to system performance, optimization, and scalability. Understanding these concepts helps identify bottlenecks and optimize applications effectively.

---

## 1. Latency vs Throughput

### Latency
- **Definition**: The time it takes to complete a single operation or request
- **Measured in**: Milliseconds (ms), microseconds (μs), or nanoseconds (ns)
- **Example**: Time taken to fetch data from database = 50ms
- **Analogy**: How long it takes for one car to travel from point A to B

### Throughput
- **Definition**: The number of operations/requests completed per unit of time
- **Measured in**: Requests per second (RPS), Transactions per second (TPS), MB/s
- **Example**: Server handling 1000 requests per second
- **Analogy**: How many cars can pass through a highway in an hour

### Key Relationship
- Low latency doesn't always mean high throughput
- High throughput doesn't guarantee low latency
- **Example**: A highway (high throughput) can be congested (high latency per car)

---

## 2. CPU Bound

### Definition
A process is CPU-bound when its performance is limited by CPU processing speed.

### Characteristics
- **High CPU usage** (near 100%)
- Low I/O wait time
- Performance improves with faster CPU or more cores
- Minimal idle time waiting for external resources

### Common Examples
- Mathematical calculations and computations
- Data compression/decompression
- Video encoding/rendering
- Cryptographic operations (hashing, encryption)
- Machine learning model training
- Image processing
- Prime number calculations

### Optimization Strategies
- Use multi-threading or parallel processing
- Optimize algorithms (better time complexity)
- Upgrade to faster CPU
- Use SIMD instructions
- Profile and eliminate hot spots in code
- Consider GPU acceleration for parallelizable tasks

### Code Example (CPU-bound)
```python
# CPU-intensive task
def calculate_primes(n):
    primes = []
    for num in range(2, n):
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes
```

---

## 3. I/O Bound

### Definition
A process is I/O-bound when its performance is limited by input/output operations (disk, network, database).

### Characteristics
- **Low CPU usage** (CPU often idle)
- High I/O wait time
- Process spends most time waiting for external operations
- Performance improves with faster I/O or async operations

### Common Examples
- Reading/writing files to disk
- Database queries
- API calls over network
- Web scraping
- File uploads/downloads
- Reading from sensors
- User input operations

### Optimization Strategies
- Use asynchronous I/O (async/await)
- Implement caching layers
- Batch operations together
- Use faster storage (SSD vs HDD)
- Optimize database queries and indexes
- Use CDNs for network operations
- Implement connection pooling
- Consider non-blocking I/O

### Code Example (I/O-bound)
```python
# I/O-intensive task
import requests

def fetch_data_from_apis(urls):
    results = []
    for url in urls:
        response = requests.get(url)  # Network I/O - CPU waits
        results.append(response.json())
    return results

# Optimized version with async
import asyncio
import aiohttp

async def fetch_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def fetch_all_async(urls):
    tasks = [fetch_async(url) for url in urls]
    return await asyncio.gather(*tasks)
```

---

## 4. Memory Bound

### Definition
A process is memory-bound when its performance is limited by available RAM or memory bandwidth.

### Characteristics
- **High memory usage**
- Frequent page faults or swapping
- Performance degrades when data doesn't fit in RAM
- Memory access patterns affect performance
- Cache misses impact speed

### Common Examples
- Large dataset processing (big data analytics)
- In-memory databases
- Graph algorithms on large graphs
- Loading large files entirely into memory
- Caching large amounts of data
- Image/video processing with large buffers
- Sorting massive arrays

### Memory Hierarchy (Fastest to Slowest)
1. **CPU Registers** - Fastest, smallest (bytes)
2. **L1 Cache** - Very fast (~1-4 cycles)
3. **L2 Cache** - Fast (~10-20 cycles)
4. **L3 Cache** - Moderate (~40-75 cycles)
5. **RAM** - Slower (~100-300 cycles)
6. **SSD** - Much slower (milliseconds)
7. **HDD** - Very slow (milliseconds)

### Optimization Strategies
- Reduce memory footprint
- Use memory-efficient data structures
- Implement data streaming instead of loading all at once
- Use memory pooling
- Optimize cache locality (access nearby memory)
- Avoid memory leaks
- Use pagination for large datasets
- Consider memory mapping for large files
- Profile memory usage patterns

### Code Example (Memory-bound)
```python
# Memory-intensive - loads everything
def process_large_file_bad(filename):
    with open(filename) as f:
        lines = f.readlines()  # Loads entire file into memory
    return [line.strip() for line in lines]

# Optimized - streaming approach
def process_large_file_good(filename):
    results = []
    with open(filename) as f:
        for line in f:  # Processes one line at a time
            results.append(line.strip())
    return results

# Even better - generator for memory efficiency
def process_large_file_best(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()
```

---

## 5. How to Identify Bottlenecks

### CPU-Bound Indicators
- `top` or `htop` shows high CPU usage (90-100%)
- Low I/O wait time
- Application becomes faster with more CPU cores

### I/O-Bound Indicators
- Low CPU usage (lots of idle time)
- High I/O wait (`wa` in `top` command)
- `iostat` shows high disk utilization
- Network monitoring shows waiting on responses

### Memory-Bound Indicators
- High memory usage (near system limit)
- Swap space being used (very bad for performance)
- Frequent page faults
- `free -m` shows low available memory
- Application slows down when working with large datasets

---

## 6. Quick Reference Table

| Aspect | CPU-Bound | I/O-Bound | Memory-Bound |
|--------|-----------|-----------|--------------|
| **Bottleneck** | CPU processing | Disk/Network | RAM availability |
| **CPU Usage** | High (90-100%) | Low (idle waiting) | Variable |
| **Main Wait** | Computation | External operations | Memory access/swapping |
| **Fix Strategy** | Faster CPU, parallel processing | Async I/O, caching | More RAM, streaming |
| **Example** | Video encoding | API calls | Large dataset processing |
| **Scaling** | Vertical (better CPU) | Horizontal (more servers) | Vertical (more RAM) |

---

## 7. Profiling Tools

### CPU Profiling
- `perf` (Linux)
- `gprof`
- Python: `cProfile`, `line_profiler`
- Node.js: `--prof` flag, `clinic.js`

### I/O Profiling
- `iostat`
- `iotop`
- `strace` (system calls)
- Application-level logging

### Memory Profiling
- `valgrind`
- `top`, `htop`
- Python: `memory_profiler`, `tracemalloc`
- `heaptrack`

---

## 8. General Optimization Principles

1. **Measure First**: Always profile before optimizing
2. **Find the Bottleneck**: Focus on what's actually slow
3. **Optimize the Hot Path**: 80/20 rule applies
4. **Trade-offs**: Memory vs CPU, Latency vs Throughput
5. **Premature Optimization**: Avoid optimizing too early
6. **Scalability**: Consider both vertical and horizontal scaling

---

## Resources
- "Systems Performance" by Brendan Gregg
- Understanding the Linux Kernel
- Database indexing and query optimization guides

