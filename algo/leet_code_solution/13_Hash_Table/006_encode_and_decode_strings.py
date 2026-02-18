"""
LeetCode Problem #271: Encode and Decode Strings

Difficulty: Medium
Topics: String, Array, Design
Companies: Google, Facebook, Amazon, Microsoft, Uber, Airbnb

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
│ 4    │ 💡 SOLUTION 1: Length-Prefix ⭐      │ • WHY choose? (Pros/Cons)     │
│      │    (OPTIMAL - Most Robust)           │ • WHEN to use?                │
│      │                                      │ • Step-by-step walkthrough    │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 5    │ 💡 SOLUTION 2: Chunked Encoding      │ • WHY choose? (Pros/Cons)     │
│      │    (Fixed-Width Length)              │ • WHEN to use?                │
│      │                                      │ • Comparison with Solution 1  │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 6    │ 💡 SOLUTION 3: Escaped Delimiter     │ • WHY choose? (Pros/Cons)     │
│      │    (Not Recommended)                 │ • WHEN to use?                │
│      │                                      │ • Why it's problematic        │
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
│ ANALOGY          │ "Package Label" - Length tells you what's inside!       │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ PATTERN          │ "Length-Prefix Protocol" - Know size before reading!    │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ KEY TRICK        │ Format: "length#content" - No escaping needed!          │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ DEFAULT SOLUTION │ Length-Prefix (Works with ANY characters!)              │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ TIME COMPLEXITY  │ O(N) - Linear in total character count                  │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ SPACE COMPLEXITY │ O(N) - Store encoded string                             │
└──────────────────┴──────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        ⚡ QUICK DECISION TABLE                              │
├────────────────────────────────┬────────────────────────────────────────────┤
│ SITUATION                      │ WHICH SOLUTION TO USE?                    │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Normal interview               │ ✅ Solution 1 (Length-Prefix)             │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Any characters possible        │ ✅ Solution 1 (handles ALL chars!)        │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Known max string length        │ ⚡ Solution 2 (Chunked - simpler parse)   │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Guaranteed safe delimiters     │ ⚠️  Solution 3 (Escaped - not worth it)   │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Network protocols (HTTP, etc)  │ ✅ Solution 1 (industry standard!)        │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Want to show off               │ 🎯 Explain all 3, choose Length-Prefix   │
└────────────────────────────────┴────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     📊 SOLUTION COMPARISON TABLE                            │
├──────────────────┬──────────────┬──────────────┬──────────────┬─────────────┤
│ CRITERIA         │ LENGTH-PREFIX│ CHUNKED      │ ESCAPED      │ WINNER      │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Time Complexity  │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐⭐⭐   │ ALL TIE     │
│                  │ O(N)         │ O(N)         │ O(N)         │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Space Complexity │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐⭐⭐   │ ALL TIE     │
│                  │ O(N)         │ O(N)         │ O(N)         │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Robustness       │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐⭐     │ ⭐⭐         │ Length!     │
│                  │ ANY chars!   │ Length limit │ Escape bugs  │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Code Simplicity  │ ⭐⭐⭐⭐     │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐       │ Chunked     │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Industry Use     │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐       │ ⭐           │ Length!     │
│                  │ HTTP, etc    │ Binary proto │ Legacy       │             │
├──────────────────┼──────────────┼──────────────┼──────────────┼─────────────┤
│ Overall Best     │ ✅ YES       │ Good         │ Avoid        │ Length!     │
└──────────────────┴──────────────┴──────────────┴──────────────┴─────────────┘

⏱️  TIME TO MASTER: 15-20 minutes
🎯 DIFFICULTY: Medium
💡 TIP: "Length first, content second - No ambiguity!"
🔥 POPULAR: Classic design problem, tests protocol thinking!

================================================================================
                           🎯 PROBLEM UNDERSTANDING
================================================================================

WHAT IS THE PROBLEM?
--------------------
Design a way to convert a list of strings into ONE string, then convert it back
to the original list. The tricky part: strings can contain ANY characters!

REAL WORLD ANALOGY:
------------------
Think of it like SHIPPING PACKAGES:
- You have multiple items: ["Phone", "Book", "Pen"]
- Pack them into ONE box for shipping
- At destination, unpack to get original items back
- Challenge: How do you know where one item ends and next begins?

Solution: PUT A LABEL WITH SIZE!
- Package 1: "5 inches: Phone"
- Package 2: "4 inches: Book"
- Package 3: "3 inches: Pen"

Another analogy - NETWORK PACKETS:
- HTTP headers use "Content-Length: 1234"
- Tells receiver: "Next 1234 bytes are the content"
- Receiver reads exactly 1234 bytes, no guessing!

THE KEY INSIGHT:
---------------
If you know the LENGTH beforehand, you know EXACTLY where content ends!
No need to escape special characters or worry about delimiters!

❌ Wrong thinking: "Use a delimiter like '|' to separate strings"
   Problem: What if strings contain '|'? Need to escape... complex!

✅ Right thinking: "Prefix each string with its length!"
   "5#Hello3#Cat" → Read 5 chars after first #, then 3 chars after second #

================================================================================
                            📝 FORMAL PROBLEM
================================================================================

Design an algorithm to encode a list of strings to a single string. The encoded
string is then decoded back to the original list of strings.

Implement:
- encode(strs: List[str]) -> str
- decode(s: str) -> List[str]

Example 1:
----------
Input: ["Hello","World"]
encode() → "5#Hello5#World"
decode() → ["Hello","World"]

Example 2:
----------
Input: [""]
encode() → "0#"
decode() → [""]

Example 3:
----------
Input: ["a","#b","c#d#"]
encode() → "1#a2##b4#c#d#"
decode() → ["a","#b","c#d#"]
Note: # inside strings is perfectly fine!

Constraints:
------------
* 0 <= strs.length < 200
* 0 <= strs[i].length < 200
* strs[i] contains ANY possible characters (including special chars!)
* Must handle empty strings
* Must preserve exact original strings

Follow-up:
----------
Can you handle strings with unlimited character types without escaping?

================================================================================
                         🧠 KEY INSIGHTS TO REMEMBER
================================================================================

THE MAIN CHALLENGE:
------------------
❌ Simple delimiter doesn't work: What if delimiter appears in string?
❌ Escaping is complex: Nested escapes, edge cases galore!
✅ Length-prefix solves EVERYTHING: Know size → Read exactly that many!

THE MAGIC TRICK: "LENGTH-PREFIX PROTOCOL"
-----------------------------------------
Format: "length#content"

Examples:
  "Hello" → "5#Hello"
  ""      → "0#"
  "#"     → "1##"       (# inside is fine!)
  "a#b#c" → "5#a#b#c"   (Multiple # inside? No problem!)

THE BREAKTHROUGH INSIGHT:
------------------------
┌─────────────────────────────────────────────────────────────┐
│  Length prefix = Self-documenting protocol!                 │
│  - No escaping needed                                       │
│  - No character restrictions                                │
│  - Unambiguous parsing                                      │
│  - Industry standard (HTTP Content-Length, etc.)            │
└─────────────────────────────────────────────────────────────┘

WHY IT WORKS:
-------------
When decoding:
1. Read until '#' to get length
2. Read EXACTLY that many characters
3. Those characters can be ANYTHING (even '#'!)
4. Move to next length prefix
5. Repeat

No ambiguity because we know exact boundaries!

================================================================================
                          💡 SOLUTION APPROACHES
================================================================================
"""

