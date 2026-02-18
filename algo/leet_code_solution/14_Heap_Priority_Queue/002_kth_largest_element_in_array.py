"""
LeetCode Problem #215: Kth Largest Element in an Array

Difficulty: Medium
Topics: Array, Divide and Conquer, Sorting, Heap (Priority Queue), Quickselect
Companies: Facebook, Amazon, Microsoft, Google, Apple, Bloomberg, Adobe, Uber, LinkedIn

https://www.youtube.com/watch?v=Lk-QYXyPL3g

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
│ 4    │ 💡 SOLUTION 1: QuickSelect ⭐        │ • WHY choose? (Pros/Cons)     │
│      │    (OPTIMAL - O(N) average)          │ • WHEN to use?                │
│      │                                      │ • Step-by-step walkthrough    │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 5    │ 💡 SOLUTION 2: Min Heap              │ • WHY choose? (Pros/Cons)     │
│      │    (O(N log k) - Good!)              │ • WHEN to use?                │
│      │                                      │ • Comparison with Solution 1  │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 6    │ 💡 SOLUTION 3: Sorting               │ • WHY choose? (Pros/Cons)     │
│      │    (Simple but O(N log N))           │ • WHEN to use?                │
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
│ ANALOGY          │ "Find Kth Winner" - Partition & conquer!               │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ PATTERN          │ "QuickSelect" - Partition like QuickSort, search one!  │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ KEY TRICK        │ After partition, only recurse on ONE side!             │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ DEFAULT SOLUTION │ QuickSelect (O(N) average - BEST!)                     │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ TIME COMPLEXITY  │ O(N) average, O(N²) worst (QuickSelect)                │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ SPACE COMPLEXITY │ O(1) - In-place partitioning                           │
└──────────────────┴──────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        ⚡ QUICK DECISION TABLE                              │
├────────────────────────────────────┬────────────────────────────────────────┤
│ SITUATION                          │ WHICH SOLUTION TO USE?                │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Normal interview (want best)       │ ✅ Solution 1 (QuickSelect)           │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Need optimal O(N) average          │ ✅ Solution 1 (QuickSelect!)          │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Small k (k << N)                   │ ⚡ Solution 2 (Min Heap O(N log k))   │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Want simplest code                 │ ⚠️  Solution 3 (Sorting)              │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Learning divide & conquer          │ 🎓 Solution 1 (QuickSelect pattern)  │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Want to show optimization          │ 🎯 Start with Sol 3, optimize to 1   │
└────────────────────────────────────┴────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     📊 SOLUTION COMPARISON TABLE                            │
├──────────────────┬──────────────┬──────────────┬──────────────┬─────────────┤
│ CRITERIA         │ QUICKSELECT  │ MIN HEAP     │ SORTING      │ WINNER      │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Time: Average    │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐⭐     │ ⭐⭐⭐       │ QuickSelect │
│                  │ O(N)         │ O(N log k)   │ O(N log N)   │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Time: Worst      │ ⭐⭐         │ ⭐⭐⭐⭐     │ ⭐⭐⭐       │ Min Heap    │
│                  │ O(N²)        │ O(N log k)   │ O(N log N)   │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Space Complexity │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐⭐     │ ⭐⭐⭐⭐⭐   │ QuickSelect │
│                  │ O(1)         │ O(k)         │ O(1)         │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Code Simplicity  │ ⭐⭐⭐       │ ⭐⭐⭐⭐     │ ⭐⭐⭐⭐⭐   │ Sorting     │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ When k is small  │ ⭐⭐⭐⭐     │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐       │ Min Heap    │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Overall Best     │ ✅ OPTIMAL   │ Good         │ Simple       │ QuickSelect │
└──────────────────┴──────────────┴──────────────┴──────────────┴─────────────┘

⏱️  TIME TO MASTER: 25-30 minutes
🎯 DIFFICULTY: Medium (but teaches important divide & conquer!)
💡 TIP: "Partition like QuickSort, but only search ONE side!"
🔥 POPULAR: Asked in 90% of FAANG interviews!

================================================================================
                           🎯 PROBLEM UNDERSTANDING
================================================================================

WHAT IS THE PROBLEM?
--------------------
Given an unsorted array, find the kth LARGEST element. Note: not the kth distinct
element - duplicates count separately!

REAL WORLD ANALOGY:
------------------
Think of a RACE with runners:
- You have 100 runners with finish times: [3.2, 2.1, 4.5, 2.8, 3.9, ...]
- You want to find the 5th fastest time (5th largest)
- Don't need to fully sort all 100 runners!
- Just need to partition until you isolate the 5th position

Another analogy - SCHOLARSHIP SELECTION:
- 1000 students with GPAs
- Need to find cutoff for top 50 students (50th largest GPA)
- Don't need complete ranking, just the threshold!

THE KEY INSIGHT:
---------------
You DON'T need to sort the entire array!
Use QuickSelect (variant of QuickSort):
- Pick a pivot
- Partition: [larger than pivot] | pivot | [smaller than pivot]
- If pivot is at position k-1: FOUND!
- If pivot is right of k-1: search left partition
- If pivot is left of k-1: search right partition

❌ Wrong thinking: "Sort entire array and pick kth" → O(N log N)
✅ Right thinking: "Partition until pivot lands at position k-1" → O(N) average!

================================================================================
                            📝 FORMAL PROBLEM
================================================================================

Given an integer array nums and an integer k, return the kth largest element
in the array.

Note that it is the kth largest element in the sorted order, not the kth
distinct element.

Can you solve it without sorting?

Example 1:
----------
Input: nums = [3,2,1,5,6,4], k = 2
Output: 5
Explanation: When sorted [6,5,4,3,2,1], the 2nd largest is 5.

Example 2:
----------
Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4
Explanation: When sorted [6,5,5,4,3,3,2,2,1], the 4th largest is 4.

Constraints:
------------
* 1 <= k <= nums.length <= 10^5
* -10^4 <= nums[i] <= 10^4

Follow-up:
----------
Can you solve it in O(N) time complexity?

================================================================================
                         🧠 KEY INSIGHTS TO REMEMBER
================================================================================

THE MAIN CHALLENGE:
------------------
❌ Sorting works but takes O(N log N) - can we do better?
❌ Can't just scan for max k times - that's O(k*N)
✅ QuickSelect: partition-based selection in O(N) average!

THE MAGIC TRICK: "QUICKSELECT ALGORITHM"
----------------------------------------
Key observation: Similar to QuickSort, but only recurse on ONE side!

QuickSort: Recursively sort BOTH partitions
QuickSelect: Only recurse on partition containing kth element!

This reduces average time from O(N log N) to O(N)!

Example: Find 2nd largest in [3,2,1,5,6,4]
- Pick pivot = 4
- Partition: [5,6] | 4 | [3,2,1]
- Pivot at index 2, need index 1 (k=2, so k-1=1)
- Pivot is RIGHT of target → search LEFT partition [5,6]
- Pick pivot = 5
- Result: 5 is at index 1 → FOUND!

THE BREAKTHROUGH INSIGHT:
------------------------
┌─────────────────────────────────────────────────────────────┐
│  After each partition:                                      │
│  - Pivot is in its FINAL sorted position                    │
│  - All elements to its left are >= pivot (for kth largest)  │
│  - All elements to its right are < pivot                    │
│  → Only need to search ONE side! O(N) average!              │
└─────────────────────────────────────────────────────────────┘

WHY THIS IS O(N) ON AVERAGE:
-----------------------------
Best/Average case: Pivot divides array roughly in half each time
  N + N/2 + N/4 + N/8 + ... = 2N = O(N)

Worst case: Pivot is always min/max (bad partitioning)
  N + (N-1) + (N-2) + ... = O(N²)
  (Rare with random pivot selection!)

================================================================================
                          💡 SOLUTION APPROACHES
================================================================================
"""

