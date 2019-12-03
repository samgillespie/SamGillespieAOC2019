
from execution_time import timeit


def convert_instructions_to_points(instructions):
    traversed_positions = list()
    current_position = (0,0)
    # Don't include (0,0) in traversed positions, otherwise it will be the closest
    # Intersection in both lists
    for instruction in instructions:
        direction = instruction[0]
        distance = int(instruction[1:])
        for i in range(0, distance):
            if direction == "R":
                current_position = (current_position[0]+1, current_position[1])
            elif direction == "L":
                current_position = (current_position[0]-1, current_position[1])
            elif direction == "U":
                current_position = (current_position[0], current_position[1]+1)
            elif direction == "D":
                current_position = (current_position[0], current_position[1]-1)
            traversed_positions.append(current_position)
    print("Got Traversed List")
    return traversed_positions


def find_closest_intersection_of_two_paths(positions_a, positions_b):
    set_a = set(positions_a)
    set_b = set(positions_b)
    intersections = set_a & set_b
    print("Found Intersections")
    min_distance = 99999999
    for intersection in intersections:
        distance = abs(intersection[0]) + abs(intersection[1])
        if distance < min_distance:
            min_distance = distance
    print("Finding Shortest Distance")
    return min_distance
    

def find_lowest_steps_of_two_paths(positions_a, positions_b):
    # Get all intersections:
    set_a = set(positions_a)
    set_b = set(positions_b)
    intersections = set_a & set_b
    min_number_of_steps = 999999999
    for intersection in intersections:
        steps_a = positions_a.index(intersection)
        steps_b = positions_b.index(intersection)
        distance = steps_a + steps_b
        if distance < min_number_of_steps:
            min_number_of_steps = distance
    return min_number_of_steps + 2 # Plus two because of the initial step off the (0, 0)


def process_input(instruct_a, instruct_b):
    path_a = convert_instructions_to_points(instruct_a)
    path_b = convert_instructions_to_points(instruct_b)
    intersections = find_closest_intersection_of_two_paths(path_a, path_b)
    lowest_steps = find_lowest_steps_of_two_paths(path_a, path_b)
    return [intersections, lowest_steps]


@timeit
def question_3():
    with open("data\\q3input.txt") as f:
        input_data = f.read()
    (instruct_a, instruct_b) = input_data.split("\n")
    [ans_a, ans_b] = process_input(instruct_a.split(","), instruct_b.split(","))
    print(f"Question 3a: {ans_a}")
    print(f"Question 3b: {ans_b}")



if __name__ == "__main__":
    question_3()
