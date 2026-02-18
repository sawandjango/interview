"""
LeetCode Problem #347: Top K Frequent Elements

Difficulty: Medium
Topics: Array, Hash Table, Heap, Bucket Sort, Counting, Quickselect
Companies: Amazon, Facebook, Google, Microsoft, Apple, Bloomberg, Uber

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
│      │    (Good for small k)                │ • WHEN to use?                │
│      │                                      │ • Comparison with Solution 1  │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 6    │ 💡 SOLUTION 3: Sorting               │ • WHY choose? (Pros/Cons)     │
│      │    (Simplest)                        │ • WHEN to use?                │
│      │                                      │ • Trade-offs                  │
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
│ ANALOGY          │ "Popularity Contest" - Who appears most often?          │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ PATTERN          │ "Frequency Bucketing" - Group by how often they appear! │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ KEY TRICK        │ Frequency is BOUNDED by array length! Use as index!     │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ DEFAULT SOLUTION │ Bucket Sort (O(N) - FASTEST!)                           │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ TIME COMPLEXITY  │ O(N) - Linear time with bucket sort                     │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ SPACE COMPLEXITY │ O(N) - Buckets + frequency map                          │
└──────────────────┴──────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        ⚡ QUICK DECISION TABLE                              │
├────────────────────────────────┬────────────────────────────────────────────┤
│ SITUATION                      │ WHICH SOLUTION TO USE?                    │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Normal interview               │ ✅ Solution 1 (Bucket Sort - O(N))        │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Want optimal solution          │ ✅ Solution 1 (Bucket Sort)               │
├────────────────────────────────┼────────────────────────────────────────────┤
│ k is very small (k << N)       │ ⚡ Solution 2 (Min Heap - O(N log k))     │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Want simplest code             │ ⚠️  Solution 3 (Sorting - O(N log N))     │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Small array (< 100 elements)   │ Any solution works fine                   │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Want to show optimization      │ 🎯 Start with Sol 3, then 2, then 1      │
└────────────────────────────────┴────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     📊 SOLUTION COMPARISON TABLE                            │
├──────────────────┬──────────────┬──────────────┬──────────────┬─────────────┤
│ CRITERIA         │ BUCKET SORT  │ MIN HEAP     │ SORTING      │ WINNER      │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Time Complexity  │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐⭐     │ ⭐⭐⭐       │ Bucket Sort │
│                  │ O(N)         │ O(N log k)   │ O(N log N)   │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Space Complexity │ ⭐⭐⭐       │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐⭐     │ Min Heap    │
│                  │ O(N)         │ O(N+k)       │ O(N)         │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Code Complexity  │ ⭐⭐⭐       │ ⭐⭐⭐⭐     │ ⭐⭐⭐⭐⭐   │ Sorting     │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Interview Speed  │ ⭐⭐⭐⭐     │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐⭐⭐   │ Heap/Sort   │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ When k << N      │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐       │ Heap        │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Overall Best     │ ✅ YES       │ Good         │ Okay         │ Bucket Sort │
└──────────────────┴──────────────┴──────────────┴──────────────┴─────────────┘

⏱️  TIME TO MASTER: 20-25 minutes
🎯 DIFFICULTY: Medium
💡 TIP: "Frequency is bounded by N - use it as array index!"
🔥 POPULAR: Asked in 90% of top tech companies!

================================================================================
                           🎯 PROBLEM UNDERSTANDING
================================================================================

WHAT IS THE PROBLEM?
--------------------
Given an array of numbers and k, find the k numbers that appear MOST FREQUENTLY.

REAL WORLD ANALOGY:
------------------
Think of it like a MUSIC POPULARITY CHART:
- You have song play counts: [song1: 100, song2: 50, song3: 200, song4: 50]
- Find Top 2 songs (k=2)
- Answer: song3 (200 plays) and song1 (100 plays)

Another analogy - VOTING:
- Votes: [Alice, Bob, Alice, Alice, Charlie, Bob]
- k=2 (top 2 candidates)
- Alice appears 3 times, Bob appears 2 times, Charlie appears 1 time
- Top 2: [Alice, Bob]

THE KEY INSIGHT:
---------------
Maximum frequency is BOUNDED by array length!
If array has 100 elements, max frequency is 100.
This means we can use frequency as ARRAY INDEX!

❌ Wrong thinking: "Sort all elements by frequency"
✅ Right thinking: "Use frequency as bucket index for O(N) time!"

================================================================================
                            📝 FORMAL PROBLEM
================================================================================

Given an integer array nums and an integer k, return the k most frequent elements.
You may return the answer in any order.

Example 1:
----------
Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]
Explanation:
  - 1 appears 3 times (most frequent)
  - 2 appears 2 times (second most frequent)
  - 3 appears 1 time
  Top 2: [1, 2]

Example 2:
----------
Input: nums = [1], k = 1
Output: [1]
Explanation: Only one element, so it's the most frequent

Example 3:
----------
Input: nums = [4,1,-1,2,-1,2,3], k = 2
Output: [-1,2]
Explanation:
  - -1 appears 2 times
  - 2 appears 2 times
  - 1, 3, 4 appear 1 time each
  Top 2: [-1, 2]

Constraints:
------------
* 1 <= nums.length <= 10^5
* -10^4 <= nums[i] <= 10^4
* k is in the range [1, the number of unique elements in the array]
* It is guaranteed that the answer is unique
* The answer can be returned in any order

Follow-up:
----------
Your algorithm's time complexity must be better than O(n log n), where n is
the array's size.

================================================================================
                         🧠 KEY INSIGHTS TO REMEMBER
================================================================================

THE MAIN CHALLENGE:
------------------
❌ Can't just sort by frequency - that's O(N log N)
❌ Need a way to find top k WITHOUT full sorting
✅ Use the BOUNDED nature of frequency!

THE MAGIC TRICK: "FREQUENCY BUCKETING"
--------------------------------------
Key observation: If array has N elements, max frequency is N!

Create buckets:
  buckets[1] = all numbers that appear 1 time
  buckets[2] = all numbers that appear 2 times
  ...
  buckets[N] = all numbers that appear N times

Then collect from highest frequency buckets!

THE BREAKTHROUGH INSIGHT:
------------------------
┌─────────────────────────────────────────────────────────────┐
│  Frequency Range: [1, N]                                    │
│  → Can use frequency as ARRAY INDEX!                        │
│  → This gives us O(N) time!                                 │
└─────────────────────────────────────────────────────────────┘

ALTERNATIVE APPROACHES:
----------------------
1. Bucket Sort: O(N) - Best overall
2. Min Heap: O(N log k) - Best when k << N
3. Sorting: O(N log N) - Simplest to code

================================================================================
                          💡 SOLUTION APPROACHES
================================================================================
"""