from typing import List

# ============================================================================
#            APPROACH 1: LENGTH-PREFIX ENCODING (OPTIMAL)
# ============================================================================

class Codec:
    """
    🎯 APPROACH 1: Length-Prefix Encoding (BEST SOLUTION!)

    TIME COMPLEXITY: O(N) - N = total characters
    SPACE COMPLEXITY: O(N) - Encoded string

    🧠 MEMORIZATION TRICK: "Size Label Before Content"
    --------------------------------------------------
    Think: Like reading a package label before opening!
    - Label says "5 items inside"
    - You take out exactly 5 items
    - No guessing, no confusion!

    Format: "length#content"
    - "5#Hello" → string of length 5: "Hello"
    - "0#"      → empty string
    - "3#a#b"   → string "a#b" (# inside is OK!)

    📝 STEP-BY-STEP ALGORITHM (Encode):
    -----------------------------------
    1. For each string s in list:
       a. Get length: len(s)
       b. Append "length#s" to result
    2. Return concatenated result

    📝 STEP-BY-STEP ALGORITHM (Decode):
    -----------------------------------
    1. Start at position i=0
    2. While i < length:
       a. Find next '#' at position j
       b. Extract length = int(s[i:j])
       c. Extract string = s[j+1 : j+1+length]
       d. Add string to result
       e. Move i = j+1+length
    3. Return result list

    🎨 VISUAL EXAMPLE:
    -----------------
    Encode: ["Hello", "World", ""]

    Step 1: "Hello" (length 5)
      → "5#Hello"

    Step 2: "World" (length 5)
      → "5#Hello" + "5#World" = "5#Hello5#World"

    Step 3: "" (length 0)
      → "5#Hello5#World" + "0#" = "5#Hello5#World0#"

    Final: "5#Hello5#World0#"

    Decode: "5#Hello5#World0#"

    Step 1: i=0
      - Find '#' at j=1
      - length = int("5") = 5
      - Extract s[2:7] = "Hello"
      - i = 7

    Step 2: i=7
      - Find '#' at j=8
      - length = int("5") = 5
      - Extract s[9:14] = "World"
      - i = 14

    Step 3: i=14
      - Find '#' at j=15
      - length = int("0") = 0
      - Extract s[16:16] = ""
      - i = 16

    Result: ["Hello", "World", ""]

    WHY THIS IS BEST:
    ----------------
    ✅ Works with ANY characters (no restrictions!)
    ✅ No escaping needed
    ✅ Simple and clean
    ✅ Industry standard (HTTP, TCP, etc.)
    ✅ Unambiguous parsing
    """

    def encode(self, strs: List[str]) -> str:
        """Encodes a list of strings to a single string."""
        encoded = ""
        for s in strs:
            # Format: length + '#' + string
            encoded += str(len(s)) + "#" + s
        return encoded

    def decode(self, s: str) -> List[str]:
        """Decodes a single string to a list of strings."""
        result = []
        i = 0

        while i < len(s):
            # Find the delimiter '#'
            j = i
            while s[j] != '#':
                j += 1

            # Extract length (everything before '#')
            length = int(s[i:j])

            # Extract string of exactly 'length' characters after '#'
            start = j + 1
            end = start + length
            result.append(s[start:end])

            # Move to next encoded string
            i = end

        return result


