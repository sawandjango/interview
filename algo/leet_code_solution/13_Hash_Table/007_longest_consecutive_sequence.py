"""
LeetCode Problem #128: Longest Consecutive Sequence

Difficulty: Medium
Topics: Array, Hash Table, Union Find
Companies: Google, Facebook, Amazon, Microsoft, Bloomberg, Uber, Apple

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
│ 4    │ 💡 SOLUTION 1: Hash Set ⭐           │ • WHY choose? (Pros/Cons)     │
│      │    (OPTIMAL - O(N))                  │ • WHEN to use?                │
│      │                                      │ • Step-by-step walkthrough    │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 5    │ 💡 SOLUTION 2: Sorting               │ • WHY choose? (Pros/Cons)     │
│      │    (Simple but O(N log N))           │ • WHEN to use?                │
│      │                                      │ • Comparison with Solution 1  │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 6    │ 💡 SOLUTION 3: Union-Find            │ • WHY choose? (Pros/Cons)     │
│      │    (Advanced)                        │ • WHEN to use?                │
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
│ ANALOGY          │ "Chain Links" - Find the longest unbroken chain!       │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ PATTERN          │ "Sequence Start Detection" - Only count from START!    │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ KEY TRICK        │ If (num-1) exists, skip! Not a sequence start!         │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ DEFAULT SOLUTION │ Hash Set with smart iteration (O(N) - OPTIMAL!)        │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ TIME COMPLEXITY  │ O(N) - Linear time with hash set                       │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ SPACE COMPLEXITY │ O(N) - Hash set storage                                │
└──────────────────┴──────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        ⚡ QUICK DECISION TABLE                              │
├────────────────────────────────────┬────────────────────────────────────────┤
│ SITUATION                          │ WHICH SOLUTION TO USE?                │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Normal interview (need O(N))       │ ✅ Solution 1 (Hash Set)              │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Want optimal solution              │ ✅ Solution 1 (O(N) time!)            │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Sorting allowed, want simplicity   │ ⚠️  Solution 2 (O(N log N))           │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Learning advanced data structures  │ 🎓 Solution 3 (Union-Find)           │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Small array (< 100 elements)       │ Any solution works                    │
├────────────────────────────────────┼────────────────────────────────────────┤
│ Want to show optimization          │ 🎯 Start with Sol 2, optimize to 1   │
└────────────────────────────────────┴────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     📊 SOLUTION COMPARISON TABLE                            │
├──────────────────┬──────────────┬──────────────┬──────────────┬─────────────┤
│ CRITERIA         │ HASH SET     │ SORTING      │ UNION-FIND   │ WINNER      │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Time Complexity  │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐       │ ⭐⭐⭐⭐     │ Hash Set    │
│                  │ O(N)         │ O(N log N)   │ O(N α(N))    │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Space Complexity │ ⭐⭐⭐       │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐       │ Sorting     │
│                  │ O(N)         │ O(1)         │ O(N)         │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Code Simplicity  │ ⭐⭐⭐⭐     │ ⭐⭐⭐⭐⭐   │ ⭐⭐         │ Sorting     │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Interview Speed  │ ⭐⭐⭐⭐     │ ⭐⭐⭐⭐⭐   │ ⭐⭐         │ Sorting     │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Meets O(N) req   │ ✅ YES       │ ❌ NO        │ ✅ YES       │ Hash Set    │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Overall Best     │ ✅ OPTIMAL   │ Good         │ Educational  │ Hash Set!   │
└──────────────────┴──────────────┴──────────────┴──────────────┴─────────────┘

⏱️  TIME TO MASTER: 20-25 minutes
🎯 DIFFICULTY: Medium
💡 TIP: "Only start counting from sequence beginnings!"
🔥 POPULAR: Top 50 most asked interview question!

================================================================================
                           🎯 PROBLEM UNDERSTANDING
================================================================================

WHAT IS THE PROBLEM?
--------------------
Given an unsorted array, find the LENGTH of the longest sequence of consecutive
integers. The sequence doesn't have to be in order in the original array!

REAL WORLD ANALOGY:
------------------
Think of BUILDING BLOCKS numbered 1-100, scattered on the floor:
- You find blocks: [100, 4, 200, 1, 3, 2]
- You want to build the longest consecutive tower
- Blocks [1, 2, 3, 4] can form a tower of height 4 ✅
- Block [100] alone = tower of height 1
- Block [200] alone = tower of height 1
- Longest tower = 4

Another analogy - PAGE NUMBERS:
- You have pages: [5, 3, 4, 10, 1, 2]
- Consecutive sequences: [1,2,3,4,5] and [10]
- Longest sequence = 5 pages

THE KEY INSIGHT:
---------------
DON'T start counting from every number!
Only count when you find the START of a sequence!

How to find START? Check if (num - 1) exists:
- If num-1 exists → NOT a start, skip!
- If num-1 doesn't exist → START! Count from here!

❌ Wrong thinking: "Check every number and count forward" → O(N²)
✅ Right thinking: "Only count from sequence starts" → O(N)!

================================================================================
                            📝 FORMAL PROBLEM
================================================================================

Given an unsorted array of integers nums, return the length of the longest
consecutive elements sequence.

You must write an algorithm that runs in O(n) time.

Example 1:
----------
Input: nums = [100,4,200,1,3,2]
Output: 4
Explanation: The longest consecutive sequence is [1, 2, 3, 4].
Therefore its length is 4.

Example 2:
----------
Input: nums = [0,3,7,2,5,8,4,6,0,1]
Output: 9
Explanation: The sequence is [0,1,2,3,4,5,6,7,8] (length 9).

Constraints:
------------
* 0 <= nums.length <= 10^5
* -10^9 <= nums[i] <= 10^9

Follow-up:
----------
Your algorithm MUST be O(n) time complexity.

================================================================================
                         🧠 KEY INSIGHTS TO REMEMBER
================================================================================

THE MAIN CHALLENGE:
------------------
❌ Sorting works but takes O(N log N) - violates requirement!
❌ Checking every pair is O(N²) - too slow!
✅ Smart hash set iteration achieves O(N)!

THE MAGIC TRICK: "SEQUENCE START DETECTION"
-------------------------------------------
Key observation: Each number is visited at most TWICE!
- Once: Check if it's a sequence start
- Twice (if start): Count consecutive numbers from it

Example: [4, 1, 3, 2]
- Check 4: Is 3 in set? YES → Skip (not a start)
- Check 1: Is 0 in set? NO → START! Count 1,2,3,4 = length 4
- Check 3: Is 2 in set? YES → Skip
- Check 2: Is 1 in set? YES → Skip

Only counted ONCE from the start!

THE BREAKTHROUGH INSIGHT:
------------------------
┌─────────────────────────────────────────────────────────────┐
│  If (num - 1) NOT in set → num is a SEQUENCE START!        │
│  → Count forward: num, num+1, num+2, ...                   │
│  → This ensures O(N) because no redundant counting!        │
└─────────────────────────────────────────────────────────────┘

WHY THIS IS O(N):
-----------------
Even though there's a nested while loop, each number is visited max 2 times:
1. During the "is it a start?" check
2. When counting from an actual start

Total operations = 2N = O(N)

================================================================================
                          💡 SOLUTION APPROACHES
================================================================================
"""

