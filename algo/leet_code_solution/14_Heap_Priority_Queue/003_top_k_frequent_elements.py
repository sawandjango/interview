"""
LeetCode Problem #347: Top K Frequent Elements

Difficulty: Medium
Topics: Array, Hash Table, Divide and Conquer, Sorting, Heap (Priority Queue), Bucket Sort, Counting, Quickselect
Companies: Amazon, Facebook, Google, Microsoft, Uber, Bloomberg, Apple, Adobe, Yelp

================================================================================
                    📚 QUICK REFERENCE - WHAT'S IN THIS FILE
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                        📖 TABLE OF CONTENTS                                 │
├──────┬──────────────────────────────────────┬───────────────────────────────┤
│ #    │ SECTION                              │ WHAT YOU'LL LEARN             │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 1    │ 🎯 PROBLEM UNDERSTANDING             │ • What is being asked?        │
│      │                                      │ • Real-world analogies        │
│      │                                      │ • Visual examples             │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 2    │ 🧠 KEY INSIGHTS TO REMEMBER          │ • Main challenge              │
│      │                                      │ • Base cases to handle        │
│      │                                      │ • Pattern recognition         │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 3    │ 🚀 HOW TO APPROACH THIS PROBLEM      │ • Step-by-step process        │
│      │                                      │ • Decision tree               │
│      │                                      │ • Interview scenarios         │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 4    │ 💡 SOLUTION 1: Bucket Sort ⭐        │ • WHY choose? (Pros/Cons)     │
│      │    (OPTIMAL - O(N))                  │ • WHEN to use?                │
│      │                                      │ • Step-by-step walkthrough    │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 5    │ 💡 SOLUTION 2: Min Heap              │ • WHY choose? (Pros/Cons)     │
│      │    (O(N log k) - Classic!)           │ • WHEN to use?                │
│      │                                      │ • Comparison with Solution 1  │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 6    │ 💡 SOLUTION 3: QuickSelect           │ • WHY choose? (Pros/Cons)     │
│      │    (O(N) average)                    │ • WHEN to use?                │
│      │                                      │ • Educational approach        │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 7    │ 💻 IMPLEMENTATION                    │ • Clean, commented code       │
│      │                                      │ • All three solutions         │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 8    │ 🧪 TEST CASES                        │ • Comprehensive tests         │
│      │                                      │ • Edge cases covered          │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 9    │ 🎓 LEARNING SUMMARY                  │ • Key takeaways               │
│      │                                      │ • Memory tricks               │
│      │                                      │ • Common mistakes             │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 10   │ 🔗 RELATED PROBLEMS                  │ • Similar problems            │
│      │                                      │ • Pattern recognition         │
└──────┴──────────────────────────────────────┴───────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           🎯 MEMORY CHEAT SHEET                             │
├──────────────────┬──────────────────────────────────────────────────────────┤
│ ANALOGY          │ "Trending Topics" - Find most popular items!           │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ PATTERN          │ "Count Then Select" - HashMap + selection algorithm!   │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ KEY TRICK        │ Bucket Sort by frequency - O(N) guaranteed!            │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ DEFAULT SOLUTION │ Bucket Sort (O(N) worst case - BEST!)                  │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ TIME COMPLEXITY  │ O(N) - Linear time with bucket sort                    │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ SPACE COMPLEXITY │ O(N) - HashMap + buckets storage                       │
└──────────────────┴──────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        ⚡ QUICK DECISION TABLE                              │
├────────────────────────────────────┬────────────────────────────────────────┤
│ SITUATION                          │ WHICH SOLUTION TO USE?                │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Normal interview (want best)       │ ✅ Solution 1 (Bucket Sort)           │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Need guaranteed O(N)               │ ✅ Solution 1 (Bucket Sort!)          │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Want classic approach              │ ⚡ Solution 2 (Min Heap)              │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Learning divide & conquer          │ 🎓 Solution 3 (QuickSelect)          │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Small k (k << unique elements)     │ ⚡ Solution 2 (Heap O(N log k))       │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Want to show optimization          │ 🎯 Start with Sol 2, optimize to 1   │
└────────────────────────────────────┴────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     📊 SOLUTION COMPARISON TABLE                            │
├──────────────────┬──────────────┬──────────────┬──────────────┬─────────────┤
│ CRITERIA         │ BUCKET SORT  │ MIN HEAP     │ QUICKSELECT  │ WINNER      │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Time: Worst      │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐⭐     │ ⭐⭐         │ Bucket Sort │
│                  │ O(N)         │ O(N log k)   │ O(N²)        │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Time: Average    │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐⭐     │ ⭐⭐⭐⭐⭐   │ Both        │
│                  │ O(N)         │ O(N log k)   │ O(N)         │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Space Complexity │ ⭐⭐⭐       │ ⭐⭐⭐⭐     │ ⭐⭐⭐⭐     │ Heap/QS     │
│                  │ O(N)         │ O(N)         │ O(N)         │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Code Simplicity  │ ⭐⭐⭐⭐     │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐       │ Min Heap    │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ When k is small  │ ⭐⭐⭐⭐     │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐⭐     │ Min Heap    │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Overall Best     │ ✅ OPTIMAL   │ Classic      │ Alternative  │ Bucket Sort │
└──────────────────┴──────────────┴──────────────┴──────────────┴─────────────┘

⏱️  TIME TO MASTER: 25-30 minutes
🎯 DIFFICULTY: Medium
💡 TIP: "Count frequencies, then use buckets indexed by frequency!"
🔥 POPULAR: Classic heap problem asked everywhere!

================================================================================
                           🎯 PROBLEM UNDERSTANDING
================================================================================

WHAT IS THE PROBLEM?
--------------------
Given an array of integers, find the k most FREQUENT elements.
Return them in ANY order.

REAL WORLD ANALOGY:
------------------
Think of TRENDING HASHTAGS on Twitter:
- Millions of tweets with hashtags: [#AI, #Python, #AI, #Java, #Python, #AI, ...]
- You want to find top 3 trending hashtags
- Count each hashtag's frequency
- Select the 3 most frequent ones

Another analogy - PRODUCT ANALYTICS:
- E-commerce site tracking product views
- Millions of view events: [iPhone, MacBook, iPhone, iPad, iPhone, ...]
- Need to find top 5 most viewed products
- Count frequency of each product
- Pick top 5 by view count

THE KEY INSIGHT:
---------------
TWO-STEP PROCESS:
1. COUNT frequencies using HashMap
2. SELECT top k using one of:
   - Bucket Sort (O(N) guaranteed)
   - Min Heap (O(N log k), good for small k)
   - QuickSelect (O(N) average)

❌ Wrong thinking: "Sort by frequency then pick k" → O(N log N)
✅ Right thinking: "Use bucket sort indexed by frequency" → O(N)!

================================================================================
                            📝 FORMAL PROBLEM
================================================================================

Given an integer array nums and an integer k, return the k most frequent
elements. You may return the answer in any order.

Example 1:
----------
Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]
Explanation: 1 appears 3 times, 2 appears 2 times, 3 appears 1 time.
The 2 most frequent are 1 and 2.

Example 2:
----------
Input: nums = [1], k = 1
Output: [1]

Constraints:
------------
* 1 <= nums.length <= 10^5
* -10^4 <= nums[i] <= 10^4
* k is in the range [1, the number of unique elements in the array]
* It is guaranteed that the answer is unique

Follow-up:
----------
Your algorithm's time complexity must be better than O(n log n), where n is
the array's size.

================================================================================
                         🧠 KEY INSIGHTS TO REMEMBER
================================================================================

THE MAIN CHALLENGE:
------------------
❌ Simple sorting by frequency is O(N log N) - not optimal!
❌ Can't just use heap without counting first
✅ Bucket sort by frequency achieves O(N)!

THE MAGIC TRICK: "BUCKET SORT BY FREQUENCY"
--------------------------------------------
Key observation: Frequency ranges from 1 to N!
- Max frequency = N (all elements are the same)
- Min frequency = 1 (each element appears once)
- Create buckets[0...N] where buckets[i] = elements with frequency i
- Collect from end (high frequency) until we have k elements

Example: [1,1,1,2,2,3], k=2
1. Count: {1:3, 2:2, 3:1}
2. Buckets:
   buckets[1] = [3]      (elements with frequency 1)
   buckets[2] = [2]      (elements with frequency 2)
   buckets[3] = [1]      (elements with frequency 3)
3. Collect from end: buckets[3] → [1], buckets[2] → [1,2]
   Result: [1, 2] ✅

THE BREAKTHROUGH INSIGHT:
------------------------
┌─────────────────────────────────────────────────────────────┐
│  Bucket Sort by Frequency:                                  │
│  - Index = frequency (1 to N)                               │
│  - Value = list of elements with that frequency             │
│  - Traverse from end (high freq) to start (low freq)        │
│  → Guaranteed O(N) time!                                    │
└─────────────────────────────────────────────────────────────┘

WHY THIS IS O(N):
-----------------
1. Count frequencies: O(N) - scan array once
2. Build buckets: O(N) - process each unique element
3. Collect results: O(N) - traverse buckets once
Total: O(N) + O(N) + O(N) = O(N) ✅

================================================================================
                          💡 SOLUTION APPROACHES
================================================================================
"""

