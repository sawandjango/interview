'''
3. Trees and Graphs
   - Binary Trees
   - Depth-First Search (DFS)
   - Breadth-First Search (BFS)
   - Graph Theory Basics
'''

'''
Binary Trees
1. Maximum Depth of Binary Tree: Find the maximum depth of a binary tree.
2. Validate Binary Search Tree: Check if a binary tree is a valid binary search tree.
3. Symmetric Tree: Determine if a binary tree is symmetric.
4. Binary Tree Level Order Traversal: Perform level order traversal of a binary tree.
5. Lowest Common Ancestor of a Binary Tree: Find the lowest common ancestor of two nodes in a binary tree.

Depth-First Search (DFS)
1. Number of Islands: Count the number of islands in a 2D grid using DFS.
2. Clone Graph: Clone a graph using DFS.
3. Pacific Atlantic Water Flow: Find all points that can reach both the Pacific and Atlantic oceans.
4. Course Schedule: Determine if it's possible to finish all courses given the prerequisites.
5. Word Search: Search for a word in a 2D board.

Breadth-First Search (BFS)
1. Open the Lock: Find the minimum total number of turns to open a lock.
2. Shortest Path in Binary Matrix: Find the shortest path in a binary matrix.
3. 01 Matrix: Update a matrix to the nearest 0 for each cell.
4. Walls and Gates: Fill each empty room with the distance to its nearest gate.
5. Flood Fill: Perform a flood fill algorithm on an image.

Graph Theory Basics
1. Graph Valid Tree: Determine if a given graph is a valid tree.
2. Redundant Connection: Find an edge that, if removed, will make the graph a tree.
3. Find the Town Judge: Find the town judge in a trust graph.
4. All Paths From Source to Target: Find all possible paths from source to target in a directed acyclic graph.
5. Network Delay Time: Find the time it takes for all nodes to receive a signal.
"""


'''
'''
1. Maximum Depth of Binary Tree: Find the maximum depth of a binary tree.

Problem Description
The problem asks you to find the maximum depth (or height) of a binary tree. The maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node. A leaf is a node with no children.

For example, consider a binary tree like this:

    3
   / \
  9  20
    /  \
   15   7

Approach
A typical way to solve this problem is using recursion. We can define the depth of a tree to be the maximum of the depth of its left subtree and its right subtree, plus one (for the root node itself).

Here's how the recursive algorithm works:

If the root is null, the depth is 0.
Otherwise, calculate the depth of the left subtree and the depth of the right subtree.
The depth of the tree is the maximum of these two depths plus one.
'''

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def maxDepth(root):
    # If the node is null, return 0 (base case)
    if root is None:
        return 0
    
    # Recursively find the depth of the left and right subtrees
    left_depth = maxDepth(root.left)
    right_depth = maxDepth(root.right)
    
    # The depth of the tree is the max of left and right depths plus one
    return max(left_depth, right_depth) + 1

# Example Usage
root = TreeNode(3)
root.left = TreeNode(9)
root.right = TreeNode(20, TreeNode(15), TreeNode(7))
print(maxDepth(root))  # Output should be 3
'''
Iteration Example
Let's break down the steps of the function when applied to the example tree:

Start at the root (value 3).
Calculate depth of left subtree (node 9). Since it's a leaf node, its depth is 1.
Calculate depth of right subtree (node 20).
For node 20, calculate depth of left subtree (node 15). It's a leaf node, so depth is 1.
For node 20, calculate depth of right subtree (node 7). It's a leaf node, so depth is 1.
The depth of node 20 is max(1, 1) + 1 = 2.
The depth of the root is max(1, 2) + 1 = 3.
This recursive approach effectively traverses each node of the tree once, leading to a time complexity of O(n), where n is the number of nodes in the tree.

'''

'''
2. Validate Binary Search Tree: Check if a binary tree is a valid binary search tree.

Problem Description
The problem asks to determine if a given binary tree is a valid Binary Search Tree (BST). In a BST, for each node, all nodes in its left subtree must be less than the node's value, and all nodes in its right subtree must be greater.

Approach
The idea is to traverse the tree and ensure that all values adhere to the BST property. We can do this by keeping track of the allowable range of values at each node. When we move left, the maximum allowable value decreases; when we move right, the minimum allowable value increases.

Code Example
Here's how we can implement this in Python:

python
Copy code

'''
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def isValidBST(root, min_val=float('-inf'), max_val=float('inf')):
    # An empty tree is a valid BST
    if root is None:
        return True
    
    # The value of the current node must be within the min_val and max_val
    if not (min_val < root.val < max_val):
        return False

    # Recursively validate the left and right subtrees
    return (isValidBST(root.left, min_val, root.val) and
            isValidBST(root.right, root.val, max_val))