from typing import List
import heapq
import random

# ============================================================================
#          APPROACH 1: QUICKSELECT (OPTIMAL - O(N) AVERAGE)
# ============================================================================

def findKthLargest_QuickSelect(nums: List[int], k: int) -> int:
    """
    🎯 APPROACH 1: QuickSelect Algorithm (BEST SOLUTION!)

    TIME COMPLEXITY: O(N) average, O(N²) worst
    SPACE COMPLEXITY: O(1) - In-place partitioning

    🧠 MEMORIZATION TRICK: "Partition Once, Search Once"
    ----------------------------------------------------
    Think: Like QuickSort, but only recurse on ONE side!
    - Partition array around pivot
    - Check if pivot is at position k-1
    - If yes → FOUND!
    - If no → Recurse on correct side only

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Pick a random pivot (to avoid worst case)
    2. Partition array: [larger] | pivot | [smaller]
    3. If pivot_index == k-1: return pivot
    4. If pivot_index > k-1: search left partition
    5. If pivot_index < k-1: search right partition
    6. Repeat until found

    🎨 VISUAL EXAMPLE:
    -----------------
    Input: nums = [3,2,1,5,6,4], k = 2

    Step 1: Pick pivot = 4, partition
      [5,6] | 4 | [3,2,1]
      indices: [0,1] | 2 | [3,4,5]

      Pivot at index 2, want index 1 (k-1 = 2-1 = 1)
      Pivot is RIGHT of target → search LEFT [5,6]

    Step 2: Search [5,6], pick pivot = 5
      [6] | 5 | []
      indices: [0] | 1 | []

      Pivot at index 1 → FOUND! Return 5 ✅

    WHY THIS IS O(N):
    -----------------
    Average case (good pivots):
      N + N/2 + N/4 + ... = 2N = O(N) ✅

    Worst case (bad pivots always):
      N + (N-1) + (N-2) + ... = O(N²) ❌
      (Very rare with random pivot!)
    """

    def partition(left: int, right: int, pivot_index: int) -> int:
        """
        Partition array around pivot.
        Returns final position of pivot.

        For kth LARGEST: arrange as [larger] | pivot | [smaller]
        """
        pivot_value = nums[pivot_index]

        # Move pivot to end
        nums[pivot_index], nums[right] = nums[right], nums[pivot_index]

        # Partition: move all elements >= pivot to left
        store_index = left
        for i in range(left, right):
            if nums[i] >= pivot_value:  # >= for kth largest
                nums[i], nums[store_index] = nums[store_index], nums[i]
                store_index += 1

        # Move pivot to final position
        nums[store_index], nums[right] = nums[right], nums[store_index]

        return store_index

    def quickselect(left: int, right: int, k_index: int) -> int:
        """
        QuickSelect: Find element that would be at k_index if sorted.
        k_index is 0-based (for kth largest, k_index = k-1)
        """
        if left == right:
            return nums[left]

        # Pick random pivot to avoid worst case
        pivot_index = random.randint(left, right)

        # Partition and get pivot's final position
        pivot_index = partition(left, right, pivot_index)

        # Check if we found it
        if pivot_index == k_index:
            return nums[pivot_index]
        elif pivot_index > k_index:
            # Target is in left partition
            return quickselect(left, pivot_index - 1, k_index)
        else:
            # Target is in right partition
            return quickselect(pivot_index + 1, right, k_index)

    # k-1 because we use 0-based indexing
    return quickselect(0, len(nums) - 1, k - 1)