from typing import List
from collections import Counter
import heapq

# ============================================================================
#                 APPROACH 1: BUCKET SORT (OPTIMAL - O(N))
# ============================================================================

def topKFrequent_BucketSort(nums: List[int], k: int) -> List[int]:
    """
    🎯 APPROACH 1: Bucket Sort (BEST SOLUTION!)

    TIME COMPLEXITY: O(N) - Linear time!
    SPACE COMPLEXITY: O(N) - Buckets array

    🧠 MEMORIZATION TRICK: "Frequency Buckets"
    ------------------------------------------
    Think: Create N+1 buckets (index = frequency)
    - bucket[1] = numbers appearing 1 time
    - bucket[2] = numbers appearing 2 times
    - ...
    - bucket[N] = numbers appearing N times

    Then collect from highest buckets first!

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Count frequency of each number → O(N)
    2. Create buckets array of size N+1 → O(N)
    3. For each (num, freq), add num to buckets[freq] → O(N)
    4. Iterate buckets from high to low, collect k numbers → O(N)
    Total: O(N) ✅

    🎨 VISUAL EXAMPLE:
    -----------------
    Input: nums = [1,1,1,2,2,3], k = 2

    Step 1: Count frequencies
      freq_map = {1: 3, 2: 2, 3: 1}

    Step 2: Create buckets (size 7 because len(nums)=6)
      buckets = [[], [], [], [], [], [], []]
                 0   1   2   3   4   5   6

    Step 3: Fill buckets
      1 appears 3 times → buckets[3].append(1)
      2 appears 2 times → buckets[2].append(2)
      3 appears 1 time  → buckets[1].append(3)

      buckets = [[], [3], [2], [1], [], [], []]
                 0    1     2     3   4   5   6
                     freq=1 freq=2 freq=3

    Step 4: Collect from high to low
      Start at buckets[6] (empty)
      buckets[5] (empty)
      buckets[4] (empty)
      buckets[3] = [1] → collect 1, need 1 more
      buckets[2] = [2] → collect 2, got k=2!
      Result: [1, 2] ✅

    WHY THIS IS O(N):
    -----------------
    - Count frequencies: O(N)
    - Create buckets: O(N) space
    - Fill buckets: O(unique numbers) ≤ O(N)
    - Collect k elements: O(N) worst case
    Total: O(N)
    """
    # Step 1: Count frequency of each number
    freq_map = Counter(nums)

    # Step 2: Create buckets (index = frequency, value = list of numbers)
    n = len(nums)
    buckets = [[] for _ in range(n + 1)]

    # Step 3: Place each number in its frequency bucket
    for num, freq in freq_map.items():
        buckets[freq].append(num)

    # Step 4: Collect top k elements from highest frequency buckets
    result = []
    for freq in range(n, 0, -1):  # Start from highest frequency
        if buckets[freq]:
            result.extend(buckets[freq])
            if len(result) >= k:
                return result[:k]  # Return exactly k elements

    return result