# ============================================================================
#          APPROACH 2: CHUNKED ENCODING (FIXED-WIDTH LENGTH)
# ============================================================================

class CodecChunked:
    """
    🎯 APPROACH 2: Chunked Encoding with Fixed-Width Length

    TIME COMPLEXITY: O(N) - N = total characters
    SPACE COMPLEXITY: O(N)

    🧠 MEMORIZATION TRICK: "Fixed Size Package Labels"
    --------------------------------------------------
    Think: All labels are same width (e.g., 4 digits)
    - "0005Hello" → 5 characters follow
    - "0010HelloWorld" → 10 characters follow

    Format: "LLLL" + content (L = length digit)
    - Use fixed width (e.g., 4 digits) for length
    - Max string length = 9999 characters

    📝 ALGORITHM:
    ------------
    Encode: For each string, prepend 4-digit length
    Decode: Read 4 digits, then read that many chars

    🎨 VISUAL EXAMPLE:
    -----------------
    Encode: ["Hi", "World"]
    - "Hi" → "0002Hi"
    - "World" → "0005World"
    - Result: "0002Hi0005World"

    Decode: "0002Hi0005World"
    - Read "0002" → length=2, read "Hi"
    - Read "0005" → length=5, read "World"
    - Result: ["Hi", "World"]

    ⚠️  LIMITATION:
    --------------
    - Max string length limited (9999 with 4 digits)
    - Wastes space for short strings ("0001a")
    - But: SIMPLER parsing (no need to find '#')
    """

    def encode(self, strs: List[str]) -> str:
        """Encodes using fixed-width length prefix."""
        encoded = ""
        for s in strs:
            # 4-digit length prefix (max length 9999)
            encoded += f"{len(s):04d}" + s
        return encoded

    def decode(self, s: str) -> List[str]:
        """Decodes fixed-width length prefix string."""
        result = []
        i = 0

        while i < len(s):
            # Read 4-digit length
            length = int(s[i:i+4])

            # Read exactly 'length' characters after the 4 digits
            start = i + 4
            end = start + length
            result.append(s[start:end])

            # Move to next chunk
            i = end

        return result


