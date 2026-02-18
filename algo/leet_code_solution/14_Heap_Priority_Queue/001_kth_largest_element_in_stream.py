"""
LeetCode Problem #703: Kth Largest Element in a Stream

┌─────────────────────────────────────────────────────────────────────────────┐
│                           🎯 MEMORY CHEAT SHEET                             │
├──────────────────┬──────────────────────────────────────────────────────────┤
│ ANALOGY          │ "Top K Winners" - Keep only K largest on podium!       │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ PATTERN          │ "Min Heap of Size K" - Smallest at top, largest at K!  │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ KEY TRICK        │ If heap > k, pop smallest! Kth largest = heap.top()!   │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ DEFAULT SOLUTION │ Min Heap with size limit K (O(log k) - OPTIMAL!)       │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ TIME COMPLEXITY  │ O(log k) per add operation                              │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ SPACE COMPLEXITY │ O(k) - Store only k largest elements                    │
└──────────────────┴──────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        ⚡ QUICK DECISION TABLE                              │
├────────────────────────────────┬────────────────────────────────────────────┤
│ SITUATION                      │ WHICH SOLUTION TO USE?                    │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Normal interview               │ ✅ Solution 1 (Min Heap)                  │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Need optimal solution          │ ✅ Solution 1 (O(log k) time!)            │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Want simplest code             │ ⚠️  Solution 2 (Sorted - easier code)     │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Learning data structures       │ 🎓 Solution 3 (BST - educational)        │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Stream with many add() calls   │ ✅ Solution 1 (most efficient!)           │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Want to show optimization      │ 🎯 Start with Sol 2, optimize to Sol 1   │
└────────────────────────────────┴────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     📊 SOLUTION COMPARISON TABLE                            │
├──────────────────┬──────────────┬──────────────┬──────────────┬─────────────┤
│ CRITERIA         │ MIN HEAP     │ SORTED ARRAY │ BST          │ WINNER      │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Time: add()      │ ⭐⭐⭐⭐⭐   │ ⭐⭐         │ ⭐⭐⭐⭐     │ Min Heap    │
│                  │ O(log k)     │ O(N log N)   │ O(log N)     │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Space Complexity │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐       │ ⭐⭐⭐       │ Min Heap    │
│                  │ O(k)         │ O(N)         │ O(N)         │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────
└──────────────────┴──────────────┴──────────────┴──────────────┴─────────────┘

================================================================================
                           🎯 PROBLEM UNDERSTANDING
================================================================================

WHAT IS THE PROBLEM?
--------------------
Design a class to find the kth largest element in a stream. The stream keeps
adding new numbers, and you need to efficiently return the kth largest at any time.

REAL WORLD ANALOGY:
------------------
Think of a LEADERBOARD with K positions:
- You have a podium with K spots (k=3: Gold, Silver, Bronze)
- New scores keep coming in
- You only care about TOP K scores
- The Kth position (Bronze) is the "kth largest"
- If new score > Bronze, Bronze gets kicked off!

Another analogy - TOP K RESTAURANTS:
- Track top 5 rated restaurants in a city
- New restaurants keep opening
- Only keep track of top 5
- The 5th highest rated is your "kth largest"
- If new restaurant better than 5th → 5th gets removed

THE KEY INSIGHT:
---------------
You DON'T need to track ALL numbers!
Only need to track the K LARGEST numbers!

Use a MIN HEAP of size K:
- Heap stores only K largest numbers seen so far
- Top of heap = SMALLEST of the K largest = Kth largest!
- If new number > heap top → remove top, add new number
- If new number <= heap top → ignore it!

❌ Wrong thinking: "Sort entire array each time" → O(N log N)
✅ Right thinking: "Keep only K largest in min heap" → O(log K)

================================================================================
                            📝 FORMAL PROBLEM
================================================================================

Design a class to find the kth largest element in a stream. Note that it is
the kth largest element in the sorted order, not the kth distinct element.

Implement KthLargest class:
- KthLargest(int k, int[] nums): Initializes the object with the integer k
  and the stream of integers nums.
- int add(int val): Appends the integer val to the stream and returns the
  element representing the kth largest element in the stream.

Example 1:
----------
Input:
["KthLargest", "add", "add", "add", "add", "add"]
[[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]]

Output:
[null, 4, 5, 5, 8, 8]

Explanation:
KthLargest kthLargest = new KthLargest(3, [4, 5, 8, 2]);
kthLargest.add(3);   // return 4  (stream: [2,3,4,5,8], 3rd largest = 4)
kthLargest.add(5);   // return 5  (stream: [2,3,4,5,5,8], 3rd largest = 5)
kthLargest.add(10);  // return 5  (stream: [2,3,4,5,5,8,10], 3rd largest = 5)
kthLargest.add(9);   // return 8  (stream: [2,3,4,5,5,8,9,10], 3rd largest = 8)
kthLargest.add(4);   // return 8  (stream: [2,3,4,4,5,5,8,9,10], 3rd largest = 8)

Constraints:
------------
* 1 <= k <= 10^4
* 0 <= nums.length <= 10^4
* -10^4 <= nums[i] <= 10^4
* -10^4 <= val <= 10^4
* At most 10^4 calls will be made to add
* It is guaranteed that there will be at least k elements in the array when
  you search for the kth element

================================================================================
                         🧠 KEY INSIGHTS TO REMEMBER
================================================================================

THE MAIN CHALLENGE:
------------------
❌ Can't sort entire stream each time - too slow!
❌ Can't store all numbers - wastes space!
✅ Only need to track K largest numbers!

THE MAGIC TRICK: "MIN HEAP OF SIZE K"
--------------------------------------
Key observation: Use MIN HEAP to store K largest elements!

Why MIN heap not MAX heap?
- MAX heap gives largest element
- But we need Kth largest (the smallest among K largest)
- MIN heap of K elements: top = smallest = Kth largest!

Structure of min heap with K elements:
    Top (smallest of K largest) = Kth largest ✅
    ↓
   [4]          ← Kth largest (3rd largest among [4,5,8])
  ↙   ↘
 [5]   [8]      ← Larger elements

THE BREAKTHROUGH INSIGHT:
------------------------
┌─────────────────────────────────────────────────────────────┐
│  Min Heap maintains K largest elements automatically!      │
│  - Heap size > k? Pop smallest (it's not in top k)         │
│  - Heap size = k? Top element is kth largest!              │
│  - Each add() operation: O(log k) time!                    │
└─────────────────────────────────────────────────────────────┘

WHY THIS WORKS:
---------------
1. Heap size always ≤ k
2. Heap contains exactly k largest elements seen so far
3. Smallest element in heap = kth largest overall
4. No need to store numbers smaller than kth largest!

================================================================================
                          💡 SOLUTION APPROACHES
================================================================================
"""

