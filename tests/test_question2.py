import unittest

from code.question2 import process_instruction, process_entire_sequence


class Question2(unittest.TestCase):
    def test_part_a(self):
        sequence = [1,9,10,3,2,3,11,0,99,30,40,50]
        result = process_instruction(sequence, [1,9,10,3])
        step_1 = [1,9,10,70,2,3,11,0,99,30,40,50]
        self.assertListEqual(result, step_1)

        result = process_instruction(sequence, [2,3,11,0])
        step_2 = [3500,9,10,70,2,3,11,0,99,30,40,50]
        self.assertListEqual(step_2, result)

        sequence = [1,9,10,3,2,3,11,0,99,30,40,50]
        result = process_entire_sequence(sequence)
        self.assertListEqual(result, step_2)
        

    
    def test_part_b(self):
        pass

if __name__ == "__main__":
    unittest.main()
