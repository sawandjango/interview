"""
LeetCode Problem #100: Same Tree

Difficulty: Easy
Topics: Tree, DFS, Recursion, Binary Tree
Companies: Amazon, Microsoft, Facebook, Bloomberg, Google, Adobe

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
│ 3    │ 🚀 HOW TO APPROACH THIS PROBLEM      │ • 5-step thinking process     │
│      │                                      │ • Decision tree (which sol?)  │
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
│ 7    │ 🧪 TEST CASES                        │ • 8 comprehensive tests       │
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
│ ANALOGY          │ "Twin Buildings" - Every floor, room must match!        │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ PATTERN          │ "Three Sames" - Same VALUE? Same LEFT? Same RIGHT?     │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ BASE CASES       │ Both None → TRUE | One None → FALSE | Diff val → FALSE │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ DEFAULT SOLUTION │ Recursive DFS (Use in 90% of cases!)                   │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ TIME COMPLEXITY  │ O(min(N,M)) - Stop early when difference found         │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ SPACE COMPLEXITY │ O(min(H1,H2)) - Recursion stack depth                  │
└──────────────────┴─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        ⚡ QUICK DECISION TABLE                              │
├────────────────────────────────┬────────────────────────────────────────────┤
│ SITUATION                      │ WHICH SOLUTION TO USE?                    │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Normal interview               │ ✅ Solution 1 (Recursive)                 │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Very deep tree (height > 1000) │ ⚠️  Solution 2 (Iterative)                │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Uncomfortable with recursion   │ ⚠️  Solution 2 (Iterative)                │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Want to impress interviewer    │ 🎯 Write Sol 1, then mention Sol 2       │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Need clearest code             │ ✅ Solution 1 (Recursive) - 5 lines!      │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Avoid stack overflow           │ ⚠️  Solution 2 (Iterative)                │
└────────────────────────────────┴────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     📊 SOLUTION COMPARISON TABLE                            │
├──────────────────┬─────────────────────────┬────────────────────────────────┤
│ CRITERIA         │ SOLUTION 1 (Recursive)  │ SOLUTION 2 (Iterative)        │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Code Length      │ ⭐⭐⭐⭐⭐ 5 lines        │ ⭐⭐⭐ 15 lines                 │
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

⏱️  TIME TO MASTER: 20-30 minutes
🎯 DIFFICULTY: Easy (Perfect for beginners!)
💡 TIP: Start with Section 1 → 2 → 3 → 4, then practice!

================================================================================
                           🎯 PROBLEM UNDERSTANDING
================================================================================

WHAT IS THE PROBLEM?
--------------------
You're given TWO binary trees and need to check if they are IDENTICAL!

Think of it like: If you had two LEGO buildings, are they built EXACTLY
the same way? Same blocks, same positions, same structure!

REAL WORLD ANALOGY:
------------------
Think of TWIN BUILDINGS! 🏢🏢

Building P:          Building Q:
    1                    1
   / \                  / \
  2   3                2   3

IDENTICAL! ✓ Same floors, same layout, same everything!

Now compare:
Building P:          Building Q:
    1                    1
   / \                  / \
  2   3                3   2

NOT IDENTICAL! ✗ Different layout (2 and 3 swapped)

Another analogy: PHOTOCOPIES 📄
- Original document = Tree P
- Photocopy = Tree Q
- Perfect photocopy? Every word, every space must match!

================================================================================
                            📝 FORMAL PROBLEM
================================================================================

Given the roots of two binary trees p and q, write a function to check if
they are the same or not.

Two binary trees are considered the same if they are structurally identical,
and the nodes have the same value.

Example 1:
----------
Input: p = [1,2,3], q = [1,2,3]

Tree p:          Tree q:
    1                1
   / \              / \
  2   3            2   3

Output: true
Explanation: Both trees are structurally identical and have same values!

Example 2:
----------
Input: p = [1,2], q = [1,null,2]

Tree p:          Tree q:
    1                1
   /                  \
  2                    2

Output: false
Explanation: Different structure! p has left child, q has right child

Example 3:
----------
Input: p = [1,2,1], q = [1,1,2]

Tree p:          Tree q:
    1                1
   / \              / \
  2   1            1   2

Output: false
Explanation: Same structure but different values in children!

Example 4:
----------
Input: p = [], q = []

Output: true
Explanation: Two empty trees are identical!

Constraints:
------------
* The number of nodes in both trees is in the range [0, 100]
* -10^4 <= Node.val <= 10^4

================================================================================
                         🧠 KEY INSIGHTS TO REMEMBER
================================================================================

THE MAIN CHALLENGE:
------------------
❌ Not just comparing root values
❌ Not just checking structure
✅ Must check BOTH structure AND values at EVERY node!

KEY INSIGHT #1: Recursive Nature
---------------------------------
Two trees are the same IF:
1. Both roots have same value  AND
2. Left subtrees are the same  AND
3. Right subtrees are the same

Just like checking if twins are identical by checking every detail!

KEY INSIGHT #2: Base Cases Matter
----------------------------------
What makes two trees identical?

Case 1: Both are empty (None)
   p = None, q = None  →  TRUE ✓
   (Two empty trees are identical!)

Case 2: One is empty, one is not
   p = None, q = [1]   →  FALSE ✗
   p = [1], q = None   →  FALSE ✗
   (Different structure!)

Case 3: Both exist but different values
   p.val = 5, q.val = 3  →  FALSE ✗
   (Different data!)

Case 4: Both exist and same value
   p.val = 5, q.val = 5  →  Check children recursively

KEY INSIGHT #3: Pattern Recognition
-----------------------------------
This is a COMPARISON problem, not a transformation!
- Compare corresponding positions
- Left with left, right with right
- Like comparing two photos side-by-side

================================================================================
                    🚀 HOW TO APPROACH THIS PROBLEM
================================================================================

STEP-BY-STEP THINKING PROCESS:
------------------------------

When you see this problem, ask yourself these questions:

Q1: "What am I comparing?"
A: Two trees - need to check BOTH structure AND values

Q2: "What makes two trees identical?"
A: Every corresponding node must match (value + position)

Q3: "How do I compare ALL nodes?"
A: Start from root, then recursively compare children

Q4: "What are my base cases?"
A: - Both None? → Same
   - One None? → Different
   - Different values? → Different

Q5: "Which approach feels more natural?"
A: Recursion! Trees are recursive by nature

DECISION TREE FOR CHOOSING SOLUTION:
------------------------------------

START HERE:
│
├─ "Do I understand recursion well?"
│  │
│  ├─ YES → Use SOLUTION 1 (Recursive DFS) ✅ RECOMMENDED
│  │        • Most natural and intuitive
│  │        • Clean, short code (5 lines)
│  │        • Easy to explain in interview
│  │
│  └─ NO → Use SOLUTION 2 (Iterative BFS)
│           • More explicit with queue
│           • No recursion needed
│           • Good for learning iteration

Follow-up consideration:
│
└─ "Are trees very deep (height > 1000)?"
   │
   ├─ YES → Use SOLUTION 2 (Iterative) to avoid stack overflow
   │
   └─ NO → Use SOLUTION 1 (Recursive) - cleaner code

EASY WAY TO REMEMBER WHICH SOLUTION TO USE:
-------------------------------------------

🎯 DEFAULT CHOICE: Solution 1 (Recursive)
   ✓ Use this in 90% of cases
   ✓ Clean, simple, natural
   ✓ Perfect for interviews

⚠️  SPECIAL CASES: Solution 2 (Iterative)
   ✓ Very deep trees (avoid stack overflow)
   ✓ Need to process level by level explicitly
   ✓ Want to avoid recursion

================================================================================
                         💡 SOLUTION APPROACHES
================================================================================

APPROACH 1: RECURSIVE DFS (⭐ RECOMMENDED - Use this first!)
------------------------------------------------------------

WHY CHOOSE THIS SOLUTION?
--------------------------
✅ PROS:
   • Most intuitive - mirrors the problem structure
   • Shortest code - only 5 lines for core logic
   • Natural for tree problems - trees ARE recursive!
   • Easy to explain in interviews
   • Readable and maintainable
   • Faster to write (less code = fewer bugs)

❌ CONS:
   • Uses call stack (O(H) space)
   • Stack overflow risk for very deep trees (rare - trees > 1000 depth)
   • Need to understand recursion

WHEN TO USE:
   → Default choice for this problem
   → Trees with reasonable depth (< 1000 nodes deep)
   → Interview settings (cleaner code impresses)
   → When you're comfortable with recursion

APPROACH 1: RECURSIVE DFS
----------------------------------------
The most natural and elegant solution!

INTUITION:
----------
"Two trees are identical if:
 1. Their roots match
 2. Their left subtrees are identical
 3. Their right subtrees are identical"

It's like checking if two family trees are identical by checking each
generation one by one!

ALGORITHM:
----------
1. Base Case: If both are None → TRUE (both empty)
2. Base Case: If one is None → FALSE (different structure)
3. Base Case: If values differ → FALSE (different data)
4. Recursive Case: Check left and right subtrees

MEMORY TRICK: "Same Same Same"
-------------------------------
Same VALUE? ✓
Same LEFT?  ✓  (recursive call)
Same RIGHT? ✓  (recursive call)

All three must be true!

Visual Walkthrough - Example 1:
--------------------------------
Tree p:          Tree q:
    1                1
   / \              / \
  2   3            2   3

Step-by-step execution:

Call 1: isSameTree(p=1, q=1)
├─ Both exist? ✓
├─ Same value (1 == 1)? ✓
├─ Check left: isSameTree(p=2, q=2)
│  ├─ Both exist? ✓
│  ├─ Same value (2 == 2)? ✓
│  ├─ Check left: isSameTree(None, None) → TRUE ✓
│  └─ Check right: isSameTree(None, None) → TRUE ✓
│  └─ Return TRUE ✓
│
├─ Check right: isSameTree(p=3, q=3)
│  ├─ Both exist? ✓
│  ├─ Same value (3 == 3)? ✓
│  ├─ Check left: isSameTree(None, None) → TRUE ✓
│  └─ Check right: isSameTree(None, None) → TRUE ✓
│  └─ Return TRUE ✓
│
└─ Final: TRUE AND TRUE AND TRUE = TRUE ✓

Visual Walkthrough - Example 2:
--------------------------------
Tree p:          Tree q:
    1                1
   /                  \
  2                    2

Call 1: isSameTree(p=1, q=1)
├─ Both exist? ✓
├─ Same value (1 == 1)? ✓
├─ Check left: isSameTree(p=2, q=None)
│  ├─ p exists but q is None ✗
│  └─ Return FALSE ✗
│
└─ Short circuit! Return FALSE immediately

APPROACH 2: ITERATIVE BFS (Alternative Solution)
-------------------------------------------------

WHY CHOOSE THIS SOLUTION?
--------------------------
✅ PROS:
   • No recursion - avoids stack overflow
   • Explicit control - can see exactly what's happening
   • Level-by-level processing - good for debugging
   • No call stack overhead
   • Works for extremely deep trees

❌ CONS:
   • More code - need to manage queue manually
   • Less intuitive - doesn't mirror problem structure as naturally
   • More complex to write initially
   • Harder to explain quickly in interviews

WHEN TO USE:
   → Trees are extremely deep (height > 1000)
   → Interviewer specifically asks for iterative solution
   → You're uncomfortable with recursion
   → Need to process level by level for other reasons
   → Want to demonstrate knowledge of multiple approaches

COMPARISON: When to pick which?
-------------------------------

Scenario 1: "Coding interview, normal tree"
   → Use SOLUTION 1 (Recursive) ✅
   Why: Cleaner, faster to write, easier to explain

Scenario 2: "Very deep tree (height 10,000)"
   → Use SOLUTION 2 (Iterative) ✅
   Why: Avoid stack overflow

Scenario 3: "Want to impress with multiple solutions?"
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
SOLUTION 1: RECURSIVE DFS (RECOMMENDED)
================================================================================
"""

