"""
LeetCode Problem #98: Validate Binary Search Tree

Difficulty: Medium
Topics: Tree, DFS, Binary Search Tree, Recursion
Companies: Amazon, Facebook, Google, Microsoft, Bloomberg, Apple, Adobe

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
│ 4    │ 💡 SOLUTION 1: Range Validation ⭐    │ • WHY choose? (Pros/Cons)     │
│      │    (RECOMMENDED)                     │ • WHEN to use?                │
│      │                                      │ • Step-by-step walkthrough    │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 5    │ 💡 SOLUTION 2: Inorder Traversal     │ • WHY choose? (Pros/Cons)     │
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
│ ANALOGY          │ "Age Validator" - Left younger, Right older!            │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ PATTERN          │ "Min-Max Range" - Track valid range at each node        │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ BASE CASE        │ If None → TRUE (empty tree is valid BST)               │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ DEFAULT SOLUTION │ Range Validation (Use in 90% of cases!)                │
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
│ Normal interview               │ ✅ Solution 1 (Range Validation)          │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Want clearest logic            │ ✅ Solution 1 (Explicit constraints)      │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Know inorder property          │ ⚠️  Solution 2 (Inorder traversal)        │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Need sorted values             │ ⚠️  Solution 2 (Bonus: get sorted list)   │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Want to impress                │ 🎯 Write Sol 1, then mention Sol 2       │
└────────────────────────────────┴────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     📊 SOLUTION COMPARISON TABLE                            │
├──────────────────┬─────────────────────────┬────────────────────────────────┤
│ CRITERIA         │ SOLUTION 1 (Range)      │ SOLUTION 2 (Inorder)          │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Code Length      │ ⭐⭐⭐⭐ Short           │ ⭐⭐⭐⭐⭐ Very short            │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Readability      │ ⭐⭐⭐⭐⭐ Very clear     │ ⭐⭐⭐ Needs BST knowledge      │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Interview Speed  │ ⭐⭐⭐⭐⭐ Super fast     │ ⭐⭐⭐⭐ Fast                   │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Intuitiveness    │ ⭐⭐⭐⭐⭐ Very natural   │ ⭐⭐⭐ Requires insight         │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Elegance         │ ⭐⭐⭐⭐ Clean logic     │ ⭐⭐⭐⭐⭐ Clever BST property  │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ When to Use      │ 90% of cases (DEFAULT)  │ Show advanced BST knowledge   │
└──────────────────┴─────────────────────────┴────────────────────────────────┘

⏱️  TIME TO MASTER: 25-30 minutes
🎯 DIFFICULTY: Medium (tricky edge cases!)
💡 TIP: Remember "All descendants must respect BST property, not just children!"
🔥 POPULAR: Very common BST interview question!

================================================================================
                           🎯 PROBLEM UNDERSTANDING
================================================================================

WHAT IS THE PROBLEM?
--------------------
You're given a BINARY TREE and need to check if it's a valid BINARY SEARCH TREE!

But wait... what makes a BST VALID? 🤔

REAL WORLD ANALOGY:
------------------
Think of a BST like a FAMILY TREE with a RULE:
- Everyone on your LEFT side must be YOUNGER than you
- Everyone on your RIGHT side must be OLDER than you
- This rule applies to EVERYONE in your left/right subtrees, not just direct children!

Example:
        Grandpa (50)
        /          \
   Uncle (30)    Aunt (70)
   /      \      /      \
 You(20) Sis(40) Bro(60) Cousin(80)

✓ VALID: All left descendants < 50 < All right descendants
✗ INVALID if Sis was 55 (she'd be on left but > 50!)

================================================================================
                            📝 FORMAL PROBLEM
================================================================================

Given the root of a binary tree, determine if it is a valid binary search tree.

A valid BST is defined as follows:
1. The left subtree of a node contains only nodes with keys LESS than the node's key.
2. The right subtree of a node contains only nodes with keys GREATER than the node's key.
3. Both the left and right subtrees must also be binary search trees.

Example 1:
----------
Input: root = [2,1,3]

       2
      / \
     1   3

Output: true
Explanation:
- 1 < 2 ✓
- 3 > 2 ✓
- Valid BST!

Example 2:
----------
Input: root = [5,1,4,null,null,3,6]

       5
      / \
     1   4
        / \
       3   6

Output: false
Explanation:
- Root is 5
- Right child is 4 (4 > 5? NO! ✗)
- Invalid BST!

Example 3 (TRICKY!):
-------------------
Input: root = [5,4,6,null,null,3,7]

       5
      / \
     4   6
        / \
       3   7

Output: false
Explanation:
- 4 < 5 ✓ (left child is smaller)
- 6 > 5 ✓ (right child is bigger)
- BUT WAIT! 3 is in the RIGHT subtree of 5
- 3 < 5, so it should be on the LEFT!
- Invalid BST! ✗

Constraints:
------------
* The number of nodes in the tree is in the range [1, 10^4].
* -2^31 <= Node.val <= 2^31 - 1

================================================================================
                         🧠 KEY INSIGHTS TO REMEMBER
================================================================================

THE MAIN CHALLENGE:
------------------
❌ Can't just check if left < root < right (common mistake!)
❌ Must ensure ALL left descendants < root < ALL right descendants!
✅ Need to track VALID RANGE for each node!

THE MAGIC TRICK: "Valid Range" Method
-------------------------------------
Think of each node having a VALID RANGE [min, max]:

For each node with value 'val':
- Root: Can be anything → Range: [-∞, +∞]
- Left child: Must be < val → Range: [-∞, val)
- Right child: Must be > val → Range: (val, +∞]

Example:
           10 [Range: -∞ to +∞]
          /  \
         5    15 [Range: 10 to +∞]
        / \   / \
       3   7 12  20 [Range: 15 to +∞]

- Node 10: Can be anything ✓
- Node 5: Must be < 10 ✓ [Range: -∞ to 10]
- Node 15: Must be > 10 ✓ [Range: 10 to +∞]
- Node 3: Must be < 5 AND < 10 ✓ [Range: -∞ to 5]
- Node 7: Must be > 5 AND < 10 ✓ [Range: 5 to 10]
- Node 12: Must be > 10 AND < 15 ✓ [Range: 10 to 15]
- Node 20: Must be > 15 AND > 10 ✓ [Range: 15 to +∞]

================================================================================
                          💡 SOLUTION APPROACHES
================================================================================
"""

# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ============================================================================
#              APPROACH 1: DFS with Valid Range (MOST INTUITIVE!)
# ============================================================================

def isValidBST_Range(root):
    """
    🎯 APPROACH 1: Valid Range Method (RECOMMENDED!)

    TIME COMPLEXITY: O(n) - Visit each node once
    SPACE COMPLEXITY: O(h) - Recursion stack (h = height of tree)

    🧠 MEMORIZATION TRICK: "Range Police" 👮
    ----------------------------------------
    Each node is a "Range Police Officer" checking if it's in valid range!
    - Root: Can be anything [-∞, +∞]
    - Go left? Update max boundary
    - Go right? Update min boundary

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Start with root, range = [-∞, +∞]
    2. Check if current node's value is in valid range
    3. Recursively validate:
       - Left subtree: range = [min, current_val)
       - Right subtree: range = (current_val, max]
    4. All nodes valid? BST is valid!

    Why it works:
    - Each node carries constraints from ALL ancestors
    - Left descendants inherit upper bound
    - Right descendants inherit lower bound
    """
    def validate(node, min_val, max_val):
        # Base case: empty tree is valid
        if not node:
            return True

        # Current node violates range? Invalid BST!
        if not (min_val < node.val < max_val):
            return False

        # Recursively validate left and right subtrees
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))

    # Start with full range
    return validate(root, float('-inf'), float('inf'))


# ============================================================================
#              APPROACH 2: Inorder Traversal (ELEGANT!)
# ============================================================================

