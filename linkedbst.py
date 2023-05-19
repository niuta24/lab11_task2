"""
File: linkedbst.py
Author: Ken Lambert
"""
from math import log
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
import time
import random
import string
# from linkedqueue import LinkedQueue


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s_1 = ""
            if node is not None:
                s_1 += recurse(node.right, level + 1)
                s_1 += "| " * level
                s_1 += str(node.data) + "\n"
                s_1 += recurse(node.left, level + 1)
            return s_1

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        while True:
            if self.isEmpty():
                return None
            else:
                current = self._root
                while current is not None:
                    if item == current.data:
                        return current.data
                    elif item < current.data:
                        current = current.left
                    else:
                        current = current.right
                return None
        # def recurse(node):
        #     if node is None:
        #         return None
        #     elif item == node.data:
        #         return node.data
        #     elif item < node.data:
        #         return recurse(node.left)
        #     else:
        #         return recurse(node.right)

        # return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""
        while True:
            if self.isEmpty():
                self._root = BSTNode(item)
                break
            else:
                parent = None
                current = self._root
                while current is not None:
                    parent = current
                    if item < current.data:
                        current = current.left
                    else:
                        current = current.right
                if item < parent.data:
                    parent.left = BSTNode(item)
                    break
                else:
                    parent.right = BSTNode(item)
                    break
        # # Helper function to search for item's position
        # def recurse(node):
        #     # New item is less, go left until spot is found
        #     if item < node.data:
        #         if node.left is None:
        #             node.left = BSTNode(item)
        #         else:
        #             recurse(node.left)
        #     # New item is greater or equal,
        #     # go right until spot is found
        #     elif node.right is None:
        #         node.right = BSTNode(item)
        #     else:
        #         recurse(node.right)
        #         # End of recurse

        # # Tree is empty, so new item goes at the root
        # if self.isEmpty():
        #     self._root = BSTNode(item)
        # # Otherwise, search for the item's spot
        # else:
        #     recurse(self._root)
        # self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of the tree
        :return: int
        '''
        def height1(top):
            """Return the height of a subtree."""
            if top is None:
                return 0
            else:
                return 1 + max(height1(top.left), height1(top.right))
        return max(height1(self._root)-1, 0)

    
    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return True if self.height() < 2 * log(self._size + 1, 2) - 1 else False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        if low > high:
            raise ValueError('low must be less than or equal to high')
        result = self.inorder()
        return [i for i in result if low <= i <= high]


    def rebalance(self):
        """
        Rebalances the tree.
        """
        # Copy elements of the tree into a sorted list
        sorted_list = list(self.inorder())
        # Clear the tree
        self.clear()

        # Helper function to build a balanced tree from a sorted list
        def build_balanced_tree(lst, start, end):
            if start > end:
                return None
            mid = (start + end) // 2
            node = BSTNode(lst[mid])
            node.left = build_balanced_tree(lst, start, mid - 1)
            node.right = build_balanced_tree(lst, mid + 1, end)
            return node

        # Build a balanced tree from the sorted list
        self._root = build_balanced_tree(sorted_list, 0, len(sorted_list) - 1)


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        result = []
        for i in self:
            if i > item:
                result.append(i)
        return min(result) if result else None
    
    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        result = []
        for i in self:
            if i < item:
                result.append(i)
        return max(result) if result else None
    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        # Load the dictionary from the file
        with open(path, 'r') as file:
            dictionary = [word.strip() for word in file.readlines()]

        # Sort the dictionary for binary search
        sorted_dictionary = sorted(dictionary)

        # Build a binary search tree with the sorted dictionary
        sorted_bst = LinkedBST()
        for word in sorted_dictionary:
            sorted_bst.add(word)

        # Build a binary search tree with the unsorted dictionary
        unsorted_bst = LinkedBST()
        for word in dictionary:
            unsorted_bst.add(word)

        # Perform searches and measure the time taken
        random_words = random.sample(dictionary, 10000)

        # Search in a sorted dictionary (using list methods)
        start_time = time.time()
        for word in random_words:
            if word in sorted_dictionary:
                pass  # Do something
        end_time = time.time()
        sorted_search_time = end_time - start_time

        # Search in a sorted binary search tree
        start_time = time.time()
        for word in random_words:
            sorted_bst.find(word)
        end_time = time.time()
        sorted_bst_search_time = end_time - start_time

        # Search in an unsorted binary search tree
        start_time = time.time()
        for word in random_words:
            unsorted_bst.find(word)
        end_time = time.time()
        unsorted_bst_search_time = end_time - start_time

        # Rebalance the binary search tree
        unsorted_bst.rebalance()

        # Search in a balanced binary search tree
        start_time = time.time()
        for word in random_words:
            unsorted_bst.find(word)
        end_time = time.time()
        balanced_bst_search_time = end_time - start_time

        # Display the search times
        print("Time to search 10000 random words in a dictionary (sorted list): {:.6f} seconds".format(sorted_search_time))
        print("Time to search 10000 random words in a dictionary (sorted BST): {:.6f} seconds".format(sorted_bst_search_time))
        print("Time to search 10000 random words in a dictionary (unsorted BST): {:.6f} seconds".format(unsorted_bst_search_time))
        print("Time to search 10000 random words in a dictionary (balanced BST): {:.6f} seconds".format(balanced_bst_search_time))
        

tree = LinkedBST()
tree.add(5)
tree.add(3)
tree.add(8)
tree.add(2)
tree.add(4)
tree.add(7)

print(tree)
print(tree.height())
print(tree.is_balanced())
print(tree.rangeFind(3, 7))
print(tree.successor(3))
print(tree.predecessor(3))
tree.rebalance()
print(tree)

tree.demo_bst('words.txt')