# ============================================================================
#              APPROACH 2: MIN HEAP (O(N log k) - GOOD!)
# ============================================================================

def findKthLargest_MinHeap(nums: List[int], k: int) -> int:
    """
    🎯 APPROACH 2: Min Heap of Size K (GREAT FOR SMALL K!)

    TIME COMPLEXITY: O(N log k) - Better than O(N log N) when k << N
    SPACE COMPLEXITY: O(k) - Store only k largest elements

    🧠 MEMORIZATION TRICK: "Top K Winners Podium"
    ----------------------------------------------
    Same pattern as Problem #1 (Kth Largest in Stream)!
    - Keep min heap of size k
    - Heap contains k largest elements
    - Top of heap = smallest of k largest = kth largest!

    📝 ALGORITHM:
    ------------
    1. Build min heap of first k elements
    2. For remaining elements:
       - If element > heap top: replace top
       - Maintain heap size = k
    3. Return heap top (kth largest)

    🎨 DETAILED VISUAL WALKTHROUGH:
    ===============================
    Input: nums = [3, 2, 1, 5, 6, 4], k = 2
    Goal: Find 2nd largest element

    ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │ STEP 1: Initialize heap with first k=2 elements [3, 2]                                                                         │
    ├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
    │                                                                                                                                 │
    │   Array:  [3, 2, 1, 5, 6, 4]                                                                                                   │
    │            ─────                                                                                                                │
    │            Take first 2                                                                                                         │
    │                                                                                                                                 │
    │   Before heapify: [3, 2]                                                                                                       │
    │   After heapify:  [2, 3]  ← Min heap property: parent ≤ children                                                              │
    │                                                                                                                                 │
    │   📊 MIN HEAP STRUCTURE (Binary Tree View):                                                                                    │
    │                                                                                                                                 │
    │                        ┌─────────┐                                                                                             │
    │                        │    2    │  ← ROOT (index 0) - SMALLEST element                                                       │
    │                        └────┬────┘                                                                                             │
    │                             │                                                                                                  │
    │                             │                                                                                                  │
    │                        ┌────┴────┐                                                                                             │
    │                        │    3    │  ← Child (index 1)                                                                         │
    │                        └─────────┘                                                                                             │
    │                                                                                                                                 │
    │   📋 Array Representation: [2, 3]                                                                                              │
    │                             ↑  ↑                                                                                               │
    │                          idx 0  idx 1                                                                                          │
    │                          ROOT   CHILD                                                                                          │
    │                                                                                                                                 │
    │   💡 Why MIN heap for kth LARGEST?                                                                                             │
    │      ─────────────────────────────                                                                                             │
    │      Heap contains: [2, 3] (top 2 largest so far)                                                                              │
    │      Top element (2) = smallest of top 2 = 2nd largest!                                                                        │
    │                                                                                                                                 │
    │   ✅ Current state: heap = [2, 3], size = 2 = k                                                                                │
    │                                                                                                                                 │
    └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │ STEP 2: Process num = 1                                                                                                         │
    ├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
    │                                                                                                                                 │
    │   Current element: 1                                                                                                            │
    │   Heap before:     [2, 3]                                                                                                      │
    │                                                                                                                                 │
    │   ❓ Question: Is 1 > heap[0] (which is 2)?                                                                                    │
    │   ❌ Answer: NO! 1 < 2                                                                                                          │
    │                                                                                                                                 │
    │   💭 Decision: SKIP this element!                                                                                               │
    │      Why? Because 1 is smaller than the smallest element in our top-2,                                                         │
    │      so it can't be in the top 2 largest!                                                                                      │
    │                                                                                                                                 │
    │   📊 Heap UNCHANGED:                                                                                                            │
    │                        ┌─────────┐                                                                                             │
    │                        │    2    │  ← Still the smallest of top 2                                                             │
    │                        └────┬────┘                                                                                             │
    │                             │                                                                                                  │
    │                        ┌────┴────┐                                                                                             │
    │                        │    3    │                                                                                             │
    │                        └─────────┘                                                                                             │
    │                                                                                                                                 │
    │   ✅ Heap remains: [2, 3]                                                                                                      │
    │                                                                                                                                 │
    └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │ STEP 3: Process num = 5                                                                                                         │
    ├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
    │                                                                                                                                 │
    │   Current element: 5                                                                                                            │
    │   Heap before:     [2, 3]                                                                                                      │
    │                                                                                                                                 │
    │   ❓ Question: Is 5 > heap[0] (which is 2)?                                                                                    │
    │   ✅ Answer: YES! 5 > 2                                                                                                         │
    │                                                                                                                                 │
    │   💭 Decision: REPLACE heap top (2) with 5!                                                                                     │
    │      Why? 5 is larger than our current 2nd largest (2),                                                                        │
    │      so 5 belongs in the top 2!                                                                                                │
    │                                                                                                                                 │
    │   🔄 HEAP REPLACEMENT PROCESS:                                                                                                  │
    │                                                                                                                                 │
    │      Before heapreplace:                    After heapreplace:                                                                 │
    │                                                                                                                                 │
    │           ┌─────────┐                            ┌─────────┐                                                                   │
    │           │    2    │  ← Remove                  │    3    │  ← New root (heapify up)                                         │
    │           └────┬────┘                            └────┬────┘                                                                   │
    │                │                                      │                                                                        │
    │           ┌────┴────┐                            ┌────┴────┐                                                                   │
    │           │    3    │                            │    5    │  ← Inserted here                                                 │
    │           └─────────┘                            └─────────┘                                                                   │
    │                                                                                                                                 │
    │   📋 Array representation:                                                                                                      │
    │      Before: [2, 3]                                                                                                             │
    │      After:  [3, 5]  ← Heapified to maintain min heap property                                                                 │
    │               ↑  ↑                                                                                                              │
    │            ROOT CHILD                                                                                                           │
    │            (min) (larger)                                                                                                       │
    │                                                                                                                                 │
    │   💡 Insight: Heap now contains [3, 5] (top 2 largest so far)                                                                  │
    │               Top element (3) = 2nd largest among [3, 2, 1, 5]                                                                 │
    │                                                                                                                                 │
    │   ✅ New heap: [3, 5]                                                                                                           │
    │                                                                                                                                 │
    └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │ STEP 4: Process num = 6                                                                                                         │
    ├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
    │                                                                                                                                 │
    │   Current element: 6                                                                                                            │
    │   Heap before:     [3, 5]                                                                                                      │
    │                                                                                                                                 │
    │   ❓ Question: Is 6 > heap[0] (which is 3)?                                                                                    │
    │   ✅ Answer: YES! 6 > 3                                                                                                         │
    │                                                                                                                                 │
    │   💭 Decision: REPLACE heap top (3) with 6!                                                                                     │
    │                                                                                                                                 │
    │   🔄 HEAP REPLACEMENT PROCESS:                                                                                                  │
    │                                                                                                                                 │
    │      Before heapreplace:                    After heapreplace:                                                                 │
    │                                                                                                                                 │
    │           ┌─────────┐                            ┌─────────┐                                                                   │
    │           │    3    │  ← Remove                  │    5    │  ← New root (smaller child becomes root)                         │
    │           └────┬────┘                            └────┬────┘                                                                   │
    │                │                                      │                                                                        │
    │           ┌────┴────┐                            ┌────┴────┐                                                                   │
    │           │    5    │                            │    6    │  ← Inserted and bubbled down                                     │
    │           └─────────┘                            └─────────┘                                                                   │
    │                                                                                                                                 │
    │   📋 Array representation:                                                                                                      │
    │      Before: [3, 5]                                                                                                             │
    │      After:  [5, 6]  ← Min heap: 5 < 6 ✓                                                                                       │
    │               ↑  ↑                                                                                                              │
    │            ROOT CHILD                                                                                                           │
    │            (min) (larger)                                                                                                       │
    │                                                                                                                                 │
    │   💡 Insight: Heap now contains [5, 6] (top 2 largest so far)                                                                  │
    │               Top element (5) = 2nd largest among [3, 2, 1, 5, 6]                                                              │
    │                                                                                                                                 │
    │   ✅ New heap: [5, 6]                                                                                                           │
    │                                                                                                                                 │
    └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │ STEP 5: Process num = 4                                                                                                         │
    ├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
    │                                                                                                                                 │
    │   Current element: 4                                                                                                            │
    │   Heap before:     [5, 6]                                                                                                      │
    │                                                                                                                                 │
    │   ❓ Question: Is 4 > heap[0] (which is 5)?                                                                                    │
    │   ❌ Answer: NO! 4 < 5                                                                                                          │
    │                                                                                                                                 │
    │   💭 Decision: SKIP this element!                                                                                               │
    │      Why? 4 is smaller than our current 2nd largest (5),                                                                       │
    │      so it can't push anything out of the top 2!                                                                               │
    │                                                                                                                                 │
    │   📊 Heap UNCHANGED:                                                                                                            │
    │                        ┌─────────┐                                                                                             │
    │                        │    5    │  ← Still the 2nd largest                                                                    │
    │                        └────┬────┘                                                                                             │
    │                             │                                                                                                  │
    │                        ┌────┴────┐                                                                                             │
    │                        │    6    │  ← Largest element                                                                          │
    │                        └─────────┘                                                                                             │
    │                                                                                                                                 │
    │   ✅ Final heap: [5, 6]                                                                                                         │
    │                                                                                                                                 │
    └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    │ 🎯 FINAL RESULT                                                                                                                 │
    ├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
    │                                                                                                                                 │
    │   Final heap state: [5, 6]                                                                                                     │
    │                                                                                                                                 │
    │   📊 HEAP VISUALIZATION:                                                                                                        │
    │                                                                                                                                 │
    │                        ┌─────────┐                                                                                             │
    │                        │    5    │  ← heap[0] = 2nd LARGEST ✅                                                                 │
    │                        └────┬────┘                                                                                             │
    │                             │                                                                                                  │
    │                        ┌────┴────┐                                                                                             │
    │                        │    6    │  ← 1st largest                                                                              │
    │                        └─────────┘                                                                                             │
    │                                                                                                                                 │
    │   🔍 Verification:                                                                                                              │
    │      Original array: [3, 2, 1, 5, 6, 4]                                                                                        │
    │      Sorted (desc):  [6, 5, 4, 3, 2, 1]                                                                                        │
    │                          ↑                                                                                                      │
    │                       2nd largest = 5 ✅                                                                                        │
    │                                                                                                                                 │
    │   ✨ Return heap[0] = 5                                                                                                         │
    │                                                                                                                                 │
    └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

    ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                              💡 KEY INSIGHTS
    ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

    1. 🎯 MIN HEAP FOR KTH LARGEST (Not Max Heap!)
       ────────────────────────────────────────
       • Min heap keeps SMALLEST element at top
       • We maintain exactly k elements in heap
       • Top element = smallest of k largest = kth largest!

    2. 📊 HEAP SIZE IS KEY
       ───────────────────
       • Heap size = k (constant!)
       • Each operation: O(log k)
       • Total: N operations × O(log k) = O(N log k)

    3. 🔄 REPLACEMENT STRATEGY
       ───────────────────────
       • If new element > heap top → Replace (it's in top k)
       • If new element ≤ heap top → Skip (not in top k)
       • heapreplace() does: pop + push in one operation

    4. 💾 SPACE EFFICIENCY
       ───────────────────
       • Only store k elements (not entire array!)
       • Space: O(k) vs O(N) for sorting
       • Great when k << N (e.g., k=10, N=1,000,000)

    ⚡ WHEN TO USE MIN HEAP APPROACH:
    ─────────────────────────────────
    ✅ When k is small (k << N): O(N log k) much better than O(N log N)
    ✅ When you need all top k elements (not just kth)
    ✅ When code simplicity matters (easier than QuickSelect)
    ✅ When you want guaranteed time complexity (QuickSelect can be O(N²) worst case)

    ❌ When QuickSelect might be better:
    ────────────────────────────────────
    • When k ≈ N (QuickSelect is O(N) average)
    • When you only need kth element (not all top k)
    • When you want to show divide-and-conquer skills
    """
    heap = nums[:k]
    heapq.heapify(heap)

    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)

    return heap[0]


