#!/usr/bin/python3
import unittest

from main import Person, load_file
from alphabetizer import *

class TestAlphabetizer(unittest.TestCase):

    def test_order_first_name(self):
        harry = Person('Harry', 'Potter', 'hpotter@hogwarts.edu')
        hermione = Person('Hermione', 'Granger', 'hgranger@hogwarts.edu')
        self.assertTrue(order_first_name(harry, hermione))
        self.assertFalse(order_first_name(hermione, harry))
        
    def test_order_last_name(self):
        harry = Person('Harry', 'Potter', 'hpotter@hogwarts.edu')
        hermione = Person('Hermione', 'Granger', 'hgranger@hogwarts.edu')
        self.assertFalse(order_last_name(harry, hermione))
        self.assertTrue(order_last_name(hermione, harry))
        
    def test_is_alphabetized(self):
        member_list = load_file('gryffindor.txt')
        self.assertFalse(is_alphabetized(member_list, order_first_name))
        self.assertFalse(is_alphabetized(member_list, order_last_name))
        member_list = load_file('sorted_first_name.txt')
        self.assertTrue(is_alphabetized(member_list, order_first_name))
        member_list = load_file('sorted_last_name.txt')
        self.assertTrue(is_alphabetized(member_list, order_last_name))
        
    def test_alphabetize_by_first(self):
        member_list = load_file('gryffindor.txt')
        solution = load_file('sorted_first_name.txt')
        (sorted_list, cost) = alphabetize(member_list, order_first_name)
        self.assertEqual(sorted_list, solution)
        
    def test_alphabetize_by_last(self):
        member_list = load_file('gryffindor.txt')
        solution = load_file('sorted_last_name.txt')
        (sorted_list, cost) = alphabetize(member_list, order_last_name)
        self.assertEqual(sorted_list, solution)
        
if __name__ == '__main__':
    unittest.main()
