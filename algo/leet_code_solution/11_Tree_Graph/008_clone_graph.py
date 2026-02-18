"""
LeetCode Problem #133: Clone Graph

Difficulty: Medium
Topics: Graph, DFS, BFS, Hash Table
Companies: Facebook, Amazon, Google, Microsoft, Uber

================================================================================
                    📚 QUICK REFERENCE - WHAT'S IN THIS FILE
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                        📖 TABLE OF CONTENTS                                 │
├──────┬──────────────────────────────────────────┬───────────────────────────┤
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
│ 4    │ 💡 SOLUTION 1: DFS with HashMap ⭐    │ • WHY choose? (Pros/Cons)     │
│      │    (RECOMMENDED)                     │ • WHEN to use?                │
│      │                                      │ • Step-by-step walkthrough    │
├──────┼──────────────────────────────────────┼───────────────────────────────┤
│ 5    │ 💡 SOLUTION 2: BFS with Queue        │ • WHY choose? (Pros/Cons)     │
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
│ ANALOGY          │ "Phone Book" - Old Node → New Node mapping!            │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ PATTERN          │ "HashMap Tracking" - Track cloned nodes to avoid loops  │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ BASE CASE        │ If None → Return None | If cloned → Return clone       │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ DEFAULT SOLUTION │ DFS with HashMap (Use in 90% of cases!)                │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ TIME COMPLEXITY  │ O(N+E) - Visit N nodes + E edges                       │
├──────────────────┼─────────────────────────────────────────────────────────┤
│ SPACE COMPLEXITY │ O(N) - HashMap stores N nodes                          │
└──────────────────┴─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        ⚡ QUICK DECISION TABLE                              │
├────────────────────────────────┬────────────────────────────────────────────┤
│ SITUATION                      │ WHICH SOLUTION TO USE?                    │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Normal interview               │ ✅ Solution 1 (DFS with HashMap)          │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Want simplest code             │ ✅ Solution 1 (Most natural)              │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Prefer iteration               │ ⚠️  Solution 2 (BFS with Queue)           │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Deep graphs (stack risk)       │ ⚠️  Solution 2 (BFS avoids stack)         │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Want to show off               │ 🎯 Write Sol 1, then mention Sol 2       │
└────────────────────────────────┴────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                     📊 SOLUTION COMPARISON TABLE                            │
├──────────────────┬─────────────────────────┬────────────────────────────────┤
│ CRITERIA         │ SOLUTION 1 (DFS)        │ SOLUTION 2 (BFS Queue)        │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Code Length      │ ⭐⭐⭐⭐⭐ Very short     │ ⭐⭐⭐ More code                │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Readability      │ ⭐⭐⭐⭐⭐ Crystal clear  │ ⭐⭐⭐⭐ Clear                  │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Interview Speed  │ ⭐⭐⭐⭐⭐ Lightning fast │ ⭐⭐⭐ Takes longer             │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Stack Safety     │ ⭐⭐⭐ Deep recursion    │ ⭐⭐⭐⭐⭐ No stack overflow     │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ Intuitiveness    │ ⭐⭐⭐⭐⭐ Very natural   │ ⭐⭐⭐⭐ Also intuitive         │
├──────────────────┼─────────────────────────┼────────────────────────────────┤
│ When to Use      │ 90% of cases (DEFAULT)  │ Very deep graphs only         │
└──────────────────┴─────────────────────────┴────────────────────────────────┘

⏱️  TIME TO MASTER: 20-25 minutes
🎯 DIFFICULTY: Medium
💡 TIP: Remember "Old → New HashMap" to track cloned nodes!
🔥 POPULAR: Common graph cloning interview question!

================================================================================
                           🎯 PROBLEM UNDERSTANDING
================================================================================

WHAT IS THE PROBLEM?
--------------------
Imagine you have a graph (like a social network). You need to make a COMPLETE
COPY of it - not just copying pointers, but creating entirely new nodes!

REAL WORLD ANALOGY:
------------------
Think of it like copying a FRIEND NETWORK:
- You (Node 1) have friends: [Node 2, Node 4]
- Node 2 has friends: [Node 1, Node 3]
- Node 3 has friends: [Node 2, Node 4]
- Node 4 has friends: [Node 1, Node 3]

You need to create a NEW network with NEW people, but the SAME friendships!

================================================================================
                            📝 FORMAL PROBLEM
================================================================================

Given a reference of a node in a connected undirected graph, return a deep
copy (clone) of the graph.

Each node in the graph contains:
- A value (val)
- A list of its neighbors (neighbors)

class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

Test case format:
For simplicity, each node's value is the same as the node's index (1-indexed).
For example, the first node with val == 1, the second node with val == 2, etc.
The graph is represented in the test case using an adjacency list.

Example 1:
----------
Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
Output: [[2,4],[1,3],[2,4],[1,3]]
Explanation:
There are 4 nodes in the graph.
Node 1: val = 1, neighbors = [2, 4]
Node 2: val = 2, neighbors = [1, 3]
Node 3: val = 3, neighbors = [2, 4]
Node 4: val = 4, neighbors = [1, 3]

Visual representation:
       1 -------- 2
       |          |
       |          |
       4 -------- 3

Example 2:
----------
Input: adjList = [[]]
Output: [[]]
Explanation: Single node with no neighbors.

Example 3:
----------
Input: adjList = []
Output: []
Explanation: Empty graph.

Constraints:
------------
* The number of nodes in the graph is in the range [0, 100].
* 1 <= Node.val <= 100
* Node.val is unique for each node.
* There are no repeated edges and no self-loops in the graph.
* The Graph is connected and all nodes can be visited starting from the given node.

================================================================================
                         🧠 KEY INSIGHTS TO REMEMBER
================================================================================

THE MAIN CHALLENGE:
------------------
❌ Can't just copy node by node - you'll get infinite loops!
❌ Can't just copy neighbors directly - they're old references!
✅ Need to track which nodes you've already cloned!

THE MAGIC TRICK: "Old Node → New Node" MAPPING!
-----------------------------------------------
Think of it as a DICTIONARY/PHONE BOOK:
- Old Node 1 → New Node 1
- Old Node 2 → New Node 2
- Old Node 3 → New Node 3
- Old Node 4 → New Node 4

When you see an old friend, check your phone book:
- Already cloned? Use the cloned version!
- Not cloned yet? Clone them first, add to phone book!

================================================================================
                          💡 SOLUTION APPROACHES
================================================================================
"""