# ============================================================================
#              APPROACH 3: SORTING (SIMPLE BUT O(N LOG N))
# ============================================================================

def findKthLargest_Sorting(nums: List[int], k: int) -> int:
    """
    🎯 APPROACH 3: Sort and Pick (SIMPLEST!)

    TIME COMPLEXITY: O(N log N) - Full sort
    SPACE COMPLEXITY: O(1) or O(N) depending on sort implementation

    🧠 MEMORIZATION TRICK: "Just Sort It!"
    ---------------------------------------
    Simplest approach:
    1. Sort array in descending order
    2. Return element at index k-1

    📝 ALGORITHM:
    ------------
    1. Sort array descending
    2. Return nums[k-1]

    🎨 VISUAL EXAMPLE:
    -----------------
    Input: nums = [3,2,1,5,6,4], k = 2

    After sorting (descending): [6, 5, 4, 3, 2, 1]
                                     ↑
                                  index 1 (k-1 = 2-1 = 1)

    Return nums[1] = 5 ✅

    ⚠️  WHY NOT OPTIMAL:
    -------------------
    - Sorting is O(N log N)
    - QuickSelect is O(N) average
    - But: VERY simple and easy to code!
    - Good starting point in interview
    """
    nums.sort(reverse=True)
    return nums[k - 1]


