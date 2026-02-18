"""
LeetCode Problem #101: Symmetric Tree

Difficulty: Easy
Topics: Tree, DFS, BFS, Recursion, Mirror Tree
Companies: Amazon, Microsoft, Facebook, Bloomberg, Google, LinkedIn

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
│ ANALOGY          │ "Butterfly Wings" - Perfect mirror across center!       │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ PATTERN          │ "Mirror Comparison" - Left.left ↔ Right.right          │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ BASE CASES       │ Both None → TRUE | One None → FALSE | Diff val → FALSE │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ DEFAULT SOLUTION │ Recursive DFS (Use in 90% of cases!)                   │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ TIME COMPLEXITY  │ O(N) - Visit every node once                           │
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
│ Want simplest code             │ ✅ Solution 1 (Clean recursion)           │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Level-by-level check           │ ⚠️  Solution 2 (Iterative BFS)            │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Avoid stack overflow           │ ⚠️  Solution 2 (Iterative)                │
└────────────────────────────────┴────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     📊 SOLUTION COMPARISON TABLE                            │
├──────────────────┬─────────────────────────┬────────────────────────────────┤
│ CRITERIA         │ SOLUTION 1 (Recursive)  │ SOLUTION 2 (Iterative BFS)    │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Code Length      │ ⭐⭐⭐⭐⭐ Short & clean  │ ⭐⭐⭐ More code                │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Readability      │ ⭐⭐⭐⭐⭐ Very clear     │ ⭐⭐⭐ More complex             │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Interview Speed  │ ⭐⭐⭐⭐⭐ Super fast     │ ⭐⭐⭐ Takes longer             │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Stack Safety     │ ⭐⭐⭐ Risk overflow     │ ⭐⭐⭐⭐⭐ No stack issues       │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Intuitive        │ ⭐⭐⭐⭐⭐ Natural        │ ⭐⭐⭐ Less natural             │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ When to Use      │ 90% of cases (DEFAULT)  │ Very deep trees only          │
└──────────────────┴─────────────────────────┴────────────────────────────────┘

⏱️  TIME TO MASTER: 20-25 minutes
🎯 DIFFICULTY: Easy
💡 TIP: Remember "Butterfly Wings" - compare opposite positions!

================================================================================
                           🎯 PROBLEM UNDERSTANDING
================================================================================

WHAT IS THE PROBLEM?
--------------------
You're given a BINARY TREE and need to check if it's a MIRROR of itself!

Think of it like: If you put a MIRROR down the middle, does the left side
reflect perfectly to the right side?

REAL WORLD ANALOGY:
------------------
Think of a BUTTERFLY! 🦋

Left Wing:        Body:        Right Wing:
   A                |                A
  / \               |               / \
 B   C              |              C   B

The wings are MIRROR IMAGES of each other!
- Left wing has B then C
- Right wing has C then B (reversed!)

Another analogy: FACE in a MIRROR 🪞
- Your left eye = Mirror's right eye
- Your right eye = Mirror's right eye
- Everything is FLIPPED!

================================================================================
                            📝 FORMAL PROBLEM
================================================================================

Given the root of a binary tree, check whether it is a mirror of itself
(i.e., symmetric around its center).

Example 1:
----------
Input: root = [1,2,2,3,4,4,3]

        1
       / \
      2   2
     / \ / \
    3  4 4  3

Output: true

Explanation:
- Left subtree:  2 with children 3, 4
- Right subtree: 2 with children 4, 3 (mirrored!)
- Perfect mirror! ✓

Example 2:
----------
Input: root = [1,2,2,null,3,null,3]

        1
       / \
      2   2
       \   \
        3   3

Output: false

Explanation:
- Left subtree:  2 with right child 3
- Right subtree: 2 with right child 3
- NOT mirrored! Both children on same side ✗

Example 3:
----------
Input: root = [1]

        1

Output: true
Explanation: Single node is symmetric!

Constraints:
------------
* The number of nodes in the tree is in the range [1, 1000]
* -100 <= Node.val <= 100

================================================================================
                         🧠 KEY INSIGHTS TO REMEMBER
================================================================================

THE MAIN CHALLENGE:
------------------
❌ Can't just compare left and right subtrees directly
❌ Need to compare them in MIRROR fashion!
✅ Left's left = Right's right
✅ Left's right = Right's left

THE MAGIC TRICK: "Mirror Comparison"
------------------------------------
For a tree to be symmetric:

        Root
        /  \
       L    R

1. L.val must equal R.val
2. L's LEFT child must mirror R's RIGHT child
3. L's RIGHT child must mirror R's LEFT child

Think: "OUTER matches OUTER, INNER matches INNER"

Visual:
        1
       / \
      2   2         ← These must be equal
     / \ / \
    3  4 4  3       ← Outer: 3==3, Inner: 4==4

    Outer pair: (3, 3) ✓
    Inner pair: (4, 4) ✓

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

def isSymmetric(root):
    """
    🎯 APPROACH 1: Recursive Mirror Comparison (RECOMMENDED!)

    TIME COMPLEXITY: O(n) - Visit each node once
    SPACE COMPLEXITY: O(h) - Recursion stack (h = height)
                      Worst case O(n) for skewed tree

    🧠 MEMORIZATION TRICK: "Mirror Dance" 💃🕺
    -----------------------------------------
    Think of two dancers mirroring each other:
    - When left dancer raises LEFT hand → right dancer raises RIGHT hand
    - When left dancer steps RIGHT → right dancer steps LEFT
    - Perfect synchronization but MIRRORED!

    Mantra: "Outer with Outer, Inner with Inner"

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Start with root's left and right children
    2. Create helper function isMirror(left, right):
       a. Both null? → Symmetric! ✓
       b. One null? → Not symmetric! ✗
       c. Values different? → Not symmetric! ✗
       d. Recursively check:
          - left.left with right.right (outer pair)
          - left.right with right.left (inner pair)
    3. Both pairs must be symmetric!

    Why this works:
    - Compares nodes in mirror positions
    - Recursion naturally handles all levels
    - Base cases handle null nodes
    """
    def isMirror(left, right):
        # Base case 1: Both are null → symmetric
        if not left and not right:
            return True

        # Base case 2: One is null, other isn't → not symmetric
        if not left or not right:
            return False

        # Base case 3: Values are different → not symmetric
        if left.val != right.val:
            return False

        # Recursive case: Check mirror pairs
        # Outer pair: left.left with right.right
        # Inner pair: left.right with right.left
        return (isMirror(left.left, right.right) and
                isMirror(left.right, right.left))

    # Edge case: empty tree is symmetric
    if not root:
        return True

    # Check if left and right subtrees are mirrors
    return isMirror(root.left, root.right)


# ============================================================================
#              APPROACH 2: Iterative BFS with Queue
# ============================================================================

def isSymmetric_BFS(root):
    """
    🎯 APPROACH 2: Iterative BFS with Queue

    TIME COMPLEXITY: O(n)
    SPACE COMPLEXITY: O(w) - Queue holds max width

    🧠 MEMORIZATION TRICK: "Parallel Queue Processing"
    -------------------------------------------------
    Think: Two lines of people walking towards each other
    - Must match person by person
    - First person in left line = First person in right line
    - But they're walking in OPPOSITE directions!

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Create queue with root's left and right children
    2. While queue not empty:
       a. Pop two nodes (left, right)
       b. Both null? → Continue
       c. One null? → Return False
       d. Values different? → Return False
       e. Add mirror pairs to queue:
          - left.left, right.right (outer)
          - left.right, right.left (inner)
    3. If loop completes → Symmetric!
    """
    if not root:
        return True

    # Initialize queue with left and right subtrees
    queue = deque([(root.left, root.right)])

    while queue:
        left, right = queue.popleft()

        # Both null → continue checking other pairs
        if not left and not right:
            continue

        # One is null or values differ → not symmetric
        if not left or not right or left.val != right.val:
            return False

        # Add mirror pairs to queue
        queue.append((left.left, right.right))   # Outer pair
        queue.append((left.right, right.left))   # Inner pair

    return True


# ============================================================================
#              APPROACH 3: Iterative with Two Stacks
# ============================================================================

def isSymmetric_Stack(root):
    """
    🎯 APPROACH 3: Two Stacks for Mirror Traversal

    TIME COMPLEXITY: O(n)
    SPACE COMPLEXITY: O(h)

    🧠 MEMORIZATION TRICK: "Two Mirrors Facing Each Other"
    ----------------------------------------------------
    Think of two stacks as two mirrors:
    - Left stack processes left-to-right
    - Right stack processes right-to-left
    - They must see the same reflections!

    Similar to Approach 2 but uses stacks instead of queue.
    """
    if not root:
        return True

    stack = [(root.left, root.right)]

    while stack:
        left, right = stack.pop()

        if not left and not right:
            continue

        if not left or not right or left.val != right.val:
            return False

        # Add pairs in specific order
        stack.append((left.left, right.right))
        stack.append((left.right, right.left))

    return True


# ============================================================================
#                    🎨 VISUAL WALKTHROUGH EXAMPLE
# ============================================================================

"""
Let's walk through Example 1 step-by-step:

