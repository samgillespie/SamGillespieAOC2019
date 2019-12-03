import unittest

from code.question3 import convert_instructions_to_points
from code.question3 import find_closest_intersection_of_two_paths
from code.question3 import process_input
from code.question3 import find_lowest_steps_of_two_paths


class Question3(unittest.TestCase):
    def test_convert_instructions_to_points(self):
        instruction = ["R2"]
        ans = convert_instructions_to_points(instruction)
        self.assertEqual(list(ans), [(1,0), (2,0)])

        instruction = ["L2"]
        ans = convert_instructions_to_points(instruction)
        self.assertEqual(list(ans), [(-1,0), (-2,0)])

        instruction = ["U2"]
        ans = convert_instructions_to_points(instruction)
        self.assertEqual(list(ans), [(0,1), (0,2)])

        instruction = ["D2"]
        ans = convert_instructions_to_points(instruction)
        self.assertEqual(list(ans), [(0,-1), (0,-2)])

        instruction = ["D2", "R2"]
        ans = convert_instructions_to_points(instruction)
        self.assertEqual(list(ans), [(0,-1), (0,-2), (1, -2), (2, -2)])


    def test_a_with_cases(self):
        ins_a = "R8,U5,L5,D3"
        ins_b = "U7,R6,D4,L4"
        map_a = convert_instructions_to_points(ins_a.split(','))
        map_b = convert_instructions_to_points(ins_b.split(','))
        print(map_a)
        ans = find_closest_intersection_of_two_paths(map_a, map_b)
        self.assertEqual(ans, 6)

        ins_a = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
        ins_b = "U62,R66,U55,R34,D71,R55,D58,R83"
        map_a = convert_instructions_to_points(ins_a.split(','))
        map_b = convert_instructions_to_points(ins_b.split(','))
        ans = find_closest_intersection_of_two_paths(map_a, map_b)
        self.assertEqual(ans, 159)

        ins_a = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
        ins_b = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
        map_a = convert_instructions_to_points(ins_a.split(','))
        map_b = convert_instructions_to_points(ins_b.split(','))
        ans = find_closest_intersection_of_two_paths(map_a, map_b)
        self.assertEqual(ans, 135)

    def test_b_with_cases(self):
        ins_a = "R8,U5,L5,D3"
        ins_b = "U7,R6,D4,L4"
        map_a = convert_instructions_to_points(ins_a.split(','))
        map_b = convert_instructions_to_points(ins_b.split(','))
        print(map_a)
        ans = find_lowest_steps_of_two_paths(map_a, map_b)
        self.assertEqual(ans, 30)

        ins_a = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
        ins_b = "U62,R66,U55,R34,D71,R55,D58,R83"
        map_a = convert_instructions_to_points(ins_a.split(','))
        map_b = convert_instructions_to_points(ins_b.split(','))
        ans = find_lowest_steps_of_two_paths(map_a, map_b)
        self.assertEqual(ans, 610)

        ins_a = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
        ins_b = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
        map_a = convert_instructions_to_points(ins_a.split(','))
        map_b = convert_instructions_to_points(ins_b.split(','))
        ans = find_lowest_steps_of_two_paths(map_a, map_b)
        self.assertEqual(ans, 410)


if __name__ == "__main__":
    unittest.main()