from typing import List

# ============================================================================
#                APPROACH 1: HASH SET (OPTIMAL - O(N))
# ============================================================================

def longestConsecutive_HashSet(nums: List[int]) -> int:
    """
    🎯 APPROACH 1: Smart Hash Set Iteration (BEST SOLUTION!)

    TIME COMPLEXITY: O(N) - Each number visited at most twice
    SPACE COMPLEXITY: O(N) - Hash set storage

    🧠 MEMORIZATION TRICK: "Start From The Beginning"
    -------------------------------------------------
    Think: Don't start counting from middle of sequence!
    - Check if (num-1) exists
    - If YES → Skip (not a start)
    - If NO → Start counting!

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Convert array to set for O(1) lookups
    2. For each number in set:
       a. If (num-1) in set → SKIP (not a sequence start)
       b. If (num-1) NOT in set → COUNT from here!
          - current = num, length = 1
          - While (current+1) in set:
              current += 1, length += 1
       c. Track max length
    3. Return max length

    🎨 VISUAL EXAMPLE:
    -----------------
    Input: [100, 4, 200, 1, 3, 2]

    Step 1: Create set
      num_set = {100, 4, 200, 1, 3, 2}

    Step 2: Check each number
      100: Is 99 in set? NO → START!
           Count: 100 → length=1 (101 not in set)

      4: Is 3 in set? YES → SKIP (not a start)

      200: Is 199 in set? NO → START!
           Count: 200 → length=1 (201 not in set)

      1: Is 0 in set? NO → START!
         Count: 1 → 2 → 3 → 4 → length=4 ✅

      3: Is 2 in set? YES → SKIP

      2: Is 1 in set? YES → SKIP

    Result: max_length = 4

    WHY THIS IS O(N):
    ----------------
    Each number visited max 2 times:
    - Once in main loop
    - Once when counting (if it's part of a sequence from a start)
    Total: 2N operations = O(N)
    """
    if not nums:
        return 0

    num_set = set(nums)
    max_length = 0

    for num in num_set:
        # Check if this is the start of a sequence
        if num - 1 not in num_set:
            # This is a sequence start!
            current_num = num
            current_length = 1

            # Count consecutive numbers
            while current_num + 1 in num_set:
                current_num += 1
                current_length += 1

            max_length = max(max_length, current_length)

    return max_length


