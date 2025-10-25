from task1 import find_elements, find_elements2
import unittest


class Test(unittest.TestCase):
    def test1(self):
        arr = [1, 2, 3, 5, 6]
        target = 8
        a, b = find_elements(arr, target)
        self.assertEqual(arr[a] + arr[b], target)

    def test2(self):
        arr = [1, 2, 3, 5, 6]
        target = 8
        a, b = find_elements2(arr, target)
        self.assertEqual(arr[a] + arr[b], target)

    def test3(self):
        arr = [1, 2, 3, 5, 6]
        target = 25
        result = find_elements(arr, target)
        self.assertEqual(result, [])

    def test4(self):
        arr = [1, 2, 3, 5, 6]
        target = 25
        result = find_elements2(arr, target)
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
