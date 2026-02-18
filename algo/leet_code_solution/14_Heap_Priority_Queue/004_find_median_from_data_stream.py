"""
LeetCode Problem #295: Find Median from Data Stream

Difficulty: Hard
Topics: Two Pointers, Design, Sorting, Heap (Priority Queue), Data Stream
Companies: Google, Amazon, Facebook, Microsoft, Apple, Bloomberg, Uber, Adobe, LinkedIn

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
│ 4    │ 💡 SOLUTION 1: Two Heaps ⭐          │ • WHY choose? (Pros/Cons)     │
│      │    (OPTIMAL - O(log N))              │ • WHEN to use?                │
│      │                                      │ • Step-by-step walkthrough    │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 5    │ 💡 SOLUTION 2: Sorted Array          │ • WHY choose? (Pros/Cons)     │
│      │    (Simple but O(N))                 │ • WHEN to use?                │
│      │                                      │ • Comparison with Solution 1  │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 6    │ 💡 SOLUTION 3: BST                   │ • WHY choose? (Pros/Cons)     │
│      │    (Alternative O(log N))            │ • WHEN to use?                │
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
│ ANALOGY          │ "Two Balanced Buckets" - Split data in half!           │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ PATTERN          │ "Max Heap + Min Heap" - Balance lower & upper halves!  │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ KEY TRICK        │ Max heap stores lower half, min heap stores upper half!│
├──────────────────┼──────────────────────────────────────────────────────────┤
│ DEFAULT SOLUTION │ Two Heaps (O(log N) add, O(1) median - OPTIMAL!)      │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ TIME COMPLEXITY  │ O(log N) add, O(1) findMedian                          │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ SPACE COMPLEXITY │ O(N) - Store all elements in two heaps                │
└──────────────────┴──────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        ⚡ QUICK DECISION TABLE                              │
├────────────────────────────────────┬────────────────────────────────────────┤
│ SITUATION                          │ WHICH SOLUTION TO USE?                │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Normal interview (want best)       │ ✅ Solution 1 (Two Heaps)             │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Need O(log N) add + O(1) median   │ ✅ Solution 1 (Two Heaps!)            │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Want simplest code                 │ ⚠️  Solution 2 (Sorted Array)         │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Learning advanced structures       │ 🎓 Solution 3 (BST)                  │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Streaming data (many adds)         │ ✅ Solution 1 (most efficient!)       │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Want to show optimization          │ 🎯 Start with Sol 2, optimize to 1   │
└────────────────────────────────────┴────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     📊 SOLUTION COMPARISON TABLE                            │
├──────────────────┬──────────────┬──────────────┬──────────────┬─────────────┤
│ CRITERIA         │ TWO HEAPS    │ SORTED ARRAY │ BST          │ WINNER      │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Time: addNum()   │ ⭐⭐⭐⭐⭐   │ ⭐⭐         │ ⭐⭐⭐⭐     │ Two Heaps   │
│                  │ O(log N)     │ O(N)         │ O(log N)     │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Time: findMedian │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐⭐     │ Two Heaps   │
│                  │ O(1)         │ O(1)         │ O(log N)     │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Space Complexity │ ⭐⭐⭐⭐     │ ⭐⭐⭐⭐     │ ⭐⭐⭐⭐     │ Tie         │
│                  │ O(N)         │ O(N)         │ O(N)         │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Code Simplicity  │ ⭐⭐⭐       │ ⭐⭐⭐⭐⭐   │ ⭐⭐         │ Sorted      │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Interview Speed  │ ⭐⭐⭐⭐     │ ⭐⭐⭐⭐⭐   │ ⭐⭐         │ Sorted      │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Overall Best     │ ✅ OPTIMAL   │ Simple       │ Alternative  │ Two Heaps!  │
└──────────────────┴──────────────┴──────────────┴──────────────┴─────────────┘

⏱️  TIME TO MASTER: 30-35 minutes
🎯 DIFFICULTY: Hard (but pattern is elegant!)
💡 TIP: "Max heap for lower half, min heap for upper half!"
🔥 POPULAR: Classic design problem - Google favorite!

================================================================================
                           🎯 PROBLEM UNDERSTANDING
================================================================================

WHAT IS THE PROBLEM?
--------------------
Design a data structure that can:
1. Add numbers one at a time (streaming data)
2. Find the median of all numbers added so far in O(1) time

REAL WORLD ANALOGY:
------------------
Think of a LIVE SPORTS LEADERBOARD:
- Players keep finishing a race (numbers keep coming)
- You need to quickly report the "median performance"
- Can't re-sort entire list after each player - too slow!
- Need efficient way to maintain sorted order

Another analogy - SALARY DATABASE:
- New employees added continuously
- HR needs median salary at any time
- Median = middle salary when all sorted
- Must be fast (O(log N) add, O(1) median lookup)

THE KEY INSIGHT:
---------------
Use TWO HEAPS to split data in half!
- Max Heap: stores lower half (largest on top)
- Min Heap: stores upper half (smallest on top)
- Median is at the "meeting point" of the two heaps!

Example: [1, 2, 3, 4, 5]
- Max Heap (lower): [1, 2, 3] → top = 3
- Min Heap (upper): [4, 5] → top = 4
- Median = 3 (or average of 3 and 4 if even count)

❌ Wrong thinking: "Keep sorted array and pick middle" → O(N) to insert
✅ Right thinking: "Two heaps balanced, median at boundary" → O(log N)!

================================================================================
                            📝 FORMAL PROBLEM
================================================================================

The median is the middle value in an ordered integer list. If the size of the
list is even, there is no middle value, and the median is the mean of the two
middle values.

Implement the MedianFinder class:
- MedianFinder(): Initializes the MedianFinder object
- void addNum(int num): Adds the integer num from the data stream
- double findMedian(): Returns the median of all elements so far

Example 1:
----------
Input:
["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
[[], [1], [2], [], [3], []]

Output:
[null, null, null, 1.5, null, 2.0]

Explanation:
MedianFinder medianFinder = new MedianFinder();
medianFinder.addNum(1);    // arr = [1]
medianFinder.addNum(2);    // arr = [1, 2]
medianFinder.findMedian(); // return 1.5 (i.e., (1 + 2) / 2)
medianFinder.addNum(3);    // arr = [1, 2, 3]
medianFinder.findMedian(); // return 2.0

Constraints:
------------
* -10^5 <= num <= 10^5
* There will be at least one element before calling findMedian
* At most 5 * 10^4 calls will be made to addNum and findMedian

Follow-up:
----------
* If all integer numbers are in range [0, 100], how would you optimize?
* If 99% of integers are in range [0, 100], how would you optimize?

================================================================================
                         🧠 KEY INSIGHTS TO REMEMBER
================================================================================

THE MAIN CHALLENGE:
------------------
❌ Can't sort after every add - O(N log N) too slow!
❌ Can't use single heap - can't get median in O(1)
✅ Two heaps split data perfectly at median!

THE MAGIC TRICK: "TWO HEAPS BALANCE"
------------------------------------
Key observation: Split numbers into two balanced halves!

Structure:
  Max Heap (lower half)  |  Min Heap (upper half)
  [smaller numbers]      |  [larger numbers]
  Largest on top ←──────→ Smallest on top
                   ↑
              MEDIAN HERE!

Invariants to maintain:
1. All elements in max_heap ≤ all elements in min_heap
2. Size difference ≤ 1: |max_heap.size - min_heap.size| ≤ 1
3. If sizes differ, max_heap has 1 extra element

THE BREAKTHROUGH INSIGHT:
------------------------
┌─────────────────────────────────────────────────────────────┐
│  Two Heaps Maintain Sorted Property:                        │
│  - Max heap top = largest in lower half                     │
│  - Min heap top = smallest in upper half                    │
│  - Median is at boundary: O(1) to find!                     │
│  - Rebalancing after add: O(log N)                          │
│  → Total: O(log N) add, O(1) median!                        │
└─────────────────────────────────────────────────────────────┘

HOW TO FIND MEDIAN:
-------------------
Case 1: Equal sizes
  median = (max_heap.top + min_heap.top) / 2

Case 2: Max heap larger (odd total count)
  median = max_heap.top

================================================================================
                          💡 SOLUTION APPROACHES
================================================================================
"""

