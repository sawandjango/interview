"""
LeetCode Problem #226: Invert Binary Tree

Difficulty: Easy
Topics: Tree, DFS, BFS, Recursion, Tree Manipulation
Companies: Google, Amazon, Facebook, Microsoft, Apple, Bloomberg
Famous: "Google Interview Question - Max Howell (Homebrew creator) rejected!"

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
│ 4    │ 💡 SOLUTION 1: Recursive DFS ⭐       │ • WHY choose? (Pros/Cons)     │
│      │    (RECOMMENDED)                     │ • WHEN to use?                │
│      │                                      │ • Step-by-step walkthrough    │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 5    │ 💡 SOLUTION 2: Iterative BFS         │ • WHY choose? (Pros/Cons)     │
│      │    (Alternative)                     │ • WHEN to use?                │
│      │                                      │ • Comparison with Solution 1  │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 6    │ 💻 IMPLEMENTATION                    │ • Clean, commented code       │
│      │                                      │ • Both solutions              │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 7    │ 🧪 TEST CASES                        │ • Comprehensive tests         │
│      │                                      │ • Edge cases covered          │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 8    │ 🎓 LEARNING SUMMARY                  │ • Key takeaways               │
│      │                                      │ • Memory tricks               │
│      │                                      │ • Common mistakes             │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 9    │ 🔗 RELATED PROBLEMS                  │ • Similar problems            │
│      │                                      │ • Pattern recognition         │
└──────┴──────────────────────────────────────┴───────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           🎯 MEMORY CHEAT SHEET                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ ANALOGY          │ "Mirror Reflection" - Left becomes Right!               │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ PATTERN          │ "Swap and Recurse" - Swap children, then recurse        │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ BASE CASE        │ If None → Return None (nothing to invert)              │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ DEFAULT SOLUTION │ Recursive DFS (Use in 95% of cases!)                   │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ TIME COMPLEXITY  │ O(N) - Visit every node exactly once                   │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ SPACE COMPLEXITY │ O(H) - Recursion stack depth (H = height)              │
└──────────────────┴─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        ⚡ QUICK DECISION TABLE                              │
├────────────────────────────────┬────────────────────────────────────────────┤
│ SITUATION                      │ WHICH SOLUTION TO USE?                    │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Normal interview               │ ✅ Solution 1 (Recursive)                 │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Very deep tree (height > 1000) │ ⚠️  Solution 2 (Iterative BFS)            │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Want simplest code             │ ✅ Solution 1 (Just 3 lines!)             │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Need level-by-level processing │ ⚠️  Solution 2 (Iterative BFS)            │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Avoid recursion                │ ⚠️  Solution 2 (Iterative)                │
└────────────────────────────────┴────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     📊 SOLUTION COMPARISON TABLE                            │
├──────────────────┬─────────────────────────┬────────────────────────────────┤
│ CRITERIA         │ SOLUTION 1 (Recursive)  │ SOLUTION 2 (Iterative BFS)    │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Code Length      │ ⭐⭐⭐⭐⭐ 3 lines!       │ ⭐⭐⭐ 10+ lines                │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Readability      │ ⭐⭐⭐⭐⭐ Crystal clear  │ ⭐⭐⭐ More complex             │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Interview Speed  │ ⭐⭐⭐⭐⭐ Lightning fast │ ⭐⭐⭐ Takes longer             │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Stack Safety     │ ⭐⭐⭐ Risk overflow     │ ⭐⭐⭐⭐⭐ No stack issues       │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Intuitive        │ ⭐⭐⭐⭐⭐ Very natural   │ ⭐⭐⭐ Less intuitive           │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ When to Use      │ 95% of cases (DEFAULT)  │ Very deep trees only          │
└──────────────────┴─────────────────────────┴────────────────────────────────┘

⏱️  TIME TO MASTER: 15-20 minutes
🎯 DIFFICULTY: Easy (One of the simplest tree problems!)
💡 TIP: This is the SHORTEST solution - just swap and recurse!
🔥 FAMOUS: Max Howell (Homebrew creator) couldn't solve this at Google!

================================================================================
                           🎯 PROBLEM UNDERSTANDING
================================================================================

WHAT IS THE PROBLEM?
--------------------
You're given a BINARY TREE and need to FLIP/MIRROR it horizontally!

Think of it like: Looking at the tree in a MIRROR - left becomes right,
right becomes left!

REAL WORLD ANALOGY:
------------------
Think of FLIPPING A PHOTO horizontally! 📸

Original Photo:        Flipped Photo:
    Person                Person
   /     \               /     \
 Left    Right        Right   Left
 Hand    Hand         Hand    Hand

Everything swaps sides!

Another analogy: MIRROR REFLECTION 🪞
Stand in front of a mirror:
- Your LEFT hand appears on the RIGHT in mirror
- Your RIGHT hand appears on the LEFT in mirror
- Perfect horizontal flip!

Or think of: READING BACKWARDS
- Original: "HELLO" → Tree structure
- Inverted: "OLLEH" → Flipped structure

================================================================================
                            📝 FORMAL PROBLEM
================================================================================

Given the root of a binary tree, invert the tree, and return its root.

Inverting a binary tree means swapping the left and right children of all nodes.

Example 1:
----------
Input: root = [4,2,7,1,3,6,9]

Before Invert:
       4
      / \
     2   7
    / \ / \
   1  3 6  9

After Invert:
       4
      / \
     7   2
    / \ / \
   9  6 3  1

Output: [4,7,2,9,6,3,1]

Explanation:
- 4's children: 2,7 → become 7,2 (swapped)
- 2's children: 1,3 → become 3,1 (swapped)
- 7's children: 6,9 → become 9,6 (swapped)

Example 2:
----------
Input: root = [2,1,3]

Before:          After:
    2              2
   / \            / \
  1   3          3   1

Output: [2,3,1]

Example 3:
----------
Input: root = []

Output: []

Constraints:
------------
* The number of nodes in the tree is in the range [0, 100]
* -100 <= Node.val <= 100

================================================================================
                         🧠 KEY INSIGHTS TO REMEMBER
================================================================================

THE MAIN CHALLENGE:
------------------
❌ Don't just swap values - swap the actual NODE POINTERS!
❌ Must swap recursively at ALL levels, not just root!
✅ Swap left and right, then recurse on children!

THE MAGIC TRICK: "Swap and Recurse"
------------------------------------
For each node:
1. Swap its left and right children
2. Recursively invert the left subtree
3. Recursively invert the right subtree

Think: "SWAP THEN DIVE DEEPER"

Visual:
       A              A
      / \            / \
     B   C    →     C   B
    / \            / \
   D   E          E   D

Step 1: Swap B and C at A
Step 2: Recurse on B (now on right): Swap D and E
Result: Done!

Key Insight: EVERY node performs the SAME operation!
- No special cases
- No complex logic
- Just: SWAP, RECURSE, DONE!

================================================================================
                          💡 SOLUTION APPROACHES
================================================================================
"""