Tree:
        1
       / \\
      2   2
     / \\ / \\
    3  4 4  3

APPROACH 1: Recursive DFS
-------------------------

CALL 1: isMirror(left=2, right=2)
--------------------------------------
left = 2, right = 2
- Both exist? YES ✓
- Values equal? 2 == 2? YES ✓
- Need to check:
  1. isMirror(left.left=3, right.right=3)  ← Outer pair
  2. isMirror(left.right=4, right.left=4)  ← Inner pair

CALL 2: isMirror(left=3, right=3)  [Outer pair]
------------------------------------------------
left = 3, right = 3
- Both exist? YES ✓
- Values equal? 3 == 3? YES ✓
- Need to check:
  1. isMirror(left.left=null, right.right=null)
  2. isMirror(left.right=null, right.left=null)

CALL 3: isMirror(left=null, right=null)
----------------------------------------
- Both null? YES ✓
- Return True

CALL 4: isMirror(left=null, right=null)
----------------------------------------
- Both null? YES ✓
- Return True

Back to CALL 2: Both recursive calls returned True
Return: True ✓

CALL 5: isMirror(left=4, right=4)  [Inner pair]
------------------------------------------------
left = 4, right = 4
- Both exist? YES ✓
- Values equal? 4 == 4? YES ✓
- Need to check:
  1. isMirror(left.left=null, right.right=null)
  2. isMirror(left.right=null, right.left=null)