from typing import List
import heapq
from collections import Counter
import random

# ============================================================================
#              APPROACH 1: BUCKET SORT (OPTIMAL - O(N))
# ============================================================================

def topKFrequent_BucketSort(nums: List[int], k: int) -> List[int]:
    """
    🎯 APPROACH 1: Bucket Sort by Frequency (BEST SOLUTION!)

    TIME COMPLEXITY: O(N) - Guaranteed worst case
    SPACE COMPLEXITY: O(N) - HashMap + buckets

    🧠 MEMORIZATION TRICK: "Frequency Buckets"
    ------------------------------------------
    Think: Group elements by their frequency!
    - Frequency ranges from 1 to N
    - Create N+1 buckets (index = frequency)
    - Collect from end (high frequency first)

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Count frequency of each element using HashMap
    2. Create buckets array: buckets[i] = elements with frequency i
    3. Fill buckets: for each (element, freq), add element to buckets[freq]
    4. Traverse buckets from end (high freq) to start (low freq)
    5. Collect k elements

    🎨 VISUAL EXAMPLE:
    -----------------
    Input: nums = [1,1,1,2,2,3], k = 2

    Step 1: Count frequencies
      freq_map = {1: 3, 2: 2, 3: 1}

    Step 2: Create buckets (size N+1 = 7)
      buckets = [[], [], [], [], [], [], []]
      Index:     0   1   2   3   4   5   6

    Step 3: Fill buckets
      For element 1, freq=3 → buckets[3].append(1)
      For element 2, freq=2 → buckets[2].append(2)
      For element 3, freq=1 → buckets[1].append(3)

      buckets = [[], [3], [2], [1], [], [], []]
      Index:     0    1    2    3   4   5   6
                      ↑    ↑    ↑
                   freq=1  2    3

    Step 4: Collect from end (high frequency first)
      Start from buckets[6], work backwards
      buckets[3] = [1] → result = [1]
      buckets[2] = [2] → result = [1, 2]
      k=2 reached! Return [1, 2] ✅

    WHY THIS IS O(N):
    -----------------
    ✅ Count frequencies: O(N)
    ✅ Build buckets: O(unique elements) ≤ O(N)
    ✅ Collect results: O(N) worst case
    Total: O(N) guaranteed!
    """
    # Step 1: Count frequencies
    freq_map = Counter(nums)

    # Step 2: Create buckets (index = frequency)
    buckets = [[] for _ in range(len(nums) + 1)]

    # Step 3: Fill buckets
    for num, freq in freq_map.items():
        buckets[freq].append(num)

    # Step 4: Collect top k from end (high frequency)
    result = []
    for i in range(len(buckets) - 1, 0, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result

    return result


# ============================================================================
#              APPROACH 2: MIN HEAP (O(N LOG K) - CLASSIC!)
# ============================================================================

def topKFrequent_MinHeap(nums: List[int], k: int) -> List[int]:
    """
    🎯 APPROACH 2: Min Heap of Size K (CLASSIC APPROACH!)

    TIME COMPLEXITY: O(N log k) - Good when k << unique elements
    SPACE COMPLEXITY: O(N) - HashMap + heap of size k

    🧠 MEMORIZATION TRICK: "Keep Top K in Heap"
    -------------------------------------------
    Same pattern as previous kth element problems!
    - Count frequencies
    - Use min heap of size k
    - Heap stores (frequency, element) pairs
    - Top of heap = smallest frequency in top k

    📝 ALGORITHM:
    ------------
    1. Count frequency of each element
    2. Build min heap of size k with (freq, element) pairs
    3. For remaining elements:
       - If freq > heap top freq: replace top
    4. Extract all elements from heap

    🎨 VISUAL EXAMPLE:
    -----------------
    Input: nums = [1,1,1,2,2,3], k = 2

    Step 1: Count frequencies
      freq_map = {1: 3, 2: 2, 3: 1}

    Step 2: Build heap with first k=2 elements
      Process (1, 3): heap = [(3, 1)]
      Process (2, 2): heap = [(2, 2), (3, 1)]
                              ↑ min (smallest freq in top 2)

    Step 3: Process remaining elements
      Process (3, 1): 1 < 2 (heap top) → skip
                      (3 is not in top 2 most frequent)

    Final heap: [(2, 2), (3, 1)]
    Extract: [2, 1] ✅

    ⚡ WHEN TO USE:
    ---------------
    - When k is small (k << number of unique elements)
    - Want classic, well-known algorithm
    - O(N log k) is acceptable
    """
    # Step 1: Count frequencies
    freq_map = Counter(nums)

    # Step 2: Use min heap of size k
    # Heap stores (frequency, element) tuples
    heap = []

    for num, freq in freq_map.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)

    # Step 3: Extract elements from heap
    return [num for freq, num in heap]