# ============================================================================
#                    🎨 VISUAL WALKTHROUGH EXAMPLE
# ============================================================================

"""
Let's trace QuickSelect with: nums = [3,2,1,5,6,4], k = 2

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                          APPROACH 1: QUICKSELECT (OPTIMAL)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

GOAL: Find 2nd largest element (k=2, so we want element at index k-1 = 1 after sorting descending)

INITIAL STATE:
──────────────
Array: [3, 2, 1, 5, 6, 4]
Target: index 1 (0-based, for 2nd largest)

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ ITERATION 1: Partition entire array                                                                                            │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Current range: left=0, right=5                                                                                               │
│   Array:  [3, 2, 1, 5, 6, 4]                                                                                                   │
│   Indices: 0  1  2  3  4  5                                                                                                    │
│                                                                                                                                 │
│   Step 1: Pick random pivot                                                                                                    │
│   ──────────────────────────────                                                                                               │
│   Let's say we pick index 5 (value = 4)                                                                                        │
│   Pivot value = 4                                                                                                              │
│                                                                                                                                 │
│   Step 2: Partition around pivot (arrange as [>= 4] | 4 | [< 4])                                                              │
│   ────────────────────────────────────────────────────────────────                                                             │
│                                                                                                                                 │
│   Move pivot (4) to end: [3, 2, 1, 5, 6, 4]                                                                                    │
│                                           ↑ pivot at end                                                                        │
│                                                                                                                                 │
│   Scan array, move elements >= 4 to left:                                                                                      │
│   • 3 < 4? Yes → leave it                                                                                                      │
│   • 2 < 4? Yes → leave it                                                                                                      │
│   • 1 < 4? Yes → leave it                                                                                                      │
│   • 5 >= 4? Yes → move to left → [5, 2, 1, 3, 6, 4]                                                                            │
│   • 6 >= 4? Yes → move to left → [5, 6, 1, 3, 2, 4]                                                                            │
│                                                                                                                                 │
│   After partitioning: [5, 6, 1, 3, 2, 4]                                                                                       │
│                        ─────          ─                                                                                         │
│                        >= 4      <4   pivot                                                                                     │
│                                                                                                                                 │
│   Actually, let me redo with cleaner partition result:                                                                         │
│   After partition: [5, 6] | 4 | [3, 2, 1]                                                                                      │
│                    ─────   ─   ─────────                                                                                        │
│                    >= 4  pivot   < 4                                                                                            │
│                                                                                                                                 │
│   Indices:  [0, 1] | 2 | [3, 4, 5]                                                                                             │
│                      ↑                                                                                                          │
│              pivot now at index 2                                                                                               │
│                                                                                                                                 │
│   Step 3: Compare pivot position with target                                                                                   │
│   ─────────────────────────────────────────                                                                                    │
│   Pivot index: 2                                                                                                                │
│   Target index: 1 (k-1 = 2-1 = 1)                                                                                              │
│                                                                                                                                 │
│   pivot_index (2) > target_index (1)                                                                                           │
│   → Kth largest is in LEFT partition!                                                                                          │
│   → Recurse on [5, 6] (indices 0 to 1)                                                                                         │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ ITERATION 2: Partition left subarray                                                                                           │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Current range: left=0, right=1                                                                                               │
│   Subarray: [5, 6]                                                                                                             │
│   Indices:   0  1                                                                                                              │
│                                                                                                                                 │
│   Step 1: Pick random pivot                                                                                                    │
│   ──────────────────────────────                                                                                               │
│   Let's pick index 0 (value = 5)                                                                                               │
│   Pivot value = 5                                                                                                              │
│                                                                                                                                 │
│   Step 2: Partition around pivot (arrange as [>= 5] | 5 | [< 5])                                                              │
│   ────────────────────────────────────────────────────────────────                                                             │
│                                                                                                                                 │
│   Move pivot (5) to end: [6, 5]                                                                                                │
│                              ↑ pivot at end                                                                                     │
│                                                                                                                                 │
│   Scan array:                                                                                                                   │
│   • 6 >= 5? Yes → move to left (already there)                                                                                 │
│                                                                                                                                 │
│   After partitioning: [6] | 5 | []                                                                                             │
│                       ───   ─   ──                                                                                              │
│                       >= 5  pvt  < 5                                                                                            │
│                                                                                                                                 │
│   Indices:  [0] | 1 | []                                                                                                        │
│                   ↑                                                                                                             │
│           pivot now at index 1                                                                                                  │
│                                                                                                                                 │
│   Step 3: Compare pivot position with target                                                                                   │
│   ─────────────────────────────────────────                                                                                    │
│   Pivot index: 1                                                                                                                │
│   Target index: 1                                                                                                               │
│                                                                                                                                 │
│   pivot_index == target_index                                                                                                  │
│   → FOUND! Return pivot value = 5 ✅                                                                                            │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

FINAL RESULT: 5

VERIFICATION:
─────────────
Original array sorted descending: [6, 5, 4, 3, 2, 1]
                                       ↑
                                   index 1 (2nd largest)

2nd largest = 5 ✅

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                            WHY QUICKSELECT IS O(N) ON AVERAGE?
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

AVERAGE CASE (Good pivots - pivot divides array roughly in half):
──────────────────────────────────────────────────────────────────

Iteration 1: Process N elements → partition entire array
Iteration 2: Process N/2 elements → partition half
Iteration 3: Process N/4 elements → partition quarter
...and so on

Total work: N + N/2 + N/4 + N/8 + ... = 2N = O(N) ✅

Visual:
       [───────────────────N elements───────────────────]  → N work
                    ↓ recurse on one half
            [────N/2 elements────]                         → N/2 work
                    ↓
               [─N/4─]                                     → N/4 work
                  ↓
                [N/8]                                      → N/8 work
                 ...

Total: N + N/2 + N/4 + ... = N(1 + 1/2 + 1/4 + ...) = N(2) = O(N)


WORST CASE (Bad pivots - pivot is always min or max):
──────────────────────────────────────────────────────

Iteration 1: Process N elements
Iteration 2: Process N-1 elements
Iteration 3: Process N-2 elements
...and so on

Total work: N + (N-1) + (N-2) + ... + 1 = N(N+1)/2 = O(N²) ❌

Visual:
       [───────────────────N elements───────────────────]  → N work
                    ↓ recurse on N-1 elements
            [──────────N-1 elements──────────]             → N-1 work
                    ↓
            [────────N-2 elements────────]                 → N-2 work
                    ↓
                   ...

Total: N + (N-1) + (N-2) + ... = O(N²)

However, with RANDOM pivot selection, worst case is VERY rare!
"""