from typing import List
import heapq

# ============================================================================
#                APPROACH 1: MIN HEAP (OPTIMAL - O(log k))
# ============================================================================

class KthLargest:
    """
    🎯 APPROACH 1: Min Heap of Size K (BEST SOLUTION!)

    TIME COMPLEXITY:
      - __init__: O(N log k) - Add N elements to heap
      - add(): O(log k) - Heap operations
    SPACE COMPLEXITY: O(k) - Store only k largest elements

    🧠 MEMORIZATION TRICK: "Top K Winners on Podium"
    ------------------------------------------------
    Think: Keep only top K scores, smallest on top!
    - Podium has K spots
    - New high score? Kick off lowest from podium
    - Top of heap = lowest on podium = Kth largest!

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    __init__(k, nums):
      1. Store k
      2. Create min heap
      3. For each num in nums:
         a. Add to heap
         b. If heap size > k: remove smallest (heappop)
      4. Now heap contains k largest, top = kth largest

    add(val):
      1. Add val to heap
      2. If heap size > k: remove smallest
      3. Return heap[0] (top = kth largest)

    🎨 VISUAL EXAMPLE:
    -----------------
    k = 3, nums = [4, 5, 8, 2]

    After initialization:
      Min Heap (size 3): [4, 5, 8]
           4  ← Top (3rd largest)
          ↙ ↘
         5   8

    add(3):
      1. heap = [4,5,8,3] → heapify → [3,4,8,5]
      2. Size > 3! Pop smallest (3)
      3. heap = [4,5,8]
      4. Return heap[0] = 4 ✅

    add(5):
      1. heap = [4,5,8,5] → heapify → [4,5,5,8]
      2. Size > 3! Pop smallest (4)
      3. heap = [5,5,8]
      4. Return heap[0] = 5 ✅

    WHY THIS IS O(log k):
    --------------------
    ✅ heappush: O(log k) - Insert into heap of size k
    ✅ heappop: O(log k) - Remove from heap of size k
    ✅ Heap size never exceeds k
    ✅ Total per add(): O(log k)
    """

    def __init__(self, k: int, nums: List[int]):
        """Initialize with k and initial stream."""
        self.k = k
        self.heap = []

        # Add all initial numbers
        for num in nums:
            heapq.heappush(self.heap, num)
            # Keep only k largest elements
            if len(self.heap) > k:
                heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        """
        Add value to stream and return kth largest.

        Time: O(log k)
        """
        # Add new value to heap
        heapq.heappush(self.heap, val)

        # If heap size exceeds k, remove smallest
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)

        # Top of min heap = kth largest
        return self.heap[0]


