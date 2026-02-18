"""
LeetCode Problem #217: Contains Duplicate

Difficulty: Easy
Topics: Array, Hash Table, Sorting
Companies: Amazon, Microsoft, Apple, Google, Facebook, Adobe

================================================================================
                    📚 QUICK REFERENCE - WHAT'S IN THIS FILE
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                        📖 TABLE OF CONTENTS                                 │
├──────┬──────────────────────────────────────────┬───────────────────────────┤
│ #    │ SECTION                                  │ WHAT YOU'LL LEARN         │
├──────┼──────────────────────────────────────────┼───────────────────────────┤
│ 1    │ 🎯 PROBLEM UNDERSTANDING                 │ • What is being asked?    │
│      │                                          │ • Real-world analogies    │
│      │                                          │ • Visual examples         │
├──────┼──────────────────────────────────────────┼───────────────────────────┤
│ 2    │ 🧠 KEY INSIGHTS TO REMEMBER              │ • Main challenge          │
│      │                                          │ • Base cases to handle    │
│      │                                          │ • Pattern recognition     │
├──────┼──────────────────────────────────────────┼───────────────────────────┤
│ 3    │ 🚀 HOW TO APPROACH THIS PROBLEM          │ • Step-by-step process    │
│      │                                          │ • Decision tree           │
│      │                                          │ • Interview scenarios     │
├──────┼──────────────────────────────────────────┼───────────────────────────┤
│ 4    │ 💡 SOLUTION 1: Hash Set ⭐               │ • WHY choose? (Pros/Cons) │
│      │    (RECOMMENDED)                         │ • WHEN to use?            │
│      │                                          │ • Step-by-step walkthrough│
├──────┼──────────────────────────────────────────┼───────────────────────────┤
│ 5    │ 💡 SOLUTION 2: Sorting                   │ • WHY choose? (Pros/Cons) │
│      │    (Space Optimized)                     │ • WHEN to use?            │
│      │                                          │ • Comparison with Sol 1   │
├──────┼──────────────────────────────────────────┼───────────────────────────┤
│ 6    │ 💡 SOLUTION 3: Brute Force               │ • WHY choose? (Pros/Cons) │
│      │    (Naive Approach)                      │ • WHEN to use?            │
│      │                                          │ • Educational purposes    │
├──────┼──────────────────────────────────────────┼───────────────────────────┤
│ 7    │ 💻 IMPLEMENTATION                        │ • Clean, commented code   │
│      │                                          │ • All three solutions     │
├──────┼──────────────────────────────────────────┼───────────────────────────┤
│ 8    │ 🧪 TEST CASES                            │ • Comprehensive tests     │
│      │                                          │ • Edge cases covered      │
├──────┼──────────────────────────────────────────┼───────────────────────────┤
│ 9    │ 🎓 LEARNING SUMMARY                      │ • Key takeaways           │
│      │                                          │ • Memory tricks           │
│      │                                          │ • Common mistakes         │
├──────┼──────────────────────────────────────────┼───────────────────────────┤
│ 10   │ 🔗 RELATED PROBLEMS                      │ • Similar problems        │
│      │                                          │ • Pattern recognition     │
└──────┴──────────────────────────────────────────┴───────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           🎯 MEMORY CHEAT SHEET                             │
├──────────────────┬──────────────────────────────────────────────────────────┤
│ ANALOGY          │ "Attendance Check" - Have I seen you before?            │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ PATTERN          │ "Seen Before Tracking" - Remember what you've seen!     │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ BASE CASE        │ Empty or single element → No duplicates!                │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ DEFAULT SOLUTION │ Hash Set (Optimal time and space!)                      │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ TIME COMPLEXITY  │ O(n) - Single pass through array                        │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ SPACE COMPLEXITY │ O(n) - Set stores unique elements                       │
└──────────────────┴──────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        ⚡ QUICK DECISION TABLE                              │
├────────────────────────────────┬────────────────────────────────────────────┤
│ SITUATION                      │ WHICH SOLUTION TO USE?                    │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Normal interview               │ ✅ Solution 1 (Hash Set)                  │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Need optimal time              │ ✅ Solution 1 (O(n) time)                 │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Memory constraints             │ ✅ Solution 2 (Sorting - O(1) space)      │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Can modify input array         │ ✅ Solution 2 (Sort in-place)             │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Educational purposes           │ 📚 Solution 3 (Brute Force)               │
└────────────────────────────────┴────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     📊 SOLUTION COMPARISON TABLE                            │
├──────────────────┬─────────────────────────┬────────────────────────────────┤
│ CRITERIA         │ SOL 1 (Hash Set)        │ SOL 2 (Sorting)               │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Time Complexity  │ ⭐⭐⭐⭐⭐ O(n)          │ ⭐⭐⭐ O(n log n)               │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Space Complexity │ ⭐⭐⭐ O(n)              │ ⭐⭐⭐⭐⭐ O(1)                  │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Code Length      │ ⭐⭐⭐⭐⭐ Very short     │ ⭐⭐⭐⭐ Short                   │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Readability      │ ⭐⭐⭐⭐⭐ Crystal clear  │ ⭐⭐⭐⭐⭐ Very clear            │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Interview Speed  │ ⭐⭐⭐⭐⭐ Lightning fast │ ⭐⭐⭐⭐ Fast                    │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ When to Use      │ Best for interviews     │ When memory is limited        │
└──────────────────┴─────────────────────────┴────────────────────────────────┘

├──────────────────┬─────────────────────────────────────────────────────────┤
│ CRITERIA         │ SOL 3 (Brute Force)                                     │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ Time Complexity  │ ⭐ O(n²) - Very slow!                                   │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ Space Complexity │ ⭐⭐⭐⭐⭐ O(1) - No extra space                         │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ Code Length      │ ⭐⭐⭐⭐ Short                                            │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ When to Use      │ Never in production! (Educational only)                 │
└──────────────────┴─────────────────────────────────────────────────────────┘

⏱️  TIME TO MASTER: 5 minutes
🎯 DIFFICULTY: Easy
💡 TIP: Use a Set to track what you've seen!
🔥 POPULAR: Common warm-up question in interviews!

================================================================================
                           🎯 PROBLEM UNDERSTANDING
================================================================================

WHAT IS THE PROBLEM?
--------------------
Given an integer array, return true if any value appears at least twice in
the array, and return false if every element is distinct.

REAL WORLD ANALOGY:
------------------
Think of it like TAKING ATTENDANCE:
- You have a list of names
- As you call each name, check if you've seen it before
- If yes → Duplicate found!
- If no → Add to "already seen" list

Example:
"John, Mary, Tom, John" → Wait! I already called "John"! → Duplicate! ✅
"Alice, Bob, Carol" → All unique names → No duplicates! ❌

THE KEY INSIGHT:
---------------
We just need to track WHAT WE'VE SEEN so far!

❌ Wrong thinking: "Compare every pair of elements"
✅ Right thinking: "Have I seen this element before?"

================================================================================
                            📝 FORMAL PROBLEM
================================================================================

Given an integer array nums, return true if any value appears at least twice
in the array, and return false if every element is distinct.

Example 1:
----------
Input: nums = [1,2,3,1]
Output: true
Explanation: 1 appears twice

Example 2:
----------
Input: nums = [1,2,3,4]
Output: false
Explanation: All elements are distinct

Example 3:
----------
Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: true
Explanation: Multiple duplicates exist

Constraints:
------------
* 1 <= nums.length <= 10^5
* -10^9 <= nums[i] <= 10^9

================================================================================
                         🧠 KEY INSIGHTS TO REMEMBER
================================================================================

THE MAIN CHALLENGE:
------------------
❌ Can't check every pair - too slow O(n²)!
❌ Can't assume array is sorted!
✅ Need to track seen elements efficiently in O(1) lookup time!

THE MAGIC TRICK: "SEEN SET"
---------------------------
Keep a set of numbers you've seen
For each new number:
- If in set → Found duplicate! Return True
- If not in set → Add to set, continue

Think of it as a GUEST LIST:
- Person arrives → Check guest list
- Already there? → Duplicate entry!
- Not there? → Add them, let them in

THE BREAKTHROUGH INSIGHT:
------------------------
Sets provide O(1) lookup time!
This makes the entire solution O(n)!

================================================================================
                          💡 SOLUTION APPROACHES
================================================================================
"""

