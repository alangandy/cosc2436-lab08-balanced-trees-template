"""Lab 08: Test Cases for AVL Trees"""
import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from avl_tree import AVLTree


class TestAVLTree:
    def test_insert_and_inorder(self):
        avl = AVLTree()
        for val in [10, 20, 30, 40, 50]:
            avl.insert(val)
        assert avl.inorder() == [10, 20, 30, 40, 50]
    
    def test_balance_after_insert(self):
        avl = AVLTree()
        # Insert in sorted order (would be unbalanced in regular BST)
        for val in [1, 2, 3, 4, 5, 6, 7]:
            avl.insert(val)
        # Tree should be balanced, height should be O(log n)
        assert avl.root.height <= 4  # log2(7) ≈ 2.8, with some slack
    
    def test_left_rotation(self):
        avl = AVLTree()
        avl.insert(10)
        avl.insert(20)
        avl.insert(30)  # Should trigger left rotation
        assert avl.root.value == 20
    
    def test_right_rotation(self):
        avl = AVLTree()
        avl.insert(30)
        avl.insert(20)
        avl.insert(10)  # Should trigger right rotation
        assert avl.root.value == 20
    
    def test_empty_tree(self):
        avl = AVLTree()
        assert avl.inorder() == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
