"""
LeetCode Problem #242: Valid Anagram

Difficulty: Easy
Topics: Hash Table, String, Sorting
Companies: Amazon, Microsoft, Google, Facebook, Apple, Bloomberg

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
│ 4    │ 💡 SOLUTION 1: Hash Map/Counter ⭐        │ • WHY choose? (Pros/Cons) │
│      │    (RECOMMENDED)                         │ • WHEN to use?            │
│      │                                          │ • Step-by-step walkthrough│
├──────┼──────────────────────────────────────────┼───────────────────────────┤
│ 5    │ 💡 SOLUTION 2: Sorting                   │ • WHY choose? (Pros/Cons) │
│      │    (Simple Approach)                     │ • WHEN to use?            │
│      │                                          │ • Comparison with Sol 1   │
├──────┼──────────────────────────────────────────┼───────────────────────────┤
│ 6    │ 💡 SOLUTION 3: Manual Array Count        │ • WHY choose? (Pros/Cons) │
│      │    (Optimal for lowercase only)          │ • WHEN to use?            │
│      │                                          │ • Unicode consideration   │
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
│ ANALOGY          │ "Letter Rearrangement" - Same letters, different order! │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ PATTERN          │ "Character Frequency Match" - Count all letters!        │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ BASE CASE        │ Different lengths → Immediate False!                    │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ DEFAULT SOLUTION │ Hash Map/Counter (Clean and efficient!)                 │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ TIME COMPLEXITY  │ O(n) - Single pass through both strings                 │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ SPACE COMPLEXITY │ O(1) - Fixed 26 letters (or O(k) for k unique chars)   │
└──────────────────┴──────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        ⚡ QUICK DECISION TABLE                              │
├────────────────────────────────┬────────────────────────────────────────────┤
│ SITUATION                      │ WHICH SOLUTION TO USE?                    │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Normal interview               │ ✅ Solution 1 (Hash Map/Counter)          │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Want simplest code             │ ✅ Solution 2 (Sorting)                   │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Only lowercase English letters │ ✅ Solution 3 (Array Count - Fastest)     │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Unicode characters involved    │ ✅ Solution 1 (Hash Map)                  │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Memory constraints             │ ✅ Solution 3 (Fixed array size)          │
└────────────────────────────────┴────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     📊 SOLUTION COMPARISON TABLE                            │
├──────────────────┬─────────────────────────┬────────────────────────────────┤
│ CRITERIA         │ SOL 1 (Hash Map)        │ SOL 2 (Sorting)               │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Time Complexity  │ ⭐⭐⭐⭐⭐ O(n)          │ ⭐⭐⭐ O(n log n)               │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Space Complexity │ ⭐⭐⭐⭐ O(1)/O(k)       │ ⭐⭐⭐ O(n) (for sorting)       │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Code Length      │ ⭐⭐⭐⭐ Short           │ ⭐⭐⭐⭐⭐ Very short             │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Readability      │ ⭐⭐⭐⭐⭐ Crystal clear  │ ⭐⭐⭐⭐⭐ Very clear            │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Interview Speed  │ ⭐⭐⭐⭐⭐ Very fast      │ ⭐⭐⭐⭐ Fast                    │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ When to Use      │ Best for interviews     │ Quick solution                │
└──────────────────┴─────────────────────────┴────────────────────────────────┘

├──────────────────┬─────────────────────────────────────────────────────────┤
│ CRITERIA         │ SOL 3 (Array Count)                                     │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ Time Complexity  │ ⭐⭐⭐⭐⭐ O(n) - Fastest in practice                   │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ Space Complexity │ ⭐⭐⭐⭐⭐ O(1) - Fixed 26 size                         │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ Code Length      │ ⭐⭐⭐ Medium                                            │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ Readability      │ ⭐⭐⭐⭐ Clear                                           │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ When to Use      │ Only lowercase English (26 letters)                     │
└──────────────────┴─────────────────────────────────────────────────────────┘

⏱️  TIME TO MASTER: 10 minutes
🎯 DIFFICULTY: Easy
💡 TIP: Same letter frequency = Anagram!
🔥 POPULAR: Very common in coding interviews!

================================================================================
                           🎯 PROBLEM UNDERSTANDING
================================================================================

WHAT IS THE PROBLEM?
--------------------
Given two strings s and t, determine if t is an anagram of s. An anagram is
formed by rearranging the letters of a word using all original letters exactly
once.

REAL WORLD ANALOGY:
------------------
Think of it like SCRABBLE TILES:
- You have tiles spelling "listen"
- Your friend has tiles spelling "silent"
- Same tiles? YES! → They're anagrams!
- "listen" → l, i, s, t, e, n
- "silent" → s, i, l, e, n, t
- Same letters, just rearranged!

THE KEY INSIGHT:
---------------
An anagram has the EXACT SAME CHARACTER FREQUENCY!

❌ Wrong thinking: "Do they look similar?"
✅ Right thinking: "Do they have the same letter counts?"

Example:
"anagram" and "nagaram" → Both have: a(3), n(1), g(1), r(1), m(1) ✅
"rat" and "car" → Different letter counts ❌

================================================================================
                            📝 FORMAL PROBLEM
================================================================================

Given two strings s and t, return true if t is an anagram of s, and false
otherwise.

An anagram is a word or phrase formed by rearranging the letters of a different
word or phrase, typically using all the original letters exactly once.

Example 1:
----------
Input: s = "anagram", t = "nagaram"
Output: true
Explanation: Both strings have same characters with same frequencies

Example 2:
----------
Input: s = "rat", t = "car"
Output: false
Explanation: Different characters ('t' vs 'c')

Constraints:
------------
* 1 <= s.length, t.length <= 5 * 10^4
* s and t consist of lowercase English letters

Follow-up:
----------
What if the inputs contain Unicode characters? How would you adapt your
solution?

================================================================================
                         🧠 KEY INSIGHTS TO REMEMBER
================================================================================

THE MAIN CHALLENGE:
------------------
❌ Can't just compare strings directly - order is different!
❌ Can't assume sorted order - need to verify frequencies!
✅ Need to count character frequencies efficiently!

THE MAGIC TRICK: "CHARACTER FREQUENCY MAP"
------------------------------------------
For each character in both strings, count occurrences.
If counts match → Anagram! ✅
If counts differ → Not an anagram! ❌

Think of it as a BALLOT BOX:
- Count votes (characters) from string s
- Count votes (characters) from string t
- If results match → Same election! (Anagram!)

THE BREAKTHROUGH INSIGHT:
------------------------
Different lengths → Immediate NO!
Check this FIRST to save time!

================================================================================
                          💡 SOLUTION APPROACHES
================================================================================
"""

