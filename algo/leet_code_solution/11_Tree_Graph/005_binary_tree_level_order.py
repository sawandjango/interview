"""
LeetCode Problem #102: Binary Tree Level Order Traversal

Difficulty: Medium
Topics: Tree, BFS, Queue, Level Order Traversal
Companies: Amazon, Microsoft, Facebook, Google, Bloomberg, Apple

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
│ 4    │ 💡 SOLUTION 1: BFS with Queue ⭐      │ • WHY choose? (Pros/Cons)     │
│      │    (RECOMMENDED)                     │ • WHEN to use?                │
│      │                                      │ • Step-by-step walkthrough    │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 5    │ 💡 SOLUTION 2: DFS with Levels       │ • WHY choose? (Pros/Cons)     │
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
│ ANALOGY          │ "Reading a Book" - Process line by line, left to right! │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ PATTERN          │ "Snapshot the Wave" - Count queue size BEFORE loop!     │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ BASE CASE        │ If None → Return [] (empty tree)                       │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ DEFAULT SOLUTION │ BFS with Queue (Use in 99% of cases!)                  │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ TIME COMPLEXITY  │ O(N) - Visit every node exactly once                   │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ SPACE COMPLEXITY │ O(W) - Queue holds max width (W = max nodes at level)  │
└──────────────────┴─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        ⚡ QUICK DECISION TABLE                              │
├────────────────────────────────┬────────────────────────────────────────────┤
│ SITUATION                      │ WHICH SOLUTION TO USE?                    │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Normal interview               │ ✅ Solution 1 (BFS with Queue)            │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Level order traversal          │ ✅ Solution 1 (BFS is NATURAL!)           │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Want simplest code             │ ✅ Solution 1 (Most intuitive)            │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Prefer recursion               │ ⚠️  Solution 2 (DFS with levels)          │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Need to avoid extra space      │ ⚠️  Solution 2 (O(h) vs O(w))             │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Want to show off knowledge     │ 🎯 Write Sol 1, then mention Sol 2       │
└────────────────────────────────┴────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     📊 SOLUTION COMPARISON TABLE                            │
├──────────────────┬─────────────────────────┬────────────────────────────────┤
│ CRITERIA         │ SOLUTION 1 (BFS Queue)  │ SOLUTION 2 (DFS Levels)       │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Code Length      │ ⭐⭐⭐⭐⭐ Short & clean  │ ⭐⭐⭐⭐ Also short             │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Readability      │ ⭐⭐⭐⭐⭐ Crystal clear  │ ⭐⭐⭐ Less intuitive           │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Interview Speed  │ ⭐⭐⭐⭐⭐ Super fast     │ ⭐⭐⭐⭐ Fast but not natural  │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Intuitiveness    │ ⭐⭐⭐⭐⭐ Perfect match  │ ⭐⭐ Not natural for levels    │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Space Efficiency │ ⭐⭐⭐ O(w) queue space  │ ⭐⭐⭐⭐ O(h) recursion stack   │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ When to Use      │ 99% of cases (DEFAULT)  │ When recursion preferred      │
└──────────────────┴─────────────────────────┴────────────────────────────────┘

⏱️  TIME TO MASTER: 15-20 minutes
🎯 DIFFICULTY: Medium (but concept is easy!)
💡 TIP: Remember "Snapshot the Wave" - size before loop!
🔥 POPULAR: THE standard BFS pattern for tree problems!

================================================================================
                           🎯 PROBLEM UNDERSTANDING
================================================================================

WHAT IS THE PROBLEM?
--------------------
You're given a BINARY TREE and need to return values LEVEL by LEVEL (layer by layer)!

Each level should be a separate list, from left to right!

REAL WORLD ANALOGY:
------------------
Think of a COMPANY ORGANIZATION CHART! 🏢

CEO (Level 0):          [Alice]
         |
    _____|_____
   |           |
Managers (Level 1):  [Bob, Carol]
         |
    _____|_____
   |     |     |
Team (Level 2):    [Dan, Eve, Frank]

Output: [[Alice], [Bob, Carol], [Dan, Eve, Frank]]

Another analogy: READING A BOOK 📖
- Read line 1 from left to right
- Then line 2 from left to right
- Then line 3 from left to right
- That's level order!

================================================================================
                            📝 FORMAL PROBLEM
================================================================================

Given the root of a binary tree, return the level order traversal of its
nodes' values (i.e., from left to right, level by level).

Example 1:
----------
Input: root = [3,9,20,null,null,15,7]

       3          ← Level 0
      / \
     9  20        ← Level 1
       /  \
      15   7      ← Level 2

Output: [[3], [9,20], [15,7]]

Explanation:
- Level 0: [3]
- Level 1: [9, 20] (left to right)
- Level 2: [15, 7] (left to right)

Example 2:
----------
Input: root = [1]

       1

Output: [[1]]

Example 3:
----------
Input: root = []

Output: []

Constraints:
------------
* The number of nodes in the tree is in the range [0, 2000]
* -1000 <= Node.val <= 2000

================================================================================
                         🧠 KEY INSIGHTS TO REMEMBER
================================================================================

THE MAIN CHALLENGE:
------------------
❌ Can't just traverse randomly - need to process LEVEL BY LEVEL!
❌ DFS goes DEEP first (not level by level)
✅ Need BFS (Breadth-First Search) with a QUEUE!

THE MAGIC TRICK: "Process One Level at a Time"
----------------------------------------------
Key insight: SNAPSHOT the queue size BEFORE processing!

Why?
- Queue contains ALL nodes at current level
- Process exactly that many nodes
- Their children become the next level

Think of it like WAVES in water:
- First wave: Just the root
- Second wave: Root's children
- Third wave: Grandchildren
- Each wave is one level!

================================================================================
                    🚀 HOW TO APPROACH THIS PROBLEM
================================================================================

STEP-BY-STEP THINKING PROCESS:
------------------------------

When you see this problem, ask yourself these questions:

Q1: "What am I trying to do?"
A: Return nodes level by level, left to right

Q2: "What's the difference from normal traversal?"
A: Need to group by LEVEL (not just visit all nodes)

Q3: "DFS or BFS?"
A: BFS! Level order = processing layer by layer

Q4: "How do I separate levels?"
A: Snapshot queue size before processing each level

Q5: "What's the key trick?"
A: for loop with level_size ensures we process ONLY current level

DECISION TREE FOR CHOOSING SOLUTION:
------------------------------------

START HERE:
│
├─ "Is this level order traversal?"
│  │
│  ├─ YES → Use SOLUTION 1 (BFS with Queue) ✅ RECOMMENDED
│  │        • BFS is NATURAL for level order!
│  │        • Most intuitive approach
│  │        • Industry standard
│  │
│  └─ "Do I prefer recursion over iteration?"
│     │
│     ├─ YES → Use SOLUTION 2 (DFS with level parameter)
│     │        • Less intuitive but works
│     │        • Good to know alternative
│     │
│     └─ NO → Use SOLUTION 1 (BFS) - the obvious choice!

Follow-up consideration:
│
└─ "Which approach matches problem best?"
   │
   ├─ Level order → BFS ✅ (perfect match!)
   ├─ Pre/In/Post order → DFS
   └─ When in doubt → BFS for level order!

EASY WAY TO REMEMBER WHICH SOLUTION TO USE:
-------------------------------------------

🎯 DEFAULT CHOICE: Solution 1 (BFS with Queue)
   ✓ Use this in 99% of cases
   ✓ BFS = Level order (natural fit!)
   ✓ Perfect for interviews
   ✓ Industry standard

⚠️  SPECIAL CASES: Solution 2 (DFS with levels)
   ✓ When you love recursion
   ✓ Want to show alternative knowledge
   ✓ Slightly better space in some cases (O(h) vs O(w))

================================================================================
                          💡 SOLUTION APPROACHES
================================================================================
"""