# ============================================================================
#            APPROACH 3: ESCAPED DELIMITER (NOT RECOMMENDED)
# ============================================================================

class CodecEscaped:
    """
    🎯 APPROACH 3: Escaped Delimiter (DON'T USE THIS!)

    TIME COMPLEXITY: O(N) - But with potential escaping overhead
    SPACE COMPLEXITY: O(N) - More space due to escaping

    🧠 IDEA: Use delimiter, escape it when it appears
    -------------------------------------------------
    - Use rare delimiter like ":;"
    - If ":;" appears in string, replace with "::;;"
    - When decoding, un-escape

    ⚠️  PROBLEMS:
    ------------
    1. What if "::;;" appears in original string?
       Need double escaping... gets messy!
    2. Edge cases are complex
    3. Performance overhead from escaping
    4. Error-prone

    📝 ALGORITHM:
    ------------
    Encode:
      1. For each string, replace ":;" with "::;;"
      2. Join with ":;"

    Decode:
      1. Split by ":;"
      2. Replace "::;;" back to ":;"

    🎨 EXAMPLE:
    ----------
    Encode: ["Hello", "Wo:;rld"]
    - "Hello" → "Hello" (no escape needed)
    - "Wo:;rld" → "Wo::;;rld" (escape ":;")
    - Result: "Hello:;Wo::;;rld"

    Decode: "Hello:;Wo::;;rld"
    - Split: ["Hello", "Wo::;;rld"]
    - Unescape: ["Hello", "Wo:;rld"]

    ⚠️  WHY AVOID:
    -------------
    - Complex nested escape scenarios
    - More error-prone than length-prefix
    - No real advantage
    - NOT industry standard
    """

    def encode(self, strs: List[str]) -> str:
        """Encodes using escaped delimiter."""
        # Escape any occurrence of delimiter in strings
        escaped = [s.replace(":;", "::;;") for s in strs]
        return ":;".join(escaped)

    def decode(self, s: str) -> List[str]:
        """Decodes escaped delimiter string."""
        if not s:
            return []

        # Split by delimiter
        parts = s.split(":;")

        # Unescape
        result = [part.replace("::;;", ":;") for part in parts]
        return result


# ============================================================================
#                    🎨 VISUAL WALKTHROUGH EXAMPLE
# ============================================================================