def isValidBST_Inorder(root):
    """
    🎯 APPROACH 2: Inorder Traversal Method

    TIME COMPLEXITY: O(n) - Visit each node once
    SPACE COMPLEXITY: O(h) - Recursion stack

    🧠 MEMORIZATION TRICK: "Sorted List Check"
    ------------------------------------------
    KEY INSIGHT: Inorder traversal of a BST gives SORTED order!

    BST Inorder = [1, 2, 3, 4, 5, 6, 7] ✓ Sorted!

    If inorder gives unsorted list → NOT a valid BST!

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Perform inorder traversal (Left → Root → Right)
    2. Track previous value
    3. Current value should be > previous value
    4. If current <= previous → Invalid BST!
    """
    def inorder(node):
        if not node:
            return True

        # Check left subtree first (inorder: LEFT, root, right)
        if not inorder(node.left):
            return False

        # Check if current node violates BST property
        # Current should be > previous
        if node.val <= inorder.prev:
            return False

        # Update previous value
        inorder.prev = node.val

        # Check right subtree (inorder: left, root, RIGHT)
        return inorder(node.right)

    # Initialize previous value to negative infinity
    inorder.prev = float('-inf')
    return inorder(root)


# ============================================================================
#              APPROACH 3: Iterative Inorder (No Recursion)
# ============================================================================

def isValidBST_Iterative(root):
    """
    🎯 APPROACH 3: Iterative Inorder with Stack

    TIME COMPLEXITY: O(n)
    SPACE COMPLEXITY: O(h) - Stack size

    🧠 MEMORIZATION TRICK: "Stack-based Traversal"
    ---------------------------------------------
    Same as Approach 2 but using explicit stack instead of recursion
    """
    if not root:
        return True

    stack = []
    prev = float('-inf')
    current = root

    while stack or current:
        # Go to leftmost node
        while current:
            stack.append(current)
            current = current.left

        # Process node
        current = stack.pop()

        # Check BST property
        if current.val <= prev:
            return False

        prev = current.val

        # Move to right subtree
        current = current.right

    return True


# ============================================================================
#                    🎨 VISUAL WALKTHROUGH EXAMPLE
# ============================================================================

"""
Let's walk through Example 3 (The TRICKY one!):

Tree:
       5
      / \
     4   6
        / \
       3   7

APPROACH 1: Valid Range Method
-------------------------------

Step 1: Validate node 5
   - Range: [-∞, +∞]
   - -∞ < 5 < +∞ ✓
   - Go left with range [-∞, 5)
   - Go right with range (5, +∞]

Step 2: Validate node 4 (left of 5)
   - Range: [-∞, 5)
   - -∞ < 4 < 5 ✓
   - No children, return True

Step 3: Validate node 6 (right of 5)
   - Range: (5, +∞]
   - 5 < 6 < +∞ ✓
   - Go left with range (5, 6)
   - Go right with range (6, +∞]

Step 4: Validate node 3 (left of 6, in right subtree of 5!)
   - Range: (5, 6)  ← Must be GREATER than 5!
   - 5 < 3? NO! ✗
   - INVALID BST!

Return: False

APPROACH 2: Inorder Traversal
-----------------------------
Inorder: Left → Root → Right

Visit order: 4 → 5 → 3 → 6 → 7

Step 1: Visit 4
   - prev = -∞
   - 4 > -∞ ✓
   - prev = 4

Step 2: Visit 5
   - prev = 4
   - 5 > 4 ✓
   - prev = 5

Step 3: Visit 3
   - prev = 5
   - 3 > 5? NO! ✗
   - INVALID BST!

Return: False
"""

# ============================================================================
#              🎯 MEMORY TRICKS & COMMON MISTAKES
# ============================================================================