# ============================================================================
#              APPROACH 2: SORTED ARRAY (SIMPLE BUT O(N log N))
# ============================================================================

class KthLargest_Sorted:
    """
    🎯 APPROACH 2: Maintain Sorted Array (SIMPLER!)

    TIME COMPLEXITY:
      - __init__: O(N log N) - Sort initial array
      - add(): O(N log N) - Re-sort after each add
    SPACE COMPLEXITY: O(N) - Store all elements

    🧠 MEMORIZATION TRICK: "Sort and Pick"
    --------------------------------------
    Think: Keep all numbers sorted, pick kth from end!
    - Sort array in descending order
    - Kth largest = array[k-1]
    - Simple but slower!

    📝 ALGORITHM:
    ------------
    __init__(k, nums):
      1. Store k
      2. Store nums as list
      3. Sort in descending order

    add(val):
      1. Append val to list
      2. Sort list in descending order
      3. Return nums[k-1]

    🎨 EXAMPLE:
    ----------
    k = 3, nums = [4, 5, 8, 2]
    sorted = [8, 5, 4, 2]
    3rd largest = sorted[2] = 4 ✅

    add(3):
      sorted = [8, 5, 4, 3, 2]
      3rd largest = sorted[2] = 4 ✅

    ⚠️  WHY NOT OPTIMAL:
    -------------------
    - Sorting after each add: O(N log N)
    - Stores ALL numbers, not just top k
    - Much slower for large streams
    - But: VERY simple to code!
    """

    def __init__(self, k: int, nums: List[int]):
        """Initialize with sorted array."""
        self.k = k
        self.nums = nums

    def add(self, val: int) -> int:
        """
        Add value and return kth largest.

        Time: O(N log N) - Sort entire array
        """
        self.nums.append(val)
        self.nums.sort(reverse=True)
        return self.nums[self.k - 1]


# ============================================================================
#                APPROACH 3: BST APPROACH (ALTERNATIVE)
# ============================================================================

class TreeNode:
    """Node for BST with subtree size tracking."""
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.count = 1  # Number of nodes in subtree