"""
Let's encode and decode: ["abc", "", "x#y", "123"]

═══════════════════════════════════════════════════════════════════════
APPROACH 1: LENGTH-PREFIX
═══════════════════════════════════════════════════════════════════════

ENCODING:
---------
Step 1: "abc" (len=3)
  → "3#abc"

Step 2: "" (len=0)
  → "3#abc" + "0#" = "3#abc0#"

Step 3: "x#y" (len=3, note the # inside!)
  → "3#abc0#" + "3#x#y" = "3#abc0#3#x#y"

Step 4: "123" (len=3)
  → "3#abc0#3#x#y" + "3#123" = "3#abc0#3#x#y3#123"

FINAL ENCODED: "3#abc0#3#x#y3#123"

DECODING:
---------
Input: "3#abc0#3#x#y3#123"

Position i=0:
  - Find '#' at j=1
  - length = int("3") = 3
  - Extract s[2:5] = "abc"
  - i = 5

Position i=5:
  - Find '#' at j=6
  - length = int("0") = 0
  - Extract s[7:7] = ""
  - i = 7

Position i=7:
  - Find '#' at j=8
  - length = int("3") = 3
  - Extract s[9:12] = "x#y" (# is part of content!)
  - i = 12

Position i=12:
  - Find '#' at j=13
  - length = int("3") = 3
  - Extract s[14:17] = "123"
  - i = 17

FINAL DECODED: ["abc", "", "x#y", "123"] ✅

═══════════════════════════════════════════════════════════════════════
APPROACH 2: CHUNKED (4-DIGIT LENGTH)
═══════════════════════════════════════════════════════════════════════

ENCODING:
---------
"abc"  → "0003abc"
""     → "0000"
"x#y"  → "0003x#y"
"123"  → "0003123"

FINAL: "0003abc00000003x#y0003123"

DECODING:
---------
Read 4 digits → read that many chars → repeat

═══════════════════════════════════════════════════════════════════════
APPROACH 3: ESCAPED DELIMITER
═══════════════════════════════════════════════════════════════════════

Using delimiter ":;"

ENCODING:
---------
"abc"  → "abc" (no :; to escape)
""     → ""
"x#y"  → "x#y" (no :; to escape)
"123"  → "123"

Join with ":;" → "abc:;:;x#y:;123"

Notice the ":;:;" for empty string - this is where it gets confusing!

DECODING:
---------
Split by ":;" → ["abc", "", "x#y", "123"]
But wait! Multiple consecutive ":;" can be ambiguous!

This is why escaped delimiter is problematic!
"""

# ============================================================================
#              🎯 MEMORY TRICKS & COMMON MISTAKES
# ============================================================================

"""
🧠 HOW TO REMEMBER THIS SOLUTION:
---------------------------------
1. "PACKAGE LABEL" → Length tells you what's coming
2. "READ EXACT AMOUNT" → No need to search for end
3. "NO ESCAPING" → Length-prefix handles everything
4. "INDUSTRY STANDARD" → HTTP uses Content-Length

❌ COMMON MISTAKES TO AVOID:
----------------------------
1. ❌ Using simple delimiter without length
      WRONG: "Hello|World" - breaks if string contains '|'
      RIGHT: "5#Hello5#World" - works with any char!

2. ❌ Forgetting to handle empty strings
      WRONG: Skipping empty strings
      RIGHT: "0#" for empty string

3. ❌ Not handling special characters
      WRONG: Assuming no '#' in strings
      RIGHT: Length-prefix works even with '#' inside!

4. ❌ Complex escaping logic
      WRONG: Nested escaping rules
      RIGHT: No escaping needed with length-prefix!

5. ❌ Off-by-one errors in decode
      WRONG: Not advancing pointer correctly
      RIGHT: i = end (after reading 'length' characters)

✅ PRO TIPS:
-----------
1. Length-prefix is industry standard (HTTP, TCP)
2. Always test with edge cases (empty, special chars)
3. Draw out the encoding to verify
4. This pattern appears in network protocols
5. Remember: "Length first, content second"

🎯 INTERVIEW STRATEGY:
---------------------
"I'll use length-prefix encoding - the format is 'length#content'. This works
with any characters because we know exactly how many to read. No escaping
needed. It's the same approach used in HTTP Content-Length headers."

Then implement, explain edge cases (empty strings, # in content), done!
"""

