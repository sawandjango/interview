"""
LeetCode Problem #1: Two Sum

Difficulty: Easy
Topics: Array, Hash Table
Companies: Amazon, Google, Apple, Microsoft, Facebook, Adobe


┌─────────────────────────────────────────────────────────────────────────────┐
│                     📊 SOLUTION COMPARISON TABLE                            │
├──────────────────┬─────────────────────────┬────────────────────────────────┤
│ CRITERIA         │ SOLUTION 1 (Hash Map)   │ SOLUTION 2 (Brute Force)      │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Time Complexity  │ ⭐⭐⭐⭐⭐ O(n)          │ ⭐ O(n²)                       │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Space Complexity │ ⭐⭐⭐ O(n)              │ ⭐⭐⭐⭐⭐ O(1)                  │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Code Length      │ ⭐⭐⭐⭐⭐ Very short     │ ⭐⭐⭐⭐ Also short              │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Readability      │ ⭐⭐⭐⭐⭐ Crystal clear  │ ⭐⭐⭐⭐⭐ Very clear            │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Interview Speed  │ ⭐⭐⭐⭐⭐ Lightning fast │ ⭐⭐⭐ Slower                   │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ When to Use      │ Always! (DEFAULT)       │ Only when space is critical   │
└──────────────────┴─────────────────────────┴────────────────────────────────┘

⏱️  TIME TO MASTER: 10-15 minutes
🎯 DIFFICULTY: Easy
💡 TIP: Think "What's the complement?" not "What do I have?"
🔥 POPULAR: #1 most asked coding interview question!

================================================================================
                           🎯 PROBLEM UNDERSTANDING
================================================================================

WHAT IS THE PROBLEM?
--------------------
Given an array of integers and a target, find TWO numbers that add up to the
target. Return their indices.

REAL WORLD ANALOGY:
------------------
Think of it like SHOPPING WITH A BUDGET:
- You have $9 to spend (target)
- You see items: $2, $7, $11, $15
- You pick up $2 item → Need $7 more
- You look around → Find $7!
- Perfect! Buy both items (indices 0 and 1)

THE KEY INSIGHT:
---------------
Instead of remembering WHAT YOU SAW, remember WHAT YOU NEED!

❌ Wrong thinking: "I saw 2, 7, 11..."
✅ Right thinking: "I need 7 (because 9-2=7)"

================================================================================
                            📝 FORMAL PROBLEM
================================================================================

Given an array of integers nums and an integer target, return indices of the
two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may
not use the same element twice.

You can return the answer in any order.

Example 1:
----------
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
----------
Input: nums = [3,2,4], target = 6
Output: [1,2]
Explanation: nums[1] + nums[2] = 2 + 4 = 6

Example 3:
----------
Input: nums = [3,3], target = 6
Output: [0,1]
Explanation: nums[0] + nums[1] = 3 + 3 = 6

Constraints:
------------
* 2 <= nums.length <= 10^4
* -10^9 <= nums[i] <= 10^9
* -10^9 <= target <= 10^9
* Only one valid answer exists.

Follow-up:
----------
Can you come up with an algorithm that is less than O(n²) time complexity?


================================================================================
                          💡 SOLUTION APPROACHES
================================================================================
"""

from typing import List

# ============================================================================
#                     APPROACH 1: HASH MAP (OPTIMAL)
# ============================================================================