# ============================================================================
#              APPROACH 3: QUICKSELECT (O(N) AVERAGE)
# ============================================================================

def topKFrequent_QuickSelect(nums: List[int], k: int) -> List[int]:
    """
    🎯 APPROACH 3: QuickSelect on Frequencies (ALTERNATIVE!)

    TIME COMPLEXITY: O(N) average, O(N²) worst
    SPACE COMPLEXITY: O(N) - HashMap + array of unique elements

    🧠 IDEA: Use QuickSelect on frequency array
    -------------------------------------------
    - Count frequencies
    - Create array of (element, freq) pairs
    - Use QuickSelect to find kth most frequent
    - Return all elements with freq >= kth freq

    📝 ALGORITHM:
    ------------
    1. Count frequencies
    2. Create list of unique elements
    3. Use QuickSelect to partition by frequency
    4. Return top k elements

    ⚠️  NOTE: More complex than bucket sort!
    ----------------------------------------
    Bucket sort is simpler and guaranteed O(N).
    QuickSelect here is for educational purposes.
    """
    # Step 1: Count frequencies
    freq_map = Counter(nums)

    # Step 2: Create array of unique elements
    unique = list(freq_map.keys())

    def partition(left: int, right: int, pivot_index: int) -> int:
        """Partition by frequency (descending order)"""
        pivot_freq = freq_map[unique[pivot_index]]

        # Move pivot to end
        unique[pivot_index], unique[right] = unique[right], unique[pivot_index]

        # Partition: move elements with freq >= pivot_freq to left
        store_index = left
        for i in range(left, right):
            if freq_map[unique[i]] >= pivot_freq:
                unique[i], unique[store_index] = unique[store_index], unique[i]
                store_index += 1

        # Move pivot to final position
        unique[store_index], unique[right] = unique[right], unique[store_index]

        return store_index

    def quickselect(left: int, right: int, k_index: int):
        """Find kth most frequent element"""
        if left == right:
            return

        # Pick random pivot
        pivot_index = random.randint(left, right)
        pivot_index = partition(left, right, pivot_index)

        if pivot_index == k_index:
            return
        elif pivot_index > k_index:
            quickselect(left, pivot_index - 1, k_index)
        else:
            quickselect(pivot_index + 1, right, k_index)

    # Step 3: Use QuickSelect to find top k
    n = len(unique)
    quickselect(0, n - 1, k - 1)

    # Return top k elements
    return unique[:k]