class KthLargest_BST:
    """
    🎯 APPROACH 3: Binary Search Tree (EDUCATIONAL!)

    TIME COMPLEXITY:
      - __init__: O(N log N) average, O(N²) worst
      - add(): O(log N) average, O(N) worst
    SPACE COMPLEXITY: O(N)

    🧠 IDEA: Use BST with subtree size
    ----------------------------------
    - Each node tracks subtree size
    - Can find kth largest in O(log N)
    - Insert new values in O(log N)

    ⚠️  PROBLEMS:
    ------------
    - More complex than heap
    - Can degenerate to O(N) if unbalanced
    - No real advantage over min heap
    - Included for educational purposes

    💡 LESSON: Min heap is simpler and better!
    """

    def __init__(self, k: int, nums: List[int]):
        """Initialize BST with tracking."""
        self.k = k
        self.root = None
        for num in nums:
            self.root = self._insert(self.root, num)

    def _insert(self, node, val):
        """Insert value into BST."""
        if not node:
            return TreeNode(val)
        if val <= node.val:
            node.left = self._insert(node.left, val)
        else:
            node.right = self._insert(node.right, val)
        node.count = 1 + self._size(node.left) + self._size(node.right)
        return node

    def _size(self, node):
        """Get size of subtree."""
        return node.count if node else 0

    def _kth_largest(self, node, k):
        """Find kth largest in BST."""
        right_size = self._size(node.right)
        if k == right_size + 1:
            return node.val
        elif k <= right_size:
            return self._kth_largest(node.right, k)
        else:
            return self._kth_largest(node.left, k - right_size - 1)

    def add(self, val: int) -> int:
        """Add value and return kth largest."""
        self.root = self._insert(self.root, val)
        return self._kth_largest(self.root, self.k)


# ============================================================================
#                    🎨 VISUAL WALKTHROUGH EXAMPLE
# ============================================================================

"""
Let's trace through: k=3, nums=[4,5,8,2], then add(3), add(5), add(10)

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                          APPROACH 1: MIN HEAP (OPTIMAL)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

INITIALIZATION: KthLargest(k=3, nums=[4,5,8,2])
────────────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Processing initial array: [4, 5, 8, 2]                                                                                         │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Add 4:  heap = [4]                          Size = 1 (< k=3, keep it)                                                        │
│                                                                                                                                 │
│   Add 5:  heap = [4, 5]                       Size = 2 (< k=3, keep it)                                                        │
│           Min Heap Structure:                                                                                                   │
│                4                                                                                                                │
│                 ↘                                                                                                               │
│                  5                                                                                                              │
│                                                                                                                                 │
│   Add 8:  heap = [4, 5, 8]                    Size = 3 (= k, perfect!)                                                         │
│           Min Heap Structure:                                                                                                   │
│                4  ← Top (smallest of 3 largest = 3rd largest)                                                                   │
│               ↙ ↘                                                                                                               │
│              5   8                                                                                                              │
│                                                                                                                                 │
│   Add 2:  heap = [2, 4, 8, 5]                 Size = 4 (> k=3, need to evict!)                                                 │
│           After heappop(): [4, 5, 8]          Evicted 2 (smallest)                                                             │
│           Min Heap Structure:                                                                                                   │
│                4  ← Top (3rd largest among [2,4,5,8])                                                                           │
│               ↙ ↘                                                                                                               │
│              5   8                                                                                                              │
│                                                                                                                                 │
│   Final heap after initialization: [4, 5, 8]                                                                                   │
│   Kth largest (3rd largest): heap[0] = 4 ✅                                                                                     │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

OPERATION 1: add(3)
───────────────────

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Adding value: 3                                                                                                                 │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Current heap: [4, 5, 8]                                                                                                      │
│                                                                                                                                 │
│   Step 1: heappush(heap, 3)                                                                                                    │
│           heap = [3, 4, 8, 5]  ← After heapify                                                                                 │
│           Min Heap Structure:                                                                                                   │
│                3  ← New top (temporarily)                                                                                       │
│               ↙ ↘                                                                                                               │
│              4   8                                                                                                              │
│             ↙                                                                                                                   │
│            5                                                                                                                    │
│                                                                                                                                 │
│   Step 2: len(heap) = 4 > k=3, so heappop()                                                                                    │
│           Popped: 3 (smallest, not in top 3!)                                                                                  │
│           heap = [4, 5, 8]                                                                                                     │
│           Min Heap Structure:                                                                                                   │
│                4  ← Top (3rd largest)                                                                                           │
│               ↙ ↘                                                                                                               │
│              5   8                                                                                                              │
│                                                                                                                                 │
│   Stream now: [2, 3, 4, 5, 8]                                                                                                  │
│   Heap contains top 3: [4, 5, 8]                                                                                               │
│                                                                                                                                 │
│   Return: heap[0] = 4 ✅                                                                                                        │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

OPERATION 2: add(5)
───────────────────

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Adding value: 5                                                                                                                 │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Current heap: [4, 5, 8]                                                                                                      │
│                                                                                                                                 │
│   Step 1: heappush(heap, 5)                                                                                                    │
│           heap = [4, 5, 8, 5]  ← After heapify                                                                                 │
│           Min Heap Structure:                                                                                                   │
│                4  ← Top                                                                                                         │
│               ↙ ↘                                                                                                               │
│              5   8                                                                                                              │
│             ↙                                                                                                                   │
│            5                                                                                                                    │
│                                                                                                                                 │
│   Step 2: len(heap) = 4 > k=3, so heappop()                                                                                    │
│           Popped: 4 (was smallest of top 4)                                                                                    │
│           heap = [5, 5, 8]  ← After heapify                                                                                    │
│           Min Heap Structure:                                                                                                   │
│                5  ← Top (NEW 3rd largest!)                                                                                      │
│               ↙ ↘                                                                                                               │
│              5   8                                                                                                              │
│                                                                                                                                 │
│   Stream now: [2, 3, 4, 5, 5, 8]                                                                                               │
│   Heap contains top 3: [5, 5, 8]                                                                                               │
│                                                                                                                                 │
│   Return: heap[0] = 5 ✅                                                                                                        │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

OPERATION 3: add(10)
────────────────────

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Adding value: 10                                                                                                                │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                 │
│   Current heap: [5, 5, 8]                                                                                                      │
│                                                                                                                                 │
│   Step 1: heappush(heap, 10)                                                                                                   │
│           heap = [5, 5, 8, 10]  ← After heapify                                                                                │
│           Min Heap Structure:                                                                                                   │
│                5  ← Top                                                                                                         │
│               ↙ ↘                                                                                                               │
│              5   8                                                                                                              │
│             ↙                                                                                                                   │
│           10                                                                                                                    │
│                                                                                                                                 │
│   Step 2: len(heap) = 4 > k=3, so heappop()                                                                                    │
│           Popped: 5 (smallest of [5,5,8,10])                                                                                   │
│           heap = [5, 8, 10]  ← After heapify, exact order may vary                                                             │
│           Min Heap Structure:                                                                                                   │
│                5  ← Top (3rd largest)                                                                                           │
│               ↙ ↘                                                                                                               │
│              8  10  (or 10, 8 - heap property maintained)                                                                       │
│                                                                                                                                 │
│   Stream now: [2, 3, 4, 5, 5, 8, 10]                                                                                           │
│   Heap contains top 3: [5, 8, 10]                                                                                              │
│                                                                                                                                 │
│   Return: heap[0] = 5 ✅                                                                                                        │
│                                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

KEY INSIGHT: Why Min Heap Works
────────────────────────────────

The min heap of size k always contains the k LARGEST elements seen so far.
The SMALLEST element in this heap (heap[0]) is the kth largest overall!

Example with k=3:
  Stream: [2, 3, 4, 5, 5, 8, 10]
  Top 3: [5, 8, 10]
  3rd largest = smallest of top 3 = 5 ✅

This is why we use MIN heap, not MAX heap!
"""