# ============================================================================
#                         🧪 TEST CASES
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("              ENCODE AND DECODE STRINGS - TEST CASES")
    print("="*80)

    codec1 = Codec()
    codec2 = CodecChunked()
    codec3 = CodecEscaped()

    # Test Case 1: Standard strings
    print("\n📝 Test Case 1: Standard strings")
    print("-" * 80)
    strs1 = ["Hello", "World"]
    print(f"Input: {strs1}")
    enc1 = codec1.encode(strs1)
    dec1 = codec1.decode(enc1)
    print(f"Length-Prefix Encoded: {enc1}")
    print(f"Length-Prefix Decoded: {dec1}")
    print(f"✅ PASS" if dec1 == strs1 else "❌ FAIL")

    # Test Case 2: Empty string in list
    print("\n📝 Test Case 2: Empty string in list")
    print("-" * 80)
    strs2 = ["a", "", "bc"]
    print(f"Input: {strs2}")
    enc2 = codec1.encode(strs2)
    dec2 = codec1.decode(enc2)
    print(f"Encoded: {enc2}")
    print(f"Decoded: {dec2}")
    print(f"✅ PASS" if dec2 == strs2 else "❌ FAIL")

    # Test Case 3: Strings with delimiter character
    print("\n📝 Test Case 3: Strings with # character")
    print("-" * 80)
    strs3 = ["#abc", "def#", "g#h#i"]
    print(f"Input: {strs3}")
    enc3 = codec1.encode(strs3)
    dec3 = codec1.decode(enc3)
    print(f"Encoded: {enc3}")
    print(f"Decoded: {dec3}")
    print(f"✅ PASS" if dec3 == strs3 else "❌ FAIL")

    # Test Case 4: Single empty string
    print("\n📝 Test Case 4: Single empty string")
    print("-" * 80)
    strs4 = [""]
    print(f"Input: {strs4}")
    enc4 = codec1.encode(strs4)
    dec4 = codec1.decode(enc4)
    print(f"Encoded: {enc4}")
    print(f"Decoded: {dec4}")
    print(f"✅ PASS" if dec4 == strs4 else "❌ FAIL")

    # Test Case 5: Numbers and special chars
    print("\n📝 Test Case 5: Numbers and special characters")
    print("-" * 80)
    strs5 = ["123", "456#789", "#", "!@#$%"]
    print(f"Input: {strs5}")
    enc5 = codec1.encode(strs5)
    dec5 = codec1.decode(enc5)
    print(f"Encoded: {enc5}")
    print(f"Decoded: {dec5}")
    print(f"✅ PASS" if dec5 == strs5 else "❌ FAIL")

    # Test Case 6: Very long string
    print("\n📝 Test Case 6: Long string")
    print("-" * 80)
    strs6 = ["a" * 100, "b" * 50]
    print(f"Input: ['{'a'*100}', '{'b'*50}'] (lengths: 100, 50)")
    enc6 = codec1.encode(strs6)
    dec6 = codec1.decode(enc6)
    print(f"Encoded length: {len(enc6)}")
    print(f"Decoded lengths: {[len(s) for s in dec6]}")
    print(f"✅ PASS" if dec6 == strs6 else "❌ FAIL")

    # Test Case 7: Consecutive empty strings
    print("\n📝 Test Case 7: Consecutive empty strings")
    print("-" * 80)
    strs7 = ["", "", "a", ""]
    print(f"Input: {strs7}")
    enc7 = codec1.encode(strs7)
    dec7 = codec1.decode(enc7)
    print(f"Encoded: {enc7}")
    print(f"Decoded: {dec7}")
    print(f"✅ PASS" if dec7 == strs7 else "❌ FAIL")

    # Compare all three approaches
    print("\n" + "="*80)
    print("              COMPARING ALL APPROACHES")
    print("="*80)
    test_strs = ["Hi", "World", "#", ""]
    print(f"\nTest input: {test_strs}")
    print("-" * 80)

    enc_a = codec1.encode(test_strs)
    enc_b = codec2.encode(test_strs)
    enc_c = codec3.encode(test_strs)

    print(f"Length-Prefix:  {enc_a}")
    print(f"Chunked:        {enc_b}")
    print(f"Escaped:        {enc_c}")

    dec_a = codec1.decode(enc_a)
    dec_b = codec2.decode(enc_b)
    dec_c = codec3.decode(enc_c)

    print(f"\nAll decoded correctly: {dec_a == dec_b == dec_c == test_strs}")

    print("\n" + "="*80)
    print("              ✅ ALL TEST CASES COMPLETED!")
    print("="*80)


