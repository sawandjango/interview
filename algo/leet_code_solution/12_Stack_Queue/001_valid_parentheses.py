"""
LeetCode Problem #20: Valid Parentheses

Difficulty: Easy
Topics: String, Stack
Companies: Amazon, Facebook, Google, Microsoft, Bloomberg, Apple

Problem Statement:
================================================================================
Given a string s containing just the characters '(', ')', '{', '}', '[' and
']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

Example 1:
----------
Input: s = "()"
Output: true

Example 2:
----------
Input: s = "()[]{}"
Output: true

Example 3:
----------
Input: s = "(]"
Output: false

Example 4:
----------
Input: s = "([])"
Output: true

Constraints:
------------
* 1 <= s.length <= 10^4
* s consists of parentheses only '()[]{}'.

================================================================================

Hints:
------
1. Use a stack of characters.
2. When you encounter an opening bracket, push it to the top of the stack.
3. When you encounter a closing bracket, check if the top of the stack is the
   corresponding opening bracket. If yes, pop it from the stack. Otherwise,
   return false.

================================================================================
"""

# Solution:
def isValid(s):
    """
    Approach: Stack
    Time Complexity: O(n) where n is length of string
    Space Complexity: O(n) for the stack

    Algorithm:
    1. Use a stack to keep track of opening brackets
    2. For each character:
       - If opening bracket: push to stack
       - If closing bracket: check if it matches top of stack
    3. At the end, stack should be empty
    """
    # Mapping of closing to opening brackets
    mapping = {')': '(', '}': '{', ']': '['}
    stack = []

    for char in s:
        if char in mapping:  # closing bracket
            # Pop from stack if not empty, otherwise use dummy value
            top_element = stack.pop() if stack else '#'

            # Check if the mapping matches
            if mapping[char] != top_element:
                return False
        else:  # opening bracket
            stack.append(char)

    # Valid if stack is empty
    return not stack


# Test cases
if __name__ == "__main__":
    # Test case 1
    s1 = "()"
    print(f"Input: s = '{s1}'")
    print(f"Output: {isValid(s1)}")
    print(f"Expected: true\n")

    # Test case 2
    s2 = "()[]{}"
    print(f"Input: s = '{s2}'")
    print(f"Output: {isValid(s2)}")
    print(f"Expected: true\n")

    # Test case 3
    s3 = "(]"
    print(f"Input: s = '{s3}'")
    print(f"Output: {isValid(s3)}")
    print(f"Expected: false\n")

    # Test case 4
    s4 = "([])"
    print(f"Input: s = '{s4}'")
    print(f"Output: {isValid(s4)}")
    print(f"Expected: true\n")

    # Test case 5
    s5 = "([)]"
    print(f"Input: s = '{s5}'")
    print(f"Output: {isValid(s5)}")
    print(f"Expected: false\n")
