# Pasted for this r/adventofcode comment:
# https://www.reddit.com/r/adventofcode/comments/ecogl3/2019_day_19_solutions/fbex8km/

from question9 import Computer


def get_data():
    with open("data\\q19input.txt") as f:
        data = f.read().rstrip()
    intcode_program = data.split(",")
    intcode_program = list(map(int, intcode_program))
    return intcode_program


def inbeam(program, point):
    computer = Computer(program, point)
    computer.set_input(point)
    return computer.execute_until_output()

def part2(program, bottom_left=(0, 10), square_size=100):
    coord_diff = square_size - 1

    while True:
        if inbeam(program, bottom_left):
            top_right = (bottom_left[0] + coord_diff, bottom_left[1] - coord_diff)
            if inbeam(program, top_right):  # True implies top_left and bottom_right
                top_left = (bottom_left[0], bottom_left[1] - coord_diff)
                return 10000 * top_left[0] + top_left[1]

            bottom_left = bottom_left[0], bottom_left[1] + 1
        else:
            bottom_left = bottom_left[0] + 1, bottom_left[1]


def main(data):
    print("Part 2: {}".format(part2(data)))


if __name__ == "__main__":
    try:
        data = get_data()
    except FileNotFoundError:
        print("Input file not found")

    main(data)
