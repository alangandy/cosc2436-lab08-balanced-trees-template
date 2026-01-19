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

## Your Tasks

### Task 1: Implement `height()`
Return the height of a node (0 if `None`).

### Task 2: Implement `balance_factor()`
Calculate: `height(left) - height(right)`

### Task 3: Implement `rotate_right()`
Perform right rotation:
```python
#     y                x
#    / \              / \
#   x   C    →       A   y
#  / \                  / \
# A   B                B   C
```
- `x` becomes the new root
- `y` becomes `x`'s right child
- `x`'s right child (`B`) becomes `y`'s left child
- Update heights!

### Task 4: Implement `rotate_left()`
Mirror of right rotation.

### Task 5: Implement `_insert()`
Insert with rebalancing:
1. Standard BST insert
2. Update height: `1 + max(height(left), height(right))`
3. Check balance factor
4. If unbalanced, determine case and rotate:
   - LL: `rotate_right(node)`
   - RR: `rotate_left(node)`
   - LR: `rotate_left(node.left)`, then `rotate_right(node)`
   - RL: `rotate_right(node.right)`, then `rotate_left(node)`

## Example

```python
avl = AVLTree()
for val in [10, 20, 30]:  # Would be unbalanced in regular BST
    avl.insert(val)

# Regular BST:     AVL Tree:
#   10                20
#    \               /  \
#     20     →      10  30
#      \
#       30

>>> avl.inorder()
[10, 20, 30]
```

## Testing
```bash
python -m pytest tests/ -v
```

## Hints
- Always update heights after any structural change
- Determine rotation case by checking balance factors:
  - Node balance > 1 and left child balance >= 0: LL case
  - Node balance > 1 and left child balance < 0: LR case
  - Node balance < -1 and right child balance <= 0: RR case
  - Node balance < -1 and right child balance > 0: RL case
- Return the new root after rotation!

## Submission
Commit and push your completed `avl_tree.py` file.
