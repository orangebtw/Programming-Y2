from main import gen_bin_tree, Node
import unittest


def left_leaf(x):
    return x * 4


def right_leaf(x):
    return x + 1


class Test(unittest.TestCase):
    def test1(self):
        l = left_leaf
        r = right_leaf
        root = 2
        self.assertEqual(
            gen_bin_tree(3, root),
            (root,
                (l(root),
                    (l(l(root)),
                        (l(l(l(root))), None, None),
                        (r(l(l(root))), None, None)),
                    (r(l(root)),
                        (l(r(l(root))), None, None),
                        (r(r(l(root))), None, None))),
                (r(root),
                    (l(r(root)),
                        (l(l(r(root))), None, None),
                        (r(l(r(root))), None, None)),
                    (r(r(root)),
                        (l(r(r(root))), None, None),
                        (r(r(r(root))), None, None)))
             )
        )

    def test2(self):
        """Тест при нулевом height"""
        self.assertEqual(gen_bin_tree(0, 4), (4, None, None))

    def test3(self):
        """Тест при отрицательном height"""
        self.assertEqual(gen_bin_tree(-5, 4), None)

    def test4(self):
        l = left_leaf
        r = right_leaf
        root = 4
        self.assertEqual(
            gen_bin_tree(4, root),
            (root,
                (l(root),
                    (l(l(root)),
                        (l(l(l(root))),
                            (l(l(l(l(root)))), None, None),
                            (r(l(l(l(root)))), None, None)),
                        (r(l(l(root))),
                            (l(r(l(l(root)))), None, None),
                            (r(r(l(l(root)))), None, None))),
                    (r(l(root)),
                        (l(r(l(root))),
                            (l(l(r(l(root)))), None, None),
                            (r(l(r(l(root)))), None, None)),
                        (r(r(l(root))),
                            (l(r(r(l(root)))), None, None),
                            (r(r(r(l(root)))), None, None)))),
                (r(root),
                    (l(r(root)),
                        (l(l(r(root))),
                            (l(l(l(r(root)))), None, None),
                            (r(l(l(r(root)))), None, None)),
                        (r(l(r(root))),
                            (l(r(l(r(root)))), None, None),
                            (r(r(l(r(root)))), None, None))),
                    (r(r(root)),
                        (l(r(r(root))),
                            (l(l(r(r(root)))), None, None),
                            (r(l(r(r(root)))), None, None)),
                        (r(r(r(root))),
                            (l(r(r(r(root)))), None, None),
                            (r(r(r(r(root)))), None, None))))
             )
        )


if __name__ == "__main__":
    unittest.main()
