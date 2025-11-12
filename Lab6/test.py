from main import get_currencies
import unittest

class Test(unittest.TestCase):
    def test1(self):
        result = get_currencies3(['USD', 'EUR'])

        self.assertIsNotNone(result)
        
        for k, v in result.items():
            self.assertIsInstance(k, str)
            self.assertIsInstance(v, float)

    def test2(self):
        result = get_currencies3(['KEK'])
        self.assertIsNone(result)

    def test3(self):
        result = get_currencies3(['USD'], 'https://google.com')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