# ============================================================================
#              🎯 MEMORY TRICKS & COMMON MISTAKES
# ============================================================================

"""
🧠 HOW TO REMEMBER THIS SOLUTION:
---------------------------------
1. "TOP K PODIUM" → Keep only k largest on podium
2. "MIN HEAP MAGIC" → Smallest on top = kth largest!
3. "SIZE LIMIT K" → Heap size never exceeds k
4. "POP SMALLEST" → If size > k, remove smallest!

❌ COMMON MISTAKES TO AVOID:
----------------------------
1. ❌ Using max heap instead of min heap
      WRONG: Max heap gives largest, not kth largest
      RIGHT: Min heap of size k gives kth largest at top

2. ❌ Not limiting heap size
      WRONG: Adding all elements to heap
      RIGHT: Keep heap size ≤ k, pop when exceeds

3. ❌ Forgetting to initialize heap with nums
      WRONG: Start with empty heap
      RIGHT: Process all initial nums in __init__

4. ❌ Using sorted array for streaming data
      WRONG: O(N log N) for each add()
      RIGHT: O(log k) with min heap

5. ❌ Checking if heap is empty before returning
      WRONG: May return from empty heap
      RIGHT: Problem guarantees at least k elements

✅ PRO TIPS:
-----------
1. Min heap of size k is THE pattern for "kth largest"
2. Python heapq is always min heap (smallest on top)
3. For kth smallest, use max heap (or negate values)
4. Heap size limit = k is crucial for efficiency
5. This pattern appears in many "top k" problems

🎯 INTERVIEW STRATEGY:
---------------------
"I'll use a min heap of size k to track the k largest elements. The top of
the heap will be the smallest among these k largest, which is exactly the
kth largest overall. When a new element comes in, I add it and if the heap
exceeds size k, I remove the smallest. This gives O(log k) time per add()."
"""

