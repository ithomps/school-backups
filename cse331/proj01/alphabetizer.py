"""
Provides class to hold members information
Provides methods to sort members by first or last name
"""
class Person:
    """
    Holds first name, last name, and email of all memeber
    """
    def __init__(self, first, last, email):
        self.first = first
        self.last = last
        self.email = email

    def __str__(self):
        return '{0} {1} <{2}>'.format(self.first, self.last, self.email)

    def __repr__(self):
        return '({0}, {1}, {2})'.format(self.first, self.last, self.email)

    def __eq__(self, other):
        return self.first == other.first and self.last == other.last and self.email == other.email

def order_first_name(a, b):
    """
    Orders two people by their first names
    :param a: a Person
    :param b: a Person
    :return: True if a comes before b alphabetically and False otherwise
    """
    if a.first == b.first:
        if not a.last == b.last:
            return order_last_name(a, b)
    return bool(a.first < b.first)

def order_last_name(a, b):
    """
    Orders two people by their last names
    :param a: a Person
    :param b: a Person
    :return: True if a comes before b alphabetically and False otherwise
    """
    if a.last == b.last:
        if not a.first == b.first:
            return order_first_name(a, b)
    return bool(a.last < b.last)

def is_alphabetized(roster, ordering):
    """
    Checks whether the roster of names is alphabetized in the given order
    :param roster: a list of people
    :param ordering: a function comparing two elements
    :return: True if the roster is alphabetized and False otherwise
    """
    i = 0
    while i < len(roster) - 1:
        if not ordering(roster[i], roster[i+1]): # out of order
            if not roster[i] == roster[i+1]:
                return False
        i += 1

    return True # will return if entire list is sorted

def merge(list_1, list_2, ordering):
    """
    Takes two ordered lists and combines them
    :param list_1: first sorted list
    :param list_2: second sorted list
    :param ordering: function for which way elements are sorted
    :return: a new combined list
    :return: the number of comparisons
    """
    comparisons = 0
    new_list = []
    l1_iter = 0
    l2_iter = 0
    while l1_iter < len(list_1) and l2_iter < len(list_2):
        comparisons += 1
        if not ordering(list_2[l2_iter], list_1[l1_iter]):
            new_list.append(list_1[l1_iter])
            l1_iter += 1
        else:
            new_list.append(list_2[l2_iter])
            l2_iter += 1

    # Fills out rest of list
    while l1_iter != len(list_1):
        new_list.append(list_1[l1_iter])
        l1_iter += 1
    while l2_iter != len(list_2):
        new_list.append(list_2[l2_iter])
        l2_iter += 1

    return (new_list, comparisons)


def alphabetize(roster, ordering):
    """
    Alphabetizes the roster according to the given ordering
    Uses the merge sort algoritm, calling the merge function to help
    :param roster: a list of people
    :param ordering: a function comparing two elements
    :return: a sorted version of roster
    :return: the number of comparisons made
    """
    comparisons = 0
    cost = 0

    length = len(roster)
    new_list = []
    l1 = []
    l2 = []

    if length == 1:
        pass # list is sorted
    else:
        (l1, cost) = alphabetize(roster[0:length//2], ordering)
        comparisons += cost
        (l2, cost) = alphabetize(roster[length//2:length], ordering)
        comparisons += cost
        (new_list, cost) = merge(l1, l2, ordering)
        comparisons += cost
        roster = new_list
        return (list(roster), comparisons)
    return(list(roster), comparisons)