# ============================================================================
#              APPROACH 2: SORTING (SIMPLE BUT O(N LOG N))
# ============================================================================

def longestConsecutive_Sorting(nums: List[int]) -> int:
    """
    🎯 APPROACH 2: Sort and Scan (VIOLATES O(N) requirement!)

    TIME COMPLEXITY: O(N log N) - Sorting dominates
    SPACE COMPLEXITY: O(1) or O(N) depending on sort

    🧠 MEMORIZATION TRICK: "Sort Then Count"
    ----------------------------------------
    Simple approach:
    1. Sort array
    2. Count consecutive runs
    3. Skip duplicates

    📝 ALGORITHM:
    ------------
    1. Sort array
    2. Initialize: max_length=1, current_length=1
    3. For each adjacent pair:
       - If duplicate → Skip
       - If consecutive (diff=1) → Increment current_length
       - If gap → Reset current_length
    4. Return max_length

    🎨 VISUAL EXAMPLE:
    -----------------
    Input: [100, 4, 200, 1, 3, 2]

    After sorting: [1, 2, 3, 4, 100, 200]

    Scan:
      1 → 2: consecutive! length=2
      2 → 3: consecutive! length=3
      3 → 4: consecutive! length=4
      4 → 100: gap! reset, length=1
      100 → 200: gap! reset, length=1

    Result: max_length = 4

    ⚠️  WHY NOT OPTIMAL:
    -------------------
    - Sorting takes O(N log N)
    - Violates problem requirement of O(N)
    - But: SIMPLER to code and understand!
    - Good starting point in interview before optimizing
    """
    if not nums:
        return 0

    nums.sort()
    max_length = 1
    current_length = 1

    for i in range(1, len(nums)):
        if nums[i] == nums[i-1]:
            # Skip duplicates
            continue
        elif nums[i] == nums[i-1] + 1:
            # Consecutive
            current_length += 1
            max_length = max(max_length, current_length)
        else:
            # Gap - reset
            current_length = 1

    return max_length


# ============================================================================
#                APPROACH 3: UNION-FIND (ADVANCED)
# ============================================================================

def longestConsecutive_UnionFind(nums: List[int]) -> int:
    """
    🎯 APPROACH 3: Union-Find Data Structure (EDUCATIONAL!)

    TIME COMPLEXITY: O(N α(N)) ≈ O(N) where α is inverse Ackermann
    SPACE COMPLEXITY: O(N)

    🧠 IDEA: Group consecutive numbers using Union-Find
    --------------------------------------------------
    - Each number starts as its own set
    - If num+1 exists, union(num, num+1)
    - Find largest set size

    📝 ALGORITHM:
    ------------
    1. Initialize parent and size dicts
    2. For each num, union with num+1 if exists
    3. Return max set size

    ⚠️  NOTE: This is overkill for this problem!
    -------------------------------------------
    Hash set approach is simpler and equally fast.
    Union-Find is here for educational purposes.
    """
    if not nums:
        return 0

    parent = {}
    size = {}

    def find(x):
        if x not in parent:
            parent[x] = x
            size[x] = 1
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]

    def union(x, y):
        root_x, root_y = find(x), find(y)
        if root_x != root_y:
            # Union by size
            if size[root_x] < size[root_y]:
                root_x, root_y = root_y, root_x
            parent[root_y] = root_x
            size[root_x] += size[root_y]

    # Initialize
    for num in nums:
        find(num)

    # Union consecutive numbers
    for num in nums:
        if num + 1 in parent:
            union(num, num + 1)

    return max(size.values())


# ============================================================================
#                    🎨 VISUAL WALKTHROUGH EXAMPLE
# ============================================================================