# ============================================================================
#                         🧪 TEST CASES
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("          KTH LARGEST ELEMENT IN STREAM - TEST CASES")
    print("="*80)

    # Test Case 1: Standard case from problem
    print("\n📝 Test Case 1: Standard case (k=3)")
    print("-" * 80)
    kth1 = KthLargest(3, [4, 5, 8, 2])
    print(f"Initialized with k=3, nums=[4, 5, 8, 2]")

    result1_1 = kth1.add(3)
    print(f"add(3) = {result1_1}, Expected: 4")
    print(f"✅ PASS" if result1_1 == 4 else "❌ FAIL")

    result1_2 = kth1.add(5)
    print(f"add(5) = {result1_2}, Expected: 5")
    print(f"✅ PASS" if result1_2 == 5 else "❌ FAIL")

    result1_3 = kth1.add(10)
    print(f"add(10) = {result1_3}, Expected: 5")
    print(f"✅ PASS" if result1_3 == 5 else "❌ FAIL")

    result1_4 = kth1.add(9)
    print(f"add(9) = {result1_4}, Expected: 8")
    print(f"✅ PASS" if result1_4 == 8 else "❌ FAIL")

    result1_5 = kth1.add(4)
    print(f"add(4) = {result1_5}, Expected: 8")
    print(f"✅ PASS" if result1_5 == 8 else "❌ FAIL")

    # Test Case 2: k=1 (find largest)
    print("\n📝 Test Case 2: k=1 (find largest)")
    print("-" * 80)
    kth2 = KthLargest(1, [1, 2, 3])
    print(f"Initialized with k=1, nums=[1, 2, 3]")
    result2_1 = kth2.add(4)
    print(f"add(4) = {result2_1}, Expected: 4")
    print(f"✅ PASS" if result2_1 == 4 else "❌ FAIL")

    result2_2 = kth2.add(2)
    print(f"add(2) = {result2_2}, Expected: 4")
    print(f"✅ PASS" if result2_2 == 4 else "❌ FAIL")

    # Test Case 3: Empty initial array
    print("\n📝 Test Case 3: Empty initial array")
    print("-" * 80)
    kth3 = KthLargest(2, [])
    print(f"Initialized with k=2, nums=[]")
    result3_1 = kth3.add(3)
    print(f"add(3) = {result3_1} (only 1 element, returns smallest)")

    result3_2 = kth3.add(5)
    print(f"add(5) = {result3_2}, Expected: 3")
    print(f"✅ PASS" if result3_2 == 3 else "❌ FAIL")

    result3_3 = kth3.add(10)
    print(f"add(10) = {result3_3}, Expected: 5")
    print(f"✅ PASS" if result3_3 == 5 else "❌ FAIL")

    # Test Case 4: Negative numbers
    print("\n📝 Test Case 4: Negative numbers")
    print("-" * 80)
    kth4 = KthLargest(2, [-1, -2])
    print(f"Initialized with k=2, nums=[-1, -2]")
    result4_1 = kth4.add(3)
    print(f"add(3) = {result4_1}, Expected: -1")
    print(f"✅ PASS" if result4_1 == -1 else "❌ FAIL")

    result4_2 = kth4.add(-3)
    print(f"add(-3) = {result4_2}, Expected: -1")
    print(f"✅ PASS" if result4_2 == -1 else "❌ FAIL")

    # Test Case 5: All same values
    print("\n📝 Test Case 5: All same values")
    print("-" * 80)
    kth5 = KthLargest(3, [5, 5, 5, 5])
    print(f"Initialized with k=3, nums=[5, 5, 5, 5]")
    result5_1 = kth5.add(5)
    print(f"add(5) = {result5_1}, Expected: 5")
    print(f"✅ PASS" if result5_1 == 5 else "❌ FAIL")

    # Test Case 6: Compare all three approaches
    print("\n📝 Test Case 6: Comparing all approaches")
    print("-" * 80)
    kth_heap = KthLargest(2, [1, 2, 3])
    kth_sorted = KthLargest_Sorted(2, [1, 2, 3])

    result_heap = kth_heap.add(4)
    result_sorted = kth_sorted.add(4)
    print(f"Min Heap approach: {result_heap}")
    print(f"Sorted approach: {result_sorted}")
    print(f"✅ PASS" if result_heap == result_sorted == 3 else "❌ FAIL")

    print("\n" + "="*80)
    print("              ✅ ALL TEST CASES COMPLETED!")
    print("="*80)


