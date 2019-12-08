#!/usr/bin/python3

import unittest, re

from HashMap import HashMap, year_count

symbols = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu',
           'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega',
           'alfa', 'bravo', 'charlie', 'DELTA', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett', 'kilo',
           'lima', 'mike', 'november', 'oscar', 'papa', 'quebec', 'romeo', 'sierra', 'tango', 'uniform', 'victor',
           'whiskey', 'x-ray', 'yankee', 'zulu']

class HashMapTests(unittest.TestCase):

    def test_len(self):
        hashmap = HashMap()
        for i, l in enumerate(symbols):
            hashmap[l] = i
            self.assertEqual(i + 1, len(hashmap), l)
        for l in symbols:
            hashmap[l] = len(l)
            self.assertEqual(len(symbols), len(hashmap), l)
        for i, l in enumerate(symbols):
            del hashmap[l]
            self.assertEqual(len(symbols) - i - 1, len(hashmap), l)

    def test_contains(self):
        hashmap = HashMap()
        for l in symbols:
            self.assertFalse(l in hashmap, l)
            hashmap[l] = l
            self.assertTrue(l in hashmap, l)
        for l in symbols:
            self.assertTrue(l in hashmap, l)
            del hashmap[l]
            self.assertFalse(l in hashmap, l)

    def test_insert(self):
        hashmap = HashMap()
        for i, l in enumerate(symbols):
            self.assertFalse(l in hashmap, l)
            hashmap[l] = i
            self.assertTrue(l in hashmap, l)
        for l in symbols:
            self.assertTrue(l in hashmap, l)
            hashmap[l] = len(l)
            self.assertTrue(l in hashmap, l)

    def test_get(self):
        hashmap = HashMap()
        for i, l in enumerate(symbols):
            with self.assertRaises(KeyError, msg=l):
                hashmap[l]
            hashmap[l] = i
            self.assertEqual(i, hashmap[l], l)
        for i, l in enumerate(symbols):
            self.assertEqual(i, hashmap[l], l)
            hashmap[l] = len(l)
            self.assertEqual(len(l), hashmap[l], l)
        for l in symbols:
            self.assertEqual(len(l), hashmap[l], l)
            del hashmap[l]
            with self.assertRaises(KeyError, msg=l):
                hashmap[l]

    def test_delete(self):
        hashmap = HashMap()
        for i, l in enumerate(symbols):
            with self.assertRaises(KeyError, msg=l):
                hashmap[l]
            hashmap[l] = i
            self.assertEqual(i, hashmap[l], l)
        for i, l in enumerate(symbols):
            self.assertEqual(i, hashmap[l], l)
            hashmap[l] = len(l)
            self.assertEqual(len(l), hashmap[l], l)
        for l in symbols:
            self.assertEqual(len(l), hashmap[l], l)
            del hashmap[l]
            with self.assertRaises(KeyError, msg=l):
                hashmap[l]

    def test_load(self):
        hashmap = HashMap()
        self.assertGreaterEqual(20, hashmap.buckets())
        self.assertGreaterEqual(1.0, hashmap.max_load_factor)
        self.assertAlmostEqual(0, hashmap.load())
        for l in symbols:
            hashmap[l] = l
            self.assertLessEqual(0.05, hashmap.load(), msg=ll)
            self.assertGreaterEqual(hashmap.max_load_factor, hashmap.load(), msg=l)
            self.assertAlmostEqual(len(hashmap) / hashmap.buckets(), hashmap.load(), msg=l)
        for l in symbols:
            self.assertLessEqual(0.05, hashmap.load(), msg=l)
            self.assertGreaterEqual(hashmap.max_load_factor, hashmap.load(), msg=l)
            del hashmap[l]
            self.assertAlmostEqual(len(hashmap) / hashmap.buckets(), hashmap.load(), msg=l)
        self.assertAlmostEqual(0, hashmap.load())
        for l in symbols:
            hashmap[l] = l
            self.assertLessEqual(0.05, hashmap.load(), msg=l)
            self.assertGreaterEqual(hashmap.max_load_factor, hashmap.load(), msg=l)
            self.assertAlmostEqual(len(hashmap) / hashmap.buckets(), hashmap.load(), msg=l)
        load = hashmap.load()
        for l in symbols:
            hashmap[l] = len(l)
            self.assertAlmostEqual(load, hashmap.load(), msg=l)
            self.assertAlmostEqual(len(hashmap) / hashmap.buckets(), hashmap.load(), msg=l)
        hashmap.clear()
        self.assertAlmostEqual(0, hashmap.load())
        self.assertGreaterEqual(1.0, hashmap.max_load_factor)

    def test_keys(self):
        hashmap = HashMap()
        for l in symbols:
            hashmap[l] = l
        self.assertEqual(len(symbols), len(hashmap.keys()), str(hashmap.keys()))
        self.assertSetEqual(set(symbols), hashmap.keys(), str(hashmap.keys()))

    def test_clear(self):
        hashmap = HashMap()
        for l in symbols:
            hashmap[l] = l
        self.assertFalse(hashmap.is_empty())
        hashmap.clear()
        self.assertTrue(hashmap.is_empty())
        self.assertAlmostEqual(0, hashmap.load())
        for l in symbols:
            self.assertFalse(l in hashmap, l)
            with self.assertRaises(KeyError, msg=l):
                hashmap[l]
            with self.assertRaises(KeyError, msg=l):
                del hashmap[l]

    def test_iter(self):
        hashmap = HashMap()
        for l in symbols:
            hashmap[l] = l
        self.assertFalse(hashmap.is_empty())
        hashmap.clear()
        self.assertTrue(hashmap.is_empty())
        self.assertAlmostEqual(0, hashmap.load())
        for l in symbols:
            self.assertFalse(l in hashmap, l)
            with self.assertRaises(KeyError, msg=l):
                hashmap[l]
            with self.assertRaises(KeyError, msg=l):
                del hashmap[l]

    def test_year_count(self):
        student_info = [ ('Charlotte', 1997), ('Liam', 1999), ('Emma', 1999), ('William',1998), ('Elijah', 1998), 
            ('Oliver', 1998), ('Isabella', 1998), ('Amelia', 1999),('Mason', 1999), ('Sophia', 1999),('Mia', 2000),
            ('Noah', 2000), ('Logan', 2000),  ('James', 2001), ('Olivia', 2001), ('Benjamin', 2001), ('Evelyn', 2001),
            ('Ava', 2001),  ('Jacob', 2002), ('Abigail', 2002)]
        input_hash = HashMap()
        for name, year in student_info:
            input_hash[name] = year

        year_hash = year_count(input_hash)
        self.assertEqual(6, len(year_hash))
        self.assertEqual(1, year_hash[1997])
        self.assertEqual(4, year_hash[1998])
        self.assertEqual(5, year_hash[1999])
        self.assertEqual(3, year_hash[2000])

        for name, year in student_info:
            self.assertEqual(year, input_hash[name])

    def test_complexity(self):
        from random import seed, shuffle
        lbound = -5000
        ubound = 10000

        seed(871847)

        data = [x for x in range(lbound, ubound)]

        for _ in range(5):
            shuffle(data)

            hashmap = HashMap()
            self.assertAlmostEqual(0, hashmap.load())
            for i in data:
                self.assertFalse(i in hashmap, i)
                hashmap[i] = i
                self.assertTrue(i in hashmap, i)
                self.assertEqual(i, hashmap[i], i)
            self.assertLessEqual(0.05, hashmap.load())
            self.assertGreaterEqual(hashmap.max_load_factor, hashmap.load())
            
            load = hashmap.load()
            size = 0
            for k, v in hashmap:
                self.assertEqual(k, v)
                size += 1
            self.assertEqual(len(data), len(hashmap.keys()))
            self.assertEqual(len(data), size)
            
            load = hashmap.load()
            for i in data:
                self.assertTrue(i in hashmap, i)
                self.assertEqual(i, hashmap[i], i)
                hashmap[i] = i * i
                self.assertTrue(i in hashmap, i)
                self.assertEqual(i * i, hashmap[i], i)
            self.assertAlmostEqual(load, hashmap.load())
            
            load = hashmap.load()
            for i in data:
                self.assertTrue(i in hashmap, i)
                self.assertEqual(i * i, hashmap[i], i)
                del hashmap[i]
                self.assertFalse(i in hashmap, i)
            self.assertAlmostEqual(0.0, hashmap.load())


    def test_sequence(self):
        hashmap = HashMap()
        hashmap['alpha'] = 5
        hashmap['bravo'] = 5
        hashmap['charlie'] = 7
        hashmap['delta'] = 5
        hashmap['echo'] = 4
        hashmap['foxtrot'] = 7
        hashmap['golf'] = 4
        hashmap['hotel'] = 5
        hashmap['india'] = 5
        hashmap['juliet'] = 6
        hashmap['kilo'] = 4
        hashmap['lima'] = 4
        hashmap['mike'] = 4
        self.assertEqual(13, len(hashmap))
        self.assertEqual(7, hashmap['charlie'])
        self.assertTrue('mike' in hashmap)
        self.assertFalse('november' in hashmap)
        self.assertEqual(6, hashmap['juliet'])
        self.assertTrue('alpha' in hashmap)
        self.assertFalse('sierra' in hashmap)
        self.assertEqual(13, len(hashmap))

        del hashmap['alpha']
        self.assertEqual(12, len(hashmap))
        hashmap['alfa'] = 4
        self.assertFalse('alpha' in hashmap)
        self.assertTrue('alfa' in hashmap)
        self.assertTrue('lima' in hashmap)
        self.assertEqual(5, hashmap['india'])
        self.assertEqual(13, len(hashmap))
        with self.assertRaises(KeyError):
            hashmap['alpha']

        hashmap['november'] = 8
        hashmap['oscar'] = 5
        hashmap['x-ray'] = 4
        hashmap['papa'] = 4
        hashmap['quebec'] = 6
        hashmap['romeo'] = 5
        hashmap['sierra'] = 6
        hashmap['tango'] = 5
        hashmap['uniform'] = 7
        self.assertEqual(22, len(hashmap))
        self.assertFalse('zulu' in hashmap)
        self.assertTrue('quebec' in hashmap)
        self.assertTrue('lima' in hashmap)
        self.assertEqual(5, hashmap['romeo'])
        self.assertEqual(4, hashmap['x-ray'])
        self.assertEqual(22, len(hashmap))
        with self.assertRaises(KeyError):
            hashmap['zulu']

        hashmap['victor'] = 6
        hashmap['whiskey'] = 7
        del hashmap['juliet']
        hashmap['juliett'] = 7
        hashmap['x-ray'] = 5
        hashmap['yankee'] = 6
        hashmap['zulu'] = 4
        self.assertEqual(26, len(hashmap))
        self.assertFalse('juliet' in hashmap)
        self.assertTrue('juliett' in hashmap)
        self.assertTrue('lima' in hashmap)
        self.assertFalse('alpha' in hashmap)
        self.assertEqual(5, hashmap['x-ray'])
        self.assertEqual(26, len(hashmap))
        with self.assertRaises(KeyError):
            hashmap['juliet']
        with self.assertRaises(KeyError):
            del hashmap['juliet']
        symbols = {'alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett', 'kilo',
                   'lima', 'mike', 'november', 'oscar', 'papa', 'quebec', 'romeo', 'sierra', 'tango', 'uniform', 'victor',
                   'whiskey', 'x-ray', 'yankee', 'zulu'}
        self.assertEqual(symbols, hashmap.keys())


if __name__ == '__main__':
    unittest.main()