"""
Input: nums = [100, 4, 200, 1, 3, 2]

═══════════════════════════════════════════════════════════════════════════
                    APPROACH 1: HASH SET (OPTIMAL)
═══════════════════════════════════════════════════════════════════════════

STEP 1: Convert to Set
──────────────────────
num_set = {100, 4, 200, 1, 3, 2}

STEP 2: Process Each Number
────────────────────────────

┌─────────────────────────────────────────────────────────────────────────┐
│ Check num = 100                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Is (100 - 1 = 99) in set? NO ✅                                      │
│   → This is a SEQUENCE START!                                          │
│                                                                         │
│   Count forward:                                                        │
│   100 → Is 101 in set? NO                                              │
│                                                                         │
│   Sequence: [100]                                                       │
│   Length: 1                                                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ Check num = 4                                                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Is (4 - 1 = 3) in set? YES ❌                                        │
│   → NOT a sequence start! SKIP!                                        │
│   (Will be counted when we process '1')                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ Check num = 200                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Is (200 - 1 = 199) in set? NO ✅                                     │
│   → This is a SEQUENCE START!                                          │
│                                                                         │
│   Count forward:                                                        │
│   200 → Is 201 in set? NO                                              │
│                                                                         │
│   Sequence: [200]                                                       │
│   Length: 1                                                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ Check num = 1                                                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Is (1 - 1 = 0) in set? NO ✅                                         │
│   → This is a SEQUENCE START!                                          │
│                                                                         │
│   Count forward:                                                        │
│   1 → Is 2 in set? YES! current=2, length=2                            │
│   2 → Is 3 in set? YES! current=3, length=3                            │
│   3 → Is 4 in set? YES! current=4, length=4                            │
│   4 → Is 5 in set? NO, stop                                            │
│                                                                         │
│   Sequence: [1, 2, 3, 4]                                               │
│   Length: 4 ⭐ LONGEST!                                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ Check num = 3                                                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Is (3 - 1 = 2) in set? YES ❌                                        │
│   → NOT a sequence start! SKIP!                                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ Check num = 2                                                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Is (2 - 1 = 1) in set? YES ❌                                        │
│   → NOT a sequence start! SKIP!                                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

FINAL RESULT: max_length = 4

SEQUENCES FOUND:
────────────────
  [100]        → length 1
  [200]        → length 1
  [1,2,3,4]    → length 4 ✅ ANSWER!

═══════════════════════════════════════════════════════════════════════════
                    APPROACH 2: SORTING (SIMPLER)
═══════════════════════════════════════════════════════════════════════════

Original: [100, 4, 200, 1, 3, 2]
Sorted:   [1, 2, 3, 4, 100, 200]

Scan consecutive pairs:
───────────────────────
1 → 2:   consecutive! length=2
2 → 3:   consecutive! length=3
3 → 4:   consecutive! length=4 ✅
4 → 100: gap (96), reset to length=1
100 → 200: gap (100), reset to length=1

RESULT: max_length = 4

═══════════════════════════════════════════════════════════════════════════
                    WHY HASH SET IS O(N) - DETAILED PROOF
═══════════════════════════════════════════════════════════════════════════

Question: "Doesn't the while loop make it O(N²)?"
Answer: NO! Here's why:

Each number is visited AT MOST TWICE:

Visit 1: During main for loop - checking "is this a start?"
Visit 2: During while loop - when counting from an actual start

Example: [1, 2, 3, 4]

Number 1: Visited 2 times
  - Main loop: "Is 0 in set? No → START!"
  - While loop: "Count from 1..."

Number 2: Visited 2 times
  - Main loop: "Is 1 in set? Yes → SKIP!"
  - While loop: "...2 is consecutive..."

Number 3: Visited 2 times
  - Main loop: "Is 2 in set? Yes → SKIP!"
  - While loop: "...3 is consecutive..."

Number 4: Visited 2 times
  - Main loop: "Is 3 in set? Yes → SKIP!"
  - While loop: "...4 is consecutive, stop"

Total visits = 2N = O(N)!

The key: We ONLY count forward from sequence STARTS!
"""

# ============================================================================
#              🎯 MEMORY TRICKS & COMMON MISTAKES
# ============================================================================