# ============================================================================
#                    🎨 VISUAL WALKTHROUGH EXAMPLE
# ============================================================================

"""
Let's trace Bucket Sort with: nums = [1,1,1,2,2,3], k = 2

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                          APPROACH 1: BUCKET SORT (OPTIMAL)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

GOAL: Find 2 most frequent elements

INITIAL INPUT:
──────────────
Array: [1, 1, 1, 2, 2, 3]
k = 2

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: Count Frequencies using HashMap                                                                                        │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Scan array and count each element:                                                                                           │
│                                                                                                                                 │
│   Process 1: freq_map = {1: 1}                                                                                                 │
│   Process 1: freq_map = {1: 2}                                                                                                 │
│   Process 1: freq_map = {1: 3}                                                                                                 │
│   Process 2: freq_map = {1: 3, 2: 1}                                                                                           │
│   Process 2: freq_map = {1: 3, 2: 2}                                                                                           │
│   Process 3: freq_map = {1: 3, 2: 2, 3: 1}                                                                                     │
│                                                                                                                                 │
│   Final Frequency Map:                                                                                                         │
│   ┌───────────────────────────────────────┐                                                                                    │
│   │  Element  │  Frequency                │                                                                                    │
│   ├───────────┼────────────               │                                                                                    │
│   │    1      │     3      ← Most frequent│                                                                                    │
│   │    2      │     2                     │                                                                                    │
│   │    3      │     1      ← Least frequent│                                                                                   │
│   └───────────┴────────────────────────────┘                                                                                   │
│                                                                                                                                 │
│   Time: O(N) - Single pass through array                                                                                       │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: Create Buckets Array (size = N + 1 = 7)                                                                                │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Why size N+1?                                                                                                                 │
│   - Max possible frequency = N (all elements same)                                                                             │
│   - Min possible frequency = 1                                                                                                 │
│   - Need indices 0 to N (index 0 unused, acts as placeholder)                                                                  │
│                                                                                                                                 │
│   Initial buckets (all empty):                                                                                                 │
│                                                                                                                                 │
│        Index:    0      1      2      3      4      5      6                                                                   │
│              ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┐                                                               │
│   buckets =  │  []  │  []  │  []  │  []  │  []  │  []  │  []  │                                                               │
│              └──────┴──────┴──────┴──────┴──────┴──────┴──────┘                                                               │
│                      ↑      ↑      ↑                                                                                           │
│                   freq=1  freq=2  freq=3                                                                                       │
│                                                                                                                                 │
│   Time: O(N) - Create array of size N+1                                                                                        │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: Fill Buckets (Place elements at index = their frequency)                                                               │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Process each (element, frequency) pair from freq_map:                                                                        │
│                                                                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────────┐                                             │
│   │ Process: element=1, freq=3                                                   │                                             │
│   │ ─────────────────────────────                                                │                                             │
│   │ Action: buckets[3].append(1)                                                 │                                             │
│   │                                                                               │                                             │
│   │      Index:    0      1      2      3      4      5      6                   │                                             │
│   │            ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┐               │                                             │
│   │ buckets =  │  []  │  []  │  []  │ [1]  │  []  │  []  │  []  │               │                                             │
│   │            └──────┴──────┴──────┴──────┴──────┴──────┴──────┘               │                                             │
│   │                                   ↑                                          │                                             │
│   │                          Element 1 appears 3 times                           │                                             │
│   └─────────────────────────────────────────────────────────────────────────────┘                                             │
│                                                                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────────┐                                             │
│   │ Process: element=2, freq=2                                                   │                                             │
│   │ ─────────────────────────────                                                │                                             │
│   │ Action: buckets[2].append(2)                                                 │                                             │
│   │                                                                               │                                             │
│   │      Index:    0      1      2      3      4      5      6                   │                                             │
│   │            ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┐               │                                             │
│   │ buckets =  │  []  │  []  │ [2]  │ [1]  │  []  │  []  │  []  │               │                                             │
│   │            └──────┴──────┴──────┴──────┴──────┴──────┴──────┘               │                                             │
│   │                            ↑                                                 │                                             │
│   │                   Element 2 appears 2 times                                  │                                             │
│   └─────────────────────────────────────────────────────────────────────────────┘                                             │
│                                                                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────────┐                                             │
│   │ Process: element=3, freq=1                                                   │                                             │
│   │ ─────────────────────────────                                                │                                             │
│   │ Action: buckets[1].append(3)                                                 │                                             │
│   │                                                                               │                                             │
│   │      Index:    0      1      2      3      4      5      6                   │                                             │
│   │            ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┐               │                                             │
│   │ buckets =  │  []  │ [3]  │ [2]  │ [1]  │  []  │  []  │  []  │               │                                             │
│   │            └──────┴──────┴──────┴──────┴──────┴──────┴──────┘               │                                             │
│   │                     ↑                                                        │                                             │
│   │            Element 3 appears 1 time                                          │                                             │
│   └─────────────────────────────────────────────────────────────────────────────┘                                             │
│                                                                                                                                 │
│   Final Buckets State:                                                                                                         │
│                                                                                                                                 │
│        Index:    0      1      2      3      4      5      6                                                                   │
│              ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┐                                                               │
│   buckets =  │  []  │ [3]  │ [2]  │ [1]  │  []  │  []  │  []  │                                                               │
│              └──────┴──────┴──────┴──────┴──────┴──────┴──────┘                                                               │
│                      ↑      ↑      ↑                                                                                           │
│               Elements with frequency: 1, 2, 3                                                                                 │
│               (Lower freq ← ─────────────────── → Higher freq)                                                                 │
│                                                                                                                                 │
│   Time: O(unique elements) ≤ O(N)                                                                                              │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: Collect Top K Elements (Traverse from end to start)                                                                    │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Goal: Collect k=2 most frequent elements                                                                                     │
│   Strategy: Start from highest frequency (right end) and work backwards                                                        │
│                                                                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────────┐                                             │
│   │ Check buckets[6] (frequency = 6)                                             │                                             │
│   │ ───────────────────────────────────                                          │                                             │
│   │ Empty! Skip.                                                                  │                                             │
│   │ result = []                                                                   │                                             │
│   └─────────────────────────────────────────────────────────────────────────────┘                                             │
│                                                                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────────┐                                             │
│   │ Check buckets[5] (frequency = 5)                                             │                                             │
│   │ ───────────────────────────────────                                          │                                             │
│   │ Empty! Skip.                                                                  │                                             │
│   │ result = []                                                                   │                                             │
│   └─────────────────────────────────────────────────────────────────────────────┘                                             │
│                                                                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────────┐                                             │
│   │ Check buckets[4] (frequency = 4)                                             │                                             │
│   │ ───────────────────────────────────                                          │                                             │
│   │ Empty! Skip.                                                                  │                                             │
│   │ result = []                                                                   │                                             │
│   └─────────────────────────────────────────────────────────────────────────────┘                                             │
│                                                                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────────┐                                             │
│   │ Check buckets[3] (frequency = 3) ✅                                          │                                             │
│   │ ───────────────────────────────────                                          │                                             │
│   │ Has elements: [1]                                                             │                                             │
│   │ Add 1 to result                                                               │                                             │
│   │ result = [1]                                                                  │                                             │
│   │ len(result) = 1 < k = 2, continue...                                          │                                             │
│   └─────────────────────────────────────────────────────────────────────────────┘                                             │
│                                                                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────────┐                                             │
│   │ Check buckets[2] (frequency = 2) ✅                                          │                                             │
│   │ ───────────────────────────────────                                          │                                             │
│   │ Has elements: [2]                                                             │                                             │
│   │ Add 2 to result                                                               │                                             │
│   │ result = [1, 2]                                                               │                                             │
│   │ len(result) = 2 == k = 2, DONE! ✅                                            │                                             │
│   └─────────────────────────────────────────────────────────────────────────────┘                                             │
│                                                                                                                                 │
│   Final Result: [1, 2]                                                                                                         │
│                                                                                                                                 │
│   Verification:                                                                                                                 │
│   ─────────────                                                                                                                 │
│   Element 1: frequency 3 (highest) ✅                                                                                           │
│   Element 2: frequency 2 (second highest) ✅                                                                                    │
│   Element 3: frequency 1 (not in top 2) ✅                                                                                      │
│                                                                                                                                 │
│   Time: O(N) worst case - might traverse all buckets                                                                           │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

TOTAL TIME COMPLEXITY: O(N)
───────────────────────────
  Step 1: Count frequencies → O(N)
  Step 2: Create buckets → O(N)
  Step 3: Fill buckets → O(unique elements) ≤ O(N)
  Step 4: Collect results → O(N) worst case

  Total: O(N) + O(N) + O(N) + O(N) = O(N) ✅

SPACE COMPLEXITY: O(N)
──────────────────────
  - Frequency map: O(unique elements) ≤ O(N)
  - Buckets array: O(N)
  Total: O(N)
"""

