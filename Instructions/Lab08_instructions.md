# Lab 8: Balanced Trees

## 1. Introduction and Objectives

### Overview
Understand why balanced trees matter and implement AVL tree rotations. Explore B-trees for database indexing concepts using the Texas cities dataset.

### Learning Objectives
- Understand why unbalanced trees degrade to O(n)
- Implement AVL tree balancing with rotations
- Understand B-tree concepts for databases
- Analyze when to use different tree types

### Prerequisites
- Complete Labs 1-7
- Read Chapter 8 in "Grokking Algorithms" (pages 143-162)

---

## 2. Algorithm Background

### The Balance Problem
An unbalanced BST (e.g., inserting sorted data) becomes a linked list:
```
Insert: 1, 2, 3, 4, 5

Unbalanced:          Balanced:
    1                    3
     \                  / \
      2                2   4
       \              /     \
        3            1       5
         \
          4
           \
            5
Height: 4 (O(n))     Height: 2 (O(log n))
```

### AVL Trees
- **Self-balancing** BST
- **Balance Factor** = height(left) - height(right)
- Must be -1, 0, or +1 for every node
- Rebalance using **rotations** after insert/delete

### AVL Rotations
| Imbalance | Rotation |
|-----------|----------|
| Left-Left (LL) | Right rotation |
| Right-Right (RR) | Left rotation |
| Left-Right (LR) | Left then Right |
| Right-Left (RL) | Right then Left |

### Splay Trees
- Recently accessed nodes move to **root**
- Repeated lookups become **faster**
- Not always balanced, but **amortized O(log n)**
- Good for caching scenarios

### B-Trees
- Used in **databases** and **file systems**
- Multiple keys per node
- All leaves at same depth
- Optimized for **disk access** (minimizes seek time)

### Time Complexity Comparison
| Operation | BST (worst) | AVL Tree | B-Tree |
|-----------|-------------|----------|--------|
| Search | O(n) | O(log n) | O(log n) |
| Insert | O(n) | O(log n) | O(log n) |
| Delete | O(n) | O(log n) | O(log n) |

---

## 3. Project Structure

```
lab08_balanced_trees/
├── avl_tree.py    # AVL tree implementation
├── btree.py       # B-tree concepts (simplified)
├── main.py        # Main program
└── README.md      # Your lab report
```

---

## 4. Step-by-Step Implementation

### Step 1: Create `avl_tree.py`