from collections import deque
from typing import Optional, List


# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ============================================================================
#              APPROACH 1: BFS with Queue (RECOMMENDED!)
# ============================================================================

"""
APPROACH 1: BFS WITH QUEUE (⭐ RECOMMENDED - Use this first!)
------------------------------------------------------------

WHY CHOOSE THIS SOLUTION?
--------------------------
✅ PROS:
   • Perfect match for level order - BFS naturally processes level by level
   • Most intuitive - mirrors how we think about the problem
   • Industry standard - this is how everyone does it
   • Clear separation of levels - snapshot size before loop
   • Easy to explain in interviews
   • Works for all tree shapes (balanced, skewed, complete)

❌ CONS:
   • Uses queue space O(w) where w = max width
   • For complete binary tree, w can be n/2 (lots of space)
   • Iteration, not recursion (if you prefer recursion)

WHEN TO USE:
   → Default choice for ANY level order traversal problem
   → Anytime you need to process tree layer by layer
   → Interview settings (this is the expected solution)
   → Real-world applications (BFS is standard for levels)

COMPLEXITY:
   ⏱️ TIME: O(N) - Visit each node exactly once
   💾 SPACE: O(W) - Queue holds max width W
            Worst case O(N) for complete binary tree (last level has ~N/2 nodes)

INTUITION:
----------
"Process each floor of a building, one floor at a time!"

Think of an apartment building:
- Start at ground floor (root)
- Visit ALL apartments on ground floor
- Their residents tell you who lives on next floor (children)
- Move up one floor
- Visit ALL apartments on that floor
- Repeat until you reach the top!

"""