"""
🧠 HOW TO REMEMBER THIS SOLUTION:
---------------------------------
1. "SEQUENCE START" → Check if num-1 exists
2. "SKIP THE MIDDLE" → Don't count from middle of sequence
3. "HASH FOR SPEED" → Set gives O(1) lookup
4. "VISIT TWICE MAX" → That's why it's O(N)!

❌ COMMON MISTAKES TO AVOID:
----------------------------
1. ❌ Counting from every number
      WRONG: For each num, count forward (O(N²))
      RIGHT: Only count from sequence starts (O(N))

2. ❌ Sorting when O(N) is required
      WRONG: Sort first (O(N log N))
      RIGHT: Use hash set (O(N))

3. ❌ Forgetting to handle duplicates (when sorting)
      WRONG: Count duplicates as consecutive
      RIGHT: Skip duplicates

4. ❌ Not handling empty array
      WRONG: Assume array has elements
      RIGHT: Check if empty, return 0

5. ❌ Thinking nested loop = O(N²)
      WRONG: "While loop inside for = O(N²)"
      RIGHT: Each element visited max twice = O(N)

✅ PRO TIPS:
-----------
1. Hash set is KEY to O(N) solution
2. The "num-1 check" is the magic insight
3. Draw out the sequence checking process
4. Explain WHY it's O(N) (visits twice max)
5. Start with sorting in interview, then optimize

🎯 INTERVIEW STRATEGY:
---------------------
"I'll use a hash set for O(1) lookups. The key insight is to only start
counting from the BEGINNING of each sequence. I check if num-1 exists - if
not, this is a sequence start. Then I count forward. This ensures each number
is visited at most twice, giving us O(N) time complexity."
"""

# ============================================================================
#                         🧪 TEST CASES
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("          LONGEST CONSECUTIVE SEQUENCE - TEST CASES")
    print("="*80)

    # Test Case 1: Standard case
    print("\n📝 Test Case 1: Standard case")
    print("-" * 80)
    nums1 = [100, 4, 200, 1, 3, 2]
    print(f"Input: {nums1}")
    result1_a = longestConsecutive_HashSet(nums1)
    result1_b = longestConsecutive_Sorting(nums1)
    result1_c = longestConsecutive_UnionFind(nums1)
    print(f"Output (Hash Set):  {result1_a}")
    print(f"Output (Sorting):   {result1_b}")
    print(f"Output (Union-Find): {result1_c}")
    print(f"Expected: 4 (sequence [1,2,3,4])")
    print(f"✅ PASS" if result1_a == 4 else "❌ FAIL")

    # Test Case 2: Longer sequence
    print("\n📝 Test Case 2: Longer consecutive sequence")
    print("-" * 80)
    nums2 = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
    print(f"Input: {nums2}")
    result2_a = longestConsecutive_HashSet(nums2)
    result2_b = longestConsecutive_Sorting(nums2)
    result2_c = longestConsecutive_UnionFind(nums2)
    print(f"Output (Hash Set):  {result2_a}")
    print(f"Output (Sorting):   {result2_b}")
    print(f"Output (Union-Find): {result2_c}")
    print(f"Expected: 9 (sequence [0,1,2,3,4,5,6,7,8])")
    print(f"✅ PASS" if result2_a == 9 else "❌ FAIL")

    # Test Case 3: Empty array
    print("\n📝 Test Case 3: Empty array")
    print("-" * 80)
    nums3 = []
    print(f"Input: {nums3}")
    result3_a = longestConsecutive_HashSet(nums3)
    result3_b = longestConsecutive_Sorting(nums3)
    result3_c = longestConsecutive_UnionFind(nums3)
    print(f"Output (Hash Set):  {result3_a}")
    print(f"Output (Sorting):   {result3_b}")
    print(f"Output (Union-Find): {result3_c}")
    print(f"Expected: 0")
    print(f"✅ PASS" if result3_a == 0 else "❌ FAIL")

    # Test Case 4: Single element
    print("\n📝 Test Case 4: Single element")
    print("-" * 80)
    nums4 = [1]
    print(f"Input: {nums4}")
    result4_a = longestConsecutive_HashSet(nums4)
    result4_b = longestConsecutive_Sorting(nums4)
    result4_c = longestConsecutive_UnionFind(nums4)
    print(f"Output (Hash Set):  {result4_a}")
    print(f"Output (Sorting):   {result4_b}")
    print(f"Output (Union-Find): {result4_c}")
    print(f"Expected: 1")
    print(f"✅ PASS" if result4_a == 1 else "❌ FAIL")

    # Test Case 5: No consecutive numbers
    print("\n📝 Test Case 5: No consecutive numbers")
    print("-" * 80)
    nums5 = [1, 3, 5, 7, 9]
    print(f"Input: {nums5}")
    result5_a = longestConsecutive_HashSet(nums5)
    result5_b = longestConsecutive_Sorting(nums5)
    result5_c = longestConsecutive_UnionFind(nums5)
    print(f"Output (Hash Set):  {result5_a}")
    print(f"Output (Sorting):   {result5_b}")
    print(f"Output (Union-Find): {result5_c}")
    print(f"Expected: 1")
    print(f"✅ PASS" if result5_a == 1 else "❌ FAIL")

    # Test Case 6: Duplicates
    print("\n📝 Test Case 6: Array with duplicates")
    print("-" * 80)
    nums6 = [1, 2, 0, 1, 2, 3]
    print(f"Input: {nums6}")
    result6_a = longestConsecutive_HashSet(nums6)
    result6_b = longestConsecutive_Sorting(nums6)
    result6_c = longestConsecutive_UnionFind(nums6)
    print(f"Output (Hash Set):  {result6_a}")
    print(f"Output (Sorting):   {result6_b}")
    print(f"Output (Union-Find): {result6_c}")
    print(f"Expected: 4 (sequence [0,1,2,3])")
    print(f"✅ PASS" if result6_a == 4 else "❌ FAIL")

    # Test Case 7: Negative numbers
    print("\n📝 Test Case 7: Negative numbers")
    print("-" * 80)
    nums7 = [-1, -2, 0, 1, 2]
    print(f"Input: {nums7}")
    result7_a = longestConsecutive_HashSet(nums7)
    result7_b = longestConsecutive_Sorting(nums7)
    result7_c = longestConsecutive_UnionFind(nums7)
    print(f"Output (Hash Set):  {result7_a}")
    print(f"Output (Sorting):   {result7_b}")
    print(f"Output (Union-Find): {result7_c}")
    print(f"Expected: 5 (sequence [-2,-1,0,1,2])")
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
1. Hash set enables O(N) solution with smart iteration
2. Only count from sequence STARTS (num-1 check)
3. Each number visited at most twice = O(N)
4. Three approaches with different trade-offs