# Definition for a Node.
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


# ============================================================================
#                        APPROACH 1: DFS (RECURSIVE)
# ============================================================================

def cloneGraph_DFS(node):
    """
    🎯 APPROACH 1: DFS with Recursion (MOST INTUITIVE!)

    TIME COMPLEXITY: O(N + E) where N = nodes, E = edges
    SPACE COMPLEXITY: O(N) for the hashmap + O(N) for recursion stack

    🧠 MEMORIZATION TRICK: "Clone & Connect"
    ----------------------------------------
    Think: "Have I cloned you before?"
    - YES → Return the clone from my map
    - NO  → Clone you, then clone all your friends!

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. BASE CASE: If node is None, return None
    2. CHECK MAP: Already cloned? Return it!
    3. CLONE NODE: Create new node with same value
    4. ADD TO MAP: old_node → new_node
    5. CLONE NEIGHBORS: Recursively clone each neighbor
    6. RETURN: The cloned node
    """
    if not node:
        return None

    # This is our "phone book" - maps old nodes to new nodes
    old_to_new = {}

    def dfs(node):
        # 📞 Already in our phone book? Return the cloned version!
        if node in old_to_new:
            return old_to_new[node]

        # 🆕 Create a NEW person with the same name (value)
        clone = Node(node.val)

        # 📝 Add to phone book IMMEDIATELY (prevents infinite loops!)
        old_to_new[node] = clone

        # 👥 Clone all their friends (neighbors)
        for neighbor in node.neighbors:
            clone.neighbors.append(dfs(neighbor))

        return clone

    return dfs(node)


