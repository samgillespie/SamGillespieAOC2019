
from execution_time import timeit
import math

# Ok so here's my approach.
# Build up a list of all the asteroids
# For each asteroid, convert all the other asteriods into a distance vector
# Normalize all the vectors, and when there are two identical vectors, take the vector with
# The shortest distance.

# Could use symmetry.  If A -> B, then B -> A

def convert_image_to_data(image_map):
    x_len = len(image_map[0])
    y_len = len(image_map)
    asteroid_locations = []
    for y in range(y_len):
        for x in range(x_len):
            if image_map[y][x] == "#":
                asteroid_locations.append([x, y])
    return asteroid_locations

def assign_str_value(string, pos, value):
    return string[0:pos] + str(value) + string[pos+1:]

def convert_data_to_image(initial_map, image_data, counts):
    x_len = len(initial_map[0])
    y_len = len(initial_map)
    new_map = ["." * x_len] * y_len
    for asteroid_num in range(len(image_data)):
        x = image_data[asteroid_num][0]
        y = image_data[asteroid_num][1]
        new_map[y] = assign_str_value(new_map[y], x, counts[asteroid_num])
    return new_map


def convert_asteroids_to_relative(asteroids, central_asteroid):
    relative_asteroid_pos = []
    for asteroid in asteroids:
        rel_pos_x = asteroid[0] - central_asteroid[0]
        rel_pos_y = asteroid[1] - central_asteroid[1]
        relative_asteroid_pos.append([rel_pos_x, rel_pos_y])
    return relative_asteroid_pos

def normalize_vector(vector):
    total = abs(vector[0]) + abs(vector[1])
    if total == 0:
        return [0, 0, 0]
    # Round to prevent floating point errors
    x = int(vector[0]/total * 100000)/100000
    y = int(vector[1]/total * 100000)/100000
    return [x, y, total]

def convert_asteroids_to_normalized(asteroids, central_asteroid):
    normalized_asteroid_pos = []
    for asteroid in asteroids:
        if asteroid == []:
            # Destroyed-asteroid
            return []
        rel_pos_x = asteroid[0] - central_asteroid[0]
        rel_pos_y = asteroid[1] - central_asteroid[1]
        normalized_asteroid_pos.append(normalize_vector([rel_pos_x, rel_pos_y]))
    return normalized_asteroid_pos


def count_asteroids(mapping):
    count = 0
    for x in mapping:
        for y in mapping[x]:
            count += 1
    
    # minus 1 because it counts itself
    return count - 1


def return_closest_asteroids(asteroids, central_asteroid):
    normalized_asteroids = convert_asteroids_to_normalized(asteroids, central_asteroid)
    # so we have a list of [x, y, dist] objects
    visible_asteroids = {}

    for asteroid in enumerate(normalized_asteroids):
        if asteroid[1] == []:
            # Destroyed-asteroid
            continue
        x = asteroid[1][0]
        y = asteroid[1][1]
        dist = asteroid[1][2]
        asteroid_number = asteroid[0]
        if x in visible_asteroids:
            if y in visible_asteroids[x]:
                if visible_asteroids[x][y]["distance"] > dist:
                    visible_asteroids[x][y] = {"distance": dist, "position": asteroid_number}
            else:
                visible_asteroids[x][y] = {"distance": dist, "position": asteroid_number}
        else:
            visible_asteroids[x] = {}
            visible_asteroids[x][y] = {"distance": dist, "position": asteroid_number}
    return visible_asteroids


def count_visible_asteroids(asteroids, central_asteroid):
    visible_asteroids = return_closest_asteroids(asteroids, central_asteroid)
    return count_asteroids(visible_asteroids)


def get_counts(map_data):
    counts = []
    for asteroid in map_data:
        counts.append(count_visible_asteroids(map_data, asteroid))
    return counts


def process_map(input_data):
    map_data = convert_image_to_data(input_data)
    counts = get_counts(map_data)

    best_asteroid = counts.index(max(counts))
    return map_data[best_asteroid] + [counts[best_asteroid]]


def perform_laser_sweep(central_asteroid, alive_asteroids):
    # Does one full rotation
    
    asteroid_map = return_closest_asteroids(alive_asteroids, central_asteroid)
    asteroid_list = []
    for x in asteroid_map:
        for y in asteroid_map[x]:
            if x == 0 and y == 0:
                continue
            # degrees is 0 on the y axis.
            degrees = math.atan2(x, -y)/math.pi*180
            if degrees < 0:
                degrees = 360 + degrees
            asteroid_list.append([x, y, asteroid_map[x][y]["position"], degrees])
    asteroid_list.sort(key=lambda x: x[3])
    destroyed = [x[2] for x in asteroid_list]
    return destroyed

def destroy_with_lasers_until_asteroid_number(central_asteroid, alive_asteroids, target_number):
    asteroids = alive_asteroids.copy()
    destroyed_counter = 0
    while True:
        destroyed = perform_laser_sweep(central_asteroid, asteroids)
        for i in destroyed:
            destroyed_counter += 1
            if destroyed_counter == target_number:
                return asteroids[i]
            else:
                asteroids[i] == []

@timeit
def question_10():
    with open("data\\q10input.txt") as f:
        input_data = f.read()
    input_data = input_data.split("\n")
    answer = process_map(input_data) 
    print(answer)
    print(f"Question 10a: {answer[2]}")

    map_data = convert_image_to_data(input_data)
    num200 = destroy_with_lasers_until_asteroid_number([answer[0], answer[1]], map_data, 200)
    print(f"Question 10b: {num200[0]*100 + num200[1]}")
    # map_data = convert_image_to_data(input_data)
    # newmap = convert_data_to_image(input_data, map_data, counts)
    # print("\n".join(newmap))


if __name__ == "__main__":
    question_10()