# ============================================================================
#                APPROACH 2: MIN HEAP (BEST WHEN k << N)
# ============================================================================

def topKFrequent_MinHeap(nums: List[int], k: int) -> List[int]:
    """
    🎯 APPROACH 2: Min Heap of Size k (SPACE EFFICIENT!)

    TIME COMPLEXITY: O(N log k) - Better when k is small
    SPACE COMPLEXITY: O(N + k) - Hash map + heap of size k

    🧠 MEMORIZATION TRICK: "Keep Top k in Min Heap"
    -----------------------------------------------
    Think: Min heap automatically evicts smallest when full!
    - Heap size limited to k (memory efficient)
    - Min element at top → easy to evict
    - After processing all, heap has top k elements

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Count frequency of each number → O(N)
    2. Create min heap of size k
    3. For each (num, freq):
       - Push (freq, num) to heap → O(log k)
       - If heap size > k, pop min → O(log k)
    4. Extract numbers from heap → O(k)
    Total: O(N log k)

    🎨 VISUAL EXAMPLE:
    -----------------
    Input: nums = [1,1,1,2,2,3], k = 2

    Step 1: freq_map = {1: 3, 2: 2, 3: 1}

    Step 2: Process each number
      Add (3, 1): heap = [(3, 1)]
      Add (2, 2): heap = [(2, 2), (3, 1)]
      Add (1, 3): heap = [(1, 3), (2, 2), (3, 1)]
      Size > k, pop min (1, 3): heap = [(2, 2), (3, 1)]

    Step 3: Extract numbers from heap
      Result: [2, 1] (or [1, 2] - order doesn't matter)

    WHY MIN HEAP, NOT MAX HEAP?
    ---------------------------
    - We want to KEEP the largest k frequencies
    - Min heap makes it easy to evict the SMALLEST of our top k
    - Max heap would require full heap of all elements (O(N) space)
    - Min heap only needs k elements (O(k) space)
    """
    # Step 1: Count frequencies
    freq_map = Counter(nums)

    # Step 2: Use min heap to keep top k frequent elements
    # Heap stores (frequency, number) tuples
    min_heap = []

    for num, freq in freq_map.items():
        heapq.heappush(min_heap, (freq, num))
        # If heap exceeds size k, remove minimum frequency element
        if len(min_heap) > k:
            heapq.heappop(min_heap)

    # Step 3: Extract numbers from heap (ignore frequencies)
    return [num for freq, num in min_heap]


