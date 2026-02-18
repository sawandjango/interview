
1. Pre-order Traversal
In pre-order traversal, the nodes are recursively visited in this order:

Visit the root.
Traverse the left subtree.
Traverse the right subtree.
This traversal is used to create a copy of the tree, get a prefix expression on an expression tree, etc.

Code Example
python
Copy code
def preorderTraversal(root):
    if not root:
        return []
    
    # Visiting the root, then left and right subtrees
    return [root.val] + preorderTraversal(root.left) + preorderTraversal(root.right)
2. In-order Traversal
In in-order traversal, the nodes are recursively visited in this order:

Traverse the left subtree.
Visit the root.
Traverse the right subtree.
This traversal is commonly used for binary search trees where it returns values in sorted order.

Code Example
python
Copy code
def inorderTraversal(root):
    if not root:
        return []

    # Visiting left subtree, then root, and then right subtree
    return inorderTraversal(root.left) + [root.val] + inorderTraversal(root.right)
3. Post-order Traversal
In post-order traversal, the nodes are recursively visited in this order:

Traverse the left subtree.
Traverse the right subtree.
Visit the root.
This traversal is used to delete the tree, get the postfix expression of an expression tree, etc.

Code Example
python
Copy code
def postorderTraversal(root):
    if not root:
        return []
    
    # Visiting left and right subtrees, then the root
    return postorderTraversal(root.left) + postorderTraversal(root.right) + [root.val]
Each of these traversals can be implemented iteratively as well, often using a stack to maintain the order of nodes to be visited.