CALL 6 & 7: Both return True (both null)

Back to CALL 5: Return True ✓

Back to CALL 1:
- Outer pair (3,3): True ✓
- Inner pair (4,4): True ✓
- Return: True AND True = True ✓

FINAL RESULT: True ✓


APPROACH 2: BFS with Queue
--------------------------

INITIALIZATION:
queue = [(2, 2)]  ← Left and right children of root

ITERATION 1:
------------
Pop: (left=2, right=2)
- Both exist? YES ✓
- Values equal? 2 == 2? YES ✓
- Add mirror pairs:
  queue.append((3, 3))  ← Outer: left.left, right.right
  queue.append((4, 4))  ← Inner: left.right, right.left

queue = [(3, 3), (4, 4)]

ITERATION 2:
------------
Pop: (left=3, right=3)
- Both exist? YES ✓
- Values equal? 3 == 3? YES ✓
- Add mirror pairs:
  queue.append((null, null))  ← left.left, right.right
  queue.append((null, null))  ← left.right, right.left

queue = [(4, 4), (null, null), (null, null)]

ITERATION 3:
------------
Pop: (left=4, right=4)
- Both exist? YES ✓
- Values equal? 4 == 4? YES ✓
- Add mirror pairs:
  queue.append((null, null))
  queue.append((null, null))

queue = [(null, null), (null, null), (null, null), (null, null)]

ITERATION 4-7:
--------------
Pop: (null, null)
- Both null? YES → Continue