from typing import Dict
from collections import Counter

# ============================================================================
#              APPROACH 1: HASH MAP / COUNTER (OPTIMAL)
# ============================================================================

def isAnagram_HashMap(s: str, t: str) -> bool:
    """
    🎯 APPROACH 1: Hash Map / Counter (BEST SOLUTION!)

    TIME COMPLEXITY: O(n) - Single pass through both strings
    SPACE COMPLEXITY: O(1) - At most 26 characters (lowercase English)
                      or O(k) where k is number of unique characters

    🧠 MEMORIZATION TRICK: "Count and Compare"
    -----------------------------------------
    Think: "Do both strings have same letter inventory?"
    1. Count all letters in string s
    2. Count all letters in string t
    3. Compare the counts

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Quick check: If lengths differ → return False
    2. Create frequency map for string s
    3. Create frequency map for string t
    4. Compare both maps
    5. Return True if identical, False otherwise

    🎨 VISUAL EXAMPLE:
    -----------------
    s = "anagram", t = "nagaram"

    Count s: {'a': 3, 'n': 1, 'g': 1, 'r': 1, 'm': 1}
    Count t: {'n': 1, 'a': 3, 'g': 1, 'r': 1, 'm': 1}

    Same counts? YES ✅ → Return True

    s = "rat", t = "car"

    Count s: {'r': 1, 'a': 1, 't': 1}
    Count t: {'c': 1, 'a': 1, 'r': 1}

    Same counts? NO ❌ → Return False
    """
    # Quick optimization: Different lengths can't be anagrams
    if len(s) != len(t):
        return False

    # Python's Counter makes this super clean!
    return Counter(s) == Counter(t)