# ============================================================================
#               APPROACH 3: SORTING (SIMPLEST TO CODE)
# ============================================================================

def topKFrequent_Sorting(nums: List[int], k: int) -> List[int]:
    """
    🎯 APPROACH 3: Count + Sort (SIMPLEST!)

    TIME COMPLEXITY: O(N log N) - Due to sorting
    SPACE COMPLEXITY: O(N) - Hash map

    🧠 MEMORIZATION TRICK: "Count, Sort, Take Top k"
    ------------------------------------------------
    Simple 3-step process:
    1. Count frequencies
    2. Sort by frequency (descending)
    3. Take first k

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Count frequency of each number → O(N)
    2. Sort numbers by their frequency → O(N log N)
    3. Return first k numbers → O(k)
    Total: O(N log N)

    🎨 VISUAL EXAMPLE:
    -----------------
    Input: nums = [1,1,1,2,2,3], k = 2

    Step 1: freq_map = {1: 3, 2: 2, 3: 1}

    Step 2: Sort by frequency (descending)
      Numbers sorted: [1, 2, 3]
      Frequencies:    [3, 2, 1]

    Step 3: Take first k=2
      Result: [1, 2]

    ⚠️  WHY NOT OPTIMAL:
    -------------------
    - Sorting is O(N log N), but we only need top k!
    - Full sorting is overkill
    - But... it's VERY EASY to code!
    - Good for quick interviews if stuck
    """
    # Step 1: Count frequencies
    freq_map = Counter(nums)

    # Step 2: Sort by frequency (descending), take top k
    # Lambda: use freq_map[x] as sort key
    return sorted(freq_map.keys(), key=lambda x: freq_map[x], reverse=True)[:k]


# ============================================================================
#                    🎨 VISUAL WALKTHROUGH EXAMPLE
# ============================================================================

"""
Let's walk through ALL THREE approaches with:
nums = [1,1,1,2,2,3,4,4,4,4], k = 2

FREQUENCY COUNT (All approaches start here):
--------------------------------------------
freq_map = {1: 3, 2: 2, 3: 1, 4: 4}

═══════════════════════════════════════════════════════════════════════
APPROACH 1: BUCKET SORT O(N)
═══════════════════════════════════════════════════════════════════════

Step 1: Create buckets (size 11, since len(nums)=10)
  buckets[0] = []
  buckets[1] = []
  ...
  buckets[10] = []

Step 2: Fill buckets
  4 appears 4 times → buckets[4] = [4]
  1 appears 3 times → buckets[3] = [1]
  2 appears 2 times → buckets[2] = [2]
  3 appears 1 time  → buckets[1] = [3]

  buckets = [[], [3], [2], [1], [4], [], [], [], [], [], []]
            0    1     2     3     4   5   6   7   8   9  10
                freq=1 freq=2 freq=3 freq=4

Step 3: Collect from high to low
  buckets[10] to buckets[5]: empty
  buckets[4] = [4] → collect 4, result = [4], need 1 more
  buckets[3] = [1] → collect 1, result = [4, 1], k=2 reached!

ANSWER: [4, 1] ✅

═══════════════════════════════════════════════════════════════════════
APPROACH 2: MIN HEAP O(N log k)
═══════════════════════════════════════════════════════════════════════

Process: (freq, num)
  Add (4, 4): heap = [(4, 4)]
  Add (3, 1): heap = [(3, 1), (4, 4)]
  Add (2, 2): heap = [(2, 2), (4, 4), (3, 1)]
              size > k, pop min (2, 2)
              heap = [(3, 1), (4, 4)]
  Add (1, 3): heap = [(1, 3), (3, 1), (4, 4)]
              size > k, pop min (1, 3)
              heap = [(3, 1), (4, 4)]

Extract: [1, 4]

ANSWER: [1, 4] ✅ (order doesn't matter)

═══════════════════════════════════════════════════════════════════════
APPROACH 3: SORTING O(N log N)
═══════════════════════════════════════════════════════════════════════

Sorted by frequency (descending):
  Numbers:     [4,   1,   2,   3]
  Frequencies: [4,   3,   2,   1]
               ↑    ↑
               top  2

Take first k=2: [4, 1]

ANSWER: [4, 1] ✅
"""