def levelOrder(root):
    """
    🎯 APPROACH 1: BFS with Queue (MOST INTUITIVE!)

    TIME COMPLEXITY: O(n) - Visit each node exactly once
    SPACE COMPLEXITY: O(w) - Queue holds max width of tree
                      Worst case O(n) for complete binary tree

    🧠 MEMORIZATION TRICK: "Snapshot the Wave" 🌊
    --------------------------------------------
    Think: WATERFALL going down level by level!
    - Count how many water drops at current level
    - Process exactly that many
    - New drops (children) form next level

    Mantra: "Size Before Loop!"

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Handle edge case: empty tree → return []
    2. Create queue, add root
    3. While queue not empty:
       a. SNAPSHOT queue size (current level size) ← KEY STEP!
       b. Create empty list for current level
       c. Process exactly 'size' nodes:
          - Remove from queue
          - Add value to current level list
          - Add children (left, right) to queue
       d. Add current level to result
    4. Return result

    Why SNAPSHOT size?
    - Queue changes size as we add children
    - Need to know how many nodes in THIS level
    - Don't want to process children until NEXT iteration!
    """
    # Edge case: empty tree
    if not root:
        return []

    result = []
    queue = deque([root])  # Start with root in queue

    while queue:
        # 🔑 KEY: Snapshot current level size BEFORE processing!
        level_size = len(queue)
        current_level = []

        # Process exactly 'level_size' nodes (all nodes at this level)
        for i in range(level_size):
            # Remove node from front of queue
            node = queue.popleft()

            # Add node's value to current level
            current_level.append(node.val)

            # Add children to queue (they'll be processed in next level!)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        # Add completed level to result
        result.append(current_level)

    return result


# ============================================================================
#              APPROACH 2: DFS with Level Tracking (Alternative)
# ============================================================================