from collections import deque
from typing import Optional


# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ============================================================================
#              APPROACH 1: Recursive DFS (MOST INTUITIVE!)
# ============================================================================

def invertTree(root):
    """
    🎯 APPROACH 1: Recursive DFS (RECOMMENDED!)

    TIME COMPLEXITY: O(n) - Visit each node once
    SPACE COMPLEXITY: O(h) - Recursion stack (h = height)
                      Worst case O(n) for skewed tree

    🧠 MEMORIZATION TRICK: "Swap Hands and Continue" 🤝
    --------------------------------------------------
    Imagine shaking hands with everyone in a family tree:
    1. Swap your left and right hands
    2. Shake with left person (using swapped hand)
    3. Shake with right person (using swapped hand)
    4. Tell each person to do the same with THEIR children!

    Mantra: "Swap at Every Stop, Top to Bottom!"

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Base case: If node is null → return null
    2. Swap left and right children
    3. Recursively invert left subtree
    4. Recursively invert right subtree
    5. Return root

    Why this works:
    - Each node swaps its children
    - Recursion handles all descendants automatically
    - Post-order traversal ensures bottom-up correctness
    - Simple and elegant!
    """
    # Base case: empty tree or null node
    if not root:
        return None

    # Swap left and right children (THE MAGIC LINE!)
    root.left, root.right = root.right, root.left

    # Recursively invert both subtrees
    invertTree(root.left)
    invertTree(root.right)

    # Return the root of inverted tree
    return root


# ============================================================================
#              APPROACH 2: Recursive with Explicit Swap (Clearer)
# ============================================================================