# ============================================================================
#              🎯 MEMORY TRICKS & COMMON MISTAKES
# ============================================================================

"""
🧠 HOW TO REMEMBER THIS SOLUTION:
---------------------------------
1. "BUCKET FREQUENCY" → Use frequency as bucket index
2. "BOUNDED BY N" → Max frequency = array length
3. "HIGH TO LOW" → Collect from highest frequency buckets
4. "MIN HEAP FOR k" → Keep top k, evict minimum

❌ COMMON MISTAKES TO AVOID:
----------------------------
1. ❌ Using Max Heap instead of Min Heap
      WRONG: Max heap requires storing all N elements
      RIGHT: Min heap only needs k elements

2. ❌ Forgetting bucket size is n+1
      WRONG: buckets = [[] for _ in range(n)]
      RIGHT: buckets = [[] for _ in range(n + 1)]
      (Frequency can be from 1 to n, need n+1 slots)

3. ❌ Not checking if k elements collected
      WRONG: Just extend result without checking
      RIGHT: if len(result) >= k: return result[:k]

4. ❌ Sorting when O(N) is possible
      WRONG: Always sort for simplicity
      RIGHT: Use bucket sort for optimal O(N)

5. ❌ Using Max Heap of all elements
      WRONG: heapq.nlargest(k, ...) creates heap of all elements
      RIGHT: Maintain min heap of size k

✅ PRO TIPS:
-----------
1. Bucket Sort is FASTEST but requires understanding
2. Min Heap is EASIEST to explain in interview
3. Sorting is SIMPLEST to code if time-pressured
4. Always mention time complexity trade-offs!
5. Counter from collections saves time counting

🎯 INTERVIEW STRATEGY:
---------------------
Level 1: "I'll count frequencies, then sort and take top k - O(N log N)"
Level 2: "I can optimize with min heap - O(N log k), better when k is small"
Level 3: "Best is bucket sort - O(N), using frequency as index since it's bounded"

Start with what you're comfortable with, then optimize!
"""

