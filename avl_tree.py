"""
Lab 08: Balanced Trees
Implement AVL tree from Chapter 8.

Chapter 8 covers:
- BST problems (unbalanced = O(n))
- AVL Trees (self-balancing)
- Splay Trees
- B-Trees
"""
from typing import Optional, Any, List


class AVLNode:
    """AVL tree node with height tracking."""
    def __init__(self, value: Any):
        self.value = value
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height: int = 1


class AVLTree:
    """Self-balancing AVL tree."""
    
    def __init__(self):
        self.root: Optional[AVLNode] = None
    
    def height(self, node: Optional[AVLNode]) -> int:
        """Get height of node (None = 0)."""
        # TODO: Return node.height if node exists, else 0
        pass
    
    def balance_factor(self, node: AVLNode) -> int:
        """
        Calculate balance factor: height(left) - height(right)
        
        From Chapter 8:
        - Balance factor of -1, 0, or 1 is balanced
        - Other values require rotation
        """
        # TODO: Return height(left) - height(right)
        pass
    
    def rotate_right(self, y: AVLNode) -> AVLNode:
        """
        Right rotation for left-heavy tree.
        
            y                x
           / \              / \
          x   C    -->     A   y
         / \                  / \
        A   B                B   C
        """
        # TODO: Implement right rotation
        pass
    
    def rotate_left(self, x: AVLNode) -> AVLNode:
        """Left rotation for right-heavy tree."""
        # TODO: Implement left rotation
        pass
    
    def insert(self, value: Any) -> None:
        """Insert value and rebalance."""
        self.root = self._insert(self.root, value)
    
    def _insert(self, node: Optional[AVLNode], value: Any) -> AVLNode:
        """Recursive insert with rebalancing."""
        # TODO: Implement AVL insert
        # 1. Standard BST insert
        # 2. Update height
        # 3. Check balance factor
        # 4. Rotate if needed (4 cases: LL, RR, LR, RL)
        pass
    
    def inorder(self) -> List[Any]:
        """Return sorted values."""
        result = []
        self._inorder(self.root, result)
        return result
    
    def _inorder(self, node: Optional[AVLNode], result: List) -> None:
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)