from typing import List

# ============================================================================
#                     APPROACH 1: HASH SET (OPTIMAL)
# ============================================================================

def containsDuplicate_HashSet(nums: List[int]) -> bool:
    """
    🎯 APPROACH 1: Hash Set (BEST SOLUTION!)

    TIME COMPLEXITY: O(n) - Single pass through array
    SPACE COMPLEXITY: O(n) - Set stores unique elements

    🧠 MEMORIZATION TRICK: "Seen It Check"
    ---------------------------------------
    Think: "Have I seen this number before?"
    - YES → Return True (found duplicate!)
    - NO  → Add to seen set, continue

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Create empty set 'seen'
    2. For each number in array:
       a. Check if number is in 'seen'
       b. If YES → Return True (duplicate found!)
       c. If NO → Add number to 'seen'
    3. If loop completes → Return False (no duplicates)

    🎨 VISUAL EXAMPLE:
    -----------------
    nums = [1, 2, 3, 1]

    Step 1: num=1, seen={}
      1 not in seen → seen = {1}

    Step 2: num=2, seen={1}
      2 not in seen → seen = {1, 2}

    Step 3: num=3, seen={1, 2}
      3 not in seen → seen = {1, 2, 3}

    Step 4: num=1, seen={1, 2, 3}
      1 IS in seen! ✅ → Return True
    """
    seen = set()

    for num in nums:
        # Have we seen this number before?
        if num in seen:
            return True  # Duplicate found!
        # Add to seen set
        seen.add(num)

    # No duplicates found
    return False