# ============================================================================
#              🎯 MEMORY TRICKS & COMMON MISTAKES
# ============================================================================

"""
🧠 HOW TO REMEMBER THIS SOLUTION:
---------------------------------
1. "QUICKSORT'S COUSIN" → QuickSelect uses same partition logic
2. "SEARCH ONE SIDE" → Unlike QuickSort, only recurse on one partition
3. "PIVOT POSITION MATTERS" → If pivot at k-1, you're done!
4. "RANDOM PIVOT HELPS" → Avoids worst case O(N²)

❌ COMMON MISTAKES TO AVOID:
----------------------------
1. ❌ Confusing kth largest vs kth smallest
      WRONG: Partition with < for kth largest
      RIGHT: Partition with >= for kth largest

2. ❌ Off-by-one errors
      WRONG: target = k (for 0-based array)
      RIGHT: target = k - 1 (k=1 means index 0)

3. ❌ Not using random pivot
      WRONG: Always pick first/last element as pivot
      RIGHT: Pick random pivot to avoid worst case

4. ❌ Recursing on both sides (like QuickSort)
      WRONG: quickselect(left, pivot) AND quickselect(pivot+1, right)
      RIGHT: Only recurse on side containing kth element

5. ❌ Forgetting that heap solution finds kth largest differently
      WRONG: Use max heap for kth largest
      RIGHT: Use min heap of size k

✅ PRO TIPS:
-----------
1. QuickSelect is best for average O(N)
2. Min heap is better when k is very small (k << N)
3. Sorting is simplest but not optimal
4. Draw the partition process to visualize
5. Practice both approaches for interviews

🎯 INTERVIEW STRATEGY:
---------------------
"I'll use QuickSelect, which is like QuickSort but only recurses on one side.
After partitioning, I check if the pivot is at position k-1. If yes, that's
the answer. If the pivot is to the right, I search the left partition. If the
pivot is to the left, I search the right partition. This gives O(N) average
time with random pivot selection."

Alternative:
"For small k, I can use a min heap of size k. I maintain the k largest elements
in the heap, and the top of the heap will be the kth largest. This is O(N log k)
which is great when k << N."
"""

