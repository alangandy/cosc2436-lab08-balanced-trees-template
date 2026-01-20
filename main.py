#!/usr/bin/env python3
"""
Lab 08: AVL Trees - Interactive Tutorial
=========================================

🎯 GOAL: Implement self-balancing AVL tree in avl_tree.py

📚 AVL TREES (Chapter 8):
-------------------------
AVL trees are self-balancing binary search trees.
Named after inventors: Adelson-Velsky and Landis (1962)

THE PROBLEM WITH REGULAR BST:
If you insert sorted data, BST becomes a linked list → O(n) operations!

THE SOLUTION:
Keep the tree balanced! After each insert, check balance and rotate if needed.

BALANCE FACTOR = height(left) - height(right)
- Balanced: -1, 0, or 1
- Unbalanced: anything else → needs rotation!

HOW TO RUN:
-----------
    python main.py           # Run this tutorial
    python -m pytest tests/ -v   # Run the grading tests
"""

from avl_tree import AVLNode, AVLTree


def print_header(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def balance_factor_explained() -> None:
    """Explain balance factor."""
    print_header("BALANCE FACTOR")
    
    print("""
    BALANCE FACTOR = height(left subtree) - height(right subtree)
    
    BALANCED EXAMPLES (balance factor is -1, 0, or 1):
    
        10          10           10
       /           /  \\            \\
      5           5    15          15
    
    BF=1        BF=0           BF=-1
    
    UNBALANCED EXAMPLES (need rotation!):
    
        10              10
       /               /
      5               5
     /               /
    2               2
                   /
                  1
    
    BF=2            BF=3
    (left-heavy)    (very left-heavy!)
    
    HEIGHT CALCULATION:
    - Empty node (None): height = 0
    - Leaf node: height = 1
    - Internal node: height = 1 + max(left_height, right_height)
    """)


def rotations_explained() -> None:
    """Explain AVL rotations."""
    print_header("AVL ROTATIONS")
    
    print("""
    When balance factor is outside [-1, 1], we need to ROTATE!
    
    ═══════════════════════════════════════════════════════════
    RIGHT ROTATION (for left-heavy tree, BF > 1):
    ═══════════════════════════════════════════════════════════
    
        y                x
       / \\              / \\
      x   C    →→→     A   y
     / \\                  / \\
    A   B                B   C
    
    Code:
        def rotate_right(y):
            x = y.left
            B = x.right
            
            x.right = y
            y.left = B
            
            # Update heights
            y.height = 1 + max(height(y.left), height(y.right))
            x.height = 1 + max(height(x.left), height(x.right))
            
            return x  # x is new root
    
    ═══════════════════════════════════════════════════════════
    LEFT ROTATION (for right-heavy tree, BF < -1):
    ═══════════════════════════════════════════════════════════
    
      x                    y
     / \\                  / \\
    A   y      →→→       x   C
       / \\              / \\
      B   C            A   B
    
    (Mirror of right rotation)
    """)


def four_cases_explained() -> None:
    """Explain the four rotation cases."""
    print_header("THE FOUR CASES")
    
    print("""
    After insertion, check balance factor of each ancestor.
    If unbalanced, determine which of 4 cases applies:
    
    ═══════════════════════════════════════════════════════════
    CASE 1: LEFT-LEFT (LL)
    ═══════════════════════════════════════════════════════════
    Inserted in left subtree of left child
    Fix: Single RIGHT rotation
    
          z                y
         /                / \\
        y      →→→       x   z
       /
      x
    
    ═══════════════════════════════════════════════════════════
    CASE 2: RIGHT-RIGHT (RR)
    ═══════════════════════════════════════════════════════════
    Inserted in right subtree of right child
    Fix: Single LEFT rotation
    
      z                      y
       \\                    / \\
        y      →→→         z   x
         \\
          x
    
    ═══════════════════════════════════════════════════════════
    CASE 3: LEFT-RIGHT (LR)
    ═══════════════════════════════════════════════════════════
    Inserted in right subtree of left child
    Fix: LEFT rotation on left child, then RIGHT rotation on root
    
        z              z              x
       /              /              / \\
      y      →→→     x      →→→     y   z
       \\            /
        x          y
    
    ═══════════════════════════════════════════════════════════
    CASE 4: RIGHT-LEFT (RL)
    ═══════════════════════════════════════════════════════════
    Inserted in left subtree of right child
    Fix: RIGHT rotation on right child, then LEFT rotation on root
    
      z                z                  x
       \\                \\                / \\
        y      →→→       x      →→→     z   y
       /                  \\
      x                    y
    """)


def demo_avl_tree() -> None:
    """Demonstrate AVL tree operations."""
    print_header("TESTING AVL TREE")
    
    print("""
    Let's insert values that would unbalance a regular BST:
    [1, 2, 3, 4, 5] - ascending order!
    
    Regular BST would become:
        1
         \\
          2
           \\
            3
             \\
              4
               \\
                5
    
    AVL tree stays balanced through rotations!
    """)
    
    try:
        avl = AVLTree()
        
        # Insert values that would unbalance regular BST
        values = [1, 2, 3, 4, 5]
        print(f"Inserting: {values}")
        
        for v in values:
            avl.insert(v)
            print(f"    Inserted {v}")
        
        # Test inorder (should be sorted)
        print("\nTesting inorder() - should return sorted values:")
        result = avl.inorder()
        expected = sorted(values)
        if result == expected:
            print(f"    inorder() = {result} ✅")
        elif result is None:
            print(f"    inorder() = None ❌ (not implemented)")
        else:
            print(f"    inorder() = {result}")
            print(f"    Expected: {expected}")
        
        # Check if tree is balanced
        print("\nChecking balance:")
        if avl.root:
            root_bf = avl.balance_factor(avl.root)
            if root_bf is not None and -1 <= root_bf <= 1:
                print(f"    Root balance factor: {root_bf} ✅ (balanced)")
            elif root_bf is not None:
                print(f"    Root balance factor: {root_bf} ❌ (unbalanced!)")
            else:
                print("    balance_factor() returned None")
        else:
            print("    Tree is empty")
            
    except Exception as e:
        print(f"    ❌ Error: {e}")


def implementation_tips() -> None:
    """Tips for implementing AVL tree."""
    print_header("IMPLEMENTATION TIPS")
    
    print("""
    ORDER OF IMPLEMENTATION:
    
    1. height(node) - Return node.height if exists, else 0
    
    2. balance_factor(node) - Return height(left) - height(right)
    
    3. rotate_right(y) and rotate_left(x)
       - Rearrange pointers
       - Update heights (bottom-up!)
       - Return new root
    
    4. _insert(node, value) - The main logic:
       a. Standard BST insert (recursively)
       b. Update height of current node
       c. Get balance factor
       d. If unbalanced, determine case (LL, RR, LR, RL)
       e. Apply appropriate rotation(s)
       f. Return (possibly new) root of subtree
    
    COMMON MISTAKES:
    ----------------
    1. Forgetting to update heights after rotation
    2. Updating heights in wrong order (must be bottom-up)
    3. Not returning the new root after rotation
    4. Checking wrong conditions for LR and RL cases
    
    DEBUGGING TIP:
    --------------
    Add print statements to trace rotations:
        print(f"Rotating right at node {y.value}")
    """)


def main():
    """Main entry point."""
    print("\n" + "⚖️" * 30)
    print("   LAB 08: AVL TREES")
    print("   Self-Balancing BST!")
    print("⚖️" * 30)
    
    print("""
    📋 YOUR TASKS:
    1. Open avl_tree.py
    2. Implement these methods:
       - height()
       - balance_factor()
       - rotate_right()
       - rotate_left()
       - _insert()
    3. Run this file to test: python main.py
    4. Run pytest when ready: python -m pytest tests/ -v
    """)
    
    balance_factor_explained()
    rotations_explained()
    four_cases_explained()
    demo_avl_tree()
    implementation_tips()
    
    print_header("NEXT STEPS")
    print("""
    When all tests pass, run: python -m pytest tests/ -v
    Then complete the Lab Report in README.md
    """)


if __name__ == "__main__":
    main()