def twoSum_HashMap(nums: List[int], target: int) -> List[int]:
    """
    🎯 APPROACH 1: Hash Map / Dictionary (BEST SOLUTION!)

    TIME COMPLEXITY: O(n) - Single pass through array
    SPACE COMPLEXITY: O(n) - HashMap stores at most n elements

    🧠 MEMORIZATION TRICK: "Seen It Before?"
    ----------------------------------------
    Think: "Have I seen the complement before?"
    - YES → Return [old_index, current_index]
    - NO  → Remember current number for later

    📝 PSEUDOCODE:
    --------------
    seen = {}                           # Track seen numbers → indices
    for i, num in enumerate(nums):
        complement = target - num       # What we need to find
        if complement in seen:          # Found pair?
            return [seen[complement], i]
        seen[num] = i                   # Store for later lookup
    # Time: O(n), Space: O(n)

    🎨 VISUAL EXAMPLE:
    -----------------
    nums = [2, 7, 11, 15], target = 9

    Step 1: num=2, i=0
      complement = 9-2 = 7
      7 not in map {}
      map = {2: 0}

    Step 2: num=7, i=1
      complement = 9-7 = 2
      2 IS in map! ✅
      return [0, 1]
    """
    # Our "phone book" - maps number to its index
    seen = {}

    for i, num in enumerate(nums):
        # What number do we need to reach target?
        complement = target - num

        # Have we seen this complement before?
        if complement in seen:
            # Yes! Return the indices
            return [seen[complement], i]

        # No? Remember this number for later
        seen[num] = i

    # No solution found (won't happen per problem constraints)
    return []


# ============================================================================
#                   APPROACH 2: BRUTE FORCE (NAIVE)
# ============================================================================

def twoSum_BruteForce(nums: List[int], target: int) -> List[int]:
    """
    🎯 APPROACH 2: Brute Force (NOT RECOMMENDED!)

    TIME COMPLEXITY: O(n²) - Nested loops
    SPACE COMPLEXITY: O(1) - No extra space needed

    🧠 MEMORIZATION TRICK: "Check Every Pair"
    -----------------------------------------
    Simple but slow - check all possible pairs

    📝 PSEUDOCODE:
    --------------
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):     # Check all pairs
            if nums[i] + nums[j] == target:   # Found match?
                return [i, j]
    # Time: O(n²), Space: O(1)

    ⚠️  WHY NOT USE THIS:
    --------------------
    - Too slow for large arrays
    - Interview expects O(n) solution
    - Only use if space is extremely limited
    """
    n = len(nums)

    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]

    return []


# ============================================================================
#              APPROACH 3: TWO-PASS HASH MAP (ALTERNATIVE)
# ============================================================================

def twoSum_TwoPass(nums: List[int], target: int) -> List[int]:
    """
    🎯 APPROACH 3: Two-Pass Hash Map (EDUCATIONAL)

    TIME COMPLEXITY: O(n) - Two passes
    SPACE COMPLEXITY: O(n) - HashMap

    📝 PSEUDOCODE:
    --------------
    # Pass 1: Build map
    num_to_index = {num: i for i, num in enumerate(nums)}

    # Pass 2: Find complement
    for i, num in enumerate(nums):
        complement = target - num                      # What we need
        if complement in num_to_index:                 # Found it?
            if num_to_index[complement] != i:          # Not same index?
                return [i, num_to_index[complement]]
    # Time: O(n), Space: O(n)

    ⚠️  NOTE: One-pass (Solution 1) is better!
    """
    # First pass: Build the map
    num_to_index = {num: i for i, num in enumerate(nums)}

    # Second pass: Find complement
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_to_index and num_to_index[complement] != i:
            return [i, num_to_index[complement]]

    return []



