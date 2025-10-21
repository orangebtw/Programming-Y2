from main import gen_bin_tree, left_value, right_value, Node
import unittest

class Test(unittest.TestCase):
    def test1(self):
        self.assertEqual(
            gen_bin_tree(3, 2), 
            (2,
                (left_value(2),
                    (left_value(left_value(2)),
                        None,
                        None),
                    (right_value(left_value(2)),
                        None,
                        None)),
                (right_value(2),
                    (left_value(right_value(2)),
                        None,
                        None),
                    (right_value(right_value(2)),
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