queue = []  ← Empty!

Exit loop → Return True ✓


Example 2 (NOT Symmetric):
---------------------------
Tree:
        1
       / \\
      2   2
       \\   \\
        3   3

CALL: isMirror(left=2, right=2)
- Values equal? 2 == 2? YES ✓
- Check outer: isMirror(left.left=null, right.right=3)

  left = null, right = 3
  - One is null? YES ✗
  - Return False ✗

FINAL RESULT: False ✗
"""

# ============================================================================
#              🎯 MEMORY TRICKS & COMMON MISTAKES
# ============================================================================

"""
🧠 HOW TO REMEMBER THIS SOLUTION:
---------------------------------
Analogy: "HANDSHAKE PROTOCOL" 🤝

Imagine two people greeting each other:
- They extend OPPOSITE hands (left hand meets right hand)
- Their OUTER shoulders align with outer shoulders
- Their INNER shoulders align with inner shoulders
- Perfect mirror image!

In tree terms:
        Root
        /  \\
       L    R
      /\\   /\\
     a  b  c  d

For symmetry:
- L and R must be equal ✓
- a (L's left) must equal d (R's right) ← Outer pair
- b (L's right) must equal c (R's left) ← Inner pair

Mantra: "Cross-Compare, Not Direct-Compare"

Visual Memory Aid:
-----------------
     LEFT          RIGHT
       2      =      2      ✓ Values match
      / \\          / \\
     3   4        4   3    ✓ Mirror positions

     Compare: (3 ↔ 3) and (4 ↔ 4)
     NOT:     (3 ↔ 4) and (4 ↔ 3)

❌ COMMON MISTAKES TO AVOID:
----------------------------
1. ❌ Comparing left.left with right.left (same side!)
   ```python
   # WRONG:
   return isMirror(left.left, right.left)  # Both left side!

   # CORRECT:
   return isMirror(left.left, right.right)  # Mirror sides!
   ```

2. ❌ Forgetting to check both pairs
   ```python
   # WRONG (incomplete):
   return isMirror(left.left, right.right)  # Only checks outer!

   # CORRECT:
   return (isMirror(left.left, right.right) and
           isMirror(left.right, right.left))  # Checks both!
   ```

3. ❌ Not handling null cases properly
   ```python
   # WRONG:
   if not left or not right:
       return True  # What if only one is null?

   # CORRECT:
   if not left and not right:
       return True  # Both null
   if not left or not right:
       return False  # Only one null
   ```

4. ❌ Comparing root with itself
   ```python
   # WRONG:
   return isMirror(root, root)  # Always returns true!

   # CORRECT:
   return isMirror(root.left, root.right)  # Compare subtrees!
   ```

5. ❌ Wrong order in queue/stack
   ```python
   # CONFUSING (works but hard to read):
   queue.append((left.right, right.left))
   queue.append((left.left, right.right))

   # BETTER (clear outer then inner):
   queue.append((left.left, right.right))   # Outer first
   queue.append((left.right, right.left))   # Inner second
   ```

✅ PRO TIPS:
-----------
1. Draw the tree and mark mirror pairs with arrows
2. Always check both null cases separately
3. Recursive solution is most intuitive for interviews
4. BFS solution shows you understand iterative approaches
5. Test with: single node, two nodes, all same values