def invertTree_Verbose(root):
    """
    🎯 APPROACH 2: Same as Approach 1 but more explicit

    TIME COMPLEXITY: O(n)
    SPACE COMPLEXITY: O(h)

    🧠 MEMORIZATION TRICK: "Store, Swap, Recurse"
    --------------------------------------------
    Same logic but written more explicitly for clarity:
    1. Store left child temporarily
    2. Assign right to left
    3. Assign temp (old left) to right
    4. Recurse on new left and right

    This is EXACTLY the same as Approach 1, just spelled out!
    """
    if not root:
        return None

    # Store left child temporarily
    temp = root.left

    # Swap children
    root.left = root.right
    root.right = temp

    # Recursively invert both subtrees
    invertTree_Verbose(root.left)
    invertTree_Verbose(root.right)

    return root


# ============================================================================
#              APPROACH 3: Iterative BFS with Queue
# ============================================================================

def invertTree_BFS(root):
    """
    🎯 APPROACH 3: Iterative BFS with Queue

    TIME COMPLEXITY: O(n)
    SPACE COMPLEXITY: O(w) - Queue holds max width

    🧠 MEMORIZATION TRICK: "Level by Level Swap"
    -------------------------------------------
    Think: Process tree like reading a book (left to right, level by level):
    - Visit each node
    - Swap its children
    - Add children to queue for later processing
    - Repeat until queue empty

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Create queue, add root
    2. While queue not empty:
       a. Remove node from queue
       b. Swap its left and right children
       c. Add children to queue (if they exist)
    3. Return root
    """
    if not root:
        return None

    queue = deque([root])

    while queue:
        # Get current node
        node = queue.popleft()

        # Swap left and right children
        node.left, node.right = node.right, node.left

        # Add children to queue for processing
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return root


# ============================================================================
#              APPROACH 4: Iterative DFS with Stack
# ============================================================================

def invertTree_Stack(root):
    """
    🎯 APPROACH 4: Iterative DFS with Stack

    TIME COMPLEXITY: O(n)
    SPACE COMPLEXITY: O(h)

    🧠 MEMORIZATION TRICK: "Stack of Swap Tasks"
    ------------------------------------------
    Similar to BFS but uses stack (LIFO) instead of queue (FIFO):
    - Push root to stack
    - Pop node, swap children
    - Push children to stack
    - Repeat until stack empty

    Same result as BFS, different traversal order.
    """
    if not root:
        return None

    stack = [root]

    while stack:
        # Pop node from stack
        node = stack.pop()

        # Swap left and right children
        node.left, node.right = node.right, node.left

        # Add children to stack
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)

    return root


# ============================================================================
#                    🎨 VISUAL WALKTHROUGH EXAMPLE
# ============================================================================

"""
Let's walk through Example 1 step-by-step:

Original Tree:
       4
      / \\
     2   7
    / \\ / \\
   1  3 6  9

APPROACH 1: Recursive DFS
-------------------------

CALL 1: invertTree(4)
---------------------
root = 4
- Not null ✓
- Swap children: 2 and 7

  Before swap:        After swap:
       4                   4
      / \\                / \\
     2   7              7   2
    / \\ / \\          / \\ / \\
   1  3 6  9        6  9 1  3

- Now recurse on left (which is now 7!)
- And recurse on right (which is now 2!)

CALL 2: invertTree(7) [left subtree of 4]
------------------------------------------
root = 7
- Not null ✓
- Swap children: 6 and 9

  Before swap:        After swap:
       7                   7
      / \\                / \\
     6   9              9   6

- Recurse on 9: no children, returns 9
- Recurse on 6: no children, returns 6
- Return 7

CALL 3: invertTree(2) [right subtree of 4]
-------------------------------------------
root = 2
- Not null ✓
- Swap children: 1 and 3

  Before swap:        After swap:
       2                   2
      / \\                / \\
     1   3              3   1

- Recurse on 3: no children, returns 3
- Recurse on 1: no children, returns 1
- Return 2

Back to CALL 1:
- Left subtree (7) inverted ✓
- Right subtree (2) inverted ✓
- Return 4

FINAL RESULT:
       4
      / \\
     7   2
    / \\ / \\
   9  6 3  1

Success! ✓


APPROACH 3: BFS with Queue
---------------------------

INITIALIZATION:
queue = deque([4])

ITERATION 1:
------------
Pop: node = 4
Swap children: 2 ↔ 7

Tree after swap:
       4
      / \\
     7   2
    / \\ / \\
   6  9 1  3

Add to queue: 7, 2
queue = deque([7, 2])

ITERATION 2:
------------
Pop: node = 7
Swap children: 6 ↔ 9

Tree after swap:
       4
      / \\
     7   2
    / \\ / \\
   9  6 1  3

Add to queue: 9, 6
queue = deque([2, 9, 6])

ITERATION 3:
------------
Pop: node = 2
Swap children: 1 ↔ 3

Tree after swap:
       4
      / \\
     7   2
    / \\ / \\
   9  6 3  1

Add to queue: 3, 1
queue = deque([9, 6, 3, 1])

ITERATION 4-7:
--------------
Pop: 9 (no children, nothing to swap)
Pop: 6 (no children, nothing to swap)
Pop: 3 (no children, nothing to swap)
Pop: 1 (no children, nothing to swap)

queue = deque([])  ← Empty!

Exit loop → Return root

FINAL RESULT:
       4
      / \\
     7   2
    / \\ / \\
   9  6 3  1

Success! ✓
"""