def isAnagram_HashMap_Manual(s: str, t: str) -> bool:
    """
    Same as above but with manual hash map (more educational)
    """
    if len(s) != len(t):
        return False

    # Build frequency map for s
    count_s = {}
    for char in s:
        count_s[char] = count_s.get(char, 0) + 1

    # Build frequency map for t
    count_t = {}
    for char in t:
        count_t[char] = count_t.get(char, 0) + 1

    # Compare the maps
    return count_s == count_t


# ============================================================================
#                   APPROACH 2: SORTING (SIMPLEST)
# ============================================================================

def isAnagram_Sorting(s: str, t: str) -> bool:
    """
    🎯 APPROACH 2: Sorting (SIMPLEST CODE!)

    TIME COMPLEXITY: O(n log n) - Due to sorting
    SPACE COMPLEXITY: O(n) - For sorted strings

    🧠 MEMORIZATION TRICK: "Sort and Match"
    ----------------------------------------
    Think: "If I sort both, do they look the same?"

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Sort characters in string s
    2. Sort characters in string t
    3. Compare sorted strings
    4. Return True if equal, False otherwise

    🎨 VISUAL EXAMPLE:
    -----------------
    s = "anagram" → sorted → "aaagmnr"
    t = "nagaram" → sorted → "aaagmnr"

    Same? YES ✅ → Return True

    s = "rat" → sorted → "art"
    t = "car" → sorted → "acr"

    Same? NO ❌ → Return False

    ⚠️  WHY THIS WORKS:
    -------------------
    - Anagrams have same letters
    - Sorting puts letters in same order
    - If sorted versions match → Original had same letters!
    """
    # One-liner solution!
    return sorted(s) == sorted(t)


# ============================================================================
#            APPROACH 3: MANUAL ARRAY COUNT (OPTIMAL FOR 26 LETTERS)
# ============================================================================

def isAnagram_ArrayCount(s: str, t: str) -> bool:
    """
    🎯 APPROACH 3: Array Count (OPTIMAL FOR LOWERCASE ENGLISH ONLY!)

    TIME COMPLEXITY: O(n) - Single pass
    SPACE COMPLEXITY: O(1) - Fixed array of size 26

    🧠 MEMORIZATION TRICK: "26 Buckets"
    ------------------------------------
    Think: "26 buckets, one for each letter"
    - Increment for letters in s
    - Decrement for letters in t
    - All zeros at end? → Anagram! ✅

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Quick check: If lengths differ → return False
    2. Create array of 26 zeros (for a-z)
    3. For each char in s: Increment count[char - 'a']
    4. For each char in t: Decrement count[char - 'a']
    5. Check if all counts are zero
    6. Return True if all zero, False otherwise

    🎨 VISUAL EXAMPLE:
    -----------------
    s = "abc", t = "bca"

    count = [0] * 26  # a-z buckets

    Process s="abc":
      'a': count[0]++ → [1,0,0,...,0]
      'b': count[1]++ → [1,1,0,...,0]
      'c': count[2]++ → [1,1,1,...,0]

    Process t="bca":
      'b': count[1]-- → [1,0,1,...,0]
      'c': count[2]-- → [1,0,0,...,0]
      'a': count[0]-- → [0,0,0,...,0]

    All zeros? YES ✅ → Return True

    ⚠️  LIMITATION:
    ---------------
    Only works for lowercase English letters (a-z)
    For Unicode, use Hash Map approach!
    """
    if len(s) != len(t):
        return False

    # Array for 26 lowercase letters
    count = [0] * 26

    # Increment for s, decrement for t
    for i in range(len(s)):
        count[ord(s[i]) - ord('a')] += 1
        count[ord(t[i]) - ord('a')] -= 1

    # Check if all counts are zero
    return all(c == 0 for c in count)


