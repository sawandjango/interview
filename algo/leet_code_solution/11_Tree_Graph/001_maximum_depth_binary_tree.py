"""
LeetCode Problem #104: Maximum Depth of Binary Tree

Difficulty: Easy
Topics: Tree, DFS, BFS, Recursion, Tree Height
Companies: Amazon, Microsoft, Facebook, Google, Apple, LinkedIn, Adobe

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
│ ANALOGY          │ "Building Height" - Count floors from top to bottom!    │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ PATTERN          │ "1 + Max(Left, Right)" - Current + Deeper child        │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ BASE CASE        │ If None → Return 0 (no height)                         │
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
│ Want simplest code             │ ✅ Solution 1 (Just 2 lines!)             │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Need to count levels           │ ⚠️  Solution 2 (Explicit level counting)  │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Avoid recursion                │ ⚠️  Solution 2 (Iterative)                │
└────────────────────────────────┴────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     📊 SOLUTION COMPARISON TABLE                            │
├──────────────────┬─────────────────────────┬────────────────────────────────┤
│ CRITERIA         │ SOLUTION 1 (Recursive)  │ SOLUTION 2 (Iterative BFS)    │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Code Length      │ ⭐⭐⭐⭐⭐ 2 lines!       │ ⭐⭐⭐ 10+ lines                │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Readability      │ ⭐⭐⭐⭐⭐ Crystal clear  │ ⭐⭐⭐ More complex             │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Interview Speed  │ ⭐⭐⭐⭐⭐ Lightning fast │ ⭐⭐⭐ Takes longer             │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Stack Safety     │ ⭐⭐⭐ Risk overflow     │ ⭐⭐⭐⭐⭐ No stack issues       │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Intuitive        │ ⭐⭐⭐⭐⭐ Very natural   │ ⭐⭐⭐⭐ Also intuitive         │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ When to Use      │ 95% of cases (DEFAULT)  │ Very deep trees only          │
└──────────────────┴─────────────────────────┴────────────────────────────────┘

⏱️  TIME TO MASTER: 10-15 minutes
🎯 DIFFICULTY: Easy (Perfect for beginners!)
💡 TIP: This is THE SIMPLEST tree problem - great place to start!
🔥 POPULAR: One of the most common tree interview questions!

================================================================================
                           🎯 PROBLEM UNDERSTANDING
================================================================================

WHAT IS THE PROBLEM?
--------------------
You're given a BINARY TREE and need to find its MAXIMUM DEPTH (height)!

The depth = number of nodes along the LONGEST path from root to leaf.

REAL WORLD ANALOGY:
------------------
Think of a BUILDING! 🏢

        [10th Floor]  ← Penthouse (deepest leaf)
            |
        [9th Floor]
            |
        [8th Floor]
            |
          ...
            |
        [2nd Floor]
            |
        [1st Floor]
            |
        [Ground]      ← Root

Maximum Depth = 10 floors!

Another analogy: FAMILY TREE 👨‍👩‍👧‍👦
- You (root) = generation 1
- Your children = generation 2
- Your grandchildren = generation 3
- Your great-grandchildren = generation 4

Maximum depth = How many generations down?

Or think of: FOLDER DEPTH 📁
```
Root/
  ├─ Folder1/
  │   ├─ Folder2/
  │   │   └─ Folder3/
  │   │       └─ File.txt  ← Depth = 4
  │   └─ File2.txt         ← Depth = 3
  └─ File3.txt             ← Depth = 2
```

Maximum depth = 4 (longest path from root to any file)

================================================================================
                            📝 FORMAL PROBLEM
================================================================================

Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path
from the root node down to the farthest leaf node.

Example 1:
----------
Input: root = [3,9,20,null,null,15,7]

        3         ← Level 1 (depth 1)
       / \\
      9   20      ← Level 2 (depth 2)
         /  \\
        15   7    ← Level 3 (depth 3)

Output: 3
Explanation: The longest path is 3 → 20 → 15 (or 3 → 20 → 7), depth = 3

Example 2:
----------
Input: root = [1,null,2]

        1         ← Level 1
         \\
          2       ← Level 2

Output: 2

Example 3:
----------
Input: root = []

Output: 0
Explanation: Empty tree has depth 0

Example 4:
----------
Input: root = [1]

        1         ← Single node

Output: 1

Constraints:
------------
* The number of nodes in the tree is in the range [0, 10^4]
* -100 <= Node.val <= 100

================================================================================
                         🧠 KEY INSIGHTS TO REMEMBER
================================================================================

THE MAIN CHALLENGE:
------------------
❌ Not counting just one path
❌ Not stopping at first leaf
✅ Must find the LONGEST path from root to ANY leaf!

KEY INSIGHT #1: Recursive Definition
-------------------------------------
The depth of a tree is:
- 0 if tree is empty (None)
- 1 + maximum depth of its subtrees (left or right)

Think: "I'm at height 1, plus the taller of my children!"

Visual:
       ROOT (depth = ?)
       /   \\
    Left   Right
   (d=2)   (d=3)    ← Left depth = 2, Right depth = 3

   ROOT depth = 1 + max(2, 3) = 4

KEY INSIGHT #2: Base Case
--------------------------
Empty tree (None) → depth = 0

This is the "ground floor" - no more levels to count!

KEY INSIGHT #3: Pattern - Post-order Traversal
-----------------------------------------------
We need children's depths BEFORE we can calculate parent's depth!

Order:
1. Calculate left subtree depth
2. Calculate right subtree depth
3. Calculate current node depth = 1 + max(left, right)

This is POST-ORDER: Left → Right → Root

KEY INSIGHT #4: Choose the Deeper Child
----------------------------------------
At each node, we care about the DEEPER child, not both!

        5
       / \\
      2   8
     /
    1

Left depth = 2 (path: 5→2→1)
Right depth = 1 (path: 5→8)
Answer = 1 + max(2, 1) = 3

We take the longer path!

================================================================================
                    🚀 HOW TO APPROACH THIS PROBLEM
================================================================================

STEP-BY-STEP THINKING PROCESS:
------------------------------

When you see this problem, ask yourself these questions:

Q1: "What am I measuring?"
A: The longest path from root to leaf (depth/height)

Q2: "What defines depth?"
A: Number of nodes from root to farthest leaf

Q3: "How do I find the longest path?"
A: At each node, pick the deeper of left/right subtrees

Q4: "What's my base case?"
A: Empty tree (None) has depth 0

Q5: "Which approach feels natural?"
A: Recursion! Depth is defined recursively

DECISION TREE FOR CHOOSING SOLUTION:
------------------------------------

START HERE:
│
├─ "Do I understand recursion?"
│  │
│  ├─ YES → Use SOLUTION 1 (Recursive DFS) ✅ RECOMMENDED
│  │        • Most intuitive
│  │        • Just 2 lines of code!
│  │        • Perfect for interviews
│  │
│  └─ NO → Use SOLUTION 2 (Iterative BFS)
│           • Count levels explicitly
│           • No recursion needed
│           • Good for learning

Follow-up consideration:
│
└─ "Is tree very deep (height > 1000)?"
   │
   ├─ YES → Use SOLUTION 2 (Iterative) to avoid stack overflow
   │
   └─ NO → Use SOLUTION 1 (Recursive) - cleaner code

EASY WAY TO REMEMBER WHICH SOLUTION TO USE:
-------------------------------------------

🎯 DEFAULT CHOICE: Solution 1 (Recursive)
   ✓ Use this in 95% of cases
   ✓ Shortest possible code (2 lines!)
   ✓ Perfect for interviews

⚠️  SPECIAL CASES: Solution 2 (Iterative)
   ✓ Very deep trees (avoid stack overflow)
   ✓ Need explicit level counting
   ✓ Want to avoid recursion

================================================================================
                         💡 SOLUTION APPROACHES
================================================================================

APPROACH 1: RECURSIVE DFS (⭐ RECOMMENDED - Use this first!)
------------------------------------------------------------

WHY CHOOSE THIS SOLUTION?
--------------------------
✅ PROS:
   • Shortest code - ONLY 2 lines!
   • Most intuitive - mirrors problem definition
   • Natural for trees - depth is recursive by nature
   • Fast to write - fewer bugs
   • Easy to explain in interviews
   • Elegant and beautiful

❌ CONS:
   • Uses call stack (O(H) space)
   • Stack overflow risk for very deep trees (rare)
   • Need to understand recursion

WHEN TO USE:
   → Default choice for this problem
   → Normal interviews (trees < 1000 depth)
   → When you want clean, short code
   → When comfortable with recursion

INTUITION:
----------
"The depth of a tree is 1 (current node) plus the deeper of its children!"

It's like asking: "How tall is this building?"
Answer: "1 floor (me) + height of taller wing!"

ALGORITHM:
----------
1. Base Case: If node is None → return 0
2. Recursive Case:
   - Get left subtree depth
   - Get right subtree depth
   - Return 1 + max(left, right)

MEMORY TRICK: "1 + Max"
-----------------------
Depth = 1 + max(left_depth, right_depth)

That's it! Just remember "1 + Max"!

Visual Walkthrough - Example 1:
--------------------------------
        3
       / \\
      9   20
         /  \\
        15   7

Step-by-step execution:

Call 1: maxDepth(3)
├─ Get left: maxDepth(9)
│  ├─ Get left: maxDepth(None) → 0
│  ├─ Get right: maxDepth(None) → 0
│  └─ Return 1 + max(0, 0) = 1 ✓
│
├─ Get right: maxDepth(20)
│  ├─ Get left: maxDepth(15)
│  │  ├─ maxDepth(None) → 0
│  │  ├─ maxDepth(None) → 0
│  │  └─ Return 1 + max(0, 0) = 1 ✓
│  │
│  ├─ Get right: maxDepth(7)
│  │  ├─ maxDepth(None) → 0
│  │  ├─ maxDepth(None) → 0
│  │  └─ Return 1 + max(0, 0) = 1 ✓
│  │
│  └─ Return 1 + max(1, 1) = 2 ✓
│
└─ Final: 1 + max(1, 2) = 3 ✓

Answer: 3 (correct!)

APPROACH 2: ITERATIVE BFS (Alternative Solution)
-------------------------------------------------

WHY CHOOSE THIS SOLUTION?
--------------------------
✅ PROS:
   • No recursion - avoids stack overflow
   • Explicit level counting - easy to understand
   • Level-by-level processing - intuitive
   • No call stack overhead
   • Works for extremely deep trees

❌ CONS:
   • More code - need to manage queue
   • Less intuitive - doesn't mirror problem structure
   • Takes longer to write
   • More complex to explain

WHEN TO USE:
   → Trees are extremely deep (height > 1000)
   → Interviewer asks for iterative solution
   → Want to avoid recursion
   → Need to explicitly process levels

INTUITION:
----------
"Count how many floors the building has by visiting each floor!"

Process tree level by level, increment depth counter for each level.

COMPARISON: When to pick which?
-------------------------------

Scenario 1: "Normal coding interview"
   → Use SOLUTION 1 (Recursive) ✅
   Why: Cleaner, faster to write, easier to explain

Scenario 2: "Very deep tree (height 10,000)"
   → Use SOLUTION 2 (Iterative) ✅
   Why: Avoid stack overflow

Scenario 3: "Want to impress?"
   → Write SOLUTION 1 first, then mention SOLUTION 2 exists
   Why: Shows you know optimal solution AND alternatives

================================================================================
                            💻 IMPLEMENTATION
================================================================================
"""

# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


"""
================================================================================
SOLUTION 1: RECURSIVE DFS (⭐ RECOMMENDED)
================================================================================
"""

def maxDepth(root: TreeNode) -> int:
    """
    Find maximum depth of binary tree using recursion.

    Time Complexity: O(N) where N = number of nodes
                     We visit every node exactly once
    Space Complexity: O(H) where H = height of tree
                      Recursion stack depth

    Args:
        root: Root of binary tree

    Returns:
        Maximum depth (number of nodes in longest path from root to leaf)
    """
    # BASE CASE: Empty tree has depth 0
    if not root:
        return 0

    # RECURSIVE CASE: 1 (current) + deeper child
    # Get depth of left subtree
    left_depth = maxDepth(root.left)

    # Get depth of right subtree
    right_depth = maxDepth(root.right)

    # Return 1 (current node) + max of children
    return 1 + max(left_depth, right_depth)


# ULTRA-CLEAN ONE-LINER VERSION (same logic):
def maxDepth_oneliner(root: TreeNode) -> int:
    """
    Most concise version - same logic but condensed.
    """
    return 0 if not root else 1 + max(maxDepth(root.left), maxDepth(root.right))


"""
================================================================================
SOLUTION 2: ITERATIVE BFS (Using Queue)
================================================================================
"""