# ============================================================================
#              🎯 MEMORY TRICKS & COMMON MISTAKES
# ============================================================================

"""
🧠 HOW TO REMEMBER THIS SOLUTION:
---------------------------------
Analogy: "MIRROR SELFIE" 🤳

When you take a selfie with your phone:
- Front camera FLIPS the image horizontally
- What's on your left appears on right in photo
- What's on your right appears on left in photo
- This happens to EVERYTHING in the image!

Same with tree inversion:
- Every node's children get flipped
- Left becomes right, right becomes left
- Apply to ALL nodes, not just root!

Mantra: "Swap Everywhere, Top to Bottom!"

Visual Memory Aid:
-----------------
Before:          After:
   4               4
  / \\            / \\
 2   7          7   2
/ \\ / \\      / \\ / \\
1 3 6 9      9 6 3 1

Notice: EVERY level is mirrored!
- Level 1: 2,7 → 7,2
- Level 2: 1,3,6,9 → 9,6,3,1

❌ COMMON MISTAKES TO AVOID:
----------------------------
1. ❌ Only swapping at root level
   ```python
   # WRONG:
   root.left, root.right = root.right, root.left
   return root  # Forgot to recurse!

   # CORRECT:
   root.left, root.right = root.right, root.left
   invertTree(root.left)   # Recurse left
   invertTree(root.right)  # Recurse right
   return root
   ```

2. ❌ Swapping values instead of nodes
   ```python
   # WRONG:
   root.left.val, root.right.val = root.right.val, root.left.val
   # This only swaps VALUES, not the subtrees!

   # CORRECT:
   root.left, root.right = root.right, root.left
   # This swaps the actual NODE REFERENCES!
   ```

3. ❌ Recursing before swapping
   ```python
   # WRONG (subtle bug):
   invertTree(root.left)   # Recurse first
   invertTree(root.right)
   root.left, root.right = root.right, root.left  # Then swap
   # This inverts THEN swaps, wrong order!

   # CORRECT:
   root.left, root.right = root.right, root.left  # Swap first
   invertTree(root.left)   # Then recurse
   invertTree(root.right)
   ```

4. ❌ Not handling null nodes
   ```python
   # WRONG:
   def invertTree(root):
       root.left, root.right = root.right, root.left
       # What if root is null? Crash!

   # CORRECT:
   def invertTree(root):
       if not root:
           return None
       root.left, root.right = root.right, root.left
   ```

5. ❌ Forgetting to return the root
   ```python
   # WRONG:
   def invertTree(root):
       if not root:
           return None
       root.left, root.right = root.right, root.left
       invertTree(root.left)
       invertTree(root.right)
       # Forgot to return!

   # CORRECT:
   def invertTree(root):
       # ... swap and recurse ...
       return root  # Don't forget!
   ```

✅ PRO TIPS:
-----------
1. Python's swap syntax is beautiful: a, b = b, a
2. Recursive solution is simplest (just 5 lines!)
3. Can swap before or after recursing (both work)
4. BFS and DFS iterative also work fine
5. Test with: null tree, single node, skewed tree

🔧 DEBUGGING CHECKLIST:
-----------------------
If your solution doesn't work:
□ Did you handle null/empty tree?
□ Are you swapping NODES not VALUES?
□ Did you recurse on BOTH children?
□ Did you return the root?
□ Are you swapping at EVERY node, not just root?

🎭 FAMOUS STORY:
---------------
Max Howell (creator of Homebrew) was rejected by Google
because he couldn't invert a binary tree on a whiteboard!

His tweet: "Google: 90% of our engineers use the software you wrote
(Homebrew), but you can't invert a binary tree on a whiteboard so f*** off."

This problem became FAMOUS after that incident!

Lesson: Even senior engineers can struggle with interview questions.
Practice is important! 🎯
"""

# ============================================================================
#                         🧪 TEST CASES
# ============================================================================

