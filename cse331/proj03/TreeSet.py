"""
TreeSet.py
Author: Ian Thompson
02/27/2019
"""


class TreeSet:
    """
    A set data structure backed by a tree.
    Items will be stored in an order determined by a comparison
    function rather than their natural order.
    """

    def __init__(self, comp):
        """
        Constructor for the tree set.
        You can perform additional setup steps here
        :param comp: A comparison function over two elements
        """
        self.comp = comp
        # added stuff below
        self.tree_height = -1
        self.head = None
        self.length = 0

    def __len__(self):
        """
        Counts the number of elements in the tree
        :return:
        """
        return self.length

    def height(self):
        """
        Finds the height of the tree
        :return:
        """
        return self.tree_height

    def insert(self, item):
        """
        Inserts the item into the tree
        :param item:
        :return: If the operation was successful
        """
        if self.is_empty():
            self.head = NodePointer(TreeNode(item))
            self.length += 1
            return True
        return self.recursive_insert(self.head, item)

    def remove(self, item):
        """
        Removes the item from the tree
        :param item:
        :return: If the operation was successful
        """
        if self.is_empty():
            return False
        return self.recursive_remove(self.head, item)

    def __contains__(self, item):
        """
        Checks if the item is in the tree
        :param item:
        :return: if the item was in the tree
        """
        if self:
            return self.recursive_search(self.head, item)
        return False

    def first(self):
        """
        Finds the minimum item of the tree
        :return:
        """
        if self.is_empty():
            raise KeyError
        return self.recursive_smallest(self.head).data

    def last(self):
        """
        Finds the maximum item of the tree
        :return:
        """
        if self.is_empty():
            raise KeyError
        return self.recursive_biggest(self.head).data

    def clear(self):
        """
        Empties the tree
        :return:
        """
        self.length = 0
        self.tree_height = 0
        self.head = None

    def __iter__(self):
        """
        Does an in-order traversal of the tree
        :return:
        """
        items = []
        if not self.is_empty():
            items = self.in_order(self.head)
        for item in items:
            yield item

    def is_disjoint(self, other):
        """
        Check if two TreeSet is disjoint
        :param other: A TreeSet object
        :return: True if the sets have no elements in common
        """
        if self.is_empty() or other.is_empty():
            return True
        return self.recursive_disjoint(self.head, other, other.head)

    # Pre-defined methods

    def is_empty(self):
        """
        Determines whether the set is empty
        :return: False if the set contains no items, True otherwise
        """
        return len(self) == 0

    def __repr__(self):
        """
        Creates a string representation of this set using an in-order traversal.
        :return: A string representing this set
        """
        return 'TreeSet([{0}])'.format(','.join(str(item) for item in self))

    def __bool__(self):
        """
        Checks if the tree is non-empty
        :return:
        """
        return not self.is_empty()

    # Helper functions
    # You can add additional functions here

    def recursive_biggest(self, pointer):
        """
        Helper function of last
        :param pointer: Pointer to node in the tree
        :return: node at the bottom of the right subtree
        """
        node = pointer.data
        biggest = node
        if node.right is not None:
            biggest = self.recursive_biggest(node.right)
        return biggest

    def recursive_smallest(self, pointer):
        """
        Helper function of last
        :param pointer: Pointer to node in the tree
        :return: node at the bottom of the left subtree
        """
        node = pointer.data
        smallest = node
        if node.left is not None:
            smallest = self.recursive_smallest(node.left)
        return smallest

    def recursive_search(self, pointer, item):
        """
        Helper function of contains
        :param pointer: Pointer to node in the tree
        :param item: Number that is searched for
        :return: if the item is in the tree
        """
        if pointer is not None and pointer.data is not None:
            node = pointer.data
            if self.comp(node.data, item) == 0:
                return True
            elif self.comp(node.data, item) < 0:
                return self.recursive_search(node.right, item)
            else:
                return self.recursive_search(node.left, item)
        else:
            return False

    def in_order(self, pointer):
        """
        Helper function of the iterator
        :param pointer: Pointer to current node in the tree
        """
        items = []
        if pointer is None or pointer.data is None:
            return items
        node = pointer.data

        items.extend(self.in_order(node.left))
        items.append(node.data)
        items.extend(self.in_order(node.right))

        return items

    def recursive_insert(self, pointer, item):
        """
        Helper function of insert
        :param pointer: Pointer to current node being checked for insert
        :param item: Item to be inserted
        :return: If the item was inserted into the tree
        """
        node = pointer.data
        if self.comp(node.data, item) == 0:
            return False
        elif self.comp(node.data, item) < 0:
            if node.right is None:
                node.right = NodePointer(TreeNode(item))
                self.length += 1
            else:
                res = self.recursive_insert(node.right, item)
                node.height = self.calc_height(pointer)
                if node.height > self.tree_height:
                    self.tree_height = node.height
                return res
        elif self.comp(node.data, item) > 0:
            if node.left is None:
                node.left = NodePointer(TreeNode(item))
                self.length += 1
            else:
                res = self.recursive_insert(node.left, item)
                node.height = self.calc_height(pointer)
                if node.height > self.tree_height:
                    self.tree_height = node.height
                return res
        return True

    def recursive_remove(self, pointer, item):
        """
        Helper function of remove
        :param pointer: Pointer to current node being checked
        :param item: Item to be removed
        :return: If item was removed
        """
        node = pointer.data
        if self.comp(node.data, item) == 0:
            if node.right is None and node.left is None:  # No children
                pointer.data = None
                self.length -= 1
            elif node.right is None and node.left is not None:  # Left child only
                pointer.data = node.left.data
                self.length -= 1
            elif node.left is None and node.right is not None:  # Right child only
                pointer.data = node.right.data
                self.length -= 1
            else:  # Two children
                if node.right.data is None:
                    return False
                if node.right.data.left is not None:
                    swap_node = self.recursive_successor(node.right)
                    swap_node.data.left = node.left
                    swap_node.data.right = node.right
                    pointer.data = swap_node.data
                    swap_node.data = node
                    swap_node.data.left = None
                    swap_node.data.right = None
                    return self.recursive_remove(swap_node, item)
            return True
        elif self.comp(node.data, item) < 0:
            if node.right is None or node.right.data is None:
                return False
            return self.recursive_remove(node.right, item)
        else:
            if node.left is None or node.left.data is None:
                return False
            return self.recursive_remove(node.left, item)

    def recursive_disjoint(self, pointer, other, other_pointer):
        """
        Works through both trees to find items in common
        :param pointer: Pointer in first tree
        :param other: Second tree for comparison
        :param other_pointer: Pointer in second tree
        :return:
        """
        if pointer is not None and other_pointer is not None:
            node = pointer.data
            other_node = other_pointer.data
            to_return = self.recursive_disjoint(node.left, other, other_node.left)
            if other_node.data in self:
                return False
            if node.data in other:
                return False
            return to_return and self.recursive_disjoint(node.right, other, other_node.right)
        elif pointer is not None:
            node = pointer.data
            to_return = self.recursive_disjoint(node.left, other, None)
            if node.data in other:
                return False
            return to_return and self.recursive_disjoint(node.right, other, None)
        elif other_pointer is not None:
            other_node = other_pointer.data
            to_return = self.recursive_disjoint(None, other, other_node.left)
            if other_node.data in self:
                return False
            return to_return and self.recursive_disjoint(None, other, other_node.right)
        else:
            return True

    def calc_height(self, pointer):
        """
        Finds the height at a node
        :param pointer:
        :return:
        """
        if pointer is not None and pointer.data is not None:
            node = pointer.data
            left_height = self.calc_height(node.left)
            right_height = self.calc_height(node.right)

            if left_height > right_height:
                return left_height + 1
            else:
                return right_height + 1
        else:
            return -1

    def recursive_successor(self, pointer):
        """
        Finds node to swap with in the two child remove case
        :param pointer:
        :return:
        """
        new_pointer = pointer
        if pointer.data.left is not None and pointer.data.left.data is not None:
            new_pointer = self.recursive_successor(pointer.data.left)
        return new_pointer

    def is_balanced(self, pointer):
        """
        Finds out if a node is balanced
        :param pointer:
        :return:
        """
        if pointer.data is None:
            return True
        else:
            return abs(self.calc_height(pointer.data.left) - self.calc_height(pointer.data.right)) <= 1

    def rotate_right(self, pointer, parent):
        """
        Left Left case
        :param pointer:
        :param parent:
        :return:
        """
        if parent.data.right == pointer:
            parent.data.right = pointer.data.left
        else:
            parent.data.left = pointer.data.left
        temp = pointer.data.left.data.right
        pointer.data.left.data.right = pointer
        pointer.data.left = temp

    def rotate_left(self, pointer, parent):
        """
        Right Right Case
        :param pointer:
        :param parent:
        :return:
        """
        if parent.data.right == pointer:
            parent.data.right = pointer.data.right
        else:
            parent.data.left = pointer.data.right
        temp = pointer.data.right.data.left
        pointer.data.right.data.left = pointer
        pointer.data.right = temp

    def rotate_left_right(self, pointer, parent):
        """
        Double rotation, left, right
        :param pointer:
        :param parent:
        :return:
        """
        temp_0 = pointer.data.left.data.right.data.left
        temp_1 = pointer.data.left
        pointer.left = pointer.data.left.right
        pointer.data.left.data.left = temp_1
        pointer.data.left.data.left.data.right = temp_0
        self.rotate_right(pointer, parent)

    def rotate_right_left(self, pointer, parent):
        """
        Double rotation, right, left
        :param pointer:
        :param parent:
        :return:
        """
        temp_0 = pointer.data.right.data.left.data.right
        temp_1 = pointer.data.right
        pointer.right = pointer.data.right.data.left
        pointer.data.right.data.right = temp_1
        pointer.data.right.data.right.data.left = temp_0
        self.rotate_left(pointer, parent)




class TreeNode:
    """
    A TreeNode to be used by the TreeSet
    """

    def __init__(self, data):
        """
        Constructor
        You can add additional data as needed
        :param data:
        """
        self.data = data
        self.left = None
        self.right = None
        # added stuff below
        self.height = 0

    def __repr__(self):
        """
        A string representing this node
        :return: A string
        """
        return 'TreeNode({0})'.format(self.data)


class NodePointer:
    """
    Points to a TreeNode
    """

    def __init__(self, data):
        """
        Constructor
        :param data:
        """
        self.data = data