# ============================================================================
#                    🎨 VISUAL WALKTHROUGH EXAMPLE
# ============================================================================

"""
Let's walk through Example 1: s = "anagram", t = "nagaram"

APPROACH 1 (HASH MAP):
---------------------

Step 1: Length check
  len(s) = 7, len(t) = 7 ✅ Same length!

Step 2: Count characters in s
╔════════════════════════════════════════════════════════════════╗
║ Character Frequency Map for s = "anagram"                     ║
╠════════════════════════════════════════════════════════════════╣
║ 'a': 3  (appears at indices 0, 2, 4)                          ║
║ 'n': 1  (appears at index 1)                                  ║
║ 'a': [already counted]                                        ║
║ 'g': 1  (appears at index 3)                                  ║
║ 'r': 1  (appears at index 5)                                  ║
║ 'a': [already counted]                                        ║
║ 'm': 1  (appears at index 6)                                  ║
║                                                                ║
║ Final: {'a': 3, 'n': 1, 'g': 1, 'r': 1, 'm': 1}               ║
╚════════════════════════════════════════════════════════════════╝

Step 3: Count characters in t
╔════════════════════════════════════════════════════════════════╗
║ Character Frequency Map for t = "nagaram"                     ║
╠════════════════════════════════════════════════════════════════╣
║ 'n': 1  (appears at index 0)                                  ║
║ 'a': 3  (appears at indices 1, 3, 5)                          ║
║ 'g': 1  (appears at index 2)                                  ║
║ 'r': 1  (appears at index 4)                                  ║
║ 'm': 1  (appears at index 6)                                  ║
║                                                                ║
║ Final: {'n': 1, 'a': 3, 'g': 1, 'r': 1, 'm': 1}               ║
╚════════════════════════════════════════════════════════════════╝

Step 4: Compare maps
  s_map: {'a': 3, 'n': 1, 'g': 1, 'r': 1, 'm': 1}
  t_map: {'n': 1, 'a': 3, 'g': 1, 'r': 1, 'm': 1}

  Are they equal? YES ✅

  RETURN True

APPROACH 2 (SORTING):
--------------------

Step 1: Sort s
  "anagram" → ['a','n','a','g','r','a','m'] → sort → "aaagmnr"

Step 2: Sort t
  "nagaram" → ['n','a','g','a','r','a','m'] → sort → "aaagmnr"

Step 3: Compare
  "aaagmnr" == "aaagmnr" → True ✅

  RETURN True

APPROACH 3 (ARRAY COUNT):
-------------------------

Initial: count = [0] * 26

Process s = "anagram":
  'a': count[0]++  → [1,0,0,...]
  'n': count[13]++ → [1,0,...,1,0,...]
  'a': count[0]++  → [2,0,...,1,0,...]
  'g': count[6]++  → [2,0,...,1,1,0,...]
  'r': count[17]++ → [2,0,...,1,1,0,...,1,0,...]
  'a': count[0]++  → [3,0,...,1,1,0,...,1,0,...]
  'm': count[12]++ → [3,0,...,1,1,0,...,1,1,0,...]

Process t = "nagaram":
  'n': count[13]-- → [3,0,...,0,1,0,...,1,1,0,...]
  'a': count[0]--  → [2,0,...,0,1,0,...,1,1,0,...]
  'g': count[6]--  → [2,0,...,0,0,0,...,1,1,0,...]
  'a': count[0]--  → [1,0,...,0,0,0,...,1,1,0,...]
  'r': count[17]-- → [1,0,...,0,0,0,...,0,1,0,...]
  'a': count[0]--  → [0,0,...,0,0,0,...,0,1,0,...]
  'm': count[12]-- → [0,0,...,0,0,0,...,0,0,0,...]

Final: All zeros? YES ✅

RETURN True
"""