def isSameTree(p: TreeNode, q: TreeNode) -> bool:
    """
    Check if two binary trees are identical using recursion.

    Time Complexity: O(min(N, M)) where N = nodes in p, M = nodes in q
                     We might stop early if trees differ
    Space Complexity: O(min(H1, H2)) for recursion stack
                      where H1, H2 are heights of the trees

    Args:
        p: Root of first binary tree
        q: Root of second binary tree

    Returns:
        True if trees are identical, False otherwise
    """
    # BASE CASE 1: Both trees are empty
    # Two empty trees are identical!
    if not p and not q:
        return True

    # BASE CASE 2: One tree is empty, other is not
    # Different structure → NOT identical
    if not p or not q:
        return False

    # BASE CASE 3: Both nodes exist but have different values
    # Same structure but different data → NOT identical
    if p.val != q.val:
        return False

    # RECURSIVE CASE: Check if left and right subtrees are identical
    # Like checking if both wings of twin butterflies match!
    left_same = isSameTree(p.left, q.left)    # Compare left children
    right_same = isSameTree(p.right, q.right)  # Compare right children

    # Both subtrees must be identical
    return left_same and right_same


# CLEANER ONE-LINER VERSION (same logic):
def isSameTree_oneliner(p: TreeNode, q: TreeNode) -> bool:
    """
    Concise version - same logic but condensed.
    """
    # All conditions in one return statement
    return (not p and not q) or \
           (p and q and p.val == q.val and
            isSameTree(p.left, q.left) and
            isSameTree(p.right, q.right))