"""
APPROACH 2: DFS WITH LEVEL PARAMETER (Alternative Solution)
-----------------------------------------------------------

WHY CHOOSE THIS SOLUTION?
--------------------------
✅ PROS:
   • Uses recursion (if you prefer recursive thinking)
   • Slightly better space in tall, narrow trees (O(h) vs O(w))
   • Demonstrates understanding of multiple approaches
   • Good mental exercise (depth = level!)
   • Elegant recursive structure

❌ CONS:
   • Less intuitive - DFS doesn't naturally group by level
   • Harder to explain - "why use DFS for level order?"
   • Not the standard approach for this problem
   • Pre-order traversal (left before right) might not be obvious
   • Interviewer might question choice

WHEN TO USE:
   → When you strongly prefer recursion over iteration
   → To show you know multiple approaches
   → When tree is very tall and narrow (h << w)
   → Practice understanding depth = level index

COMPLEXITY:
   ⏱️ TIME: O(N) - Visit each node exactly once
   💾 SPACE: O(H) - Recursion stack depth (H = height)
            Best case O(log N) for balanced tree
            Worst case O(N) for skewed tree

COMPARISON: When to pick which?
-------------------------------

Scenario 1: "Normal level order interview question"
   → Use SOLUTION 1 (BFS) ✅
   Why: It's the natural, expected solution

Scenario 2: "Tall, narrow tree (skewed tree)"
   → Use SOLUTION 2 (DFS) ✅
   Why: O(h) space vs O(w), but h ≈ n in skewed tree

Scenario 3: "Want to impress with multiple solutions?"
   → Write SOLUTION 1 first, then mention SOLUTION 2 exists
   Why: Shows you know the right tool but understand alternatives

"""

def levelOrder_DFS(root):
    """
    🎯 APPROACH 2: DFS with Level Parameter

    TIME COMPLEXITY: O(n)
    SPACE COMPLEXITY: O(h) - Recursion stack (h = height)

    🧠 MEMORIZATION TRICK: "Depth = Level Index"
    -------------------------------------------
    Use DFS but track DEPTH (which IS the level number!)
    - Depth 0 → result[0]
    - Depth 1 → result[1]
    - Depth 2 → result[2]

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. Create result list
    2. DFS(node, level):
       a. If node is None → return
       b. If this level doesn't exist in result → create it
       c. Add node's value to result[level]
       d. Recurse left child with level+1
       e. Recurse right child with level+1
    3. Return result

    Note: Less intuitive than BFS for level order!
    """
    if not root:
        return []

    result = []

    def dfs(node, level):
        if not node:
            return

        # If this is a new level, create new list
        if level == len(result):
            result.append([])

        # Add current node to its level
        result[level].append(node.val)

        # Recurse for children (next level)
        dfs(node.left, level + 1)
        dfs(node.right, level + 1)

    dfs(root, 0)
    return result


# ============================================================================
#                    🎨 VISUAL WALKTHROUGH EXAMPLE
# ============================================================================