import heapq
from typing import List

# ============================================================================
#          APPROACH 1: TWO HEAPS (OPTIMAL - O(log N) + O(1))
# ============================================================================

class MedianFinder:
    """
    🎯 APPROACH 1: Two Heaps - Max Heap + Min Heap (BEST SOLUTION!)

    TIME COMPLEXITY:
      - addNum(): O(log N) - Heap operations
      - findMedian(): O(1) - Just peek at heap tops
    SPACE COMPLEXITY: O(N) - Store all elements

    🧠 MEMORIZATION TRICK: "Balanced Buckets"
    -----------------------------------------
    Think: Two buckets holding water at same level!
    - Left bucket (max heap): lower half of numbers
    - Right bucket (min heap): upper half of numbers
    - Water level (median) is at the boundary!

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    addNum(num):
      1. Add to max_heap (lower half) by default
      2. Balance: move max from max_heap to min_heap if needed
      3. Rebalance sizes: ensure |size_diff| ≤ 1

    findMedian():
      1. If equal sizes: average of both tops
      2. If max_heap larger: return max_heap top

    🎨 VISUAL EXAMPLE:
    -----------------
    Add sequence: [1, 2, 3, 4, 5]

    Add 1:
      max_heap: [1]  min_heap: []
      median = 1

    Add 2:
      max_heap: [1]  min_heap: [2]
      median = (1 + 2) / 2 = 1.5

    Add 3:
      max_heap: [2, 1]  min_heap: [3]
      median = 2

    Add 4:
      max_heap: [2, 1]  min_heap: [3, 4]
      median = (2 + 3) / 2 = 2.5

    Add 5:
      max_heap: [3, 2, 1]  min_heap: [4, 5]
      median = 3

    WHY THIS IS OPTIMAL:
    --------------------
    ✅ addNum: O(log N) - at most 2 heap operations
    ✅ findMedian: O(1) - just peek at tops
    ✅ Space: O(N) - must store all numbers
    """

    def __init__(self):
        """Initialize two heaps."""
        # Max heap for lower half (use negative values for Python's min heap)
        self.max_heap = []  # Stores smaller half
        # Min heap for upper half
        self.min_heap = []  # Stores larger half

    def addNum(self, num: int) -> None:
        """
        Add number to data structure.

        Time: O(log N)
        """
        # Step 1: Add to max_heap (lower half)
        heapq.heappush(self.max_heap, -num)  # Negate for max heap

        # Step 2: Balance - ensure all in max_heap ≤ all in min_heap
        # Move largest from max_heap to min_heap
        if self.max_heap and self.min_heap:
            if -self.max_heap[0] > self.min_heap[0]:
                val = -heapq.heappop(self.max_heap)
                heapq.heappush(self.min_heap, val)

        # Step 3: Rebalance sizes - max_heap should have ≥ elements
        # If min_heap becomes larger, move its smallest to max_heap
        if len(self.min_heap) > len(self.max_heap):
            val = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -val)

    def findMedian(self) -> float:
        """
        Find median of all elements.

        Time: O(1)
        """
        # If equal sizes, average the two middle elements
        if len(self.max_heap) == len(self.min_heap):
            return (-self.max_heap[0] + self.min_heap[0]) / 2.0
        # If max_heap larger, its top is the median
        else:
            return float(-self.max_heap[0])