def containsDuplicate_HashSet_Oneliner(nums: List[int]) -> bool:
    """
    Same as above but using Python's set length trick
    If set length < array length → duplicates exist!
    """
    return len(set(nums)) < len(nums)


# ============================================================================
#                   APPROACH 2: SORTING (SPACE OPTIMIZED)
# ============================================================================

def containsDuplicate_Sorting(nums: List[int]) -> bool:
    """
    🎯 APPROACH 2: Sorting (SPACE OPTIMIZED!)

    TIME COMPLEXITY: O(n log n) - Due to sorting
    SPACE COMPLEXITY: O(1) - Sort in-place (or O(n) if can't modify input)

    🧠 MEMORIZATION TRICK: "Sort and Check Neighbors"
    -------------------------------------------------
    Think: "If duplicates exist, they'll be next to each other after sorting!"

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Sort the array
    2. Check consecutive elements
    3. If any two neighbors are equal → Return True
    4. If no equal neighbors → Return False

    🎨 VISUAL EXAMPLE:
    -----------------
    nums = [1, 3, 2, 1]

    Step 1: Sort
      [1, 3, 2, 1] → [1, 1, 2, 3]

    Step 2: Check neighbors
      Compare nums[0] and nums[1]: 1 == 1 ✅
      → Return True (duplicate found!)

    ⚠️  WHY THIS WORKS:
    -------------------
    - Sorting groups identical elements together
    - Duplicates will be adjacent
    - Only need to check consecutive elements!
    """
    # Sort the array
    nums.sort()

    # Check consecutive elements
    for i in range(len(nums) - 1):
        if nums[i] == nums[i + 1]:
            return True  # Found duplicate!

    return False


# ============================================================================
#                   APPROACH 3: BRUTE FORCE (NAIVE)
# ============================================================================

def containsDuplicate_BruteForce(nums: List[int]) -> bool:
    """
    🎯 APPROACH 3: Brute Force (NOT RECOMMENDED!)

    TIME COMPLEXITY: O(n²) - Nested loops
    SPACE COMPLEXITY: O(1) - No extra space

    🧠 MEMORIZATION TRICK: "Check Every Pair"
    -----------------------------------------
    Think: "Compare each element with all others"

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. For each element at index i:
       2. For each element at index j (where j > i):
          3. If nums[i] == nums[j]:
             4. Return True
    5. If no match found → Return False

    ⚠️  WHY NOT USE THIS:
    --------------------
    - Too slow for large arrays
    - Interview expects O(n) or O(n log n) solution
    - Only use for educational purposes!
    """
    n = len(nums)

    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] == nums[j]:
                return True

    return False


# ============================================================================
#                    🎨 VISUAL WALKTHROUGH EXAMPLE
# ============================================================================