"""
Let's walk through Example 1 step-by-step:

Tree:
       3
      / \\
     9  20
       /  \\
      15   7

APPROACH 1: BFS with Queue
---------------------------

INITIALIZATION:
---------------
result = []
queue = deque([3])  ← Start with root

ITERATION 1 (Process Level 0):
-------------------------------
queue = deque([3])
level_size = 1  ← SNAPSHOT! This is crucial!
current_level = []

  Loop iteration i=0:
    node = queue.popleft()  → node = 3
    current_level.append(3)  → current_level = [3]
    Add children:
      node.left exists → queue.append(9)
      node.right exists → queue.append(20)

  After loop:
    queue = deque([9, 20])
    current_level = [3]

result.append([3])  → result = [[3]]
queue = deque([9, 20])

ITERATION 2 (Process Level 1):
-------------------------------
queue = deque([9, 20])
level_size = 2  ← SNAPSHOT! Two nodes at this level!
current_level = []

  Loop iteration i=0:
    node = queue.popleft()  → node = 9
    current_level.append(9)  → current_level = [9]
    Add children:
      node.left is None → skip
      node.right is None → skip

  Loop iteration i=1:
    node = queue.popleft()  → node = 20
    current_level.append(20)  → current_level = [9, 20]
    Add children:
      node.left exists → queue.append(15)
      node.right exists → queue.append(7)

  After loop:
    queue = deque([15, 7])
    current_level = [9, 20]

result.append([9, 20])  → result = [[3], [9, 20]]
queue = deque([15, 7])

ITERATION 3 (Process Level 2):
-------------------------------
queue = deque([15, 7])
level_size = 2  ← SNAPSHOT!
current_level = []

  Loop iteration i=0:
    node = queue.popleft()  → node = 15
    current_level.append(15)  → current_level = [15]
    Add children:
      node.left is None → skip
      node.right is None → skip

  Loop iteration i=1:
    node = queue.popleft()  → node = 7
    current_level.append(7)  → current_level = [15, 7]
    Add children:
      node.left is None → skip
      node.right is None → skip

  After loop:
    queue = deque([])  ← Empty!
    current_level = [15, 7]

result.append([15, 7])  → result = [[3], [9, 20], [15, 7]]
queue = deque([])

ITERATION 4:
------------
queue is empty → exit while loop

FINAL RESULT: [[3], [9, 20], [15, 7]] ✓


WHY SNAPSHOT SIZE IS CRITICAL:
-------------------------------
❌ Without snapshot:
   - Start with queue = [3]
   - Process 3, add children → queue = [9, 20]
   - Continue loop? Process 9 and 20 in SAME iteration!
   - Wrong! They're different levels!

✓ With snapshot:
   - Start with queue = [3], SIZE = 1
   - Loop exactly 1 time (process only 3)
   - Children added but not processed this iteration
   - Next iteration handles new level!
"""

# ============================================================================
#              🎯 MEMORY TRICKS & COMMON MISTAKES
# ============================================================================

"""
🧠 HOW TO REMEMBER THIS SOLUTION:
---------------------------------
Analogy: "ELEVATOR LOADING" 🛗

Imagine an elevator that opens at each floor:
1. Count how many people waiting at THIS floor (snapshot size)
2. Let exactly that many people in
3. They press buttons for their kids' floors (add children to queue)
4. Move to next floor
5. Repeat!

Mantra: "Count the Floor, Empty the Floor, Go to Next Floor"

Visual Memory Aid:
-----------------
Queue = [A, B, C]  ← Current level
         ↓  ↓  ↓
Queue = [D, E, F, G, H, I]  ← Next level (children)

Must process A, B, C completely BEFORE touching D, E, F!

❌ COMMON MISTAKES TO AVOID:
----------------------------
1. ❌ Forgetting to snapshot level_size
   ```python
   # WRONG:
   while queue:
       node = queue.popleft()  # Processes nodes one by one, mixes levels!
       # ...
   ```

   ```python
   # CORRECT:
   while queue:
       level_size = len(queue)  # ← SNAPSHOT!
       for i in range(level_size):
           node = queue.popleft()
           # ...
   ```

2. ❌ Using queue.pop() instead of queue.popleft()
   - pop() removes from END → gives you LIFO (stack behavior)
   - popleft() removes from FRONT → gives you FIFO (queue behavior)
   - You want FIFO for BFS!

3. ❌ Not handling empty tree
   ```python
   if not root:
       return []  # ← Don't forget this!
   ```

4. ❌ Adding null children to queue
   ```python
   # WRONG:
   queue.append(node.left)  # What if left is None?

   # CORRECT:
   if node.left:
       queue.append(node.left)
   ```

5. ❌ Using regular list instead of deque
   ```python
   # SLOW:
   queue = [root]
   node = queue.pop(0)  # O(n) operation!

   # FAST:
   queue = deque([root])
   node = queue.popleft()  # O(1) operation!
   ```

6. ❌ Forgetting to add current_level to result
   ```python
   while queue:
       level_size = len(queue)
       current_level = []
       for i in range(level_size):
           # ... process nodes ...
       result.append(current_level)  # ← Don't forget!
   ```

✅ PRO TIPS:
-----------
1. Always use deque from collections (O(1) popleft)
2. Snapshot size BEFORE the for loop
3. BFS is THE pattern for level-order problems
4. Draw the tree and trace queue state!
5. Test with: empty tree, single node, complete tree, skewed tree

🔧 DEBUGGING CHECKLIST:
-----------------------
If your solution doesn't work:
□ Did you snapshot level_size before the loop?
□ Are you using popleft() not pop()?
□ Are you checking if children exist before adding?
□ Did you handle empty tree?
□ Are you appending current_level to result?
"""