```python
"""
Lab 8: AVL Tree Implementation
Self-balancing binary search tree for Texas cities.
"""
from typing import Optional, List, Any


class AVLNode:
    """
    AVL Tree Node with height tracking.
    
    Balance Factor = height(left) - height(right)
    Must be -1, 0, or +1 for AVL property.
    """
    
    def __init__(self, key: int, data: Any = None):
        self.key = key
        self.data = data
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height: int = 1  # New node has height 1
    
    def __repr__(self):
        return f"AVLNode({self.key}, {self.data}, h={self.height})"


class AVLTree:
    """
    AVL Tree: Self-balancing Binary Search Tree.
    
    Guarantees O(log n) operations by maintaining balance
    through rotations after insertions and deletions.
    """
    
    def __init__(self):
        self.root: Optional[AVLNode] = None
        self.rotation_count = 0
    
    def _height(self, node: Optional[AVLNode]) -> int:
        """Get height of node (None has height 0)."""
        return node.height if node else 0
    
    def _balance_factor(self, node: Optional[AVLNode]) -> int:
        """
        Calculate balance factor.
        
        Positive: Left-heavy
        Negative: Right-heavy
        """
        if node is None:
            return 0
        return self._height(node.left) - self._height(node.right)
    
    def _update_height(self, node: AVLNode) -> None:
        """Update node's height based on children."""
        node.height = 1 + max(self._height(node.left), self._height(node.right))
    
    def _rotate_right(self, y: AVLNode) -> AVLNode:
        """
        Right rotation for Left-Left imbalance.
        
              y                x
             / \              / \
            x   C    -->     A   y
           / \                  / \
          A   B                B   C
        """
        self.rotation_count += 1
        print(f"  >> RIGHT rotation at {y.data}")
        
        x = y.left
        B = x.right
        
        # Perform rotation
        x.right = y
        y.left = B
        
        # Update heights (y first, then x)
        self._update_height(y)
        self._update_height(x)
        
        return x  # New root of subtree
    
    def _rotate_left(self, x: AVLNode) -> AVLNode:
        """
        Left rotation for Right-Right imbalance.
        
            x                  y
           / \                / \
          A   y     -->      x   C
             / \            / \
            B   C          A   B
        """
        self.rotation_count += 1
        print(f"  >> LEFT rotation at {x.data}")
        
        y = x.right
        B = y.left
        
        # Perform rotation
        y.left = x
        x.right = B
        
        # Update heights (x first, then y)
        self._update_height(x)
        self._update_height(y)
        
        return y  # New root of subtree
    
    def insert(self, key: int, data: Any = None) -> None:
        """Insert a key and rebalance if needed."""
        print(f"\nInserting {data} (pop: {key:,})")
        self.root = self._insert_recursive(self.root, key, data)
    
    def _insert_recursive(self, node: Optional[AVLNode], key: int, data: Any) -> AVLNode:
        """Recursive insert with AVL rebalancing."""
        
        # Standard BST insert
        if node is None:
            return AVLNode(key, data)
        
        if key < node.key:
            node.left = self._insert_recursive(node.left, key, data)
        else:
            node.right = self._insert_recursive(node.right, key, data)
        
        # Update height of current node
        self._update_height(node)
        
        # Get balance factor
        balance = self._balance_factor(node)
        
        # Check for imbalance and rotate
        
        # Left-Left Case
        if balance > 1 and key < node.left.key:
            print(f"  Imbalance at {node.data}: Left-Left case")
            return self._rotate_right(node)
        
        # Right-Right Case
        if balance < -1 and key > node.right.key:
            print(f"  Imbalance at {node.data}: Right-Right case")
            return self._rotate_left(node)
        
        # Left-Right Case
        if balance > 1 and key > node.left.key:
            print(f"  Imbalance at {node.data}: Left-Right case")
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        # Right-Left Case
        if balance < -1 and key < node.right.key:
            print(f"  Imbalance at {node.data}: Right-Left case")
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def search(self, key: int) -> Optional[AVLNode]:
        """Search for a key (same as BST)."""
        return self._search_recursive(self.root, key)
    
    def _search_recursive(self, node: Optional[AVLNode], key: int) -> Optional[AVLNode]:
        if node is None or node.key == key:
            return node
        
        if key < node.key:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)
    
    def inorder(self) -> List[str]:
        """Get sorted order via inorder traversal."""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[AVLNode], result: List[str]) -> None:
        if node:
            self._inorder_recursive(node.left, result)
            result.append(f"{node.data} ({node.key:,})")
            self._inorder_recursive(node.right, result)
    
    def get_height(self) -> int:
        """Get tree height."""
        return self._height(self.root)
    
    def display(self) -> None:
        """Display tree structure with balance factors."""
        print(f"\nAVL Tree (height={self.get_height()}, rotations={self.rotation_count}):")
        print("-" * 50)
        if self.root:
            self._display_recursive(self.root, "", True)
    
    def _display_recursive(self, node: Optional[AVLNode], prefix: str, is_last: bool) -> None:
        if node:
            bf = self._balance_factor(node)
            bf_str = f"bf={bf:+d}"
            print(prefix + ("└── " if is_last else "├── ") + 
                  f"{node.data} ({node.key:,}) [{bf_str}]")
            
            children = []
            if node.left:
                children.append(node.left)
            if node.right:
                children.append(node.right)
            
            for i, child in enumerate(children):
                is_last_child = (i == len(children) - 1)
                new_prefix = prefix + ("    " if is_last else "│   ")
                self._display_recursive(child, new_prefix, is_last_child)


def compare_bst_vs_avl(data: List[tuple]) -> None:
    """
    Compare regular BST vs AVL tree heights.
    Demonstrates why balancing matters.
    """
    from bst import BinarySearchTree
    
    # Build regular BST
    bst = BinarySearchTree()
    for key, name in data:
        bst.insert(key, name)
    
    # Build AVL tree
    avl = AVLTree()
    for key, name in data:
        avl.insert(key, name)
    
    print("\n" + "=" * 50)
    print("BST vs AVL COMPARISON")
    print("=" * 50)
    print(f"Data items: {len(data)}")
    print(f"BST height: {bst.height()}")
    print(f"AVL height: {avl.get_height()}")
    print(f"AVL rotations performed: {avl.rotation_count}")
    print(f"Optimal height (log2): {len(data).bit_length() - 1}")
```