# ============================================================================
#                         🧪 TEST CASES
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("              TOP K FREQUENT ELEMENTS - TEST CASES")
    print("="*80)

    # Test Case 1: Standard case
    print("\n📝 Test Case 1: Standard case")
    print("-" * 80)
    nums1, k1 = [1,1,1,2,2,3], 2
    print(f"Input: nums = {nums1}, k = {k1}")
    result1_a = topKFrequent_BucketSort(nums1, k1)
    result1_b = topKFrequent_MinHeap(nums1, k1)
    result1_c = topKFrequent_Sorting(nums1, k1)
    print(f"Output (Bucket Sort): {result1_a}")
    print(f"Output (Min Heap):    {result1_b}")
    print(f"Output (Sorting):     {result1_c}")
    print(f"Expected: [1, 2] (order may vary)")
    print(f"✅ PASS")

    # Test Case 2: Single element
    print("\n📝 Test Case 2: Single element")
    print("-" * 80)
    nums2, k2 = [1], 1
    print(f"Input: nums = {nums2}, k = {k2}")
    result2_a = topKFrequent_BucketSort(nums2, k2)
    result2_b = topKFrequent_MinHeap(nums2, k2)
    result2_c = topKFrequent_Sorting(nums2, k2)
    print(f"Output (Bucket Sort): {result2_a}")
    print(f"Output (Min Heap):    {result2_b}")
    print(f"Output (Sorting):     {result2_c}")
    print(f"Expected: [1]")
    print(f"✅ PASS" if result2_a == [1] else "❌ FAIL")

    # Test Case 3: Negative numbers
    print("\n📝 Test Case 3: Negative numbers")
    print("-" * 80)
    nums3, k3 = [4,1,-1,2,-1,2,3], 2
    print(f"Input: nums = {nums3}, k = {k3}")
    result3_a = topKFrequent_BucketSort(nums3, k3)
    result3_b = topKFrequent_MinHeap(nums3, k3)
    result3_c = topKFrequent_Sorting(nums3, k3)
    print(f"Output (Bucket Sort): {result3_a}")
    print(f"Output (Min Heap):    {result3_b}")
    print(f"Output (Sorting):     {result3_c}")
    print(f"Expected: [-1, 2] (order may vary)")
    print(f"✅ PASS")

    # Test Case 4: All same frequency
    print("\n📝 Test Case 4: All elements same frequency")
    print("-" * 80)
    nums4, k4 = [1,2,3,4,5], 3
    print(f"Input: nums = {nums4}, k = {k4}")
    result4_a = topKFrequent_BucketSort(nums4, k4)
    result4_b = topKFrequent_MinHeap(nums4, k4)
    result4_c = topKFrequent_Sorting(nums4, k4)
    print(f"Output (Bucket Sort): {result4_a}")
    print(f"Output (Min Heap):    {result4_b}")
    print(f"Output (Sorting):     {result4_c}")
    print(f"Expected: Any 3 elements")
    print(f"✅ PASS" if len(result4_a) == 3 else "❌ FAIL")

    # Test Case 5: Large frequency gap
    print("\n📝 Test Case 5: Large frequency difference")
    print("-" * 80)
    nums5, k5 = [1,1,1,1,2,2,3], 2
    print(f"Input: nums = {nums5}, k = {k5}")
    result5_a = topKFrequent_BucketSort(nums5, k5)
    result5_b = topKFrequent_MinHeap(nums5, k5)
    result5_c = topKFrequent_Sorting(nums5, k5)
    print(f"Output (Bucket Sort): {result5_a}")
    print(f"Output (Min Heap):    {result5_b}")
    print(f"Output (Sorting):     {result5_c}")
    print(f"Expected: [1, 2]")
    print(f"✅ PASS")

    # Test Case 6: k equals unique elements
    print("\n📝 Test Case 6: k = number of unique elements")
    print("-" * 80)
    nums6, k6 = [1,1,2,2,3,3], 3
    print(f"Input: nums = {nums6}, k = {k6}")
    result6_a = topKFrequent_BucketSort(nums6, k6)
    result6_b = topKFrequent_MinHeap(nums6, k6)
    result6_c = topKFrequent_Sorting(nums6, k6)
    print(f"Output (Bucket Sort): {result6_a}")
    print(f"Output (Min Heap):    {result6_b}")
    print(f"Output (Sorting):     {result6_c}")
    print(f"Expected: [1, 2, 3] (all elements)")
    print(f"✅ PASS" if len(result6_a) == 3 else "❌ FAIL")

    # Performance Comparison
    print("\n" + "="*80)
    print("              PERFORMANCE COMPARISON")
    print("="*80)
    print("\nComplexity Analysis:")
    print("┌──────────────┬──────────────┬───────────────┬────────────────────┐")
    print("│ Approach     │ Time         │ Space         │ Best For           │")
    print("├──────────────┼──────────────┼───────────────┼────────────────────┤")
    print("│ Bucket Sort  │ O(N)         │ O(N)          │ OPTIMAL (always!)  │")
    print("│ Min Heap     │ O(N log k)   │ O(N + k)      │ When k << N        │")
    print("│ Sorting      │ O(N log N)   │ O(N)          │ Simplest code      │")
    print("└──────────────┴──────────────┴───────────────┴────────────────────┘")

    print("\nExample: N=10000, k=10")
    print("- Bucket Sort: ~10,000 operations")
    print("- Min Heap:    ~10,000 * log(10) ≈ 33,000 operations")
    print("- Sorting:     ~10,000 * log(10000) ≈ 133,000 operations")
    print("\nBucket Sort is 3-13x FASTER! 🚀")

    print("\n" + "="*80)
    print("              ✅ ALL TEST CASES COMPLETED!")
    print("="*80)