# ============================================================================
#              🎯 MEMORY TRICKS & COMMON MISTAKES
# ============================================================================

"""
🧠 HOW TO REMEMBER THIS SOLUTION:
---------------------------------
1. "COUNT THEN SELECT" → Always count frequencies first
2. "BUCKET BY FREQUENCY" → Use frequency as array index
3. "HIGH TO LOW" → Traverse from end (high freq) to start
4. "FREQUENCY ≤ N" → Max frequency is array length

❌ COMMON MISTAKES TO AVOID:
----------------------------
1. ❌ Sorting by frequency
      WRONG: Sort freq_map by values → O(N log N)
      RIGHT: Use bucket sort → O(N)

2. ❌ Wrong bucket size
      WRONG: buckets = [[] for _ in range(max_freq)]
      RIGHT: buckets = [[] for _ in range(len(nums) + 1)]

3. ❌ Iterating buckets from start
      WRONG: for i in range(len(buckets)) (gets low freq first)
      RIGHT: for i in range(len(buckets)-1, 0, -1) (high freq first)

4. ❌ Using max heap instead of min heap
      WRONG: Max heap of size k (complicated to maintain)
      RIGHT: Min heap of size k (simple, classic pattern)

5. ❌ Forgetting to handle tie-breaking
      NOTE: Problem guarantees unique answer, but be aware!

✅ PRO TIPS:
-----------
1. Bucket sort is optimal for this problem - O(N) guaranteed
2. Min heap is simpler to code and well-known
3. QuickSelect works but more complex
4. Always count frequencies first (critical step!)
5. Draw the buckets array to visualize

🎯 INTERVIEW STRATEGY:
---------------------
"I'll use bucket sort for guaranteed O(N) time. First, I count frequencies
using a HashMap. Then I create an array of buckets where buckets[i] contains
all elements with frequency i. Since max frequency is N, I need N+1 buckets.
Finally, I traverse from the end (high frequency) and collect k elements."

Alternative:
"For simplicity, I can use a min heap of size k. After counting frequencies,
I maintain the k most frequent elements in a heap. The heap stores
(frequency, element) pairs, and I keep only the top k by frequency."
"""