# ============================================================================
#                         🧪 TEST CASES
# ============================================================================

def test_levelOrder():
    """Run comprehensive test cases"""

    print("="*70)
    print("       BINARY TREE LEVEL ORDER TRAVERSAL - TEST CASES")
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

    # Test Case 1: Standard tree
    print("\n📝 Test Case 1: Standard tree [3,9,20,null,null,15,7]")
    print("-" * 70)
    print("Tree:")
    print("       3")
    print("      / \\")
    print("     9  20")
    print("       /  \\")
    print("      15   7")

    root1 = build_tree([3, 9, 20, None, None, 15, 7])
    result1 = levelOrder(root1)
    expected1 = [[3], [9, 20], [15, 7]]

    print(f"\nBFS Result: {result1}")
    print(f"DFS Result: {levelOrder_DFS(root1)}")
    print(f"Expected:   {expected1}")
    print(f"✓ PASS" if result1 == expected1 else f"✗ FAIL")

    # Test Case 2: Single node
    print("\n📝 Test Case 2: Single node [1]")
    print("-" * 70)
    print("Tree:")
    print("    1")

    root2 = build_tree([1])
    result2 = levelOrder(root2)
    expected2 = [[1]]

    print(f"\nResult:   {result2}")
    print(f"Expected: {expected2}")
    print(f"✓ PASS" if result2 == expected2 else f"✗ FAIL")

    # Test Case 3: Empty tree
    print("\n📝 Test Case 3: Empty tree []")
    print("-" * 70)
    print("Tree: (empty)")

    root3 = build_tree([])
    result3 = levelOrder(root3)
    expected3 = []

    print(f"\nResult:   {result3}")
    print(f"Expected: {expected3}")
    print(f"✓ PASS" if result3 == expected3 else f"✗ FAIL")

    # Test Case 4: Complete binary tree
    print("\n📝 Test Case 4: Complete binary tree [1,2,3,4,5,6,7]")
    print("-" * 70)
    print("Tree:")
    print("        1")
    print("       / \\")
    print("      2   3")
    print("     / \\ / \\")
    print("    4  5 6  7")

    root4 = build_tree([1, 2, 3, 4, 5, 6, 7])
    result4 = levelOrder(root4)
    expected4 = [[1], [2, 3], [4, 5, 6, 7]]

    print(f"\nResult:   {result4}")
    print(f"Expected: {expected4}")
    print(f"✓ PASS" if result4 == expected4 else f"✗ FAIL")

    # Test Case 5: Skewed tree (left)
    print("\n📝 Test Case 5: Left-skewed tree [1,2,null,3,null,4]")
    print("-" * 70)
    print("Tree:")
    print("    1")
    print("   /")
    print("  2")
    print(" /")
    print("3")
    print("/")
    print("4")

    root5 = build_tree([1, 2, None, 3, None, 4])
    result5 = levelOrder(root5)
    expected5 = [[1], [2], [3], [4]]

    print(f"\nResult:   {result5}")
    print(f"Expected: {expected5}")
    print(f"Explanation: Each level has only 1 node")
    print(f"✓ PASS" if result5 == expected5 else f"✗ FAIL")

    # Test Case 6: Skewed tree (right)
    print("\n📝 Test Case 6: Right-skewed tree [1,null,2,null,3]")
    print("-" * 70)
    print("Tree:")
    print("1")
    print(" \\")
    print("  2")
    print("   \\")
    print("    3")

    root6 = build_tree([1, None, 2, None, 3])
    result6 = levelOrder(root6)
    expected6 = [[1], [2], [3]]

    print(f"\nResult:   {result6}")
    print(f"Expected: {expected6}")
    print(f"✓ PASS" if result6 == expected6 else f"✗ FAIL")

    # Test Case 7: Larger tree
    print("\n📝 Test Case 7: Larger tree")
    print("-" * 70)
    print("Tree:")
    print("         1")
    print("       /   \\")
    print("      2     3")
    print("     / \\     \\")
    print("    4   5     6")
    print("   /          \\")
    print("  7            8")

    root7 = build_tree([1, 2, 3, 4, 5, None, 6, 7, None, None, None, None, 8])
    result7 = levelOrder(root7)
    expected7 = [[1], [2, 3], [4, 5, 6], [7, 8]]

    print(f"\nResult:   {result7}")
    print(f"Expected: {expected7}")
    print(f"✓ PASS" if result7 == expected7 else f"✗ FAIL")

    print("\n" + "="*70)
    print("              ✅ ALL TEST CASES COMPLETED!")
    print("="*70)