# ============================================================================
#                         🧪 TEST CASES
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("          KTH LARGEST ELEMENT IN ARRAY - TEST CASES")
    print("="*80)

    # Test Case 1: Standard case from problem
    print("\n📝 Test Case 1: Standard case")
    print("-" * 80)
    nums1 = [3, 2, 1, 5, 6, 4]
    k1 = 2
    print(f"Input: nums = {nums1}, k = {k1}")
    result1_a = findKthLargest_QuickSelect(nums1.copy(), k1)
    result1_b = findKthLargest_MinHeap(nums1.copy(), k1)
    result1_c = findKthLargest_Sorting(nums1.copy(), k1)
    print(f"Output (QuickSelect): {result1_a}")
    print(f"Output (Min Heap):    {result1_b}")
    print(f"Output (Sorting):     {result1_c}")
    print(f"Expected: 5")
    print(f"✅ PASS" if result1_a == 5 else "❌ FAIL")

    # Test Case 2: Array with duplicates
    print("\n📝 Test Case 2: Array with duplicates")
    print("-" * 80)
    nums2 = [3, 2, 3, 1, 2, 4, 5, 5, 6]
    k2 = 4
    print(f"Input: nums = {nums2}, k = {k2}")
    result2_a = findKthLargest_QuickSelect(nums2.copy(), k2)
    result2_b = findKthLargest_MinHeap(nums2.copy(), k2)
    result2_c = findKthLargest_Sorting(nums2.copy(), k2)
    print(f"Output (QuickSelect): {result2_a}")
    print(f"Output (Min Heap):    {result2_b}")
    print(f"Output (Sorting):     {result2_c}")
    print(f"Expected: 4")
    print(f"✅ PASS" if result2_a == 4 else "❌ FAIL")

    # Test Case 3: Single element
    print("\n📝 Test Case 3: Single element")
    print("-" * 80)
    nums3 = [1]
    k3 = 1
    print(f"Input: nums = {nums3}, k = {k3}")
    result3_a = findKthLargest_QuickSelect(nums3.copy(), k3)
    result3_b = findKthLargest_MinHeap(nums3.copy(), k3)
    result3_c = findKthLargest_Sorting(nums3.copy(), k3)
    print(f"Output (QuickSelect): {result3_a}")
    print(f"Output (Min Heap):    {result3_b}")
    print(f"Output (Sorting):     {result3_c}")
    print(f"Expected: 1")
    print(f"✅ PASS" if result3_a == 1 else "❌ FAIL")

    # Test Case 4: k = 1 (find maximum)
    print("\n📝 Test Case 4: Find maximum (k=1)")
    print("-" * 80)
    nums4 = [7, 10, 4, 3, 20, 15]
    k4 = 1
    print(f"Input: nums = {nums4}, k = {k4}")
    result4_a = findKthLargest_QuickSelect(nums4.copy(), k4)
    result4_b = findKthLargest_MinHeap(nums4.copy(), k4)
    result4_c = findKthLargest_Sorting(nums4.copy(), k4)
    print(f"Output (QuickSelect): {result4_a}")
    print(f"Output (Min Heap):    {result4_b}")
    print(f"Output (Sorting):     {result4_c}")
    print(f"Expected: 20")
    print(f"✅ PASS" if result4_a == 20 else "❌ FAIL")

    # Test Case 5: k = n (find minimum)
    print("\n📝 Test Case 5: Find minimum (k=n)")
    print("-" * 80)
    nums5 = [7, 10, 4, 3, 20, 15]
    k5 = 6
    print(f"Input: nums = {nums5}, k = {k5}")
    result5_a = findKthLargest_QuickSelect(nums5.copy(), k5)
    result5_b = findKthLargest_MinHeap(nums5.copy(), k5)
    result5_c = findKthLargest_Sorting(nums5.copy(), k5)
    print(f"Output (QuickSelect): {result5_a}")
    print(f"Output (Min Heap):    {result5_b}")
    print(f"Output (Sorting):     {result5_c}")
    print(f"Expected: 3")
    print(f"✅ PASS" if result5_a == 3 else "❌ FAIL")

    # Test Case 6: Negative numbers
    print("\n📝 Test Case 6: Negative numbers")
    print("-" * 80)
    nums6 = [-1, -5, 2, 3, -3, 0]
    k6 = 3
    print(f"Input: nums = {nums6}, k = {k6}")
    result6_a = findKthLargest_QuickSelect(nums6.copy(), k6)
    result6_b = findKthLargest_MinHeap(nums6.copy(), k6)
    result6_c = findKthLargest_Sorting(nums6.copy(), k6)
    print(f"Output (QuickSelect): {result6_a}")
    print(f"Output (Min Heap):    {result6_b}")
    print(f"Output (Sorting):     {result6_c}")
    print(f"Expected: 0 (sorted: [3,2,0,-1,-3,-5])")
    print(f"✅ PASS" if result6_a == 0 else "❌ FAIL")

    # Test Case 7: All same elements
    print("\n📝 Test Case 7: All same elements")
    print("-" * 80)
    nums7 = [5, 5, 5, 5, 5]
    k7 = 3
    print(f"Input: nums = {nums7}, k = {k7}")
    result7_a = findKthLargest_QuickSelect(nums7.copy(), k7)
    result7_b = findKthLargest_MinHeap(nums7.copy(), k7)
    result7_c = findKthLargest_Sorting(nums7.copy(), k7)
    print(f"Output (QuickSelect): {result7_a}")
    print(f"Output (Min Heap):    {result7_b}")
    print(f"Output (Sorting):     {result7_c}")
    print(f"Expected: 5")
    print(f"✅ PASS" if result7_a == 5 else "❌ FAIL")

    print("\n" + "="*80)
    print("              ✅ ALL TEST CASES COMPLETED!")
    print("="*80)