🔧 DEBUGGING CHECKLIST:
-----------------------
If your solution doesn't work:
□ Are you comparing mirror positions (not same positions)?
□ Did you handle both-null case?
□ Did you handle one-null case?
□ Are you checking both outer AND inner pairs?
□ Did you return the AND of both recursive calls?
"""

# ============================================================================
#                         🧪 TEST CASES
# ============================================================================

def test_isSymmetric():
    """Run comprehensive test cases"""

    print("="*70)
    print("              SYMMETRIC TREE - TEST CASES")
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

    # Test Case 1: Symmetric tree
    print("\n📝 Test Case 1: Symmetric tree [1,2,2,3,4,4,3]")
    print("-" * 70)
    print("Tree:")
    print("        1")
    print("       / \\")
    print("      2   2")
    print("     / \\ / \\")
    print("    3  4 4  3")

    root1 = build_tree([1, 2, 2, 3, 4, 4, 3])
    result1_recursive = isSymmetric(root1)
    result1_bfs = isSymmetric_BFS(root1)
    result1_stack = isSymmetric_Stack(root1)
    expected1 = True

    print(f"\nRecursive: {result1_recursive}")
    print(f"BFS:       {result1_bfs}")
    print(f"Stack:     {result1_stack}")
    print(f"Expected:  {expected1}")
    print(f"Explanation: Perfect mirror - outer (3,3) and inner (4,4)")
    print(f"✓ PASS" if result1_recursive == expected1 else f"✗ FAIL")

    # Test Case 2: Not symmetric
    print("\n📝 Test Case 2: Not symmetric [1,2,2,null,3,null,3]")
    print("-" * 70)
    print("Tree:")
    print("        1")
    print("       / \\")
    print("      2   2")
    print("       \\   \\")
    print("        3   3")

    root2 = build_tree([1, 2, 2, None, 3, None, 3])
    result2 = isSymmetric(root2)
    expected2 = False

    print(f"\nResult:   {result2}")
    print(f"Expected: {expected2}")
    print(f"Explanation: Both 3's on right side, not mirrored!")
    print(f"✓ PASS" if result2 == expected2 else f"✗ FAIL")

    # Test Case 3: Single node
    print("\n📝 Test Case 3: Single node [1]")
    print("-" * 70)
    print("Tree:")
    print("    1")

    root3 = build_tree([1])
    result3 = isSymmetric(root3)
    expected3 = True

    print(f"\nResult:   {result3}")
    print(f"Expected: {expected3}")
    print(f"Explanation: Single node is symmetric by definition")
    print(f"✓ PASS" if result3 == expected3 else f"✗ FAIL")

    # Test Case 4: Two nodes symmetric
    print("\n📝 Test Case 4: Two nodes [1,2,2]")
    print("-" * 70)
    print("Tree:")
    print("    1")
    print("   / \\")
    print("  2   2")

    root4 = build_tree([1, 2, 2])
    result4 = isSymmetric(root4)
    expected4 = True

    print(f"\nResult:   {result4}")
    print(f"Expected: {expected4}")
    print(f"✓ PASS" if result4 == expected4 else f"✗ FAIL")

    # Test Case 5: Two nodes not symmetric
    print("\n📝 Test Case 5: Not symmetric [1,2,3]")
    print("-" * 70)
    print("Tree:")
    print("    1")
    print("   / \\")
    print("  2   3")

    root5 = build_tree([1, 2, 3])
    result5 = isSymmetric(root5)
    expected5 = False

    print(f"\nResult:   {result5}")
    print(f"Expected: {expected5}")
    print(f"Explanation: 2 != 3")
    print(f"✓ PASS" if result5 == expected5 else f"✗ FAIL")

    # Test Case 6: All same values but not symmetric
    print("\n📝 Test Case 6: All 1's but not symmetric [1,1,1,1,null,1]")
    print("-" * 70)
    print("Tree:")
    print("      1")
    print("     / \\")
    print("    1   1")
    print("   /     \\")
    print("  1       1")

    root6 = build_tree([1, 1, 1, 1, None, None, 1])
    result6 = isSymmetric(root6)
    expected6 = False

    print(f"\nResult:   {result6}")
    print(f"Expected: {expected6}")
    print(f"Explanation: Structure not mirrored (left has left child, right has right child)")
    print(f"✓ PASS" if result6 == expected6 else f"✗ FAIL")

    # Test Case 7: Deep symmetric tree
    print("\n📝 Test Case 7: Deep symmetric tree")
    print("-" * 70)
    print("Tree:")
    print("        1")
    print("       / \\")
    print("      2   2")
    print("     /\\   /\\")
    print("    3  4 4  3")
    print("   /\\     /\\")
    print("  5  6   6  5")

    root7 = build_tree([1, 2, 2, 3, 4, 4, 3, 5, 6, None, None, None, None, 6, 5])
    result7 = isSymmetric(root7)
    expected7 = True

    print(f"\nResult:   {result7}")
    print(f"Expected: {expected7}")
    print(f"✓ PASS" if result7 == expected7 else f"✗ FAIL")

    # Test Case 8: Empty tree
    print("\n📝 Test Case 8: Empty tree []")
    print("-" * 70)
    print("Tree: (empty)")

    root8 = build_tree([])
    result8 = isSymmetric(root8)
    expected8 = True

    print(f"\nResult:   {result8}")
    print(f"Expected: {expected8}")
    print(f"Explanation: Empty tree is symmetric")
    print(f"✓ PASS" if result8 == expected8 else f"✗ FAIL")

    print("\n" + "="*70)
    print("              ✅ ALL TEST CASES COMPLETED!")
    print("="*70)


if __name__ == "__main__":
    test_isSymmetric()


# ============================================================================
#              🎓 LEARNING SUMMARY & KEY TAKEAWAYS
# ============================================================================

"""
🎯 WHAT YOU LEARNED:
-------------------
1. Symmetric tree = Mirror comparison, not direct comparison
2. Compare OPPOSITE positions: left.left ↔ right.right
3. Must check BOTH outer pair AND inner pair
4. Handle null cases carefully (both null vs one null)
5. Recursive solution is most intuitive