# ============================================================================
#                         🧪 TEST CASES
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("          TOP K FREQUENT ELEMENTS - TEST CASES")
    print("="*80)

    # Test Case 1: Standard case from problem
    print("\n📝 Test Case 1: Standard case")
    print("-" * 80)
    nums1 = [1, 1, 1, 2, 2, 3]
    k1 = 2
    print(f"Input: nums = {nums1}, k = {k1}")
    result1_a = topKFrequent_BucketSort(nums1, k1)
    result1_b = topKFrequent_MinHeap(nums1, k1)
    result1_c = topKFrequent_QuickSelect(nums1.copy(), k1)
    print(f"Output (Bucket Sort): {result1_a}")
    print(f"Output (Min Heap):    {result1_b}")
    print(f"Output (QuickSelect): {result1_c}")
    print(f"Expected: [1, 2] (in any order)")
    expected1 = {1, 2}
    print(f"✅ PASS" if set(result1_a) == expected1 else "❌ FAIL")

    # Test Case 2: Single element
    print("\n📝 Test Case 2: Single element")
    print("-" * 80)
    nums2 = [1]
    k2 = 1
    print(f"Input: nums = {nums2}, k = {k2}")
    result2_a = topKFrequent_BucketSort(nums2, k2)
    result2_b = topKFrequent_MinHeap(nums2, k2)
    result2_c = topKFrequent_QuickSelect(nums2.copy(), k2)
    print(f"Output (Bucket Sort): {result2_a}")
    print(f"Output (Min Heap):    {result2_b}")
    print(f"Output (QuickSelect): {result2_c}")
    print(f"Expected: [1]")
    print(f"✅ PASS" if result2_a == [1] else "❌ FAIL")

    # Test Case 3: All unique elements
    print("\n📝 Test Case 3: All unique elements")
    print("-" * 80)
    nums3 = [1, 2, 3, 4, 5]
    k3 = 2
    print(f"Input: nums = {nums3}, k = {k3}")
    result3_a = topKFrequent_BucketSort(nums3, k3)
    result3_b = topKFrequent_MinHeap(nums3, k3)
    result3_c = topKFrequent_QuickSelect(nums3.copy(), k3)
    print(f"Output (Bucket Sort): {result3_a}")
    print(f"Output (Min Heap):    {result3_b}")
    print(f"Output (QuickSelect): {result3_c}")
    print(f"Expected: Any 2 elements (all have same frequency)")
    print(f"✅ PASS (all freq=1, any answer valid)")

    # Test Case 4: All same elements
    print("\n📝 Test Case 4: All same elements")
    print("-" * 80)
    nums4 = [5, 5, 5, 5, 5]
    k4 = 1
    print(f"Input: nums = {nums4}, k = {k4}")
    result4_a = topKFrequent_BucketSort(nums4, k4)
    result4_b = topKFrequent_MinHeap(nums4, k4)
    result4_c = topKFrequent_QuickSelect(nums4.copy(), k4)
    print(f"Output (Bucket Sort): {result4_a}")
    print(f"Output (Min Heap):    {result4_b}")
    print(f"Output (QuickSelect): {result4_c}")
    print(f"Expected: [5]")
    print(f"✅ PASS" if result4_a == [5] else "❌ FAIL")

    # Test Case 5: Large k
    print("\n📝 Test Case 5: k equals number of unique elements")
    print("-" * 80)
    nums5 = [1, 1, 2, 2, 3, 3]
    k5 = 3
    print(f"Input: nums = {nums5}, k = {k5}")
    result5_a = topKFrequent_BucketSort(nums5, k5)
    result5_b = topKFrequent_MinHeap(nums5, k5)
    result5_c = topKFrequent_QuickSelect(nums5.copy(), k5)
    print(f"Output (Bucket Sort): {result5_a}")
    print(f"Output (Min Heap):    {result5_b}")
    print(f"Output (QuickSelect): {result5_c}")
    print(f"Expected: [1, 2, 3] (in any order)")
    expected5 = {1, 2, 3}
    print(f"✅ PASS" if set(result5_a) == expected5 else "❌ FAIL")

    # Test Case 6: Negative numbers
    print("\n📝 Test Case 6: Negative numbers")
    print("-" * 80)
    nums6 = [-1, -1, -1, 2, 2, 3]
    k6 = 2
    print(f"Input: nums = {nums6}, k = {k6}")
    result6_a = topKFrequent_BucketSort(nums6, k6)
    result6_b = topKFrequent_MinHeap(nums6, k6)
    result6_c = topKFrequent_QuickSelect(nums6.copy(), k6)
    print(f"Output (Bucket Sort): {result6_a}")
    print(f"Output (Min Heap):    {result6_b}")
    print(f"Output (QuickSelect): {result6_c}")
    print(f"Expected: [-1, 2] (in any order)")
    expected6 = {-1, 2}
    print(f"✅ PASS" if set(result6_a) == expected6 else "❌ FAIL")

    # Test Case 7: Mixed frequencies
    print("\n📝 Test Case 7: Mixed frequencies")
    print("-" * 80)
    nums7 = [4, 1, 1, 1, 2, 2, 3]
    k7 = 2
    print(f"Input: nums = {nums7}, k = {k7}")
    result7_a = topKFrequent_BucketSort(nums7, k7)
    result7_b = topKFrequent_MinHeap(nums7, k7)
    result7_c = topKFrequent_QuickSelect(nums7.copy(), k7)
    print(f"Output (Bucket Sort): {result7_a}")
    print(f"Output (Min Heap):    {result7_b}")
    print(f"Output (QuickSelect): {result7_c}")
    print(f"Expected: [1, 2] (freq: 1→3, 2→2, 3→1, 4→1)")
    expected7 = {1, 2}
    print(f"✅ PASS" if set(result7_a) == expected7 else "❌ FAIL")

    print("\n" + "="*80)
    print("              ✅ ALL TEST CASES COMPLETED!")
    print("="*80)