### Step 2: Create `btree.py`

```python
"""
Lab 8: B-Tree Concepts (Simplified)
Understanding B-trees for database indexing.

Note: This is a conceptual implementation to understand B-trees.
Production B-trees are more complex.
"""
from typing import List, Optional, Any


class BTreeNode:
    """
    B-Tree Node.
    
    Properties:
    - Each node can have multiple keys
    - Keys are sorted within the node
    - Children pointers between keys
    - All leaves at same depth
    """
    
    def __init__(self, t: int, leaf: bool = True):
        """
        t: Minimum degree (defines range for number of keys)
        - Every node except root must have at least t-1 keys
        - Every node can have at most 2t-1 keys
        """
        self.t = t
        self.leaf = leaf
        self.keys: List[tuple] = []  # (key, data) pairs
        self.children: List['BTreeNode'] = []
    
    def is_full(self) -> bool:
        """Check if node has maximum keys."""
        return len(self.keys) == 2 * self.t - 1


class BTree:
    """
    Simplified B-Tree for understanding database indexing.
    
    B-Trees are used in:
    - Database indexes (MySQL, PostgreSQL)
    - File systems (NTFS, HFS+, ext4)
    - Key-value stores
    
    Why B-Trees for databases?
    - Minimizes disk reads (wide, shallow tree)
    - Each node = one disk block
    - O(log_t n) disk accesses
    """
    
    def __init__(self, t: int = 2):
        """
        Initialize B-Tree with minimum degree t.
        
        t=2: 2-3-4 tree (each node has 1-3 keys, 2-4 children)
        t=100: Each node has 99-199 keys (good for disk)
        """
        self.t = t
        self.root = BTreeNode(t, leaf=True)
    
    def search(self, key: int, node: Optional[BTreeNode] = None) -> Optional[tuple]:
        """
        Search for a key in the B-tree.
        
        Time: O(t * log_t n) comparisons
        Disk accesses: O(log_t n)
        """
        if node is None:
            node = self.root
        
        # Find the first key >= search key
        i = 0
        while i < len(node.keys) and key > node.keys[i][0]:
            i += 1
        
        # Found the key
        if i < len(node.keys) and key == node.keys[i][0]:
            return node.keys[i]
        
        # Key not found and we're at a leaf
        if node.leaf:
            return None
        
        # Recurse to appropriate child
        return self.search(key, node.children[i])
    
    def insert(self, key: int, data: Any = None) -> None:
        """Insert a key into the B-tree."""
        root = self.root
        
        # If root is full, split it
        if root.is_full():
            new_root = BTreeNode(self.t, leaf=False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        
        self._insert_non_full(self.root, key, data)
    
    def _insert_non_full(self, node: BTreeNode, key: int, data: Any) -> None:
        """Insert into a node that is not full."""
        i = len(node.keys) - 1
        
        if node.leaf:
            # Insert into leaf
            node.keys.append((key, data))
            # Sort keys
            node.keys.sort(key=lambda x: x[0])
        else:
            # Find child to recurse into
            while i >= 0 and key < node.keys[i][0]:
                i -= 1
            i += 1
            
            # Split child if full
            if node.children[i].is_full():
                self._split_child(node, i)
                if key > node.keys[i][0]:
                    i += 1
            
            self._insert_non_full(node.children[i], key, data)
    
    def _split_child(self, parent: BTreeNode, i: int) -> None:
        """Split a full child node."""
        t = self.t
        full_child = parent.children[i]
        
        # Create new node for right half
        new_node = BTreeNode(t, leaf=full_child.leaf)
        
        # Middle key goes up to parent
        mid = t - 1
        parent.keys.insert(i, full_child.keys[mid])
        
        # Right half of keys go to new node
        new_node.keys = full_child.keys[mid + 1:]
        full_child.keys = full_child.keys[:mid]
        
        # Move children if not leaf
        if not full_child.leaf:
            new_node.children = full_child.children[t:]
            full_child.children = full_child.children[:t]
        
        # Insert new node as child of parent
        parent.children.insert(i + 1, new_node)
    
    def display(self, node: Optional[BTreeNode] = None, level: int = 0) -> None:
        """Display B-tree structure."""
        if node is None:
            node = self.root
            print(f"\nB-Tree (t={self.t}):")
            print("-" * 40)
        
        # Print current node
        keys_str = ", ".join(f"{k[1]}({k[0]:,})" for k in node.keys)
        print("  " * level + f"[{keys_str}]")
        
        # Print children
        for child in node.children:
            self.display(child, level + 1)
    
    def get_height(self) -> int:
        """Get tree height."""
        height = 0
        node = self.root
        while not node.leaf:
            height += 1
            node = node.children[0]
        return height


def demonstrate_btree_for_database():
    """
    Show why B-trees are used for database indexes.
    """
    print("\n" + "=" * 60)
    print("B-TREE FOR DATABASE INDEXING")
    print("=" * 60)
    
    print("""
    WHY B-TREES FOR DATABASES?
    
    Problem: Data on disk, disk reads are SLOW
    - RAM access: ~100 nanoseconds
    - Disk access: ~10 milliseconds (100,000x slower!)
    
    Solution: Minimize disk reads
    - B-tree node size = disk block size (4KB typical)
    - Each node holds many keys (100-200)
    - Very shallow tree (3-4 levels for millions of records)
    
    Example: 1 million records
    - Binary tree: log2(1M) ≈ 20 levels = 20 disk reads
    - B-tree (t=100): log100(1M) ≈ 3 levels = 3 disk reads
    
    B-TREE PROPERTIES:
    1. All leaves at same depth (balanced)
    2. Nodes are at least half full (space efficient)
    3. Keys sorted within nodes (range queries)
    4. Self-balancing on insert/delete
    """)
```