def test_invertTree():
    """Run comprehensive test cases"""

    print("="*70)
    print("              INVERT BINARY TREE - TEST CASES")
    print("="*70)

    # Helper function to build tree from list
    def build_tree(values):
        if not values:
            return None

        root = TreeNode(values[0])
        queue = deque([root])
        i = 1

        while queue and i < len(values):
            node = queue.popleft()

            if i < len(values) and values[i] is not None:
                node.left = TreeNode(values[i])
                queue.append(node.left)
            i += 1

            if i < len(values) and values[i] is not None:
                node.right = TreeNode(values[i])
                queue.append(node.right)
            i += 1

        return root

    # Helper to convert tree to list (level order)
    def tree_to_list(root):
        if not root:
            return []
        result = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if node:
                result.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append(None)
        # Remove trailing Nones
        while result and result[-1] is None:
            result.pop()
        return result

    # Test Case 1: Standard tree
    print("\n📝 Test Case 1: Standard tree [4,2,7,1,3,6,9]")
    print("-" * 70)
    print("Before Invert:")
    print("       4")
    print("      / \\")
    print("     2   7")
    print("    / \\ / \\")
    print("   1  3 6  9")
    print("\nAfter Invert:")
    print("       4")
    print("      / \\")
    print("     7   2")
    print("    / \\ / \\")
    print("   9  6 3  1")

    root1 = build_tree([4, 2, 7, 1, 3, 6, 9])
    result1_recursive = invertTree(build_tree([4, 2, 7, 1, 3, 6, 9]))
    result1_bfs = invertTree_BFS(build_tree([4, 2, 7, 1, 3, 6, 9]))
    expected1 = [4, 7, 2, 9, 6, 3, 1]

    print(f"\nRecursive: {tree_to_list(result1_recursive)}")
    print(f"BFS:       {tree_to_list(result1_bfs)}")
    print(f"Expected:  {expected1}")
    print(f"✓ PASS" if tree_to_list(result1_recursive) == expected1 else f"✗ FAIL")

    # Test Case 2: Small tree
    print("\n📝 Test Case 2: Small tree [2,1,3]")
    print("-" * 70)
    print("Before:          After:")
    print("    2              2")
    print("   / \\            / \\")
    print("  1   3          3   1")

    result2 = invertTree(build_tree([2, 1, 3]))
    expected2 = [2, 3, 1]

    print(f"\nResult:   {tree_to_list(result2)}")
    print(f"Expected: {expected2}")
    print(f"✓ PASS" if tree_to_list(result2) == expected2 else f"✗ FAIL")

    # Test Case 3: Single node
    print("\n📝 Test Case 3: Single node [1]")
    print("-" * 70)
    print("Tree: 1")
    print("Stays: 1")

    result3 = invertTree(build_tree([1]))
    expected3 = [1]

    print(f"\nResult:   {tree_to_list(result3)}")
    print(f"Expected: {expected3}")
    print(f"Explanation: Single node stays same")
    print(f"✓ PASS" if tree_to_list(result3) == expected3 else f"✗ FAIL")

    # Test Case 4: Empty tree
    print("\n📝 Test Case 4: Empty tree []")
    print("-" * 70)
    print("Tree: (empty)")

    result4 = invertTree(build_tree([]))
    expected4 = []

    print(f"\nResult:   {tree_to_list(result4)}")
    print(f"Expected: {expected4}")
    print(f"✓ PASS" if tree_to_list(result4) == expected4 else f"✗ FAIL")

    # Test Case 5: Left-skewed tree
    print("\n📝 Test Case 5: Left-skewed tree [1,2,null,3,null,4]")
    print("-" * 70)
    print("Before:          After:")
    print("    1              1")
    print("   /                \\")
    print("  2                  2")
    print(" /                    \\")
    print("3                      3")
    print("/                        \\")
    print("4                          4")

    result5 = invertTree(build_tree([1, 2, None, 3, None, 4]))
    expected5 = [1, None, 2, None, 3, None, 4]

    print(f"\nResult:   {tree_to_list(result5)}")
    print(f"Expected: {expected5}")
    print(f"Explanation: Left-skewed becomes right-skewed")
    print(f"✓ PASS" if tree_to_list(result5) == expected5 else f"✗ FAIL")

    # Test Case 6: Complete tree
    print("\n📝 Test Case 6: Complete tree [1,2,3,4,5,6,7]")
    print("-" * 70)
    print("Before:          After:")
    print("      1              1")
    print("     / \\            / \\")
    print("    2   3          3   2")
    print("   / \\ / \\        / \\ / \\")
    print("  4  5 6  7      7  6 5  4")

    result6 = invertTree(build_tree([1, 2, 3, 4, 5, 6, 7]))
    expected6 = [1, 3, 2, 7, 6, 5, 4]

    print(f"\nResult:   {tree_to_list(result6)}")
    print(f"Expected: {expected6}")
    print(f"✓ PASS" if tree_to_list(result6) == expected6 else f"✗ FAIL")

    # Test Case 7: Unbalanced tree
    print("\n📝 Test Case 7: Unbalanced tree [1,2,3,4,null,null,5]")
    print("-" * 70)
    print("Before:          After:")
    print("      1              1")
    print("     / \\            / \\")
    print("    2   3          3   2")
    print("   /     \\          /   \\")
    print("  4       5        5     4")

    result7 = invertTree(build_tree([1, 2, 3, 4, None, None, 5]))
    expected7 = [1, 3, 2, 5, None, None, 4]

    print(f"\nResult:   {tree_to_list(result7)}")
    print(f"Expected: {expected7}")
    print(f"✓ PASS" if tree_to_list(result7) == expected7 else f"✗ FAIL")

    print("\n" + "="*70)
    print("              ✅ ALL TEST CASES COMPLETED!")
    print("="*70)


