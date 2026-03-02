import unittest
from main import FetchCourses, ConvertToYAML, ConvertToCSV

class Test(unittest.TestCase):
    def test1(self):
        result = FetchCourses(['USD']).operation()[0]
        self.assertEqual(result['ID'], 'R01235')
        self.assertEqual(result['NumCode'], '840')
        self.assertEqual(result['CharCode'], 'USD')

    def test2(self):
        result = ConvertToYAML(FetchCourses(['USD'])).operation()
        lines = result.split('\n')
        self.assertEqual(lines[0], "- CharCode: USD")
        self.assertEqual(lines[1], "  ID: R01235")
        self.assertEqual(lines[2], "  Name: Доллар США")
        self.assertEqual(lines[3], "  Nominal: 1")
        self.assertEqual(lines[4], "  NumCode: '840'")
    
    def test3(self):
        result = ConvertToCSV(FetchCourses(['USD'])).operation()
        lines = result.split('\n')
        header = lines[0]
        values = lines[1].split(',')
        self.assertEqual(header, "ID,NumCode,CharCode,Nominal,Name,Value,Previous")
        self.assertEqual(values[0], "R01235")
        self.assertEqual(values[1], "840")
        self.assertEqual(values[2], "USD")
        self.assertEqual(values[3], "1")
        self.assertEqual(values[4], "Доллар США")

if __name__ == "__main__":
    unittest.main()
