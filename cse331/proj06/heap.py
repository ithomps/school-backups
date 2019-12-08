"""
Heap.py
Author: Ian Thompson
03/15/2019
"""


class Heap:
    """
    A heap-based priority queue
    Items in the queue are ordered according to a comparison function
    """

    def __init__(self, comp):
        """
        Constructor
        :param comp: A comparison function determining the priority of the included elements
        """
        self.comp = comp
        # Added Members
        self.length = 0
        self.array = []

    def __len__(self):
        """
        Finds the number of items in the heap
        :return: The size
        """
        return self.length

    def peek(self):
        """
        Finds the item of highest priority
        :return: The item item of highest priority
        """
        if self.is_empty():
            raise IndexError

        return self.array[0]

    def insert(self, item):
        """
        Adds the item to the heap
        :param item: An item to insert
        """
        index = self.length
        self.array.append(item)
        parent = (index - 1) // 2

        # While still unbalanced
        while self.comp(self.array[index], self.array[parent]) and self.length != 0:
            self.array[parent], self.array[index] = self.array[index], self.array[parent]  # swap

            if parent != 0:
                index = parent  # move down tree
                parent = (index - 1) // 2

        self.length += 1

    def extract(self):
        """
        Removes the item of highest priority
        :return: the item of highest priority
        """
        if self.is_empty():
            raise IndexError

        min_val = self.array[0]
        self.array[0] = self.array[-1]
        self.array.pop()
        self.length -= 1

        self.heapify(0)  # recursive fixing of the heap

        return min_val

    def extend(self, seq):
        """
        Adds all elements from the given sequence to the heap
        :param seq: An iterable sequence
        """
        for item in seq:
            self.insert(item)

    def replace(self, item):
        """
        Adds the item the to the heap and returns the new highest-priority item
        Faster than insert followed by extract.
        :param item: An item to insert
        :return: The item of highest priority
        """
        if self.is_empty() or self.comp(item, self.array[0]):
            return item

        temp = self.array[0]
        self.array[0] = item  # puts item in highest priority spot
        self.heapify(0)  # fixes the heap

        return temp

    def clear(self):
        """
        Removes all items from the heap
        """
        while self.length != 0:
            self.array.pop()
            self.length -= 1

    def __iter__(self):
        """
        An iterator for this heap
        :return: An iterator
        """
        for i in range(0, self.length):
            yield self.array[i]

    # Supplied methods

    def __bool__(self):
        """
        Checks if this heap contains items
        :return: True if the heap is non-empty
        """
        return not self.is_empty()

    def is_empty(self):
        """
        Checks if this heap is empty
        :return: True if the heap is empty
        """
        return len(self) == 0

    def __repr__(self):
        """
        A string representation of this heap
        :return:
        """
        return 'Heap([{0}])'.format(','.join(str(item) for item in self))

    # Added methods

    def heapify(self, index):
        """
        Recursive function balancing a heap going downwards
        :param index:
        :return:
        """
        left = index * 2 + 1
        right = index * 2 + 2

        if left < self.length and self.comp(self.array[left], self.array[index]):
            small = left  # left item is smaller
        else:
            small = index  # parent is smaller than left child

        if right < self.length and self.comp(self.array[right], self.array[small]):
            small = right  # right is smaller than left or parent

        if small != index:
            self.array[index], self.array[small] = self.array[small], self.array[index]
            self.heapify(small)  # recursive call after switching spots
