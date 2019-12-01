import unittest

from code.question1 import calculate_fuel, calculate_fuel_with_recursion


class Question1(unittest.TestCase):
    def test_part_a(self):
        self.assertEqual(calculate_fuel([12]), 2)
        self.assertEqual(calculate_fuel([14]), 2)
        self.assertEqual(calculate_fuel([1969]), 654)
        self.assertEqual(calculate_fuel([100756]), 33583)
    
    def test_part_b(self):
        self.assertEqual(calculate_fuel_with_recursion([12]), 2)
        self.assertEqual(calculate_fuel_with_recursion([14]), 2)
        self.assertEqual(calculate_fuel_with_recursion([1969]), 966)
        self.assertEqual(calculate_fuel_with_recursion([100756]), 50346)

if __name__ == "__main__":
    unittest.main()