"""
🧠 HOW TO REMEMBER THIS SOLUTION:
---------------------------------
Analogy: "SPEED LIMIT ZONES" 🚗

Think of each node as a ROAD with SPEED LIMITS:
- Root: No limits [-∞, +∞]
- Turn left? Max speed decreases (upper bound = parent's value)
- Turn right? Min speed increases (lower bound = parent's value)
- Violate speed limit? INVALID!

Mantra: "Range Narrows As You Descend"

❌ COMMON MISTAKES TO AVOID:
----------------------------
1. ❌ Only checking immediate children
   Example:
       10
      /  \
     5   15
        /  \
       6   20

   Checking only: 5 < 10 ✓, 15 > 10 ✓, 6 < 15 ✓, 20 > 15 ✓
   BUT: 6 is in right subtree of 10, should be > 10!
   → INVALID BST but you'd say valid!

2. ❌ Not handling equal values
   - BST must have STRICTLY less/greater (no equal!)
   - Use < and >, not <= and >=

3. ❌ Forgetting null nodes
   - Empty tree/subtree is valid BST!

4. ❌ Integer overflow
   - Use float('-inf') and float('inf')
   - Don't use INT_MIN, INT_MAX (edge cases fail)

5. ❌ Wrong inorder comparison
   - Should be: current > previous
   - NOT: current >= previous (equal is invalid!)

✅ PRO TIPS:
-----------
1. Approach 1 (Range) is most intuitive and interview-friendly
2. Approach 2 (Inorder) is elegant but trickier to explain
3. Always explain your approach BEFORE coding
4. Draw the tree and trace your algorithm!
5. Test with edge cases: single node, all left, all right
"""

# ============================================================================
#                         🧪 TEST CASES
# ============================================================================