# ============================================================================
#              🎓 LEARNING SUMMARY & KEY TAKEAWAYS
# ============================================================================

"""
🎯 WHAT YOU LEARNED:
-------------------
1. Min heap of size k efficiently tracks k largest elements
2. Top of min heap = smallest of k largest = kth largest
3. Limiting heap size to k is crucial for O(log k) efficiency
4. This pattern is fundamental for streaming "top k" problems

🔑 KEY PATTERN: "Min Heap for Kth Largest"
------------------------------------------
This pattern applies when:
- Need to track kth largest/smallest in stream
- Data comes continuously (can't sort entire dataset)
- Need efficient updates (O(log k) better than O(N))

Used in:
- Kth Largest Element in Stream (this problem!)
- Kth Largest Element in Array (LeetCode #215)
- Find K Closest Points (LeetCode #973)
- Top K Frequent Elements (LeetCode #347)

💪 THREE APPROACHES TO MASTER:
-----------------------------
1. MIN HEAP (Optimal - O(log k))
   - Maintain heap of size k
   - Top = kth largest
   - Most efficient for streams

2. SORTED ARRAY (Simple - O(N log N))
   - Sort after each add
   - Pick kth element
   - Simple but inefficient

3. BST (Alternative - O(log N))
   - More complex
   - Can be unbalanced
   - No advantage over heap

🎯 INTERVIEW TIPS:
-----------------
1. Clarify: "kth largest" or "kth distinct"? (usually largest)
2. Ask about stream size (if huge, heap is essential)
3. Mention space optimization (only store k elements)
4. Explain why min heap, not max heap
5. Discuss trade-offs vs sorting

🎉 CONGRATULATIONS!
------------------
You now understand the "min heap for kth largest" pattern!
Remember: "Keep top k on podium, smallest on top is kth largest!"

📊 COMPLEXITY SUMMARY:
---------------------
┌────────────────────┬──────────────┬──────────────┐
│ Approach           │ Time (add)   │ Space        │
├────────────────────┼──────────────┼──────────────┤
│ Min Heap (Best)    │ O(log k)     │ O(k)         │
│ Sorted Array       │ O(N log N)   │ O(N)         │
│ BST                │ O(log N)     │ O(N)         │
└────────────────────┴──────────────┴──────────────┘

k = required rank, N = total elements in stream

🏆 RECOMMENDED: Use Min Heap for optimal O(log k) solution!

🔗 RELATED PROBLEMS TO PRACTICE:
-------------------------------
1. LeetCode #703: Kth Largest Element in a Stream (this problem!)
2. LeetCode #215: Kth Largest Element in an Array
3. LeetCode #347: Top K Frequent Elements
4. LeetCode #973: K Closest Points to Origin
5. LeetCode #378: Kth Smallest Element in Sorted Matrix

💡 FINAL TIP:
------------
The "min heap of size k" pattern is one of the MOST IMPORTANT heap patterns!
It appears constantly in interviews and real systems (trending topics, top
scores, leaderboards, etc.). Master this pattern and you'll solve dozens of
similar problems instantly!
"""