"""
================================================================================
SOLUTION 2: ITERATIVE BFS (Using Queue)
================================================================================
"""

from collections import deque

def isSameTree_iterative(p: TreeNode, q: TreeNode) -> bool:
    """
    Check if two trees are identical using iterative BFS approach.

    Time Complexity: O(min(N, M))
    Space Complexity: O(min(N, M)) for queue

    Think: Compare both trees level by level, like checking each floor
           of twin buildings!
    """
    # Use queue to store pairs of nodes to compare
    queue = deque([(p, q)])

    while queue:
        node1, node2 = queue.popleft()

        # Both None - this pair matches, continue
        if not node1 and not node2:
            continue

        # One is None - different structure
        if not node1 or not node2:
            return False

        # Different values - not identical
        if node1.val != node2.val:
            return False

        # Add children pairs to queue for comparison
        queue.append((node1.left, node2.left))
        queue.append((node1.right, node2.right))

    # All pairs matched!
    return True


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


def test_same_tree():
    """Comprehensive test cases"""

    print("Testing Same Tree Solutions...")
    print("=" * 60)

    # Test Case 1: Identical trees
    print("\n✅ Test 1: Identical trees [1,2,3]")
    p1 = build_tree_from_list([1, 2, 3])
    q1 = build_tree_from_list([1, 2, 3])
    result1 = isSameTree(p1, q1)
    print(f"Expected: True")
    print(f"Got: {result1}")
    assert result1 == True, "Test 1 Failed!"

    # Test Case 2: Different structure (left vs right child)
    print("\n❌ Test 2: Different structure [1,2] vs [1,null,2]")
    p2 = build_tree_from_list([1, 2])
    q2 = build_tree_from_list([1, None, 2])
    result2 = isSameTree(p2, q2)
    print(f"Expected: False")
    print(f"Got: {result2}")
    assert result2 == False, "Test 2 Failed!"

    # Test Case 3: Different values
    print("\n❌ Test 3: Different values [1,2,1] vs [1,1,2]")
    p3 = build_tree_from_list([1, 2, 1])
    q3 = build_tree_from_list([1, 1, 2])
    result3 = isSameTree(p3, q3)
    print(f"Expected: False")
    print(f"Got: {result3}")
    assert result3 == False, "Test 3 Failed!"

    # Test Case 4: Both empty
    print("\n✅ Test 4: Both empty trees")
    p4 = None
    q4 = None
    result4 = isSameTree(p4, q4)
    print(f"Expected: True")
    print(f"Got: {result4}")
    assert result4 == True, "Test 4 Failed!"

    # Test Case 5: One empty, one not
    print("\n❌ Test 5: One empty [1] vs []")
    p5 = build_tree_from_list([1])
    q5 = None
    result5 = isSameTree(p5, q5)
    print(f"Expected: False")
    print(f"Got: {result5}")
    assert result5 == False, "Test 5 Failed!"

    # Test Case 6: Single node, same value
    print("\n✅ Test 6: Single node, same value [5] vs [5]")
    p6 = TreeNode(5)
    q6 = TreeNode(5)
    result6 = isSameTree(p6, q6)
    print(f"Expected: True")
    print(f"Got: {result6}")
    assert result6 == True, "Test 6 Failed!"

    # Test Case 7: Single node, different value
    print("\n❌ Test 7: Single node, different value [5] vs [3]")
    p7 = TreeNode(5)
    q7 = TreeNode(3)
    result7 = isSameTree(p7, q7)
    print(f"Expected: False")
    print(f"Got: {result7}")
    assert result7 == False, "Test 7 Failed!"

    # Test Case 8: Larger identical trees
    print("\n✅ Test 8: Larger identical trees")
    p8 = build_tree_from_list([1, 2, 3, 4, 5, 6, 7])
    q8 = build_tree_from_list([1, 2, 3, 4, 5, 6, 7])
    result8 = isSameTree(p8, q8)
    print(f"Expected: True")
    print(f"Got: {result8}")
    assert result8 == True, "Test 8 Failed!"

    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)


