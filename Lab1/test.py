import task1
import unittest

class Test(unittest.TestCase):
    def test1(self):
        result = task1.find_elements([1, 2, 3, 5, 6], 8)
        self.assertEqual(result, (1, 4))

    def test2(self):
        result = task1.find_elements([1, 2, 3, 5, 6], 25)
        self.assertEqual(result, None)
    
if __name__ == '__main__':
    unittest.main()