# ============================================================================
#                         🧪 TEST CASES
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("                    TWO SUM - TEST CASES")
    print("="*70)

    # Test Case 1: Standard case
    print("\n📝 Test Case 1: Standard case")
    print("-" * 70)
    nums1 = [2, 7, 11, 15]
    target1 = 9
    print(f"Input: nums = {nums1}, target = {target1}")
    result1 = twoSum_HashMap(nums1, target1)
    print(f"Output: {result1}")
    print(f"Expected: [0, 1]")
    print(f"✅ PASS" if result1 == [0, 1] else "❌ FAIL")

    # Test Case 2: Numbers not at beginning
    print("\n📝 Test Case 2: Numbers not at beginning")
    print("-" * 70)
    nums2 = [3, 2, 4]
    target2 = 6
    print(f"Input: nums = {nums2}, target = {target2}")
    result2 = twoSum_HashMap(nums2, target2)
    print(f"Output: {result2}")
    print(f"Expected: [1, 2]")
    print(f"✅ PASS" if result2 == [1, 2] else "❌ FAIL")

    # Test Case 3: Same number twice
    print("\n📝 Test Case 3: Same number twice")
    print("-" * 70)
    nums3 = [3, 3]
    target3 = 6
    print(f"Input: nums = {nums3}, target = {target3}")
    result3 = twoSum_HashMap(nums3, target3)
    print(f"Output: {result3}")
    print(f"Expected: [0, 1]")
    print(f"✅ PASS" if result3 == [0, 1] else "❌ FAIL")

    # Test Case 4: Negative numbers
    print("\n📝 Test Case 4: Negative numbers")
    print("-" * 70)
    nums4 = [-1, -2, -3, -4, -5]
    target4 = -8
    print(f"Input: nums = {nums4}, target = {target4}")
    result4 = twoSum_HashMap(nums4, target4)
    print(f"Output: {result4}")
    print(f"Expected: [2, 4] (because -3 + -5 = -8)")
    print(f"✅ PASS" if result4 == [2, 4] else "❌ FAIL")

    # Test Case 5: Zero target
    print("\n📝 Test Case 5: Zero target")
    print("-" * 70)
    nums5 = [-3, 4, 3, 90]
    target5 = 0
    print(f"Input: nums = {nums5}, target = {target5}")
    result5 = twoSum_HashMap(nums5, target5)
    print(f"Output: {result5}")
    print(f"Expected: [0, 2] (because -3 + 3 = 0)")
    print(f"✅ PASS" if result5 == [0, 2] else "❌ FAIL")

    # Compare all three approaches
    print("\n" + "="*70)
    print("              COMPARING ALL APPROACHES")
    print("="*70)
    test_nums = [2, 7, 11, 15]
    test_target = 9

    print(f"\nTest: nums = {test_nums}, target = {test_target}")
    print("-" * 70)
    print(f"Approach 1 (Hash Map):     {twoSum_HashMap(test_nums, test_target)}")
    print(f"Approach 2 (Brute Force):  {twoSum_BruteForce(test_nums, test_target)}")
    print(f"Approach 3 (Two-Pass):     {twoSum_TwoPass(test_nums, test_target)}")

    print("\n" + "="*70)
    print("              ✅ ALL TEST CASES COMPLETED!")
    print("="*70)


# ============================================================================
#              🎓 LEARNING SUMMARY & KEY TAKEAWAYS
# ============================================================================

"""
🎯 WHAT YOU LEARNED:
-------------------
1. Hash Map enables O(1) complement lookup
2. Single-pass is more efficient than two-pass
3. Store what you've SEEN, check for what you NEED
4. Trade space O(n) for time O(n) - worth it!

🔑 KEY PATTERN: "Complement Lookup with Hash Map"
-------------------------------------------------
This pattern applies to:
- Two Sum (this problem)
- Three Sum (LeetCode #15)
- Four Sum (LeetCode #18)
- Two Sum II (LeetCode #167)

💪 PRACTICE VARIATIONS:
----------------------
Try these similar problems:
1. LeetCode #167: Two Sum II - Input Array Is Sorted
2. LeetCode #170: Two Sum III - Data Structure Design
3. LeetCode #653: Two Sum IV - BST
4. LeetCode #1: Two Sum Variations

🎯 INTERVIEW TIPS:
-----------------
1. Always ask: "Can array be modified?" (sorting question)
2. Always ask: "Can there be duplicates?"
3. Start with brute force, then optimize
4. Mention trade-offs: Time vs Space

🎉 CONGRATULATIONS!
------------------
You now understand the most asked interview question!
Remember: "Store what you SEE, look for what you NEED!"

📊 TIME/SPACE ANALYSIS SUMMARY:
------------------------------
┌────────────────────┬──────────────┬──────────────┐
│ Approach           │ Time         │ Space        │
├────────────────────┼──────────────┼──────────────┤
│ Hash Map (Best)    │ O(n)         │ O(n)         │
│ Brute Force        │ O(n²)        │ O(1)         │
│ Two-Pass Hash      │ O(n)         │ O(n)         │
└────────────────────┴──────────────┴──────────────┘

🏆 RECOMMENDED: Always use Hash Map approach!
"""