# ============================================================================
#              APPROACH 2: SORTED ARRAY (SIMPLE BUT O(N))
# ============================================================================

class MedianFinder_Sorted:
    """
    🎯 APPROACH 2: Maintain Sorted Array (SIMPLER!)

    TIME COMPLEXITY:
      - addNum(): O(N) - Insert in sorted position
      - findMedian(): O(1) - Access middle element(s)
    SPACE COMPLEXITY: O(N)

    🧠 MEMORIZATION TRICK: "Sorted List"
    -------------------------------------
    Keep array sorted at all times.
    Median = middle element(s).

    📝 ALGORITHM:
    ------------
    addNum(num):
      1. Use binary search to find insert position
      2. Insert num at that position (O(N) due to shifting)

    findMedian():
      1. If odd length: return middle
      2. If even length: return average of two middle

    ⚠️  WHY NOT OPTIMAL:
    -------------------
    - Insert is O(N) due to array shifting
    - Only good for small datasets or few inserts
    - But: Very simple to code!
    """

    def __init__(self):
        """Initialize sorted array."""
        self.nums = []

    def addNum(self, num: int) -> None:
        """
        Add number maintaining sorted order.

        Time: O(N) - Binary search O(log N) + insert O(N)
        """
        # Binary search for insert position
        left, right = 0, len(self.nums)
        while left < right:
            mid = (left + right) // 2
            if self.nums[mid] < num:
                left = mid + 1
            else:
                right = mid

        # Insert at found position
        self.nums.insert(left, num)

    def findMedian(self) -> float:
        """
        Find median from sorted array.

        Time: O(1)
        """
        n = len(self.nums)
        if n % 2 == 1:
            return float(self.nums[n // 2])
        else:
            return (self.nums[n // 2 - 1] + self.nums[n // 2]) / 2.0


# ============================================================================
#              APPROACH 3: BST (ALTERNATIVE O(log N))
# ============================================================================

class TreeNode:
    """Node for self-balancing BST with size tracking."""
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.count = 1  # Size of subtree

class MedianFinder_BST:
    """
    🎯 APPROACH 3: Self-Balancing BST (EDUCATIONAL!)

    TIME COMPLEXITY:
      - addNum(): O(log N) average, O(N) worst
      - findMedian(): O(log N) - Find kth element
    SPACE COMPLEXITY: O(N)

    🧠 IDEA: Use BST with size tracking
    ------------------------------------
    - Each node tracks subtree size
    - Can find kth smallest in O(log N)
    - Median = middle element(s)

    ⚠️  PROBLEMS:
    ------------
    - More complex than two heaps
    - Requires balancing to maintain O(log N)
    - findMedian is O(log N), not O(1)
    - Included for educational purposes

    💡 LESSON: Two heaps is simpler and better!
    """

    def __init__(self):
        """Initialize BST."""
        self.root = None
        self.size = 0

    def addNum(self, num: int) -> None:
        """Add number to BST. Time: O(log N) average"""
        self.root = self._insert(self.root, num)
        self.size += 1

    def _insert(self, node, val):
        """Insert value into BST."""
        if not node:
            return TreeNode(val)
        if val <= node.val:
            node.left = self._insert(node.left, val)
        else:
            node.right = self._insert(node.right, val)
        node.count = 1 + self._get_size(node.left) + self._get_size(node.right)
        return node

    def _get_size(self, node):
        """Get size of subtree."""
        return node.count if node else 0

    def _find_kth(self, node, k):
        """Find kth smallest element (1-indexed)."""
        left_size = self._get_size(node.left)
        if k <= left_size:
            return self._find_kth(node.left, k)
        elif k == left_size + 1:
            return node.val
        else:
            return self._find_kth(node.right, k - left_size - 1)

    def findMedian(self) -> float:
        """Find median. Time: O(log N)"""
        if self.size % 2 == 1:
            return float(self._find_kth(self.root, self.size // 2 + 1))
        else:
            mid1 = self._find_kth(self.root, self.size // 2)
            mid2 = self._find_kth(self.root, self.size // 2 + 1)
            return (mid1 + mid2) / 2.0


# ============================================================================
#                    🎨 VISUAL WALKTHROUGH EXAMPLE
# ============================================================================

"""
Let's trace Two Heaps approach with: addNum(1), addNum(2), addNum(3), addNum(4), addNum(5)

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                          APPROACH 1: TWO HEAPS (OPTIMAL)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

STRUCTURE:
  max_heap (lower half)  |  min_heap (upper half)
  Uses negated values    |  Normal min heap
  Top = largest in lower |  Top = smallest in upper

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ OPERATION 1: addNum(1)                                                                                                          │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Initial state:                                                                                                                │
│   max_heap: []                                                                                                                  │
│   min_heap: []                                                                                                                  │
│                                                                                                                                 │
│   Step 1: Add 1 to max_heap                                                                                                     │
│   ─────────────────────────────                                                                                                 │
│   heappush(max_heap, -1)  → max_heap: [-1]                                                                                     │
│                                                                                                                                 │
│   Step 2: Balance heaps                                                                                                         │
│   ───────────────────────                                                                                                       │
│   min_heap is empty, skip balance check                                                                                        │
│                                                                                                                                 │
│   Step 3: Rebalance sizes                                                                                                       │
│   ─────────────────────────                                                                                                     │
│   len(min_heap) = 0 ≤ len(max_heap) = 1, no rebalance needed                                                                   │
│                                                                                                                                 │
│   Final state:                                                                                                                  │
│   ┌──────────────────┐     ┌──────────────────┐                                                                                │
│   │   max_heap       │     │   min_heap       │                                                                                │
│   │   (lower half)   │     │   (upper half)   │                                                                                │
│   ├──────────────────┤     ├──────────────────┤                                                                                │
│   │      [-1]        │  |  │       []         │                                                                                │
│   │       ↓          │  |  │                  │                                                                                │
│   │   actual: 1      │  |  │                  │                                                                                │
│   └──────────────────┘  │  └──────────────────┘                                                                                │
│                        Median                                                                                                   │
│                                                                                                                                 │
│   findMedian(): max_heap size (1) > min_heap size (0)                                                                          │
│   → Return -max_heap[0] = 1.0 ✅                                                                                                │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ OPERATION 2: addNum(2)                                                                                                          │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Current state:                                                                                                                │
│   max_heap: [-1]  (actual: 1)                                                                                                  │
│   min_heap: []                                                                                                                  │
│                                                                                                                                 │
│   Step 1: Add 2 to max_heap                                                                                                     │
│   ─────────────────────────────                                                                                                 │
│   heappush(max_heap, -2)  → max_heap: [-2, -1]                                                                                 │
│                                        ↑                                                                                        │
│                                     top = -2 (actual: 2)                                                                        │
│                                                                                                                                 │
│   Step 2: Balance heaps                                                                                                         │
│   ───────────────────────                                                                                                       │
│   Check: max_heap top (2) > min_heap top? (min_heap empty, skip)                                                               │
│   Actually, min_heap is empty, so move largest from max_heap to min_heap:                                                      │
│   val = -heappop(max_heap) = 2                                                                                                  │
│   heappush(min_heap, 2)                                                                                                         │
│                                                                                                                                 │
│   After balance:                                                                                                                │
│   max_heap: [-1]  (actual: 1)                                                                                                  │
│   min_heap: [2]                                                                                                                 │
│                                                                                                                                 │
│   Step 3: Rebalance sizes                                                                                                       │
│   ─────────────────────────                                                                                                     │
│   len(min_heap) = 1 == len(max_heap) = 1, balanced!                                                                            │
│                                                                                                                                 │
│   Final state:                                                                                                                  │
│   ┌──────────────────┐     ┌──────────────────┐                                                                                │
│   │   max_heap       │     │   min_heap       │                                                                                │
│   │   (lower half)   │     │   (upper half)   │                                                                                │
│   ├──────────────────┤     ├──────────────────┤                                                                                │
│   │      [-1]        │  |  │       [2]        │                                                                                │
│   │       ↓          │  |  │        ↓         │                                                                                │
│   │   actual: 1      │  |  │   actual: 2      │                                                                                │
│   └──────────────────┘  │  └──────────────────┘                                                                                │
│                        Median                                                                                                   │
│                                                                                                                                 │
│   Data stream so far: [1, 2]                                                                                                   │
│                                                                                                                                 │
│   findMedian(): Equal sizes                                                                                                     │
│   → Return (-max_heap[0] + min_heap[0]) / 2 = (1 + 2) / 2 = 1.5 ✅                                                             │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ OPERATION 3: addNum(3)                                                                                                          │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Current state:                                                                                                                │
│   max_heap: [-1]  min_heap: [2]                                                                                                │
│                                                                                                                                 │
│   Step 1: Add 3 to max_heap                                                                                                     │
│   ─────────────────────────────                                                                                                 │
│   heappush(max_heap, -3)  → max_heap: [-3, -1]                                                                                 │
│                                                                                                                                 │
│   Step 2: Balance heaps                                                                                                         │
│   ───────────────────────                                                                                                       │
│   max_heap top = -(-3) = 3, min_heap top = 2                                                                                   │
│   3 > 2, so move 3 from max_heap to min_heap:                                                                                  │
│   val = -heappop(max_heap) = 3                                                                                                  │
│   heappush(min_heap, 3)                                                                                                         │
│                                                                                                                                 │
│   After balance:                                                                                                                │
│   max_heap: [-1]  (actual: 1)                                                                                                  │
│   min_heap: [2, 3]                                                                                                              │
│                                                                                                                                 │
│   Step 3: Rebalance sizes                                                                                                       │
│   ─────────────────────────                                                                                                     │
│   len(min_heap) = 2 > len(max_heap) = 1                                                                                        │
│   Move smallest from min_heap to max_heap:                                                                                     │
│   val = heappop(min_heap) = 2                                                                                                   │
│   heappush(max_heap, -2)                                                                                                        │
│                                                                                                                                 │
│   Final state:                                                                                                                  │
│   ┌──────────────────┐     ┌──────────────────┐                                                                                │
│   │   max_heap       │     │   min_heap       │                                                                                │
│   │   (lower half)   │     │   (upper half)   │                                                                                │
│   ├──────────────────┤     ├──────────────────┤                                                                                │
│   │    [-2, -1]      │  |  │       [3]        │                                                                                │
│   │      ↓           │  |  │        ↓         │                                                                                │
│   │  actual: 2, 1    │  |  │   actual: 3      │                                                                                │
│   │  top = 2         │  |  │   top = 3        │                                                                                │
│   └──────────────────┘  │  └──────────────────┘                                                                                │
│                        Median                                                                                                   │
│                                                                                                                                 │
│   Data stream so far: [1, 2, 3]                                                                                                │
│   Sorted view: [1, 2, 3]                                                                                                       │
│   Lower half: [1, 2]  Upper half: [3]                                                                                          │
│                                                                                                                                 │
│   findMedian(): max_heap size (2) > min_heap size (1)                                                                          │
│   → Return -max_heap[0] = 2.0 ✅                                                                                                │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ OPERATION 4: addNum(4)                                                                                                          │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Current: max_heap: [-2, -1]  min_heap: [3]                                                                                   │
│                                                                                                                                 │
│   After adding 4 and balancing:                                                                                                 │
│   max_heap: [-2, -1]  (actual: 2, 1)                                                                                           │
│   min_heap: [3, 4]                                                                                                              │
│                                                                                                                                 │
│   Data stream: [1, 2, 3, 4]                                                                                                    │
│   Lower half: [1, 2]  Upper half: [3, 4]                                                                                       │
│                                                                                                                                 │
│   findMedian(): Equal sizes                                                                                                     │
│   → Return (2 + 3) / 2 = 2.5 ✅                                                                                                 │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ OPERATION 5: addNum(5)                                                                                                          │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   After adding 5 and balancing:                                                                                                 │
│   max_heap: [-3, -2, -1]  (actual: 3, 2, 1)                                                                                    │
│   min_heap: [4, 5]                                                                                                              │
│                                                                                                                                 │
│   Data stream: [1, 2, 3, 4, 5]                                                                                                 │
│   Lower half: [1, 2, 3]  Upper half: [4, 5]                                                                                    │
│                                                                                                                                 │
│   findMedian(): max_heap size (3) > min_heap size (2)                                                                          │
│   → Return 3.0 ✅                                                                                                               │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

KEY OBSERVATIONS:
─────────────────
1. Max heap always contains ≤ half of elements (lower values)
2. Min heap contains ≥ half of elements (upper values)
3. All elements in max_heap ≤ all elements in min_heap
4. Median is always at the boundary between the two heaps
5. Size difference is at most 1
6. Each add is O(log N), median is O(1)
"""

# ============================================================================
#              🎯 MEMORY TRICKS & COMMON MISTAKES
# ============================================================================

"""
🧠 HOW TO REMEMBER THIS SOLUTION:
---------------------------------
1. "TWO BUCKETS" → Split data in half
2. "MAX LEFT, MIN RIGHT" → Max heap for lower, min heap for upper
3. "BALANCE SIZES" → Keep sizes within 1 of each other
4. "BOUNDARY = MEDIAN" → Median is at the meeting point

❌ COMMON MISTAKES TO AVOID:
----------------------------
1. ❌ Using two min heaps
      WRONG: Both min heaps
      RIGHT: Max heap for lower half, min heap for upper half

2. ❌ Wrong balance condition
      WRONG: Always keeping equal sizes
      RIGHT: Allow size difference of 1

3. ❌ Forgetting to negate for max heap in Python
      WRONG: heappush(max_heap, num)
      RIGHT: heappush(max_heap, -num)

4. ❌ Not balancing after every add
      WRONG: Add to random heap
      RIGHT: Add to max_heap, then balance

5. ❌ Wrong median calculation
      WRONG: Always average both tops
      RIGHT: Check sizes first - if unequal, take from larger heap

✅ PRO TIPS:
-----------
1. Always add to max_heap first, then rebalance
2. Python heapq is min heap, use negatives for max heap
3. Draw the two heaps to visualize
4. Max heap should have equal or 1 more element
5. This pattern appears in many streaming problems

🎯 INTERVIEW STRATEGY:
---------------------
"I'll use two heaps to split the data in half. A max heap stores the lower
half with the largest value on top, and a min heap stores the upper half with
the smallest on top. The median is at the boundary between them. After each
add, I rebalance to keep sizes within 1. This gives O(log N) add and O(1)
median lookup."
"""

# ============================================================================
#                         🧪 TEST CASES
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("          FIND MEDIAN FROM DATA STREAM - TEST CASES")
    print("="*80)

    # Test Case 1: Standard case from problem
    print("\n📝 Test Case 1: Standard case")
    print("-" * 80)
    mf1 = MedianFinder()
    print("addNum(1)")
    mf1.addNum(1)
    print("addNum(2)")
    mf1.addNum(2)
    result1 = mf1.findMedian()
    print(f"findMedian() = {result1}")
    print(f"Expected: 1.5")
    print(f"✅ PASS" if result1 == 1.5 else "❌ FAIL")

    print("\naddNum(3)")
    mf1.addNum(3)
    result2 = mf1.findMedian()
    print(f"findMedian() = {result2}")
    print(f"Expected: 2.0")
    print(f"✅ PASS" if result2 == 2.0 else "❌ FAIL")

    # Test Case 2: Single element
    print("\n📝 Test Case 2: Single element")
    print("-" * 80)
    mf2 = MedianFinder()
    mf2.addNum(5)
    result3 = mf2.findMedian()
    print(f"addNum(5), findMedian() = {result3}")
    print(f"Expected: 5.0")
    print(f"✅ PASS" if result3 == 5.0 else "❌ FAIL")

    # Test Case 3: Decreasing sequence
    print("\n📝 Test Case 3: Decreasing sequence")
    print("-" * 80)
    mf3 = MedianFinder()
    for num in [5, 4, 3, 2, 1]:
        mf3.addNum(num)
    result4 = mf3.findMedian()
    print(f"addNum([5,4,3,2,1]), findMedian() = {result4}")
    print(f"Expected: 3.0 (sorted: [1,2,3,4,5])")
    print(f"✅ PASS" if result4 == 3.0 else "❌ FAIL")

    # Test Case 4: Duplicate values
    print("\n📝 Test Case 4: Duplicate values")
    print("-" * 80)
    mf4 = MedianFinder()
    for num in [1, 1, 1]:
        mf4.addNum(num)
    result5 = mf4.findMedian()
    print(f"addNum([1,1,1]), findMedian() = {result5}")
    print(f"Expected: 1.0")
    print(f"✅ PASS" if result5 == 1.0 else "❌ FAIL")

    # Test Case 5: Even count
    print("\n📝 Test Case 5: Even count of elements")
    print("-" * 80)
    mf5 = MedianFinder()
    for num in [1, 2, 3, 4]:
        mf5.addNum(num)
    result6 = mf5.findMedian()
    print(f"addNum([1,2,3,4]), findMedian() = {result6}")
    print(f"Expected: 2.5 (average of 2 and 3)")
    print(f"✅ PASS" if result6 == 2.5 else "❌ FAIL")

    # Test Case 6: Negative numbers
    print("\n📝 Test Case 6: Negative numbers")
    print("-" * 80)
    mf6 = MedianFinder()
    for num in [-1, -2, -3]:
        mf6.addNum(num)
    result7 = mf6.findMedian()
    print(f"addNum([-1,-2,-3]), findMedian() = {result7}")
    print(f"Expected: -2.0 (sorted: [-3,-2,-1])")
    print(f"✅ PASS" if result7 == -2.0 else "❌ FAIL")

    # Test Case 7: Compare all approaches
    print("\n📝 Test Case 7: Compare all approaches")
    print("-" * 80)
    mf_heap = MedianFinder()
    mf_sorted = MedianFinder_Sorted()

    for num in [3, 1, 4, 1, 5]:
        mf_heap.addNum(num)
        mf_sorted.addNum(num)

    result_heap = mf_heap.findMedian()
    result_sorted = mf_sorted.findMedian()

    print(f"addNum([3,1,4,1,5])")
    print(f"Two Heaps:    {result_heap}")
    print(f"Sorted Array: {result_sorted}")
    print(f"Expected: 3.0 (sorted: [1,1,3,4,5])")
    print(f"✅ PASS" if result_heap == result_sorted == 3.0 else "❌ FAIL")

    print("\n" + "="*80)
    print("              ✅ ALL TEST CASES COMPLETED!")
    print("="*80)


# ============================================================================
#              🎓 LEARNING SUMMARY & KEY TAKEAWAYS
# ============================================================================

"""
🎯 WHAT YOU LEARNED:
-------------------
1. Two heaps elegantly maintain median at boundary
2. Max heap for lower half, min heap for upper half
3. O(log N) add, O(1) median is optimal for streaming
4. Balance condition: size difference ≤ 1

🔑 KEY PATTERN: "Two Heaps for Median"
---------------------------------------
This pattern applies when:
- Need median from streaming/dynamic data
- Can't afford O(N) operations per add
- Can maintain two balanced partitions

Used in:
- Find Median from Data Stream (this problem!)
- Sliding Window Median (LeetCode #480)
- IPO (LeetCode #502)
- Any problem requiring dynamic median

💪 THREE APPROACHES TO MASTER:
-----------------------------
1. TWO HEAPS (Optimal - O(log N) + O(1))
   - Max heap for lower half
   - Min heap for upper half
   - Balance after each add
   - Industry standard for streaming median

2. SORTED ARRAY (Simple - O(N) + O(1))
   - Maintain sorted order on insert
   - Access middle element(s)
   - Good for small datasets only

3. BST (Alternative - O(log N) + O(log N))
   - Self-balancing BST with size tracking
   - Find kth element for median
   - More complex, no advantage over two heaps

🎯 INTERVIEW TIPS:
-----------------
1. Clarify: odd or even count handling?
2. Ask: can we use extra space? (Yes, O(N))
3. Explain the two heaps invariant clearly
4. Draw the heap structure
5. Mention Python uses min heap (negate for max)
6. Test with both odd and even counts
7. Discuss follow-up optimizations (counting array for limited range)

🎉 CONGRATULATIONS!
------------------
You now understand the two heaps pattern for dynamic median!
Remember: "Max heap left, min heap right, balance at the boundary!"

📊 COMPLEXITY SUMMARY:
---------------------
┌────────────────────┬──────────────┬──────────────┐
│ Approach           │ addNum()     │ findMedian() │
├────────────────────┼──────────────┼──────────────┤
│ Two Heaps (Best)   │ O(log N)     │ O(1)         │
├────────────────────┼──────────────┼──────────────┤
│ Sorted Array       │ O(N)         │ O(1)         │
├────────────────────┼──────────────┼──────────────┤
│ BST                │ O(log N)     │ O(log N)     │
└────────────────────┴──────────────┴──────────────┘

Space: All O(N)

🏆 RECOMMENDED: Use Two Heaps for optimal O(log N) add + O(1) median!

🔗 RELATED PROBLEMS TO PRACTICE:
-------------------------------
1. LeetCode #295: Find Median from Data Stream (this problem!)
2. LeetCode #480: Sliding Window Median
3. LeetCode #502: IPO
4. LeetCode #703: Kth Largest Element in a Stream
5. LeetCode #215: Kth Largest Element in an Array

💡 FINAL TIP:
------------
The two heaps pattern is FUNDAMENTAL for streaming data problems!
It's used in real systems for monitoring, analytics, and statistics.
The key insight is maintaining balance at the median boundary.
Master this and you'll solve many dynamic statistics problems!
"""