# ============================================================================
#              🎓 LEARNING SUMMARY & KEY TAKEAWAYS
# ============================================================================

"""
🎯 WHAT YOU LEARNED:
-------------------
1. Length-prefix encoding is the BEST approach
2. Works with ANY characters (no restrictions!)
3. No escaping needed
4. Industry standard (HTTP, TCP, etc.)
5. Three approaches with different trade-offs

🔑 KEY PATTERN: "Self-Documenting Protocol"
-------------------------------------------
This pattern applies when:
- Need to serialize/deserialize data
- Character set is unrestricted
- Want simple, robust solution

Used in:
- HTTP Content-Length header
- TCP message framing
- Binary protocols
- Database wire protocols

💪 THREE APPROACHES TO MASTER:
-----------------------------
1. LENGTH-PREFIX (Best - O(N))
   - Format: "length#content"
   - Works with ANY characters
   - No escaping needed
   - Industry standard

2. CHUNKED (Good - O(N))
   - Format: "LLLLcontent" (fixed width)
   - Simpler parsing
   - Limited max length
   - More space for small strings

3. ESCAPED (Avoid - O(N))
   - Use delimiter with escaping
   - Complex edge cases
   - Error-prone
   - No advantage over length-prefix

🎯 INTERVIEW TIPS:
-----------------
1. Mention length-prefix as industry standard
2. Explain why it works (no ambiguity)
3. Test with edge cases (empty, special chars)
4. Compare to HTTP Content-Length
5. Draw encoding/decoding example

🎉 CONGRATULATIONS!
------------------
You now understand how to encode/decode strings robustly!
Remember: "Length first, content second - No escaping needed!"

📊 COMPLEXITY SUMMARY:
---------------------
┌────────────────────┬──────────────┬──────────────┐
│ Approach           │ Time         │ Space        │
├────────────────────┼──────────────┼──────────────┤
│ Length-Prefix      │ O(N)         │ O(N)         │
│ Chunked            │ O(N)         │ O(N)         │
│ Escaped            │ O(N)         │ O(N + E)     │
└────────────────────┴──────────────┴──────────────┘

N = total characters
E = escaping overhead

🏆 RECOMMENDED: Use Length-Prefix for robust, clean solution!

🔗 RELATED PROBLEMS TO PRACTICE:
-------------------------------
1. LeetCode #271: Encode and Decode Strings (this problem!)
2. LeetCode #297: Serialize and Deserialize Binary Tree
3. LeetCode #449: Serialize and Deserialize BST
4. LeetCode #535: Encode and Decode TinyURL
5. Design problems involving serialization

💡 FINAL TIP:
------------
Length-prefix encoding is used EVERYWHERE in real systems:
- HTTP: "Content-Length: 1234"
- TCP: Message framing
- Databases: Protocol messages
- File formats: Chunk sizes

Master this pattern - it's fundamental to system design!
"""