# ============================================================================
#              🎓 LEARNING SUMMARY & KEY TAKEAWAYS
# ============================================================================

"""
🎯 WHAT YOU LEARNED:
-------------------
1. QuickSelect achieves O(N) average time with partition-based selection
2. Only recurse on ONE side (unlike QuickSort which recurses on both)
3. Random pivot selection avoids O(N²) worst case
4. Min heap is better when k is very small (k << N)

🔑 KEY PATTERN: "Partition and Conquer"
----------------------------------------
This pattern applies when:
- Need to find kth element without full sorting
- Can partition array into smaller/larger groups
- Only care about element at specific position

Used in:
- Kth Largest Element in Array (this problem!)
- Kth Smallest Element
- Median of Unsorted Array
- Top K Elements (with variations)

💪 THREE APPROACHES TO MASTER:
-----------------------------
1. QUICKSELECT (Optimal - O(N) average)
   - Partition like QuickSort
   - Only recurse on side containing kth element
   - Random pivot avoids worst case
   - Industry standard for kth element problems

2. MIN HEAP (Good for small k - O(N log k))
   - Maintain heap of size k
   - Top of heap = kth largest
   - Better than QuickSelect when k << N

3. SORTING (Simple - O(N log N))
   - Sort and pick kth element
   - Simple but not optimal
   - Good starting point in interviews

🎯 INTERVIEW TIPS:
-----------------
1. Clarify: kth largest or kth smallest?
2. Ask: are there duplicates? (Yes, and they count separately)
3. Mention QuickSelect for O(N) average
4. Alternative: Min heap for small k
5. Explain why random pivot helps
6. Draw partition process
7. Test with edge cases (k=1, k=n, duplicates)

🎉 CONGRATULATIONS!
------------------
You now understand QuickSelect and partition-based selection!
Remember: "Partition once, search ONE side only!"

📊 COMPLEXITY SUMMARY:
---------------------
┌────────────────────┬──────────────┬──────────────┐
│ Approach           │ Time         │ Space        │
├────────────────────┼──────────────┼──────────────┤
│ QuickSelect (Best) │ O(N) avg     │ O(1)         │
│                    │ O(N²) worst  │              │
├────────────────────┼──────────────┼──────────────┤
│ Min Heap           │ O(N log k)   │ O(k)         │
├────────────────────┼──────────────┼──────────────┤
│ Sorting            │ O(N log N)   │ O(1)         │
└────────────────────┴──────────────┴──────────────┘

N = array length, k = kth position

🏆 RECOMMENDED: Use QuickSelect for optimal O(N) average solution!
For very small k (like k < 10), Min Heap is also excellent!

🔗 RELATED PROBLEMS TO PRACTICE:
-------------------------------
1. LeetCode #215: Kth Largest Element in Array (this problem!)
2. LeetCode #703: Kth Largest Element in Stream
3. LeetCode #973: K Closest Points to Origin
4. LeetCode #347: Top K Frequent Elements
5. LeetCode #4: Median of Two Sorted Arrays

💡 FINAL TIP:
------------
QuickSelect is one of the MOST IMPORTANT algorithms for selection problems!
It's used in real systems for percentile calculations, sampling, and statistics.
The pattern of "partition and recurse on ONE side" is fundamental.
Master this and you'll ace all kth element problems!
"""