"""
================================================================================
                         🎓 LEARNING SUMMARY
================================================================================

KEY TAKEAWAYS:
--------------
1. **Same Tree = Same Structure + Same Values**
   - Both conditions must be satisfied!
   - Check every node, every position

2. **Think Recursively**
   - Break down: "Are these two nodes and their subtrees identical?"
   - Natural fit for tree comparison

3. **Base Cases Are Critical**
   - Both None → True
   - One None → False
   - Different values → False

4. **Comparison Pattern**
   - This is different from Symmetric Tree!
   - Same Tree: Compare left with left, right with right
   - Symmetric Tree: Compare left with right (mirror!)

MEMORY TRICKS:
--------------
🔹 "Twin Buildings" - Every floor, every room must match!
🔹 "Photo vs Photocopy" - Perfect copy or not?
🔹 "Three Sames" - Same value? Same left? Same right?

COMMON MISTAKES TO AVOID:
--------------------------
❌ Forgetting to check if nodes exist before accessing .val
❌ Only checking values, not structure
❌ Confusing with Symmetric Tree (different comparison!)
❌ Not handling None cases properly

WHEN TO USE THIS PATTERN:
--------------------------
✓ Tree equality/comparison problems
✓ Tree serialization/deserialization validation
✓ Finding duplicate subtrees
✓ Tree cloning verification

COMPLEXITY CHEAT SHEET:
-----------------------
Time: O(min(N, M)) - Visit each node once until difference found
Space: O(min(H1, H2)) - Recursion stack depth

================================================================================
                            🔗 RELATED PROBLEMS
================================================================================

Similar Problems to Practice:
-----------------------------
1. Symmetric Tree (LeetCode #101) - Compare tree with its mirror
2. Subtree of Another Tree (LeetCode #572) - Check if tree contains subtree
3. Serialize and Deserialize Binary Tree (LeetCode #297) - Tree representation
4. Find Duplicate Subtrees (LeetCode #652) - Find identical subtrees

Pattern Recognition:
--------------------
This problem uses the "Tree Comparison" pattern:
- Recursive comparison
- Simultaneous traversal of two trees
- Base case handling for None
- Value and structure checking

================================================================================
"""

if __name__ == "__main__":
    test_same_tree()

    # Quick manual test
    print("\n" + "="*60)
    print("Manual Test:")
    print("="*60)

    # Create two identical trees
    tree1 = TreeNode(1)
    tree1.left = TreeNode(2)
    tree1.right = TreeNode(3)

    tree2 = TreeNode(1)
    tree2.left = TreeNode(2)
    tree2.right = TreeNode(3)

    print(f"\nAre tree1 and tree2 identical? {isSameTree(tree1, tree2)}")

    # Create two different trees
    tree3 = TreeNode(1)
    tree3.left = TreeNode(2)

    tree4 = TreeNode(1)
    tree4.right = TreeNode(2)

    print(f"Are tree3 and tree4 identical? {isSameTree(tree3, tree4)}")