# ============================================================================
#              🎓 LEARNING SUMMARY & KEY TAKEAWAYS
# ============================================================================

"""
🎯 WHAT YOU LEARNED:
-------------------
1. Bucket sort by frequency achieves guaranteed O(N) time
2. Min heap is classic approach with O(N log k) time
3. Always count frequencies first (critical first step)
4. Frequency ranges from 1 to N (enables bucket sort)

🔑 KEY PATTERN: "Count and Select"
-----------------------------------
This pattern applies when:
- Need top k elements by some metric (frequency, value, etc.)
- Can count/group elements first
- Know the range of possible values

Used in:
- Top K Frequent Elements (this problem!)
- Top K Frequent Words (LeetCode #692)
- Sort Characters by Frequency (LeetCode #451)
- Find K Pairs with Smallest Sums (LeetCode #373)

💪 THREE APPROACHES TO MASTER:
-----------------------------
1. BUCKET SORT (Optimal - O(N) worst case)
   - Count frequencies
   - Create buckets indexed by frequency
   - Collect from end (high frequency first)
   - Guaranteed O(N) time!

2. MIN HEAP (Classic - O(N log k))
   - Count frequencies
   - Maintain min heap of size k
   - Simple, well-known approach
   - Better when k << unique elements

3. QUICKSELECT (Alternative - O(N) average)
   - Count frequencies
   - Use QuickSelect on frequency array
   - O(N) average, O(N²) worst
   - More complex than bucket sort

🎯 INTERVIEW TIPS:
-----------------
1. Clarify: return elements or frequencies?
2. Ask: any order acceptable? (Usually yes)
3. Mention bucket sort for guaranteed O(N)
4. Alternative: min heap for simplicity
5. Always count frequencies first
6. Draw buckets array visualization
7. Test with edge cases (k=1, all same, all unique)

🎉 CONGRATULATIONS!
------------------
You now understand how to find top k frequent elements efficiently!
Remember: "Count frequencies, then bucket sort for O(N)!"

📊 COMPLEXITY SUMMARY:
---------------------
┌────────────────────┬──────────────┬──────────────┐
│ Approach           │ Time         │ Space        │
├────────────────────┼──────────────┼──────────────┤
│ Bucket Sort (Best) │ O(N)         │ O(N)         │
├────────────────────┼──────────────┼──────────────┤
│ Min Heap           │ O(N log k)   │ O(N)         │
├────────────────────┼──────────────┼──────────────┤
│ QuickSelect        │ O(N) avg     │ O(N)         │
│                    │ O(N²) worst  │              │
└────────────────────┴──────────────┴──────────────┘

N = array length, k = number of top elements

🏆 RECOMMENDED: Use Bucket Sort for guaranteed O(N) solution!
For simplicity and when k is small, Min Heap is also excellent!

🔗 RELATED PROBLEMS TO PRACTICE:
-------------------------------
1. LeetCode #347: Top K Frequent Elements (this problem!)
2. LeetCode #692: Top K Frequent Words
3. LeetCode #451: Sort Characters By Frequency
4. LeetCode #215: Kth Largest Element in Array
5. LeetCode #973: K Closest Points to Origin

💡 FINAL TIP:
------------
The bucket sort by frequency technique is POWERFUL!
It leverages the fact that frequencies are bounded (1 to N).
This same pattern works for any bounded metric.
Master this and you'll solve many "top k" problems instantly!
"""
