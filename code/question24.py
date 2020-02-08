

from execution_time import timeit
import math

def calculate_adjacency(current_state):
    ymax = len(current_state)
    xmax = len(current_state[0])

    bug_final = []
    empty_final = []
    for y in range(ymax):
        bug_count = []
        empty_count = []
        for x in range(xmax):
            bugs = 0
            empty_spaces = 0
            # UP
            if y != 0:
                if current_state[y-1][x] == "#":
                    bugs += 1
                else:
                    empty_spaces += 1
            else:
                empty_spaces += 1
            # Down
            if y != ymax - 1:
                if current_state[y+1][x] == "#":
                    bugs += 1
                else:
                    empty_spaces += 1
            else:
                empty_spaces += 1

            # Left
            if x != 0:
                if current_state[y][x-1] == "#":
                    bugs += 1
                else:
                    empty_spaces += 1
            else:
                empty_spaces += 1

            # Right
            if x != xmax -1:
                if current_state[y][x+1] == "#":
                    bugs += 1
                else:
                    empty_spaces += 1
            else:
                empty_spaces += 1
            bug_count.append(bugs)
            empty_count.append(empty_spaces)
        bug_final.append(bug_count)
        empty_final.append(empty_count)
    
    return [bug_final, empty_final]

def resolve_state_for_one_step(state):
    ymax = len(state)
    xmax = len(state[0])
    [bug_count, empty_count] = calculate_adjacency(state)
    for x in range(xmax):
        for y in range(ymax):
            if state[y][x] == "#":
                if bug_count[y][x] != 1:
                    state[y][x] = "."
            elif state[y][x] == ".":
                if bug_count[y][x] == 1 or bug_count[y][x] == 2:
                    state[y][x] = "#"
    return state

def calculate_biodiversity(state):
    ymax = len(state)
    xmax = len(state[0])
    power = 0
    rating = 0
    for y in range(xmax):
        for x in range(ymax):
            if state[y][x] == "#":
                rating += int(math.pow(2, power))
            power += 1
    return rating

@timeit
def question_24():
    with open("data\\q24input.txt") as f:
        input_data = f.read()
    input_data = input_data.split("\n")
    
    #input_data = ["....#", "#..#.", "#..##", "..#..", "#...."]
    game_state = [list(i) for i in input_data]
    
    # Track the biodiversity Ratings
    ratings = set()
    counter = 0
    while True:
        rating = calculate_biodiversity(game_state)
            
        if rating in ratings:
            print(game_state)
            print(f"Question 24a: {rating}")
            break
        ratings.add(rating)
        game_state = resolve_state_for_one_step(game_state)
        counter += 1
        print(ratings)
        if counter % 100 == 0:
            print(counter)
        



if __name__ == "__main__":
    question_24()

    # Too Low 520
    # TOo High 26214449