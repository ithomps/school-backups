"""
Deque.py
Implemented using a linked list
Author: Ian Thompson
02/08/2019
"""
class Node:
    """
    Creates nodes for linked LinkedList
    Holds data value and pointers for next and previous nodes
    """

    def __init__(self, data=None):
        """
        Creates a node of the linked list
        :param data: value for the node, default of None
        """
        self.data = data
        self.next = None
        self.previous = None


class Deque:
    """
    A double-ended queue
    """

    def __init__(self):
        """
        Initializes an empty Deque
        Creates sentinels for the head and tail
        """
        self.head_sentinel = Node()
        self.tail_sentinel = Node()
        self.head_sentinel.next = self.tail_sentinel
        self.tail_sentinel.previous = self.head_sentinel
        self.length = 0

    def __len__(self):
        """
        Computes the number of elements in the Deque
        :return: The size of the Deque
        """
        return self.length

    def peek_front(self):
        """
        Looks at, but does not remove, the first element
        :return: The first element
        """
        if self.length == 0:
            raise IndexError()
        return self.head_sentinel.next.data

    def peek_back(self):
        """
        Looks at, but does not remove, the last element
        :return: The last element
        """
        if self.length == 0:
            raise IndexError()
        return self.tail_sentinel.previous.data

    def push_front(self, e):
        """
        Inserts an element at the front of the Deque
        :param e: An element to insert
        """
        to_insert = Node(e)
        temp = self.head_sentinel.next
        self.head_sentinel.next = to_insert
        to_insert.next = temp
        to_insert.previous = self.head_sentinel
        to_insert.next.previous = to_insert
        self.length += 1


    def push_back(self, e):
        """
        Inserts an element at the back of the Deque
        :param e: An element to insert
        """
        to_insert = Node(e)
        temp = self.tail_sentinel.previous
        self.tail_sentinel.previous = to_insert
        to_insert.previous = temp
        to_insert.next = self.tail_sentinel
        to_insert.previous.next = to_insert
        self.length += 1


    def pop_front(self):
        """
        Removes and returns the first element
        :return: The (former) first element
        """
        if self.length == 0:
            raise IndexError()
        to_return = self.head_sentinel.next
        self.head_sentinel.next = to_return.next
        self.head_sentinel.next.previous = self.head_sentinel
        self.length -= 1
        return to_return.data


    def pop_back(self):
        """
        Removes and returns the last element
        :return: The (former) last element
        """
        if self.length == 0:
            raise IndexError()
        to_return = self.tail_sentinel.previous
        self.tail_sentinel.previous = to_return.previous
        self.tail_sentinel.previous.next = self.tail_sentinel
        self.length -= 1
        return to_return.data

    def clear(self):
        """
        Removes all elements from the Deque
        """
        while self.length > 0:
            self.pop_front()
        self.length = 0

    def __iter__(self):
        """
        Iterates over this Deque from front to back
        :return: An iterator
        """
        current_item = self.head_sentinel.next
        while current_item is not self.tail_sentinel:
            yield current_item.data
            current_item = current_item.next


    def extend(self, other):
        """
        Takes a Deque object and adds each of its elements to the back of self
        :param other: A Deque object
        """
        for item in other:
            self.push_back(item)

    def drop_between(self, start, end):
        """
        Deletes elements from the Deque that within the range [start, end)
        :param start: indicates the first position of the range
        :param end: indicates the last position of the range(does not drop this element)
        """
        if start < 0 or end > self.length or start > end:
            raise IndexError()

        counter = 0
        to_del = end - start
        current_item = self.head_sentinel.next

        while counter < start:
            current_item = current_item.next
            counter += 1

        while to_del > 0:
            temp = current_item
            current_item.previous.next = current_item.next
            current_item.next.previous = current_item.previous
            current_item = temp.next
            self.length -= 1
            to_del -= 1

    def count_if(self, criteria):
        """
        counts how many elements of the Deque satisfy the criteria
        :param criteria: a bool function that takes an element of the Deque
        and returns true if that element matches the criteria and false otherwise
        """
        counter = 0
        for item in self:
            if criteria(item):
                counter += 1
        return counter

    # provided functions

    def is_empty(self):
        """
        Checks if the Deque is empty
        :return: True if the Deque contains no elements, False otherwise
        """
        return len(self) == 0

    def __repr__(self):
        """
        A string representation of this Deque
        :return: A string
        """
        return 'Deque([{0}])'.format(','.join(str(item) for item in self))