# ============================================================================
#              🎯 MEMORY TRICKS & COMMON MISTAKES
# ============================================================================

"""
🧠 HOW TO REMEMBER THIS SOLUTION:
---------------------------------
1. "SAME INVENTORY" → Same letters, same counts
2. "LENGTH FIRST" → Quick rejection for different lengths
3. "COUNT OR SORT" → Two main strategies
4. "26 BUCKETS" → Fixed array for English letters

❌ COMMON MISTAKES TO AVOID:
----------------------------
1. ❌ Forgetting to check lengths first
      WRONG: Directly comparing counts
      RIGHT: Check len(s) != len(t) first

2. ❌ Comparing strings directly
      WRONG: if s == t
      RIGHT: Compare character frequencies

3. ❌ Using array count for Unicode
      WRONG: count[ord(char)] for Unicode
      RIGHT: Use hash map for Unicode characters

4. ❌ Not handling empty strings
      WRONG: Assuming strings have content
      RIGHT: Empty strings are anagrams of each other

5. ❌ Case sensitivity confusion
      WRONG: Treating 'A' and 'a' as same
      RIGHT: Problem specifies lowercase only

✅ PRO TIPS:
-----------
1. Length check saves time - do it first!
2. Counter from collections is your friend
3. Sorting is simplest but not optimal
4. Array count is fastest for lowercase English
5. Hash map works for ALL character sets

🎯 WHICH SOLUTION TO USE IN INTERVIEW:
--------------------------------------
1. Start with sorting (show you understand the problem)
2. Optimize to hash map (show you know time complexity)
3. Mention array count (show you know optimization tricks)
"""

