

from execution_time import timeit
import math

class StateManager():
    def __init__(self):
        self.highest_layer = 0
        self.lowest_layer = 0
        self.states = {}
        
    def get_level(self, level):
        if level not in self.states:
            self.states[level] = State(self, [], level)
            if level > self.highest_layer:
                self.highest_layer = level
                self.states[level].calculate_adjacency(True, False)
            if level < self.lowest_layer:
                self.lowest_layer = level
                self.states[level].calculate_adjacency(False, True)
        return self.states[level]
    
    def print_states(self):
        keys = list(self.states.keys())
        keys.sort()
        for key in keys:
            state = self.states[key]
            row_val = "\n".join(["".join(i) for i in state.state])
            if row_val.find("#") != -1:
                print(f"Level: {key}")
                print(row_val)
    
    def print_bugs(self):
        keys = list(self.states.keys())
        keys.sort()
        for key in keys:
            state = self.states[key]
            print(f"Level: {key}")
            print("\n".join(["".join(str(i)) for i in state.step_bug_count]))
    
    def count_bugs(self):
        bugs = 0
        keys = list(self.states.keys())
        keys.sort()
        for key in keys:
            state = self.states[key]
            for x in range(5):
                for y in range(5):
                    if x == 2 and y == 2:
                        continue
                    if state.state[y][x] == "#":
                        bugs += 1
        return bugs


    def resolve_step(self):
        # Calculate Adjacencies First
        state_list = list(self.states.keys())
        state_list = state_list.copy()
        for i in state_list:
            state = self.states[i]
            if state.level == self.highest_layer:
                penultimate_layer = self.states[state.level-1]
                state.calculate_adjacency(penultimate_layer.has_upper_edge_bug(), False)
            if state.level == self.lowest_layer:
                penultimate_layer = self.states[state.level+1]
                state.calculate_adjacency(False, penultimate_layer.has_lower_edge_bug())
            state.calculate_adjacency(False, False)

        state_list = list(self.states.keys())
        for i in self.states:
            state = self.states[i].resolve_state()

class State():
    def __init__(self, state_manager, initial_state = [], level=0):
        self.level = level
        self.state_manager = state_manager
        if initial_state != []:
            self.state = initial_state
        else:
            self.state = [[".", ".", ".", ".", "."],
                          [".", ".", ".", ".", "."],
                          [".", ".", "?", ".", "."],
                          [".", ".", ".", ".", "."],
                          [".", ".", ".", ".", "."]]
        self.step_bug_count = None

        # For the first inital step added
        if self.level not in state_manager.states:
            state_manager.states[self.level] = self

    def calculate_adjacency(self, use_blank_upper=False, use_blank_lower=False):
        # Since we need to calculate adjacency for new layers,
        # and we don't want to recursively go up infinitely, let's enable a blank upper without an instance
        if use_blank_lower is False: 
            lower_state = self.state_manager.get_level(self.level-1)
            lower_state = lower_state.state
        else:
            lower_state = [[".", ".", ".", ".", "."],
                           [".", ".", ".", ".", "."],
                           [".", ".", "?", ".", "."],
                           [".", ".", ".", ".", "."],
                           [".", ".", ".", ".", "."]]
        if use_blank_upper is False: 
            upper_state = self.state_manager.get_level(self.level+1)
            upper_state = upper_state.state
        else:
            upper_state = [[".", ".", ".", ".", "."],
                           [".", ".", ".", ".", "."],
                           [".", ".", "?", ".", "."],
                           [".", ".", ".", ".", "."],
                           [".", ".", ".", ".", "."]]

        ymax = len(self.state)
        xmax = len(self.state[0])

        bug_final = []
        for y in range(ymax):
            bug_count = []
            for x in range(xmax):
                if y == 2 and x == 2:
                    bug_count.append(-1)
                    continue
                bugs = 0
                # UP
                if y == 0:
                    if upper_state[1][2] == "#":
                        bugs += 1
                else:                    
                    if self.state[y-1][x] == "#":
                        bugs += 1
                    elif self.state[y-1][x] == "?": 
                        # Check the bottom row of lower state
                        for elem in lower_state[4]:
                            if elem == "#":
                                bugs += 1
                # Down
                if y == ymax - 1:
                    if upper_state[3][2] == "#":
                        bugs += 1
                else:
                    if self.state[y+1][x] == "#":
                        bugs += 1
                    elif self.state[y+1][x] == "?":
                        # Check top row of lower state
                        for elem in lower_state[0]:
                            if elem == "#":
                                bugs += 1

                # Left
                if x == 0:
                    if upper_state[2][1] == "#":
                        bugs += 1
                else:
                    if self.state[y][x-1] == "#":
                        bugs += 1
                    elif self.state[y][x-1] == "?":
                        # Check Right column of lower state
                        for y_under in range(5):
                            if lower_state[y_under][4] == "#":
                                bugs += 1


                # Right
                if x == xmax -1:
                    if upper_state[2][3] == "#":
                        bugs += 1
                else:
                    if self.state[y][x+1] == "#":
                        bugs += 1
                    elif self.state[y][x+1] == "?":
                        # Check Left column of lower state
                        for y_under in range(5):
                            if lower_state[y_under][0] == "#":
                                bugs += 1

                bug_count.append(bugs)
            bug_final.append(bug_count)
        self.step_bug_count = bug_final
    
    def resolve_state(self):
        state = self.state
        if self.step_bug_count is None:
            raise Exception("Woah, resolution order bug")

        ymax = len(state)
        xmax = len(state[0])
        for x in range(xmax):
            for y in range(ymax):
                if x == 2 and y == 2:
                    continue
                if state[y][x] == "#":
                    if self.step_bug_count[y][x] != 1:
                        state[y][x] = "."
                elif state[y][x] == ".":
                    if self.step_bug_count[y][x] == 1 or self.step_bug_count[y][x] == 2:
                        state[y][x] = "#"
        self.step_bug_count = None
        return state
    
    def has_upper_edge_bug(self):
        upper_edge = [(0,0), (0,1), (0,2), (0,3), (0,4), (1,0), (2,0), (3,0),
                      (4,0), (4,1), (4,2), (4,3), (4,4), (3,4), (2,4), (1,4)]
        for (x,y) in upper_edge:
            if self.state[y][x] == "#":
                return True
        return False

    def has_lower_edge_bug(self):
        lower_edge = [(2,1), (2,3), (3,2), (1,2)]
        for (x,y) in lower_edge:
            if self.state[y][x] == "#":
                return True
        return False

@timeit
def question_24():
    import os
    os.system("cls")
    with open("data\\q24input.txt") as f:
        input_data = f.read()
    input_data = input_data.split("\n")
    
    #input_data = ["....#", "#..#.", "#..##", "..#..", "#...."]
    input_data[2] = input_data[2][0:2] + "?" + input_data[2][3:5]
    game_state = [list(i) for i in input_data]
    print(game_state)
    

    state_manager = StateManager()
    State(state_manager, game_state, 0)
    
    # Instantiate the first upper and lower level
    state_manager.get_level(1)
    state_manager.get_level(-1)
    
    for iteration in range(0,200):
        print(f"Starting Iteration {iteration}")
        state_manager.resolve_step()
    state_manager.print_states()
    #    if iteration == 9:
    #        break
    
    print(f"Number of bugs: {state_manager.count_bugs()}")



if __name__ == "__main__":
    question_24()

    # Too Low 1922