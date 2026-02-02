import unittest
from unittest import TestCase

from gen_fib import my_genn, fib_coroutine

class TestGenFib(TestCase):
    def setUp(self):
        self.gen = fib_coroutine(my_genn)()
    
    def test1(self):
        self.assertEqual(self.gen.send(6), [0, 1, 1, 2, 3, 5])

    def test2(self):
        self.assertEqual(self.gen.send(0), [])
        
if __name__ == "__main__":
    unittest.main()