if __name__ == "__main__":
    test_invertTree()


# ============================================================================
#              🎓 LEARNING SUMMARY & KEY TAKEAWAYS
# ============================================================================

"""
🎯 WHAT YOU LEARNED:
-------------------
1. Invert tree = Swap left and right children at EVERY node
2. Swap the NODE POINTERS, not values!
3. Recursive solution is simplest (5 lines of code)
4. Can use DFS (recursive/stack) or BFS (queue)
5. Don't forget base case (null node)

🔑 KEY PATTERN: "Swap and Recurse"
----------------------------------
This pattern applies to:
- Invert Binary Tree (this problem)
- Swap Nodes in Pairs (Linked List)
- Reverse operations on trees
- Tree transformations

The Template:
-------------
```python
def invertTree(root):
    # Base case
    if not root:
        return None

    # Swap children
    root.left, root.right = root.right, root.left

    # Recurse on both subtrees
    invertTree(root.left)
    invertTree(root.right)

    return root
```

💪 SIMILAR PROBLEMS TO PRACTICE:
-------------------------------
1. LeetCode #101: Symmetric Tree (check if tree is symmetric)
2. LeetCode #100: Same Tree (compare two trees)
3. LeetCode #617: Merge Two Binary Trees
4. LeetCode #951: Flip Equivalent Binary Trees
5. LeetCode #24: Swap Nodes in Pairs (Linked List version)

🎉 CONGRATULATIONS!
------------------
You now master the Tree Inversion pattern!

Remember the KEY INSIGHTS:
1. "Swap at Every Stop"
2. "Nodes Not Values"
3. "Base Case First"

Key Differences from Similar Problems:
- Level Order: Process layer by layer with BFS
- Symmetric Tree: Compare mirror positions
- Invert Tree: MODIFY tree (swap children)
- Same Tree: COMPARE two trees

🎓 INTERVIEW TIPS:
-----------------
1. Start with the simplest recursive solution
2. Draw the tree and show swaps at each level
3. Mention the famous Max Howell story (shows you know history!)
4. Walk through a small example (3 nodes is enough)
5. Discuss time/space complexity

Explanation Template:
--------------------
"I'll invert the tree by swapping left and right children at every node.
Starting from the root, I swap its children, then recursively invert the
left subtree and right subtree. The base case is when we reach a null node.
This takes O(n) time to visit all nodes and O(h) space for the recursion stack."

🧠 WHY RECURSIVE IS NATURAL HERE:
---------------------------------
Invert tree is PERFECTLY suited for recursion:
- Same operation at EVERY node (swap children)
- Natural divide-and-conquer (invert left, invert right)
- Clean and simple (5 lines!)
- Matches the recursive structure of trees

Iterative works but adds complexity without benefit.

Decision: Recursive DFS is the NATURAL solution! ✓

🎭 FINAL NOTE:
-------------
This is one of the MOST FAMOUS interview questions!
Why? Because:
1. It's simple but easy to mess up under pressure
2. Tests understanding of recursion and trees
3. Has an interesting backstory (Max Howell)
4. Appears frequently in interviews

Master this problem - it's a classic! 🌟
"""