def test_isValidBST():
    """Run comprehensive test cases"""

    print("="*70)
    print("          VALIDATE BINARY SEARCH TREE - TEST CASES")
    print("="*70)

    # Test Case 1: Valid BST
    print("\n📝 Test Case 1: Valid BST [2,1,3]")
    print("-" * 70)
    print("Tree:")
    print("    2")
    print("   / \\")
    print("  1   3")

    root1 = TreeNode(2)
    root1.left = TreeNode(1)
    root1.right = TreeNode(3)

    result1_range = isValidBST_Range(root1)
    result1_inorder = isValidBST_Inorder(root1)
    result1_iterative = isValidBST_Iterative(root1)

    print(f"\nRange Method: {result1_range}")
    print(f"Inorder Method: {result1_inorder}")
    print(f"Iterative Method: {result1_iterative}")
    print(f"Expected: True")
    print(f"✓ PASS" if result1_range == True else "✗ FAIL")

    # Test Case 2: Invalid BST (right child smaller)
    print("\n📝 Test Case 2: Invalid BST [5,1,4,null,null,3,6]")
    print("-" * 70)
    print("Tree:")
    print("      5")
    print("     / \\")
    print("    1   4")
    print("       / \\")
    print("      3   6")

    root2 = TreeNode(5)
    root2.left = TreeNode(1)
    root2.right = TreeNode(4)
    root2.right.left = TreeNode(3)
    root2.right.right = TreeNode(6)

    result2 = isValidBST_Range(root2)
    print(f"\nResult: {result2}")
    print(f"Expected: False")
    print(f"Explanation: 4 < 5, so right child violates BST property")
    print(f"✓ PASS" if result2 == False else "✗ FAIL")

    # Test Case 3: Invalid BST (left descendant in right subtree)
    print("\n📝 Test Case 3: Tricky Invalid BST [5,4,6,null,null,3,7]")
    print("-" * 70)
    print("Tree:")
    print("      5")
    print("     / \\")
    print("    4   6")
    print("       / \\")
    print("      3   7")

    root3 = TreeNode(5)
    root3.left = TreeNode(4)
    root3.right = TreeNode(6)
    root3.right.left = TreeNode(3)
    root3.right.right = TreeNode(7)

    result3 = isValidBST_Range(root3)
    print(f"\nResult: {result3}")
    print(f"Expected: False")
    print(f"Explanation: 3 is in right subtree of 5, should be > 5!")
    print(f"✓ PASS" if result3 == False else "✗ FAIL")

    # Test Case 4: Single node (edge case)
    print("\n📝 Test Case 4: Single node [1]")
    print("-" * 70)
    print("Tree:")
    print("    1")

    root4 = TreeNode(1)
    result4 = isValidBST_Range(root4)
    print(f"\nResult: {result4}")
    print(f"Expected: True")
    print(f"✓ PASS" if result4 == True else "✗ FAIL")

    # Test Case 5: Duplicate values (invalid)
    print("\n📝 Test Case 5: Duplicate values [2,2,2]")
    print("-" * 70)
    print("Tree:")
    print("    2")
    print("   / \\")
    print("  2   2")

    root5 = TreeNode(2)
    root5.left = TreeNode(2)
    root5.right = TreeNode(2)

    result5 = isValidBST_Range(root5)
    print(f"\nResult: {result5}")
    print(f"Expected: False")
    print(f"Explanation: BST requires strict inequality (no duplicates)")
    print(f"✓ PASS" if result5 == False else "✗ FAIL")

    # Test Case 6: Large valid BST
    print("\n📝 Test Case 6: Larger valid BST")
    print("-" * 70)
    print("Tree:")
    print("        10")
    print("       /  \\")
    print("      5    15")
    print("     / \\   / \\")
    print("    3   7 12  20")

    root6 = TreeNode(10)
    root6.left = TreeNode(5)
    root6.right = TreeNode(15)
    root6.left.left = TreeNode(3)
    root6.left.right = TreeNode(7)
    root6.right.left = TreeNode(12)
    root6.right.right = TreeNode(20)

    result6 = isValidBST_Range(root6)
    print(f"\nResult: {result6}")
    print(f"Expected: True")
    print(f"✓ PASS" if result6 == True else "✗ FAIL")

    # Test Case 7: Edge case with INT_MIN/MAX simulation
    print("\n📝 Test Case 7: Extreme values")
    print("-" * 70)

    root7 = TreeNode(0)
    root7.left = TreeNode(-1)

    result7 = isValidBST_Range(root7)
    print(f"\nResult: {result7}")
    print(f"Expected: True")
    print(f"✓ PASS" if result7 == True else "✗ FAIL")

    print("\n" + "="*70)
    print("              ✅ ALL TEST CASES COMPLETED!")
    print("="*70)


if __name__ == "__main__":
    test_isValidBST()


# ============================================================================
#              🎓 LEARNING SUMMARY & KEY TAKEAWAYS
# ============================================================================

"""
🎯 WHAT YOU LEARNED:
-------------------
1. BST validation requires checking ALL descendants, not just children
2. Valid Range method: Track [min, max] for each node
3. Inorder traversal of BST must be in SORTED order
4. Use float('-inf') and float('inf') for boundaries

🔑 KEY PATTERN: "Range Propagation"
-----------------------------------
This pattern applies to:
- Validate Binary Search Tree (this problem)
- Recover Binary Search Tree
- Binary Search Tree Iterator
- Kth Smallest Element in BST
- Lowest Common Ancestor of BST

💪 SIMILAR PROBLEMS TO PRACTICE:
-------------------------------
1. LeetCode #99: Recover Binary Search Tree
2. LeetCode #230: Kth Smallest Element in a BST
3. LeetCode #235: Lowest Common Ancestor of a BST
4. LeetCode #108: Convert Sorted Array to BST
5. LeetCode #173: Binary Search Tree Iterator

🎉 CONGRATULATIONS!
------------------
You now understand BST validation!

Remember the KEY INSIGHTS:
1. "Range Police" - Each node checks valid range
2. "Inorder = Sorted" - BST property
3. "Descendants, not Children" - Check entire subtree

Key Differences from Previous Problems:
- Clone Graph: HashMap for tracking nodes
- Number of Islands: Count & mark visited
- Validate BST: Range constraints propagation
"""
