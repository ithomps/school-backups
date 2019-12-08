import unittest
import itertools
from Deque import Deque

class DequeTests(unittest.TestCase):
    def test_Empty(self):
        deque = Deque()
        self.assertTrue(deque.is_empty())
        deque.push_back(0)
        self.assertFalse(deque.is_empty())
        deque.pop_front()
        self.assertTrue(deque.is_empty())
        deque.push_front(0)
        self.assertFalse(deque.is_empty())
        deque.pop_back()
        self.assertTrue(deque.is_empty())

    def test_Len(self):
        deque = Deque()
        self.assertEqual(len(deque), 0)
        for i in range(0, 10):
            deque.push_front(i)
            self.assertEqual(i + 1, len(deque))
        for i in range(0, 10):
            deque.pop_front()
            self.assertEqual(9 - i, len(deque))

    def test_PushFront(self):
        deque = Deque()
        for i in range(0, 10):
            deque.push_front(i)
            self.assertEqual(i, deque.peek_front())
            self.assertEqual(i + 1, len(deque))
        self.assertEqual(0, deque.peek_back())

    def test_PushBack(self):
        deque = Deque()
        for i in range(0, 10):
            deque.push_back(i)
            self.assertEqual(i, deque.peek_back())
            self.assertEqual(i + 1, len(deque))
        self.assertEqual(0, deque.peek_front())

    def test_PopFront(self):
        deque = Deque()
        for i in range(0, 10):
            deque.push_back(i)

        for i in range(0, 10):
            self.assertEqual(i, deque.pop_front())
            self.assertEqual(9 - i, len(deque))
        self.assertTrue(deque.is_empty())
        self.assertRaises(IndexError, deque.pop_front)

    def test_PopBack(self):
        deque = Deque()
        for i in range(0, 10):
            deque.push_front(i)

        for i in range(0, 10):
            self.assertEqual(i, deque.pop_back())
            self.assertEqual(9 - i, len(deque))
        self.assertTrue(deque.is_empty())
        self.assertRaises(IndexError, deque.pop_back)

    def test_Iterator(self):
        import itertools
        deque = Deque()
        for i in range(0, 10):
            deque.push_back(i)

        for (i, j) in itertools.zip_longest(range(0, 10), deque):
            self.assertEqual(i, j)

    def test_CountIf(self):
        D = Deque()
        for i in range(30):
            D.push_back(i)
        self.assertEqual(len(D), 30)
        self.assertFalse(D.is_empty())
        self.assertEqual(D.count_if(lambda x: 15 - x > x), 8)
        self.assertEqual(len(D), 30)


    def test_Clear(self):
        deque = Deque()
        for i in range(0, 10):
            deque.push_back(i)

        self.assertFalse(deque.is_empty())
        deque.clear()
        self.assertTrue(deque.is_empty())
        self.assertEqual(0, len(deque))
        self.assertRaises(IndexError, deque.peek_front)
        self.assertRaises(IndexError, deque.peek_back)
        self.assertRaises(IndexError, deque.pop_front)
        self.assertRaises(IndexError, deque.pop_back)
        deque.clear()


    def test_Extend(self):
        import itertools
        L1=list(range(10))
        L2=list(range(10,20))
        D1 = Deque()
        D2 = Deque()
        self.assertTrue(D1.is_empty())
        for elt in L1:
            D1.push_back(elt)
            self.assertEqual(len(D1), elt+1)
        for elt in L2:
            D2.push_back(elt)
            self.assertEqual(len(D2), elt-9)
        D1.extend(D2)
        self.assertEqual(len(D1), 20)
        self.assertEqual(len(D2), 10)
        for d, l in itertools.zip_longest(D1, range(20)):
            self.assertEqual(d, l)
        for d, l in itertools.zip_longest(D2, range(10, 20)):
            self.assertEqual(d, l)


    def test_DropBetween(self):
        L = list(range(20))
        D = Deque()
        for elt in L:
            D.push_back(elt)
        self.assertEqual(len(D), 20)
        for d, l in zip(D,L):
            self.assertEqual(d, l)
        D.drop_between(5,15)
        result = L[:5] + L[15:]
        self.assertEqual(len(D), 10)
        for d, l in itertools.zip_longest(D, result):
            self.assertEqual(d, l)
        with self.assertRaises(IndexError):
            D.drop_between(-100,0)
        with self.assertRaises(IndexError):
            D.drop_between(0,100)
        with self.assertRaises(IndexError):
            D.drop_between(3,1)
        D.drop_between(0, 10)
        self.assertTrue(D.is_empty())

    def test_Sequence(self):
        deque = Deque()
        deque.push_front(0)
        deque.push_front(1)
        self.assertEqual(1, deque.peek_front())
        self.assertEqual(0, deque.peek_back())
        self.assertEqual(2, len(deque))
        deque.pop_back()
        self.assertEqual(1, deque.peek_front())
        self.assertEqual(1, deque.peek_back())
        self.assertEqual(1, len(deque))
        deque.push_back(2)
        self.assertEqual(1, deque.peek_front())
        self.assertEqual(2, deque.peek_back())
        self.assertEqual(2, len(deque))
        deque.pop_front()
        self.assertEqual(2, deque.peek_front())
        self.assertEqual(2, deque.peek_back())
        self.assertEqual(1, len(deque))

        d2 = Deque()
        for i in [4, 5, 6, 7]:
            d2.push_back(i)

        deque.extend(d2)

        for d, l in itertools.zip_longest(deque, [2, 4, 5, 6, 7]):
            self.assertEqual(d, l)

        self.assertEqual(2, deque.peek_front(), 'front after extend')
        self.assertEqual(7, deque.peek_back(), 'back after extend')
        self.assertEqual(5, len(deque), 'len after extend')
        deque.drop_between(2, 4)
        self.assertEqual(2, deque.peek_front(), 'front after drop')
        self.assertEqual(7, deque.peek_back(), 'back after drop')
        self.assertEqual(3, len(deque), 'len after drop')
        deque.pop_front()
        self.assertEqual(4, deque.peek_front(), 'front late')
        self.assertEqual(7, deque.peek_back(), 'back late')
        self.assertEqual(2, len(deque), 'len late')
        deque.pop_back()
        self.assertEqual(4, deque.peek_front(), 'front late')
        self.assertEqual(4, deque.peek_back(), 'back late')
        self.assertEqual(1, len(deque), 'len late')
        deque.pop_back()

        self.assertEqual(0, len(deque))
        self.assertTrue(deque.is_empty())
        self.assertRaises(IndexError, deque.pop_front)
        self.assertRaises(IndexError, deque.pop_back)
        self.assertRaises(IndexError, deque.peek_front)
        self.assertRaises(IndexError, deque.peek_back)

if __name__ == '__main__':
    unittest.main()