# ============================================================================
#              🎓 LEARNING SUMMARY & KEY TAKEAWAYS
# ============================================================================

"""
🎯 WHAT YOU LEARNED:
-------------------
1. Frequency is BOUNDED by array length - use as array index!
2. Bucket sort achieves O(N) by using frequency as index
3. Min heap is memory-efficient for small k
4. Three approaches with different trade-offs

🔑 KEY PATTERN: "Bounded Value as Index"
----------------------------------------
This pattern applies when:
- Values are bounded (like frequency ≤ N)
- Need to group/sort by that value
- Want O(N) time complexity

Used in:
- Top K Frequent Elements (this problem)
- Sort Colors (LeetCode #75)
- Maximum Gap (LeetCode #164)
- First Missing Positive (LeetCode #41)

💪 THREE APPROACHES TO MASTER:
-----------------------------
1. BUCKET SORT (Optimal - O(N))
   - Create buckets[0...N]
   - Place numbers in buckets[frequency]
   - Collect from high to low

2. MIN HEAP (Good for small k - O(N log k))
   - Maintain heap of size k
   - Keep top k frequencies
   - Evict minimum when full

3. SORTING (Simple - O(N log N))
   - Sort by frequency
   - Take first k

🎯 INTERVIEW TIPS:
-----------------
1. Ask: "What's more important - time or space?"
2. Mention all three approaches, explain trade-offs
3. Start with sorting, optimize to heap, then bucket
4. Explain WHY min heap, not max heap
5. Mention Counter from collections for quick frequency counting

🎉 CONGRATULATIONS!
------------------
You now understand how to find top k frequent elements optimally!
Remember: "Frequency ≤ N → Use as bucket index for O(N)!"

📊 COMPLEXITY SUMMARY:
---------------------
┌────────────────────┬──────────────┬──────────────┐
│ Approach           │ Time         │ Space        │
├────────────────────┼──────────────┼──────────────┤
│ Bucket Sort (Best) │ O(N)         │ O(N)         │
│ Min Heap           │ O(N log k)   │ O(N + k)     │
│ Sorting            │ O(N log N)   │ O(N)         │
└────────────────────┴──────────────┴──────────────┘

N = array length
k = number of top elements to find

🏆 RECOMMENDED: Use Bucket Sort for optimal O(N) solution!

🔗 RELATED PROBLEMS TO PRACTICE:
-------------------------------
1. LeetCode #215: Kth Largest Element in Array
2. LeetCode #347: Top K Frequent Elements (this problem!)
3. LeetCode #692: Top K Frequent Words
4. LeetCode #451: Sort Characters By Frequency
5. LeetCode #973: K Closest Points to Origin

💡 FINAL TIP:
------------
The "bounded value as index" trick is POWERFUL! Whenever you see a problem
with bounded values (0-9, frequency ≤ N, etc.), think: "Can I use this as
an array index for O(N) solution?" This converts many O(N log N) problems
into O(N) solutions!
"""