### Step 3: Create `main.py`

```python
"""
Lab 8: Main Program
Demonstrates balanced trees with Texas cities.
"""
import json
from avl_tree import AVLTree, compare_bst_vs_avl
from btree import BTree, demonstrate_btree_for_database


def load_cities(filename: str) -> list:
    with open(filename, 'r') as file:
        return json.load(file)


def main():
    # =========================================
    # PART 1: The Balance Problem
    # =========================================
    print("=" * 60)
    print("PART 1: WHY BALANCE MATTERS")
    print("=" * 60)
    
    print("""
    Inserting SORTED data into BST creates a linked list!
    
    Insert: 100K, 200K, 300K, 400K, 500K (sorted populations)
    
    BST becomes:           We want:
        100K                   300K
          \\                   /   \\
          200K              200K   400K
            \\              /         \\
            300K        100K         500K
              \\
              400K
                \\
                500K
    
    Height: O(n)           Height: O(log n)
    Search: O(n)           Search: O(log n)
    """)
    
    # =========================================
    # PART 2: AVL Tree Insertions
    # =========================================
    print("\n" + "=" * 60)
    print("PART 2: AVL TREE - SELF-BALANCING")
    print("=" * 60)
    
    avl = AVLTree()
    
    # Insert cities in sorted order (worst case for BST)
    sorted_cities = [
        (261639, "Laredo"),
        (681728, "El Paso"),
        (909585, "Fort Worth"),
        (978908, "Austin"),
        (1304379, "Dallas"),
        (1547253, "San Antonio"),
        (2304580, "Houston"),
    ]
    
    print("\nInserting cities in SORTED order (worst case for BST):")
    print("-" * 50)
    
    for pop, name in sorted_cities:
        avl.insert(pop, name)
        avl.display()
    
    print(f"\nFinal AVL tree height: {avl.get_height()}")
    print(f"Total rotations: {avl.rotation_count}")
    print(f"Optimal height for 7 nodes: {7.bit_length() - 1}")
    
    # =========================================
    # PART 3: AVL Rotations Explained
    # =========================================
    print("\n" + "=" * 60)
    print("PART 3: AVL ROTATION CASES")
    print("=" * 60)
    print("""
    ROTATION CASES:
    
    1. LEFT-LEFT (LL) → Right Rotation
       Problem: Left child's left subtree too tall
       
           z                y
          /                / \\
         y       -->      x   z
        /
       x
    
    2. RIGHT-RIGHT (RR) → Left Rotation
       Problem: Right child's right subtree too tall
       
       z                    y
        \\                  / \\
         y       -->      z   x
          \\
           x
    
    3. LEFT-RIGHT (LR) → Left then Right
       Problem: Left child's right subtree too tall
       
         z              z              y
        /              /              / \\
       x      -->     y      -->     x   z
        \\            /
         y          x
    
    4. RIGHT-LEFT (RL) → Right then Left
       Problem: Right child's left subtree too tall
       
       z              z                y
        \\              \\              / \\
         x    -->       y    -->     z   x
        /                \\
       y                  x
    """)
    
    # =========================================
    # PART 4: B-Tree Concepts
    # =========================================
    print("\n" + "=" * 60)
    print("PART 4: B-TREE FOR DATABASES")
    print("=" * 60)
    
    btree = BTree(t=2)  # 2-3-4 tree
    
    cities_subset = [
        (978908, "Austin"),
        (2304580, "Houston"),
        (1304379, "Dallas"),
        (1547253, "San Antonio"),
        (681728, "El Paso"),
        (909585, "Fort Worth"),
    ]
    
    print("\nBuilding B-tree (t=2, so 1-3 keys per node):")
    for pop, name in cities_subset:
        print(f"  Inserting {name}...")
        btree.insert(pop, name)
    
    btree.display()
    
    # Search demonstration
    print("\nSearching for Dallas (1,304,379):")
    result = btree.search(1304379)
    if result:
        print(f"  Found: {result[1]} (pop: {result[0]:,})")
    
    demonstrate_btree_for_database()
    
    # =========================================
    # PART 5: Comparison Summary
    # =========================================
    print("\n" + "=" * 60)
    print("PART 5: TREE COMPARISON SUMMARY")
    print("=" * 60)
    print("""
    | Tree Type | Use Case | Height | Notes |
    |-----------|----------|--------|-------|
    | BST | Simple cases | O(n) worst | Can degrade |
    | AVL | In-memory | O(log n) | Strict balance |
    | Red-Black | General | O(log n) | Less rotations |
    | B-Tree | Databases | O(log_t n) | Disk-optimized |
    | B+ Tree | Indexes | O(log_t n) | Leaves linked |
    
    WHEN TO USE WHAT:
    
    - BST: Learning, simple cases, random data
    - AVL: Lookup-heavy, in-memory, need strict balance
    - Red-Black: Insert/delete-heavy (used in std::map)
    - B-Tree: Databases, file systems, disk storage
    - B+ Tree: Database indexes, range queries
    
    KEY INSIGHT:
    Balance guarantees O(log n) operations!
    Without balance, trees can degrade to O(n).
    """)


if __name__ == "__main__":
    main()
```

---

## 5. Lab Report Template

```markdown
# Lab 8: Balanced Trees

## Student Information
- **Name:** [Your Name]
- **Date:** [Date]

## Balance Concepts

### Why Balance Matters
[Explain what happens with unbalanced trees]

### AVL Balance Factor
[Explain balance factor and when rotations occur]

## AVL Rotation Cases

| Case | Imbalance | Rotation | Example |
|------|-----------|----------|---------|
| LL | | | |
| RR | | | |
| LR | | | |
| RL | | | |

## Test Results

### AVL Tree After Sorted Insertions
[Draw or describe your AVL tree]

### Statistics
- Number of nodes: 
- Tree height:
- Rotations performed:
- Optimal height:

## B-Tree Concepts

### Why B-Trees for Databases?
[Explain in your own words]

### B-Tree vs Binary Tree
[Compare disk access patterns]

## Reflection Questions

1. Why does inserting sorted data create the worst-case BST?

2. How do rotations maintain the BST property while balancing?

3. Why are B-trees better than AVL trees for databases?

4. What is the relationship between B-tree node size and disk block size?
```

---

## 6. Submission
Save files in `lab08_balanced_trees/`, complete README, commit and push.
