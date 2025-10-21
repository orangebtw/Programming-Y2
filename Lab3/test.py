from main import gen_bin_tree, Node
import unittest

left_leaf = lambda x: x * 4
right_leaf = lambda x: x + 1

class Test(unittest.TestCase):
    def test1(self):
        self.assertEqual(
            gen_bin_tree(3, 2), 
            (2,
                (left_leaf(2),
                    (left_leaf(left_leaf(2)),
                        None,
                        None),
                    (right_leaf(left_leaf(2)),
                        None,
                        None)),
                (right_leaf(2),
                    (left_leaf(right_leaf(2)),
                        None,
                        None),
                    (right_leaf(right_leaf(2)),
                        None,
                        None)))
        )

    def test2(self):
        self.assertEqual(
            gen_bin_tree(1, 0),
            (0, None, None)
        )

if __name__ == "__main__":
    unittest.main()