# Example Usage
root = TreeNode(2)
root.left = TreeNode(1)
root.right = TreeNode(3)
print(isValidBST(root))  # Output should be True

'''
Iteration Example
Consider the tree used in the example:

markdown
Copy code
    2
   / \
  1   3
Start at the root (value 2). The range is (-∞, ∞).
Go to the left child (value 1). The range is now (-∞, 2). 1 is within this range.
Go to the right child (value 3). The range is now (2, ∞). 3 is within this range.
Since all nodes satisfy their respective ranges, the tree is a valid BST.
This approach ensures that we respect the BST property at every node, leading to an efficient validation process. The time complexity is O(n), where n is the number of nodes in the tree, as we might have to visit every node in the worst case.

'''

'''
3. Symmetric Tree: Determine if a binary tree is symmetric.


Problem Description
The task is to determine if a binary tree is symmetric around its center. A tree is symmetric if the left subtree is a mirror reflection of the right subtree.

Approach
To solve this, we can recursively compare nodes in the tree. Two nodes are mirror images if:

Their values are the same.
The right subtree of each tree is a mirror reflection of the left subtree of the other tree.
This recursive approach involves comparing the left subtree of the left child with the right subtree of the right child, and the right subtree of the left child with the left subtree of the right child.

Code Example
Here is a Python implementation:
'''

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def isMirror(left, right):
    # If both nodes are null, they are mirror images
    if left is None and right is None:
        return True
    # If only one of them is null, they are not mirror images
    if left is None or right is None:
        return False
    # Two nodes are mirror images if:
    # 1. Their values are the same
    # 2. The right subtree of each is a mirror of the left subtree of the other
    return (left.val == right.val and 
            isMirror(left.right, right.left) and 
            isMirror(left.left, right.right))

def isSymmetric(root):
    # A tree is symmetric if the left subtree is a mirror of the right subtree
    return isMirror(root, root)

# Example Usage
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(2)
root.left.left = TreeNode(3)
root.left.right = TreeNode(4)
root.right.left = TreeNode(4)
root.right.right = TreeNode(3)
print(isSymmetric(root))  # Output should be True

'''
Iteration Example
Consider the tree used in the example:

markdown
Copy code
    1
   / \
  2   2
 / \ / \
3  4 4  3
Start at the root (value 1). Compare its left and right child (both 2).
For the left child (2), compare its left child (3) with the right child's right child (3), and its right child (4) with the right child's left child (4).
Similarly, for the right child (2), compare its left child (4) with the left child's right child (4), and its right child (3) with the left child's left child (3).
Since all corresponding subtrees are mirror images, the tree is symmetric.
This recursive method ensures an efficient way to determine the symmetry of the tree. The time complexity is O(n), as we might have to visit every node in the worst case.

You can use this code and explanation directly in VS Code for further experimentation or modification.
'''

'''
4. Binary Tree Level Order Traversal: Perform level order traversal of a binary tree.
Problem Description
The goal is to perform level order traversal on a binary tree. In level order traversal, nodes are visited level by level from left to right. For this task, we need to return the values of the nodes at each level as a separate list or sublist.

Approach
A common approach to achieving level order traversal is using a queue. The algorithm works as follows:

Initialize a queue and add the root node.
While the queue is not empty, process the nodes of the current level:
Determine the number of nodes at the current level (the current size of the queue).
For each node at this level, remove it from the queue, record its value, and add its left and right children to the queue.
Continue this process until the queue is empty.
Code Example
Here's how we can implement this in Python:

'''

from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def levelOrder(root):
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        level = []

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result

# Example Usage
root = TreeNode(3)
root.left = TreeNode(9)
root.right = TreeNode(20, TreeNode(15), TreeNode(7))
print(levelOrder(root))  # Output should be [[3], [9, 20], [15, 7]]
'''

Iteration Example
Consider the tree used in the example:

markdown
Copy code
    3
   / \
  9  20
    /  \
   15   7
Start at the root (value 3). Add it to the queue.
Process the first level (just the root). The queue now contains 9 and 20.
Process the second level. The queue now contains 15 and 7.
Process the third level. The queue is now empty.
The result is [[3], [9, 20], [15, 7]].
This method efficiently traverses the tree level by level. The time complexity is O(n), where n is the number of nodes in the tree, as each node is processed exactly once
'''