from collections import deque

def maxDepth_iterative(root: TreeNode) -> int:
    """
    Find maximum depth using iterative BFS (level-order traversal).

    Time Complexity: O(N)
    Space Complexity: O(W) where W = maximum width of tree

    Think: Count levels by processing tree floor by floor!
    """
    # Edge case: empty tree
    if not root:
        return 0

    # BFS: Use queue to process level by level
    queue = deque([root])
    depth = 0

    while queue:
        # Process entire current level
        level_size = len(queue)  # Snapshot of current level

        # Process all nodes in this level
        for _ in range(level_size):
            node = queue.popleft()

            # Add children to queue (next level)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        # Finished one level → increment depth
        depth += 1

    return depth


"""
================================================================================
                            🧪 TEST CASES
================================================================================
"""

def build_tree_from_list(arr):
    """Helper function to build tree from level-order array"""
    if not arr:
        return None

    root = TreeNode(arr[0])
    queue = deque([root])
    i = 1

    while queue and i < len(arr):
        node = queue.popleft()

        # Left child
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1

        # Right child
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            queue.append(node.right)
        i += 1

    return root


def test_maximum_depth():
    """Comprehensive test cases"""

    print("Testing Maximum Depth Solutions...")
    print("=" * 60)

    # Test Case 1: Example from problem
    print("\\n✅ Test 1: [3,9,20,null,null,15,7]")
    tree1 = build_tree_from_list([3, 9, 20, None, None, 15, 7])
    result1 = maxDepth(tree1)
    print(f"Expected: 3")
    print(f"Got: {result1}")
    assert result1 == 3, "Test 1 Failed!"

    # Test Case 2: Skewed tree (right)
    print("\\n✅ Test 2: [1,null,2]")
    tree2 = build_tree_from_list([1, None, 2])
    result2 = maxDepth(tree2)
    print(f"Expected: 2")
    print(f"Got: {result2}")
    assert result2 == 2, "Test 2 Failed!"

    # Test Case 3: Empty tree
    print("\\n✅ Test 3: []")
    tree3 = None
    result3 = maxDepth(tree3)
    print(f"Expected: 0")
    print(f"Got: {result3}")
    assert result3 == 0, "Test 3 Failed!"

    # Test Case 4: Single node
    print("\\n✅ Test 4: [1]")
    tree4 = TreeNode(1)
    result4 = maxDepth(tree4)
    print(f"Expected: 1")
    print(f"Got: {result4}")
    assert result4 == 1, "Test 4 Failed!"

    # Test Case 5: Balanced tree
    print("\\n✅ Test 5: [1,2,3,4,5,6,7]")
    tree5 = build_tree_from_list([1, 2, 3, 4, 5, 6, 7])
    result5 = maxDepth(tree5)
    print(f"Expected: 3")
    print(f"Got: {result5}")
    assert result5 == 3, "Test 5 Failed!"

    # Test Case 6: Skewed tree (left)
    print("\\n✅ Test 6: Left-skewed [1,2,null,3]")
    tree6 = build_tree_from_list([1, 2, None, 3])
    result6 = maxDepth(tree6)
    print(f"Expected: 3")
    print(f"Got: {result6}")
    assert result6 == 3, "Test 6 Failed!"

    # Test Case 7: Larger tree
    print("\\n✅ Test 7: Larger balanced tree")
    tree7 = build_tree_from_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    result7 = maxDepth(tree7)
    print(f"Expected: 4")
    print(f"Got: {result7}")
    assert result7 == 4, "Test 7 Failed!"

    # Test iterative solution
    print("\\n🔄 Testing iterative solution...")
    result1_iter = maxDepth_iterative(tree1)
    assert result1_iter == 3, "Iterative Test Failed!"
    print("✅ Iterative solution works!")

    print("\\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)


"""
================================================================================
                         🎓 LEARNING SUMMARY
================================================================================

KEY TAKEAWAYS:
--------------
1. **Depth = 1 + Max of Children**
   - Current node counts as 1
   - Add the deeper child's depth
   - Simple recursive formula!

2. **Simplest Tree Problem**
   - Perfect introduction to tree recursion
   - Only 2 lines of code!
   - Master this pattern for other problems

3. **Base Case: None → 0**
   - Empty tree has no depth
   - This stops the recursion

4. **Post-Order Traversal**
   - Calculate children first (left, right)
   - Then calculate current (root)
   - This is the natural order for depth

MEMORY TRICKS:
--------------
🔹 "Building Floors" - Count floors from bottom up!
🔹 "1 + Max" - Depth = 1 + max(left, right)
🔹 "Empty = 0" - No tree, no depth

COMMON MISTAKES TO AVOID:
--------------------------
❌ Forgetting base case (None check)
❌ Returning max instead of 1 + max
❌ Counting edges instead of nodes
❌ Not handling empty tree

WHEN TO USE THIS PATTERN:
--------------------------
✓ Finding tree height/depth
✓ Checking if tree is balanced
✓ Minimum depth problems
✓ Any "calculate from children" problem

COMPLEXITY CHEAT SHEET:
-----------------------
Time: O(N) - Visit every node once
Space: O(H) - Recursion stack (H = height)
      Best case: O(log N) for balanced tree
      Worst case: O(N) for skewed tree

================================================================================
                            🔗 RELATED PROBLEMS
================================================================================

Similar Problems to Practice:
-----------------------------
1. Minimum Depth of Binary Tree (LeetCode #111) - Find shortest path
2. Balanced Binary Tree (LeetCode #110) - Check if depth difference ≤ 1
3. Diameter of Binary Tree (LeetCode #543) - Longest path between any nodes
4. Binary Tree Paths (LeetCode #257) - Find all root-to-leaf paths

Pattern Recognition:
--------------------
This problem uses the "Tree Depth/Height" pattern:
- Recursive definition (children → parent)
- Base case for None
- Combine children's results
- Post-order traversal (left, right, root)

Next Steps:
-----------
After mastering this, try:
→ Same Tree (comparison)
→ Invert Binary Tree (transformation)
→ Symmetric Tree (mirror comparison)

================================================================================
"""

if __name__ == "__main__":
    test_maximum_depth()

    # Quick manual test
    print("\\n" + "="*60)
    print("Manual Test:")
    print("="*60)

    # Create a simple tree
    #       1
    #      / \\
    #     2   3
    #    /
    #   4
    tree = TreeNode(1)
    tree.left = TreeNode(2)
    tree.right = TreeNode(3)
    tree.left.left = TreeNode(4)

    print(f"\\nTree depth: {maxDepth(tree)}")  # Should be 3
    print(f"One-liner version: {maxDepth_oneliner(tree)}")  # Should be 3
    print(f"Iterative version: {maxDepth_iterative(tree)}")  # Should be 3