# ============================================================================
#                        APPROACH 2: BFS (ITERATIVE)
# ============================================================================

def cloneGraph_BFS(node):
    """
    🎯 APPROACH 2: BFS with Queue (LEVEL BY LEVEL)

    TIME COMPLEXITY: O(N + E) where N = nodes, E = edges
    SPACE COMPLEXITY: O(N) for the hashmap + O(N) for the queue

    🧠 MEMORIZATION TRICK: "Clone Level by Level"
    ---------------------------------------------
    Think: Process one person at a time in a queue
    - Clone the person
    - Add them to phone book
    - Clone their friends

    📝 STEP-BY-STEP ALGORITHM:
    --------------------------
    1. BASE CASE: If node is None, return None
    2. CREATE QUEUE: Start with original node
    3. CLONE ROOT: Create clone and add to map
    4. PROCESS QUEUE:
       - For each node in queue
       - For each neighbor:
         * Not cloned? Clone and add to queue
         * Connect cloned node to cloned neighbor
    5. RETURN: The cloned root
    """
    if not node:
        return None

    from collections import deque

    # Phone book: old → new mapping
    old_to_new = {}

    # Clone the starting node
    old_to_new[node] = Node(node.val)

    # Queue for BFS
    queue = deque([node])

    while queue:
        current = queue.popleft()

        # Process each neighbor
        for neighbor in current.neighbors:
            # Haven't cloned this neighbor yet?
            if neighbor not in old_to_new:
                # Clone it!
                old_to_new[neighbor] = Node(neighbor.val)
                # Add to queue to process its neighbors later
                queue.append(neighbor)

            # Connect the cloned current node to cloned neighbor
            old_to_new[current].neighbors.append(old_to_new[neighbor])

    return old_to_new[node]


# ============================================================================
#                    🎨 VISUAL WALKTHROUGH EXAMPLE
# ============================================================================

"""
Let's walk through Example 1: [[2,4],[1,3],[2,4],[1,3]]

Original Graph:
       1 -------- 2
       |          |
       |          |
       4 -------- 3

STEP-BY-STEP DFS:
-----------------

1. Start at Node 1
   - Not in map → Create clone: Node(1)
   - Add to map: {1 → Node(1)}
   - Clone neighbors [2, 4]

2. Clone Node 2 (from Node 1's neighbor)
   - Not in map → Create clone: Node(2)
   - Add to map: {1 → Node(1), 2 → Node(2)}
   - Clone neighbors [1, 3]

3. Clone Node 1 (from Node 2's neighbor)
   - Already in map! Return existing clone

4. Clone Node 3 (from Node 2's neighbor)
   - Not in map → Create clone: Node(3)
   - Add to map: {1 → Node(1), 2 → Node(2), 3 → Node(3)}
   - Clone neighbors [2, 4]

5. Clone Node 2 (from Node 3's neighbor)
   - Already in map! Return existing clone

6. Clone Node 4 (from Node 3's neighbor)
   - Not in map → Create clone: Node(4)
   - Add to map: {1 → Node(1), 2 → Node(2), 3 → Node(3), 4 → Node(4)}
   - Clone neighbors [1, 3]

7. Clone Node 1 (from Node 4's neighbor)
   - Already in map! Return existing clone

8. Clone Node 3 (from Node 4's neighbor)
   - Already in map! Return existing clone

9. Clone Node 4 (from Node 1's neighbor)
   - Already in map! Return existing clone

DONE! Cloned Graph:
       1' ------- 2'
       |          |
       |          |
       4' ------- 3'
"""

# ============================================================================
#              🎯 MEMORY TRICKS & COMMON MISTAKES
# ============================================================================

