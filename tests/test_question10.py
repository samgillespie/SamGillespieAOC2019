import unittest

from code.question10 import *


def get_maps():
    map_1 = """.#..#
.....
#####
....#
...##"""
    map_1 = map_1.split("\n")
    map_2 = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""
    map_2 = map_2.split("\n")
        
    map_3 = """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###."""
    map_3 = map_3.split("\n")
        
    return [map_1, map_2, map_3]

class Question10(unittest.TestCase):

    def test_reading_map(self):
        [map_1, map_2, map_3] = get_maps()
        asteroids = convert_image_to_data(map_1)
        self.assertEqual(asteroids[0], [1, 0])
        self.assertEqual(len(asteroids), 10)

    def test_convert_asteroids_to_relative(self):
        positions = [[1,1], [2,3], [5, 10]]
        central = [2,3]
        test_vals = convert_asteroids_to_relative(positions, central)
        answer = [[-1, -2], [0, 0], [3, 7]]
        self.assertListEqual(answer, test_vals)
    
    def test_normalize_vector(self):
        vector = [4,6]
        test = normalize_vector(vector)
        self.assertEqual(test[0], 0.4)
        self.assertEqual(test[1], 0.6)

        vector = [4,5]
        test = normalize_vector(vector)
        self.assertEqual(test[0], 0.44444)
        self.assertEqual(test[1], 0.55555)

    def test_process_map(self):
        [map_1, map_2, map_3] = get_maps()
        ans1 = process_map(map_1)
        self.assertListEqual(ans1, [3, 4, 8])

        ans2 = process_map(map_2)
        self.assertListEqual(ans2, [5, 8, 33])

        ans3 = process_map(map_3)
        self.assertListEqual(ans3, [1, 2, 35])


if __name__ == "__main__":
    unittest.main()