'''
5. Lowest Common Ancestor of a Binary Tree: Find the lowest common ancestor of two nodes in a binary tree.

The "Lowest Common Ancestor (LCA) of a Binary Tree" problem involves finding the lowest (i.e., deepest) node in a binary tree that is an ancestor of both given nodes. The lowest common ancestor is defined between two nodes p and q as the lowest node in the tree that has both p and q as descendants (a node can be a descendant of itself).

Approach
The approach to solving this problem is usually recursive. The idea is to perform a depth-first search (DFS) where we recursively search for the nodes p and q in the left and right subtrees. The key points are:

If either p or q matches the current node, we return the current node.
We recursively check the left and right subtrees for occurrences of the nodes p and q.
If both the left and right subtree return non-null values, it means we have found the lowest common ancestor.
If only one of the subtrees returns a non-null (either left or right), it means this subtree contains one of p or q and is part of the path to the LCA.
Code Example
Here's the Python implementation:

'''


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def lowestCommonAncestor(root, p, q):
    if not root or root == p or root == q:
        return root

    # Search in left and right subtrees
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)

    # If both left and right are not null, root is the LCA
    if left and right:
        return root
    
    # Otherwise, return the non-null value
    return left if left else right

# Example Usage
root = TreeNode(3)
root.left = TreeNode(5)
root.right = TreeNode(1)
root.left.left = TreeNode(6)
root.left.right = TreeNode(2)
root.right.left = TreeNode(0)
root.right.right = TreeNode(8)
p = root.left  # Node with value 5
q = root.right # Node with value 1
print(lowestCommonAncestor(root, p, q).val)  # Output should be 3
'''

Explanation
In the example, the tree is:

markdown
Copy code
    3
   / \
  5   1
 /|  / \
6 2 0   8
The LCA of nodes 5 and 1 is 3.
The function searches both subtrees of each node.
It finds that node 5 is present in the left subtree and node 1 in the right subtree of node 3.
Since both subtrees return a non-null value, node 3 is identified as the LCA.
This recursive approach efficiently solves the problem with a time complexity of O(n), where n is the number of nodes in the tree, as it potentially visits every node.

'''

'''
1. Number of Islands: Count the number of islands in a 2D grid using DFS.

Problem Description: Number of Islands
The "Number of Islands" problem is a classic in computer science, often used to teach depth-first search (DFS). The problem statement is as follows:

Given a 2D grid map of '1's (land) and '0's (water), count the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.

Approach
The primary approach to solving this problem is to use Depth-First Search (DFS). Here's a step-by-step breakdown of the algorithm:

Iterate over each cell of the grid.
When a land cell ('1') is found, increment the islands count and then perform a DFS from that cell.
In the DFS, mark the current cell as visited (turn '1' to '0' or use a separate visited grid) and then recursively call DFS for all its adjacent land cells (up, down, left, right).
The DFS will visit all cells of the current island and mark them as visited.
Continue the main iteration until all cells are processed.
Code Example
Here's a Python implementation of the algorithm:

'''


def numIslands(grid):
    if not grid:
        return 0

    def dfs(i, j):
        # Check if current cell is out of bounds or water
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]) or grid[i][j] == '0':
            return

        # Mark the current cell as visited
        grid[i][j] = '0'

        # Recursively call DFS on all adjacent cells
        dfs(i + 1, j)
        dfs(i - 1, j)
        dfs(i, j + 1)
        dfs(i, j - 1)

    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '1':
                dfs(i, j)
                count += 1

    return count

# Example Usage
grid = [
    ["1", "1", "0", "0", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "1", "0", "0"],
    ["0", "0", "0", "1", "1"]
]
print(numIslands(grid))  # Output should be 3

'''
Explanation
In the example grid, there are three islands:

The first one is formed by the first two rows.
The second one is the single '1' in the third row.
The third one is formed by the two '1's in the bottom right corner.
The DFS function iteratively marks all adjacent lands of an island, effectively sinking it before moving on to find the next island.

This algorithm efficiently solves the problem with a time complexity of O(MxN), where M is the number of rows and N is the number of columns in the grid, as it visits each cell at least once.
'''

'''
2. Clone Graph: Clone a graph using DFS.


Problem Description: Clone Graph
The "Clone Graph" problem is a common algorithmic challenge involving graph theory. The problem statement is as follows:

Given a reference to a node in a connected, undirected graph, return a deep copy (clone) of the graph. Each node in the graph contains a value (val) and a list (neighbors) of its neighbors. The graph is represented in the following way: the number of nodes is within the range [0, 100] and each node's value is a unique integer in the range [1, 100]. A node might have no neighbors or might be connected to all other nodes.

Approach
The approach to cloning a graph typically involves a depth-first search (DFS) traversal. Here's the general idea:

Traverse the graph starting from the given node.
As you visit each node, create a clone of it and store the mapping of the original node to its clone in a hash map. This ensures that each node is cloned only once and helps in retrieving the clone node during recursive calls.
Recursively clone the neighbors of each node by exploring them using DFS.
Return the clone of the original starting node.
Code Example
Here's how this can be implemented in Python:

'''

