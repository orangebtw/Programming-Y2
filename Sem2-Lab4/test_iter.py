import unittest
from unittest import TestCase

from iter import FibonacciIter
from getitem import FibonacciGetItem

class TestFibonacciIter(TestCase):
    def test1(self):
        self.assertEqual(list(FibonacciIter(range(10))), [0, 1, 2, 3, 5, 8])
        self.assertEqual(list(FibonacciGetItem(range(10))), [0, 1, 2, 3, 5, 8])

    def test2(self):
        self.assertEqual(list(FibonacciIter(range(0))), [])
        self.assertEqual(list(FibonacciGetItem(range(0))), [])

    def test3(self):
        self.assertEqual(list(FibonacciIter(range(1))), [0])
        self.assertEqual(list(FibonacciGetItem(range(1))), [0])

if __name__ == "__main__":
    unittest.main()
