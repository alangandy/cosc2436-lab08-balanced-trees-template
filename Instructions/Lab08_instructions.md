# Lab 08: Balanced Trees (AVL Trees)

## Overview
In this lab, you will implement an **AVL Tree**, a self-balancing binary search tree from Chapter 8 of "Grokking Algorithms."

## Learning Objectives
- Understand why balanced trees matter
- Implement AVL tree rotations
- Maintain balance after insertions
- Understand balance factors

## Background

### The Problem with Unbalanced BSTs
A regular BST can become unbalanced:
```
Insert 1, 2, 3, 4, 5 in order:
    1
     \
      2
       \
        3
         \
          4
           \
            5
```
This "linked list" shape gives O(n) operations instead of O(log n)!

### AVL Trees
AVL trees maintain balance by ensuring:
- **Balance factor** = height(left) - height(right)
- Balance factor must be -1, 0, or 1 for every node
- If violated after insert, perform **rotations** to rebalance

### Rotations
Four cases require rotation:

**Left-Left (LL)**: Right rotation
```
    z                y
   /                / \
  y      →         x   z
 /
x
```

**Right-Right (RR)**: Left rotation
```
z                    y
 \                  / \
  y       →        z   x
   \
    x
```

**Left-Right (LR)**: Left rotation on left child, then right rotation
**Right-Left (RL)**: Right rotation on right child, then left rotation

---

## Complete Solutions

### AVLNode Class (provided)

```python
class AVLNode:
    """AVL tree node with height tracking."""
    def __init__(self, value: Any):
        self.value = value
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height: int = 1
```

---

### AVLTree Class - Complete Implementation

```python
class AVLTree:
    """Self-balancing AVL tree."""
    
    def __init__(self):
        self.root: Optional[AVLNode] = None
    
    def height(self, node: Optional[AVLNode]) -> int:
        """Get height of node (None = 0)."""
        if node is None:
            return 0
        return node.height
    
    def balance_factor(self, node: AVLNode) -> int:
        """
        Calculate balance factor: height(left) - height(right)
        
        From Chapter 8:
        - Balance factor of -1, 0, or 1 is balanced
        - Other values require rotation
        """
        return self.height(node.left) - self.height(node.right)
    
    def rotate_right(self, y: AVLNode) -> AVLNode:
        """
        Right rotation for left-heavy tree.
        
            y                x
           / \              / \
          x   C    -->     A   y
         / \                  / \
        A   B                B   C
        """
        x = y.left
        B = x.right
        
        # Perform rotation
        x.right = y
        y.left = B
        
        # Update heights (y first since it's now lower)
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        x.height = 1 + max(self.height(x.left), self.height(x.right))
        
        # Return new root
        return x
    
    def rotate_left(self, x: AVLNode) -> AVLNode:
        """
        Left rotation for right-heavy tree.
        
          x                  y
         / \                / \
        A   y     -->      x   C
           / \            / \
          B   C          A   B
        """
        y = x.right
        B = y.left
        
        # Perform rotation
        y.left = x
        x.right = B
        
        # Update heights (x first since it's now lower)
        x.height = 1 + max(self.height(x.left), self.height(x.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        
        # Return new root
        return y
    
    def insert(self, value: Any) -> None:
        """Insert value and rebalance."""
        self.root = self._insert(self.root, value)
    
    def _insert(self, node: Optional[AVLNode], value: Any) -> AVLNode:
        """Recursive insert with rebalancing."""
        # Step 1: Standard BST insert
        if node is None:
            return AVLNode(value)
        
        if value < node.value:
            node.left = self._insert(node.left, value)
        else:
            node.right = self._insert(node.right, value)
        
        # Step 2: Update height of this node
        node.height = 1 + max(self.height(node.left), self.height(node.right))
        
        # Step 3: Get balance factor
        balance = self.balance_factor(node)
        
        # Step 4: If unbalanced, there are 4 cases
        
        # Left-Left Case (LL): Right rotation
        if balance > 1 and value < node.left.value:
            return self.rotate_right(node)
        
        # Right-Right Case (RR): Left rotation
        if balance < -1 and value > node.right.value:
            return self.rotate_left(node)
        
        # Left-Right Case (LR): Left rotation on left child, then right rotation
        if balance > 1 and value > node.left.value:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        
        # Right-Left Case (RL): Right rotation on right child, then left rotation
        if balance < -1 and value < node.right.value:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        
        # Return the (unchanged) node pointer
        return node
    
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
```

---

## How Each Method Works

### `height(node)`
- If node is `None`, return 0
- Otherwise, return `node.height`

### `balance_factor(node)`
- Calculate: `height(left subtree) - height(right subtree)`
- Balanced if result is -1, 0, or 1
- Unbalanced if result is < -1 or > 1

### `rotate_right(y)`
```
    y                x
   / \              / \
  x   C    -->     A   y
 / \                  / \
A   B                B   C
```
1. Save `x = y.left` and `B = x.right`
2. Make `y` the right child of `x`: `x.right = y`
3. Make `B` the left child of `y`: `y.left = B`
4. Update heights (y first, then x)
5. Return `x` as the new root

### `rotate_left(x)`
Mirror of rotate_right.

### `_insert(node, value)`
1. **Standard BST insert**: Recursively find position and create node
2. **Update height**: `1 + max(height(left), height(right))`
3. **Check balance**: Calculate balance factor
4. **Rebalance if needed** (4 cases):
   - **LL** (balance > 1, value < left.value): `rotate_right(node)`
   - **RR** (balance < -1, value > right.value): `rotate_left(node)`
   - **LR** (balance > 1, value > left.value): `rotate_left(left)`, then `rotate_right(node)`
   - **RL** (balance < -1, value < right.value): `rotate_right(right)`, then `rotate_left(node)`

---

## Example Usage

```python
avl = AVLTree()

# Insert values that would create unbalanced BST
for val in [10, 20, 30]:
    avl.insert(val)

# Regular BST would be:     AVL Tree becomes:
#   10                           20
#    \                          /  \
#     20          -->          10  30
#      \
#       30

>>> avl.inorder()
[10, 20, 30]

# More complex example
avl2 = AVLTree()
for val in [10, 20, 30, 40, 50, 25]:
    avl2.insert(val)

>>> avl2.inorder()
[10, 20, 25, 30, 40, 50]

# Tree stays balanced with height ~log(n)
```

---

## Testing
```bash
python -m pytest tests/ -v
```

## Submission
Commit and push your completed `avl_tree.py` file.