🔑 KEY PATTERN: "Mirror Recursion"
----------------------------------
This pattern applies to:
- Symmetric Tree (this problem)
- Same Tree (direct comparison instead of mirror)
- Invert Binary Tree (swap instead of compare)
- Merge Two Binary Trees

The Template:
-------------
```python
def isMirror(left, right):
    # Both null → True
    if not left and not right:
        return True

    # One null → False
    if not left or not right:
        return False

    # Values differ → False
    if left.val != right.val:
        return False

    # Check mirror pairs
    return (isMirror(left.left, right.right) and    # Outer
            isMirror(left.right, right.left))        # Inner
```

💪 SIMILAR PROBLEMS TO PRACTICE:
-------------------------------
1. LeetCode #100: Same Tree (direct comparison)
2. LeetCode #226: Invert Binary Tree (swap children)
3. LeetCode #617: Merge Two Binary Trees
4. LeetCode #572: Subtree of Another Tree
5. LeetCode #951: Flip Equivalent Binary Trees

🎉 CONGRATULATIONS!
------------------
You now master the Mirror Comparison pattern!

Remember the KEY INSIGHTS:
1. "Outer with Outer, Inner with Inner"
2. "Cross-Compare, Not Direct-Compare"
3. "Both null OK, One null NOT OK"

Key Differences from Similar Problems:
- Level Order: Process layer by layer with BFS
- Validate BST: Track valid range constraints
- Symmetric Tree: Mirror comparison (opposite sides)
- Same Tree: Direct comparison (same sides)

🎓 INTERVIEW TIPS:
-----------------
1. Draw the tree and mark mirror pairs with arrows
2. Explain the "opposite sides" concept clearly
3. Walk through null cases (both null, one null)
4. Mention time/space complexity
5. Recursive is more intuitive than iterative

Explanation Template:
--------------------
"For a tree to be symmetric, we need to compare it like a mirror. The left
subtree's left child should match the right subtree's right child (outer pair),
and the left subtree's right child should match the right subtree's left child
(inner pair). I'll use recursion to check these mirror pairs. Base cases handle
when both nodes are null (symmetric), one node is null (not symmetric), or
values differ (not symmetric)."

🧠 WHY RECURSIVE IS NATURAL HERE:
---------------------------------
Unlike level order (where BFS is obvious), symmetric tree is NATURALLY recursive:
- Need to compare TWO nodes simultaneously
- Need to traverse in MIRROR fashion
- Recursion handles "compare and recurse" elegantly

BFS works but is less intuitive (need to manage pairs in queue).

Decision: Recursive DFS is the NATURAL solution! ✓
"""