class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def cloneGraph(node):
    old_to_new = {}

    def dfs(node):
        if node in old_to_new:
            return old_to_new[node]

        # Clone the node
        clone = Node(node.val)
        old_to_new[node] = clone

        # Recursively clone the neighbors
        for neighbor in node.neighbors:
            clone.neighbors.append(dfs(neighbor))
        
        return clone

    return dfs(node) if node else None

# Example Usage
node1 = Node(1)
node2 = Node(2)
node3 = Node(3)
node4 = Node(4)
node1.neighbors = [node2, node4]
node2.neighbors = [node1, node3]
node3.neighbors = [node2, node4]
node4.neighbors = [node1, node3]
cloned_graph = cloneGraph(node1)

'''
Explanation
In the example, the graph is a square where each corner is connected to two other corners. The DFS traversal clones each node and its neighbors. The hash map (old_to_new) ensures that each node is cloned only once and is reused when a neighbor is revisited, preserving the graph structure in the clone.

This approach efficiently clones the graph with a time complexity of O(N), where N is the number of nodes in the graph, as each node and edge is visited once.

'''

'''
3. Pacific Atlantic Water Flow: Find all points that can reach both the Pacific and Atlantic oceans.

'''
'''
Problem Description
Given an m x n matrix of non-negative integers representing the height of each unit cell in a continent, the "Pacific Ocean" touches the left and top edges of the matrix, and the "Atlantic Ocean" touches the right and bottom edges.

Water can only flow from a cell to another one with height equal or lower. Your task is to find the list of grid coordinates where water can flow to both the Pacific and Atlantic oceans.

Approach and Explanation
To solve this problem, we can use a depth-first search (DFS) from the oceans to the land. Instead of starting from every cell and checking if it can reach both oceans, we start from the oceans and mark cells that can reach them. This way, we avoid redundant calculations.

Initialization:

Create two matrices (or sets) to keep track of cells that can reach the Pacific and Atlantic oceans, respectively.
DFS from the Oceans:

Perform a DFS from all cells adjacent to the Pacific Ocean and mark reachable cells in the Pacific matrix/set.
Repeat the process for the Atlantic Ocean.
Find Common Cells:

A cell that can reach both oceans will be marked in both matrices/sets. The intersection of these gives the required result.
DFS Function:

The DFS function should check the base case (bounds of the matrix and height comparison).
Recursively call DFS for adjacent cells (up, down, left, right) that are higher or equal in height.
Implementation
Here's how you can implement this in Python:
'''
def pacificAtlantic(heights):
    if not heights:
        return []

    def dfs(x, y, visited, prevHeight):
        if (x, y) in visited or x < 0 or y < 0 or x >= len(heights) or y >= len(heights[0]) or heights[x][y] < prevHeight:
            return
        visited.add((x, y))
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            dfs(x + dx, y + dy, visited, heights[x][y])

    m, n = len(heights), len(heights[0])
    pacific_reachable = set()
    atlantic_reachable = set()

    # Perform DFS from each ocean
    for i in range(m):
        dfs(i, 0, pacific_reachable, heights[i][0])
        dfs(i, n - 1, atlantic_reachable, heights[i][n - 1])
    for j in range(n):
        dfs(0, j, pacific_reachable, heights[0][j])
        dfs(m - 1, j, atlantic_reachable, heights[m - 1][j])

    # Find common cells that can reach both oceans
    return list(pacific_reachable & atlantic_reachable)

# Example Usage
heights = [
    [1, 2, 2, 3, 5],
    [3, 2, 3, 4, 4],
    [2, 4, 5, 3, 1],
    [6, 7, 1, 4, 5],
    [5, 1, 1, 2, 4]
]
print(pacificAtlantic(heights))
'''
This implementation starts the DFS from the edges adjacent to the oceans and works its way inwards, marking the cells that can reach each ocean. The intersection of these sets gives the coordinates where water can flow to both oceans.

The time complexity of this approach is O(m * n), where m and n are the dimensions of the input matrix, because in the worst case, the DFS visits each cell once. The space complexity is also O(m * n) due to the additional space used for the visited sets and the recursion stack.
'''    