"""
Let's walk through Example 1: nums = [1, 2, 3, 1]

APPROACH 1 (HASH SET):
---------------------

Initial: seen = set()

╔════════════════════════════════════════════════════════════════╗
║ ITERATION 1: i=0, num=1                                        ║
╠════════════════════════════════════════════════════════════════╣
║ Is 1 in seen? NO                                               ║
║ seen.add(1) → seen = {1}                                       ║
║ Continue...                                                    ║
╚════════════════════════════════════════════════════════════════╝

╔════════════════════════════════════════════════════════════════╗
║ ITERATION 2: i=1, num=2                                        ║
╠════════════════════════════════════════════════════════════════╣
║ Is 2 in seen? NO                                               ║
║ seen.add(2) → seen = {1, 2}                                    ║
║ Continue...                                                    ║
╚════════════════════════════════════════════════════════════════╝

╔════════════════════════════════════════════════════════════════╗
║ ITERATION 3: i=2, num=3                                        ║
╠════════════════════════════════════════════════════════════════╣
║ Is 3 in seen? NO                                               ║
║ seen.add(3) → seen = {1, 2, 3}                                 ║
║ Continue...                                                    ║
╚════════════════════════════════════════════════════════════════╝

╔════════════════════════════════════════════════════════════════╗
║ ITERATION 4: i=3, num=1                                        ║
╠════════════════════════════════════════════════════════════════╣
║ Is 1 in seen? YES! ✅                                          ║
║ DUPLICATE FOUND!                                               ║
║ RETURN True                                                    ║
╚════════════════════════════════════════════════════════════════╝

APPROACH 2 (SORTING):
--------------------

Step 1: Sort array
  [1, 2, 3, 1] → [1, 1, 2, 3]

Step 2: Check consecutive elements
╔════════════════════════════════════════════════════════════════╗
║ CHECK i=0: nums[0]=1, nums[1]=1                                ║
╠════════════════════════════════════════════════════════════════╣
║ 1 == 1? YES! ✅                                                ║
║ DUPLICATE FOUND!                                               ║
║ RETURN True                                                    ║
╚════════════════════════════════════════════════════════════════╝

APPROACH 3 (BRUTE FORCE):
------------------------

Compare all pairs:
  nums[0]=1 vs nums[1]=2 → Not equal
  nums[0]=1 vs nums[2]=3 → Not equal
  nums[0]=1 vs nums[3]=1 → EQUAL! ✅

  RETURN True
"""

# ============================================================================
#              🎯 MEMORY TRICKS & COMMON MISTAKES
# ============================================================================

"""
🧠 HOW TO REMEMBER THIS SOLUTION:
---------------------------------
1. "GUEST LIST" → Track who you've seen
2. "SET = O(1) LOOKUP" → Fast checking
3. "SORT = NEIGHBORS" → Duplicates become adjacent
4. "ONE-LINER TRICK" → len(set(nums)) < len(nums)

❌ COMMON MISTAKES TO AVOID:
----------------------------
1. ❌ Using nested loops (brute force)
      WRONG: O(n²) solution
      RIGHT: Use hash set for O(n)

2. ❌ Forgetting to add to seen set
      WRONG: Just checking without adding
      RIGHT: Add number after checking

3. ❌ Not handling single element
      WRONG: Assuming array has multiple elements
      RIGHT: Single element array has no duplicates

4. ❌ Modifying input when not allowed
      WRONG: Sorting original array
      RIGHT: Ask if you can modify input

5. ❌ Using Counter when Set suffices
      WRONG: Overkill with Counter
      RIGHT: Set is simpler and faster

✅ PRO TIPS:
-----------
1. Hash Set is the default go-to solution!
2. One-liner: len(set(nums)) < len(nums)
3. Sorting good if space is critical
4. Always ask: "Can I modify the input array?"
5. This pattern appears in many problems!

🎯 WHICH SOLUTION TO USE IN INTERVIEW:
--------------------------------------
1. Start with hash set (optimal time)
2. Mention sorting if asked about space optimization
3. Never use brute force in production
4. One-liner is elegant but explain the logic!
"""

