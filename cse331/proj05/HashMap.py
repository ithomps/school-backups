"""
HashMap.py
Author: Ian Thompson
3/29/2019
"""


class HashMap:
    """
    Class to hold a hashtable for key, value pairs
    Resolves collisions with chaining
    Doubles capacity when it is full, halves capacity when a quarter full
    """
    def __init__(self, load_factor=1.00):
        """
        Constructor for HashMap
        :param load_factor:
        """
        # You may change the default maximum load factor
        self.max_load_factor = load_factor
        # Other initialization code can go here
        self.size = 5
        self.length = 0
        self.table = [None] * (self.size + 1)  # Initializes table to array of None

    def __len__(self):
        """
        Number of key value pairs in the hashmap
        :return:
        """
        return self.length

    def buckets(self):
        """
        Number of slots for values to go into
        :return:
        """
        return self.size

    def load(self):
        """
        Calculates load factor
        :return: Average number of keys per slot
        """
        return self.length / self.size

    def __contains__(self, key):
        """
        Checks the hashed table for the key
        :param key: Key to be searched for
        :return: If the key is in the map
        """
        hashed = hash(key)
        hashed = hashed % self.size
        if self.table[hashed] is not None:
            for item in self.table[hashed]:
                if item[0] == key:
                    return True
        return False

    def __getitem__(self, key):
        """
        Finds value associated with key
        :param key: Key used for searching
        :return: Value at key
        """
        hashed = hash(key)
        hashed = hashed % self.size
        if self.table[hashed] is not None:
            for item in self.table[hashed]:
                if item[0] == key:
                    return item[1]
        raise KeyError(key)

    def __setitem__(self, key, value):
        """
        Stores a tuple of the key and value
        Uses chaining to handle collisions
        :param key: Key to store
        :param value: Value to store at key
        :return:
        """
        if self.length == self.size:  # Table needs to grow
            self.size *= 2
            self.resize()
        hashed = hash(key)
        hashed = hashed % self.size
        if self.table[hashed] is None:  # No value is in that slot
            self.table[hashed] = [(key, value)]
        else:  # Chains new tuple onto array at that slot
            for item in self.table[hashed]:
                if item[0] == key:  # Case where key needs to be replaced
                    self.table[hashed].remove(item)
                    self.length -= 1
            self.table[hashed].append((key, value))
        self.length += 1

    def __delitem__(self, key):
        """
        Searches hashmap and removes tuple with key
        :param key: Key to be deleted
        :return:
        """
        if self.length < self.size // 4 and self.size > 4:  # Table is too large
            self.size = self.size // 2
            self.resize()
        found = False
        hashed = hash(key)
        hashed = hashed % self.size
        if self.table[hashed] is not None:
            for item in self.table[hashed]:
                if item[0] == key:
                    self.table[hashed].remove(item)  # Successfully removed item
                    self.length -= 1
                    found = True
        if not found:  # Key is not in hashmap
            raise KeyError(key)

    def __iter__(self):
        """
        Returns an iterator of key value pairs
        :return:
        """
        for item in self.table:
            if item is not None:
                for tup in item:  # Loops through chained items
                    key = tup[0]
                    value = tup[1]
                    yield (key, value)  # Yield key-value pairs

    def clear(self):
        """
        Removes all items from hashmap
        :return:
        """
        self.size = 5
        self.table = [None] * (self.size + 1)  # Resets to initial state
        self.length = 0

    def keys(self):
        """
        Returns only the keys in the hashmap
        :return:
        """
        keys_list = set(())
        for item in self.table:
            if item is not None:
                for tup in item:
                    keys_list.add(tup[0])
        return keys_list

    # supplied methods

    def __repr__(self):
        """
        A string representation of this map
        :return: A string representing this map
        """
        return '{{{0}}}'.format(','.join('{0}:{1}'.format(k, v) for k, v in self))

    def __bool__(self):
        """
        Checks if there are items in the map
        :return True if the map is non-empty
        """
        return not self.is_empty()

    def is_empty(self):
        """
        Checks that there are no items in the map
        :return: True if there are no bindings
        """
        return len(self) == 0

    # Helper functions can go here

    def resize(self):
        """
        Helper function to resize hashmap
        Size is changed before this function is called
        :return:
        """
        new_table = [None] * (self.size + 1)  # Table of new size
        for item in self:
            hashed = hash(item[0])
            hashed = hashed % self.size  # Calculates new position for each item
            if new_table[hashed] is None:  # No item in slot case
                new_table[hashed] = [item]
            else:  # Chains item into array at slot
                new_table[hashed].append(item)
        self.table = new_table  # Replaces old array with new table


# Required Function
def year_count(input_hashmap):
    """
    Function to count the number of students born in the given year
    :input: A HashMap of student name and its birth year
    :returns: A HashMap of the year and the number of students born in that year
    """
    new_hashmap = HashMap()
    for item in input_hashmap:
        new_hashmap[item[1]] = 0  # Builds hashmap of years with value 0
    for item in input_hashmap:
        new_hashmap[item[1]] += 1  # Loops through input again to increment value for each year
    return new_hashmap