"""
🧠 HOW TO REMEMBER THIS SOLUTION:
---------------------------------
1. "PHONE BOOK" → Use a HashMap (old → new)
2. "CHECK FIRST" → Always check if already cloned
3. "CLONE EARLY" → Add to map BEFORE processing neighbors
4. "RECURSIVE" → DFS is natural for graphs

❌ COMMON MISTAKES TO AVOID:
----------------------------
1. ❌ Forgetting to add to map before processing neighbors
      → Causes infinite recursion!

2. ❌ Not checking if node is None
      → Causes NullPointerException!

3. ❌ Cloning neighbors directly without checking map
      → Creates duplicate clones!

4. ❌ Not using a map at all
      → Infinite loops everywhere!

✅ PRO TIPS:
-----------
1. DFS is more intuitive (use recursion)
2. BFS is better if you want level-by-level processing
3. The MAP is the KEY - without it, you're lost!
4. Always add to map IMMEDIATELY after creating clone
"""

# ============================================================================
#                         🧪 TEST CASES
# ============================================================================

def buildGraph(adjList):
    """Helper function to build graph from adjacency list"""
    if not adjList:
        return None

    nodes = {i + 1: Node(i + 1) for i in range(len(adjList))}

    for i, neighbors in enumerate(adjList):
        node = nodes[i + 1]
        for neighbor_val in neighbors:
            node.neighbors.append(nodes[neighbor_val])

    return nodes[1] if nodes else None


def printGraph(node):
    """Helper function to print graph"""
    if not node:
        print("[]")
        return

    visited = set()
    result = []

    def dfs(node):
        if node.val in visited:
            return
        visited.add(node.val)
        neighbors = [n.val for n in node.neighbors]
        result.append([node.val, neighbors])
        for neighbor in node.neighbors:
            dfs(neighbor)

    dfs(node)
    for val, neighbors in sorted(result):
        print(f"Node {val}: neighbors = {neighbors}")


if __name__ == "__main__":
    print("="*70)
    print("                    CLONE GRAPH - TEST CASES")
    print("="*70)

    # Test Case 1: 4-node cycle graph
    print("\n📝 Test Case 1: 4-node cycle graph")
    print("-" * 70)
    adjList1 = [[2,4],[1,3],[2,4],[1,3]]
    graph1 = buildGraph(adjList1)
    print("Original Graph:")
    printGraph(graph1)

    cloned1 = cloneGraph_DFS(graph1)
    print("\nCloned Graph:")
    printGraph(cloned1)

    # Test Case 2: Single node
    print("\n📝 Test Case 2: Single node")
    print("-" * 70)
    adjList2 = [[]]
    graph2 = buildGraph(adjList2)
    print("Original Graph:")
    printGraph(graph2)

    cloned2 = cloneGraph_DFS(graph2)
    print("\nCloned Graph:")
    printGraph(cloned2)

    # Test Case 3: Empty graph
    print("\n📝 Test Case 3: Empty graph")
    print("-" * 70)
    adjList3 = []
    graph3 = buildGraph(adjList3)
    print("Original Graph:")
    printGraph(graph3)

    cloned3 = cloneGraph_DFS(graph3)
    print("\nCloned Graph:")
    printGraph(cloned3)

    print("\n" + "="*70)
    print("              ✅ ALL TEST CASES COMPLETED!")
    print("="*70)


# ============================================================================
#              🎓 LEARNING SUMMARY & KEY TAKEAWAYS
# ============================================================================

"""
🎯 WHAT YOU LEARNED:
-------------------
1. Graph cloning requires a MAPPING (old → new)
2. DFS and BFS both work - choose your favorite
3. Add to map BEFORE processing neighbors (critical!)
4. HashMap prevents infinite loops

🔑 KEY PATTERN: "Clone with HashMap"
------------------------------------
This pattern applies to:
- Clone Graph (this problem)
- Copy List with Random Pointer
- Deep Copy of any connected structure

💪 PRACTICE VARIATIONS:
----------------------
Try these similar problems:
1. LeetCode #138: Copy List with Random Pointer
2. LeetCode #1485: Clone Binary Tree With Random Pointer
3. LeetCode #1490: Clone N-ary Tree

🎉 CONGRATULATIONS!
------------------
You now understand how to clone a graph!
Remember: "Phone Book" (HashMap) is your best friend!
"""