# ============================================================================
#                         🧪 TEST CASES
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("              CONTAINS DUPLICATE - TEST CASES")
    print("="*70)

    # Test Case 1: Has duplicate
    print("\n📝 Test Case 1: Has duplicate")
    print("-" * 70)
    nums1 = [1, 2, 3, 1]
    print(f"Input: nums = {nums1}")
    result1 = containsDuplicate_HashSet(nums1)
    print(f"Output: {result1}")
    print(f"Expected: True")
    print(f"✅ PASS" if result1 == True else "❌ FAIL")

    # Test Case 2: No duplicate
    print("\n📝 Test Case 2: No duplicate")
    print("-" * 70)
    nums2 = [1, 2, 3, 4]
    print(f"Input: nums = {nums2}")
    result2 = containsDuplicate_HashSet(nums2)
    print(f"Output: {result2}")
    print(f"Expected: False")
    print(f"✅ PASS" if result2 == False else "❌ FAIL")

    # Test Case 3: Multiple duplicates
    print("\n📝 Test Case 3: Multiple duplicates")
    print("-" * 70)
    nums3 = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]
    print(f"Input: nums = {nums3}")
    result3 = containsDuplicate_HashSet(nums3)
    print(f"Output: {result3}")
    print(f"Expected: True")
    print(f"✅ PASS" if result3 == True else "❌ FAIL")

    # Test Case 4: Single element
    print("\n📝 Test Case 4: Single element")
    print("-" * 70)
    nums4 = [1]
    print(f"Input: nums = {nums4}")
    result4 = containsDuplicate_HashSet(nums4)
    print(f"Output: {result4}")
    print(f"Expected: False")
    print(f"✅ PASS" if result4 == False else "❌ FAIL")

    # Test Case 5: Two identical elements
    print("\n📝 Test Case 5: Two identical elements")
    print("-" * 70)
    nums5 = [1, 1]
    print(f"Input: nums = {nums5}")
    result5 = containsDuplicate_HashSet(nums5)
    print(f"Output: {result5}")
    print(f"Expected: True")
    print(f"✅ PASS" if result5 == True else "❌ FAIL")

    # Test Case 6: Large numbers
    print("\n📝 Test Case 6: Large numbers")
    print("-" * 70)
    nums6 = [1000000, 2000000, 3000000, 1000000]
    print(f"Input: nums = {nums6}")
    result6 = containsDuplicate_HashSet(nums6)
    print(f"Output: {result6}")
    print(f"Expected: True")
    print(f"✅ PASS" if result6 == True else "❌ FAIL")

    # Test Case 7: Negative numbers
    print("\n📝 Test Case 7: Negative numbers")
    print("-" * 70)
    nums7 = [-1, -2, -3, -1]
    print(f"Input: nums = {nums7}")
    result7 = containsDuplicate_HashSet(nums7)
    print(f"Output: {result7}")
    print(f"Expected: True")
    print(f"✅ PASS" if result7 == True else "❌ FAIL")

    # Compare all three approaches
    print("\n" + "="*70)
    print("              COMPARING ALL APPROACHES")
    print("="*70)
    test_nums = [5, 2, 8, 2, 9]

    print(f"\nTest: nums = {test_nums}")
    print("-" * 70)
    print(f"Approach 1 (Hash Set):         {containsDuplicate_HashSet(test_nums[:])}")
    print(f"Approach 2 (Sorting):          {containsDuplicate_Sorting(test_nums[:])}")
    print(f"Approach 3 (Brute Force):      {containsDuplicate_BruteForce(test_nums[:])}")

    print("\n" + "="*70)
    print("              ✅ ALL TEST CASES COMPLETED!")
    print("="*70)


# ============================================================================
#              🎓 LEARNING SUMMARY & KEY TAKEAWAYS
# ============================================================================

"""
🎯 WHAT YOU LEARNED:
-------------------
1. Hash Set provides O(1) lookup time
2. Sorting makes duplicates adjacent
3. Trade-off: Time (O(n)) vs Space (O(1))
4. One-liner solution is elegant

🔑 KEY PATTERN: "Seen Before Tracking with Hash Set"
----------------------------------------------------
This pattern applies to:
- Contains Duplicate (this problem)
- Contains Duplicate II (LeetCode #219)
- Contains Duplicate III (LeetCode #220)
- Find All Duplicates in Array (LeetCode #442)

💪 PRACTICE VARIATIONS:
----------------------
Try these similar problems:
1. LeetCode #219: Contains Duplicate II
2. LeetCode #220: Contains Duplicate III
3. LeetCode #442: Find All Duplicates in an Array
4. LeetCode #287: Find the Duplicate Number

🎯 INTERVIEW TIPS:
-----------------
1. Always start with hash set approach!
2. Mention one-liner: len(set(nums)) < len(nums)
3. Ask: "Can I modify the input array?"
4. Discuss time vs space trade-offs
5. Sorting is good alternative if space is critical

🎉 CONGRATULATIONS!
------------------
You now understand duplicate detection!
Remember: "Use a Set to track what you've seen!"

📊 TIME/SPACE ANALYSIS SUMMARY:
------------------------------
┌────────────────────┬──────────────┬──────────────┐
│ Approach           │ Time         │ Space        │
├────────────────────┼──────────────┼──────────────┤
│ Hash Set (Best)    │ O(n)         │ O(n)         │
│ Sorting            │ O(n log n)   │ O(1)         │
│ Brute Force        │ O(n²)        │ O(1)         │
└────────────────────┴──────────────┴──────────────┘

🏆 RECOMMENDED: Hash Set for interviews!
"""