if __name__ == "__main__":
    test_levelOrder()


# ============================================================================
#              🎓 LEARNING SUMMARY & KEY TAKEAWAYS
# ============================================================================

"""
🎯 WHAT YOU LEARNED:
-------------------
1. Level Order Traversal = BFS with Queue
2. SNAPSHOT level size BEFORE processing (most important!)
3. Process exactly 'level_size' nodes in each iteration
4. Children added during current level become next level
5. Use deque for O(1) popleft() operation

🔑 KEY PATTERN: "BFS Level-by-Level"
------------------------------------
This pattern applies to:
- Binary Tree Level Order Traversal (this problem)
- Binary Tree Level Order Traversal II (bottom-up)
- Binary Tree Zigzag Level Order Traversal
- Binary Tree Right Side View
- Average of Levels in Binary Tree
- Binary Tree Level Order Traversal (Max in each level)

The Template:
-------------
```python
def bfs_level_order(root):
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)  # ← SNAPSHOT!
        current_level = []

        for i in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(current_level)

    return result
```

💪 SIMILAR PROBLEMS TO PRACTICE:
-------------------------------
1. LeetCode #107: Binary Tree Level Order Traversal II (bottom-up)
2. LeetCode #103: Binary Tree Zigzag Level Order Traversal
3. LeetCode #199: Binary Tree Right Side View
4. LeetCode #637: Average of Levels in Binary Tree
5. LeetCode #513: Find Bottom Left Tree Value
6. LeetCode #515: Find Largest Value in Each Tree Row
7. LeetCode #116: Populating Next Right Pointers in Each Node
8. LeetCode #102: Minimum Depth of Binary Tree

🎉 CONGRATULATIONS!
------------------
You now master the BFS Level Order pattern!

Remember the KEY INSIGHTS:
1. "Snapshot the Wave" - len(queue) before loop
2. "Process One Level" - for loop with level_size
3. "Children Wait" - Added to queue but processed next iteration

Key Differences from Similar Problems:
- Number of Islands: Mark visited cells
- Clone Graph: HashMap to track cloned nodes
- Level Order: Process layer by layer with size snapshot
- Validate BST: Track valid range constraints

🎓 INTERVIEW TIPS:
-----------------
1. Draw the tree and queue state as you explain
2. Emphasize the "snapshot size" step
3. Explain why we need the for loop (to separate levels)
4. Mention time/space complexity
5. Discuss variations (zigzag, right view, etc.)

Explanation Template:
--------------------
"I'll use BFS with a queue. The key insight is to snapshot the queue size
before processing each level, so we know exactly how many nodes belong to
the current level. We process those nodes, adding their children to the queue,
which become the next level. This ensures level-by-level traversal."
"""
