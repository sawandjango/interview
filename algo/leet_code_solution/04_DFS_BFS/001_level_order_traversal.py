"""
LeetCode Problem: Binary Tree Level Order Traversal (LeetCode #102)

Difficulty: Medium

Problem Statement:
Given the root of a binary tree, return the level order traversal of its nodes' values.
(i.e., from left to right, level by level).

Example 1:
    Input: root = [3,9,20,null,null,15,7]
           3
          / \
         9  20
           /  \
          15   7
    Output: [[3],[9,20],[15,7]]

Example 2:
    Input: root = [1]
    Output: [[1]]

Example 3:
    Input: root = []
    Output: []

Constraints:
- The number of nodes in the tree is in the range [0, 2000]
- -1000 <= Node.val <= 1000
"""

from collections import deque
from typing import Optional, List


# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    """
    APPROACH 1: BFS using Queue (Iterative) - RECOMMENDED

    Time Complexity: O(n) where n is number of nodes
    Space Complexity: O(w) where w is maximum width of tree
                      Worst case O(n) for complete binary tree

    Pattern: Level Order Traversal = BFS with Queue

    Key Idea:
    - Use a queue to process nodes level by level
    - For each level, process all nodes in the current queue
    - Add children to queue for next level
    """

    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)  # Number of nodes at current level
            current_level = []

            # Process all nodes at current level
            for i in range(level_size):
                node = queue.popleft()
                current_level.append(node.val)

                # Add children for next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(current_level)

        return result


class SolutionDFS:
    """
    APPROACH 2: DFS using Recursion (Alternative)

    Time Complexity: O(n)
    Space Complexity: O(h) for recursion stack, where h is height
                      O(n) worst case for skewed tree

    Key Idea:
    - Use DFS but track the level/depth
    - Add nodes to their respective level arrays
    """

    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        result = []

        def dfs(node, level):
            if not node:
                return

            # If this is a new level, add a new list
            if level == len(result):
                result.append([])

            # Add current node to its level
            result[level].append(node.val)

            # Recurse for children
            dfs(node.left, level + 1)
            dfs(node.right, level + 1)

        dfs(root, 0)
        return result


# ============= VISUAL EXPLANATION =============

"""
STEP-BY-STEP BFS WALKTHROUGH:

Tree:       3
          /   \
         9    20
             /  \
            15   7

INITIALIZATION:
queue = [3]
result = []

LEVEL 0:
queue = [3]
level_size = 1
current_level = []

  Process node 3:
    current_level = [3]
    Add children: queue = [9, 20]

result = [[3]]
queue = [9, 20]

LEVEL 1:
queue = [9, 20]
level_size = 2
current_level = []

  Process node 9:
    current_level = [9]
    No children

  Process node 20:
    current_level = [9, 20]
    Add children: queue = [15, 7]

result = [[3], [9, 20]]
queue = [15, 7]

LEVEL 2:
queue = [15, 7]
level_size = 2
current_level = []

  Process node 15:
    current_level = [15]
    No children

  Process node 7:
    current_level = [15, 7]
    No children

result = [[3], [9, 20], [15, 7]]
queue = []

DONE!
"""


# ============= COMMON VARIATIONS =============

class SolutionVariations:
    """Level Order Traversal Variations"""

    def levelOrderBottom(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        LeetCode #107: Binary Tree Level Order Traversal II
        Return bottom-up instead of top-down

        Solution: Same as regular level order, then reverse result
        """
        if not root:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)
            current_level = []

            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(current_level)

        return result[::-1]  # Reverse the result


    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        LeetCode #103: Binary Tree Zigzag Level Order Traversal
        Alternate left-to-right and right-to-left

        Level 0: L -> R
        Level 1: R -> L
        Level 2: L -> R
        """
        if not root:
            return []

        result = []
        queue = deque([root])
        left_to_right = True

        while queue:
            level_size = len(queue)
            current_level = deque()  # Use deque for efficient appending

            for _ in range(level_size):
                node = queue.popleft()

                # Alternate append direction
                if left_to_right:
                    current_level.append(node.val)
                else:
                    current_level.appendleft(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(list(current_level))
            left_to_right = not left_to_right

        return result


    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        """
        LeetCode #199: Binary Tree Right Side View
        Return the rightmost node at each level
        """
        if not root:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)

            for i in range(level_size):
                node = queue.popleft()

                # Only add the last node of each level
                if i == level_size - 1:
                    result.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return result


    def averageOfLevels(self, root: Optional[TreeNode]) -> List[float]:
        """
        LeetCode #637: Average of Levels in Binary Tree
        Calculate average value at each level
        """
        if not root:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)
            level_sum = 0

            for _ in range(level_size):
                node = queue.popleft()
                level_sum += node.val

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(level_sum / level_size)

        return result


# ============= TEST CASES =============

def test_level_order():
    """Test cases for level order traversal"""

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

    sol = Solution()

    # Test 1: Example tree
    root1 = build_tree([3, 9, 20, None, None, 15, 7])
    assert sol.levelOrder(root1) == [[3], [9, 20], [15, 7]]
    print("✓ Test 1 passed")

    # Test 2: Single node
    root2 = build_tree([1])
    assert sol.levelOrder(root2) == [[1]]
    print("✓ Test 2 passed")

    # Test 3: Empty tree
    root3 = build_tree([])
    assert sol.levelOrder(root3) == []
    print("✓ Test 3 passed")

    # Test 4: Complete binary tree
    root4 = build_tree([1, 2, 3, 4, 5, 6, 7])
    assert sol.levelOrder(root4) == [[1], [2, 3], [4, 5, 6, 7]]
    print("✓ Test 4 passed")

    # Test 5: Skewed tree (left)
    root5 = build_tree([1, 2, None, 3, None, 4])
    assert sol.levelOrder(root5) == [[1], [2], [3], [4]]
    print("✓ Test 5 passed")

    print("\n✅ All tests passed!")


# ============= KEY TAKEAWAYS =============

"""
WHEN TO USE LEVEL ORDER TRAVERSAL:
1. Need to process tree level by level
2. Find shortest path in tree
3. Get all nodes at a specific depth
4. Serialize/deserialize tree
5. Any "layer by layer" processing

BFS vs DFS for Level Order:
- BFS (Queue): More intuitive, easier to understand
- DFS (Recursion): More concise but less obvious

COMMON MISTAKES:
1. Forgetting to track level size before processing
2. Not handling empty tree
3. Confusing queue.append() with queue.appendleft()
4. Not checking if children exist before adding to queue

OPTIMIZATION TIPS:
- Use deque instead of list for O(1) popleft()
- Pre-allocate result list if tree size is known
- For variations, modify within the same BFS pattern

SIMILAR PROBLEMS:
- #102: Binary Tree Level Order Traversal
- #103: Binary Tree Zigzag Level Order Traversal
- #107: Binary Tree Level Order Traversal II
- #199: Binary Tree Right Side View
- #637: Average of Levels in Binary Tree
- #513: Find Bottom Left Tree Value
- #515: Find Largest Value in Each Tree Row
"""


if __name__ == "__main__":
    test_level_order()