🔑 KEY PATTERN: "Smart Iteration with Hash Set"
-----------------------------------------------
This pattern applies when:
- Need to find sequences/groups
- Can't sort (O(N) requirement)
- Need O(1) membership checking

Used in:
- Longest Consecutive Sequence (this problem)
- Missing Number ranges
- Island counting (with modifications)
- Connected components

💪 THREE APPROACHES TO MASTER:
-----------------------------
1. HASH SET (Optimal - O(N))
   - Convert to set
   - Check num-1 to find starts
   - Count forward from starts only

2. SORTING (Simple - O(N log N))
   - Sort array
   - Scan for consecutive runs
   - Handle duplicates

3. UNION-FIND (Educational - O(N))
   - Build disjoint sets
   - Union consecutive numbers
   - Find max set size

🎯 INTERVIEW TIPS:
-----------------
1. Start with sorting approach (shows you can solve it)
2. Then optimize to hash set (shows you know O(N) techniques)
3. Explain WHY it's O(N) (visits twice max)
4. Draw diagram showing sequence detection
5. Test with duplicates and negative numbers

🎉 CONGRATULATIONS!
------------------
You now understand how to find longest consecutive sequence in O(N)!
Remember: "Only start counting from sequence beginnings!"

📊 COMPLEXITY SUMMARY:
---------------------
┌────────────────────┬──────────────┬──────────────┐
│ Approach           │ Time         │ Space        │
├────────────────────┼──────────────┼──────────────┤
│ Hash Set (Best)    │ O(N)         │ O(N)         │
│ Sorting            │ O(N log N)   │ O(1)         │
│ Union-Find         │ O(N α(N))    │ O(N)         │
└────────────────────┴──────────────┴──────────────┘

N = array length
α(N) = inverse Ackermann function (effectively constant)

🏆 RECOMMENDED: Use Hash Set for optimal O(N) solution!

🔗 RELATED PROBLEMS TO PRACTICE:
-------------------------------
1. LeetCode #128: Longest Consecutive Sequence (this problem!)
2. LeetCode #298: Binary Tree Longest Consecutive Sequence
3. LeetCode #549: Binary Tree Longest Consecutive Sequence II
4. LeetCode #128: Find Missing Ranges
5. Number of Islands (uses similar pattern)

💡 FINAL TIP:
------------
The "start detection" trick (checking num-1) is POWERFUL!
It transforms O(N²) to O(N) by avoiding redundant counting.
Master this pattern - it appears in many sequence problems!
"""