# ============================================================================
#                         🧪 TEST CASES
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("                VALID ANAGRAM - TEST CASES")
    print("="*70)

    # Test Case 1: Standard anagram
    print("\n📝 Test Case 1: Standard anagram")
    print("-" * 70)
    s1, t1 = "anagram", "nagaram"
    print(f"Input: s = '{s1}', t = '{t1}'")
    result1 = isAnagram_HashMap(s1, t1)
    print(f"Output: {result1}")
    print(f"Expected: True")
    print(f"✅ PASS" if result1 == True else "❌ FAIL")

    # Test Case 2: Not an anagram
    print("\n📝 Test Case 2: Not an anagram")
    print("-" * 70)
    s2, t2 = "rat", "car"
    print(f"Input: s = '{s2}', t = '{t2}'")
    result2 = isAnagram_HashMap(s2, t2)
    print(f"Output: {result2}")
    print(f"Expected: False")
    print(f"✅ PASS" if result2 == False else "❌ FAIL")

    # Test Case 3: Different lengths
    print("\n📝 Test Case 3: Different lengths")
    print("-" * 70)
    s3, t3 = "abc", "abcd"
    print(f"Input: s = '{s3}', t = '{t3}'")
    result3 = isAnagram_HashMap(s3, t3)
    print(f"Output: {result3}")
    print(f"Expected: False")
    print(f"✅ PASS" if result3 == False else "❌ FAIL")

    # Test Case 4: Single character
    print("\n📝 Test Case 4: Single character")
    print("-" * 70)
    s4, t4 = "a", "a"
    print(f"Input: s = '{s4}', t = '{t4}'")
    result4 = isAnagram_HashMap(s4, t4)
    print(f"Output: {result4}")
    print(f"Expected: True")
    print(f"✅ PASS" if result4 == True else "❌ FAIL")

    # Test Case 5: Repeated characters
    print("\n📝 Test Case 5: Repeated characters")
    print("-" * 70)
    s5, t5 = "aabbcc", "abcabc"
    print(f"Input: s = '{s5}', t = '{t5}'")
    result5 = isAnagram_HashMap(s5, t5)
    print(f"Output: {result5}")
    print(f"Expected: True")
    print(f"✅ PASS" if result5 == True else "❌ FAIL")

    # Test Case 6: All same characters
    print("\n📝 Test Case 6: All same characters")
    print("-" * 70)
    s6, t6 = "aaaa", "aaaa"
    print(f"Input: s = '{s6}', t = '{t6}'")
    result6 = isAnagram_HashMap(s6, t6)
    print(f"Output: {result6}")
    print(f"Expected: True")
    print(f"✅ PASS" if result6 == True else "❌ FAIL")

    # Test Case 7: Similar but not anagram
    print("\n📝 Test Case 7: Similar but not anagram")
    print("-" * 70)
    s7, t7 = "abc", "abd"
    print(f"Input: s = '{s7}', t = '{t7}'")
    result7 = isAnagram_HashMap(s7, t7)
    print(f"Output: {result7}")
    print(f"Expected: False")
    print(f"✅ PASS" if result7 == False else "❌ FAIL")

    # Compare all three approaches
    print("\n" + "="*70)
    print("              COMPARING ALL APPROACHES")
    print("="*70)
    test_s = "listen"
    test_t = "silent"

    print(f"\nTest: s = '{test_s}', t = '{test_t}'")
    print("-" * 70)
    print(f"Approach 1 (Hash Map):         {isAnagram_HashMap(test_s, test_t)}")
    print(f"Approach 2 (Sorting):          {isAnagram_Sorting(test_s, test_t)}")
    print(f"Approach 3 (Array Count):      {isAnagram_ArrayCount(test_s, test_t)}")

    print("\n" + "="*70)
    print("              ✅ ALL TEST CASES COMPLETED!")
    print("="*70)


# ============================================================================
#              🎓 LEARNING SUMMARY & KEY TAKEAWAYS
# ============================================================================

"""
🎯 WHAT YOU LEARNED:
-------------------
1. Anagram = Same character frequencies
2. Length check first = Quick optimization
3. Three main approaches: Hash Map, Sorting, Array Count
4. Trade-offs: Time vs Space vs Simplicity

🔑 KEY PATTERN: "Character Frequency Matching"
-----------------------------------------------
This pattern applies to:
- Valid Anagram (this problem)
- Group Anagrams (LeetCode #49)
- Find All Anagrams in a String (LeetCode #438)
- Permutation in String (LeetCode #567)

💪 PRACTICE VARIATIONS:
----------------------
Try these similar problems:
1. LeetCode #49: Group Anagrams
2. LeetCode #438: Find All Anagrams in a String
3. LeetCode #567: Permutation in String
4. LeetCode #266: Palindrome Permutation

🎯 INTERVIEW TIPS:
-----------------
1. Always check lengths first - free optimization!
2. Ask: "Are inputs only lowercase English?" (affects solution choice)
3. Mention all three approaches and their trade-offs
4. Sorting is acceptable but mention O(n) solution exists
5. For follow-up (Unicode): Use hash map, not array

🎉 CONGRATULATIONS!
------------------
You now understand character frequency matching!
Remember: "Same inventory = Anagram!"

📊 TIME/SPACE ANALYSIS SUMMARY:
------------------------------
┌────────────────────┬──────────────┬──────────────┐
│ Approach           │ Time         │ Space        │
├────────────────────┼──────────────┼──────────────┤
│ Hash Map (Best)    │ O(n)         │ O(1)/O(k)    │
│ Sorting            │ O(n log n)   │ O(n)         │
│ Array Count        │ O(n)         │ O(1)         │
└────────────────────┴──────────────┴──────────────┘

🏆 RECOMMENDED: Hash Map for interviews, Array Count for performance!
"""
