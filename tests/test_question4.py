import unittest

from code.question4 import meets_criteria


class Question4(unittest.TestCase):
    def test_meets_criteria(self):
        self.assertTrue(meets_criteria(111112, check_for_2digit_group=False))
        self.assertTrue(meets_criteria(122355, check_for_2digit_group=False))
        self.assertTrue(meets_criteria(123455, check_for_2digit_group=False))
        self.assertTrue(meets_criteria(199999, check_for_2digit_group=False))

        self.assertFalse(meets_criteria(919999, check_for_2digit_group=False))
        self.assertFalse(meets_criteria(123456, check_for_2digit_group=False))
        self.assertFalse(meets_criteria(123436, check_for_2digit_group=False))
        self.assertFalse(meets_criteria(125436, check_for_2digit_group=False))

        self.assertFalse(meets_criteria(111111, check_for_2digit_group=True))
        self.assertTrue(meets_criteria(122355, check_for_2digit_group=True))
        self.assertTrue(meets_criteria(123455, check_for_2digit_group=True))
        self.assertFalse(meets_criteria(199999, check_for_2digit_group=True))

        self.assertFalse(meets_criteria(919999, check_for_2digit_group=True))
        self.assertFalse(meets_criteria(123456, check_for_2digit_group=True))
        self.assertFalse(meets_criteria(123436, check_for_2digit_group=True))
        self.assertFalse(meets_criteria(125436, check_for_2digit_group=True))


if __name__ == "__main__":
    unittest.main()
