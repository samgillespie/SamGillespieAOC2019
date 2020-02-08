
import copy
import os
import time

class Player():
    def __init__(self, current_space):
        self.previous_step = None
        self.current_space = current_space
        self.picked_up = False
        self.inventory = list()
        self.target_keys = list()
        self.steps_taken = 0
    
    def give_key_target(self, list_of_keys_needed):
        self.target_keys = set(list_of_keys_needed)
        
    def return_state(self):
        return (self.current_space.x, self.current_space.y, tuple(sorted(self.inventory)))

    def attempt_move_to_space(self, space):
        # Forbid the movement to a previous space, unless we have just picked up a key
        # print("### Previous step Check###")
        # print(self.previous_step)
        # print(space)
        # if self.previous_step is not None:
        #     print((self.previous_step.x == space.x and self.previous_step.y == space.y))
        if self.previous_step is not None and self.previous_step.x == space.x and self.previous_step.y == space.y and self.picked_up is False:
            return False        
        # Check for locked door
        if space.content is not None and space.content.isupper():
            if space.content.lower() not in self.inventory:
                return False

        self.previous_step = self.current_space
        self.current_space = space

        self.steps_taken += 1
        #print(f"Step {self.steps_taken}: Moving to {(space.x, space.y)}")

        # pick up key
        if space.content is not None and space.content.islower() and space.content not in self.inventory:
            self.inventory.append(space.content)
            self.picked_up = True
            # Check for win state
            if len(self.inventory) == len(self.target_keys):
                print((self.inventory, self.steps_taken))
                
                return self.steps_taken
        else:
            self.picked_up = False

        return True
        
    

class Space():
    def __init__(self, x, y, content):
        self.x = x
        self.y = y
        if content is None or content == "@" or content == '.':
            self.content = None
        else:
            self.content = content
        
        self.adjacent_spaces = []
    
    def __str__(self):
        return f"{self.x}, {self.y}"
    
    def add_adjacent(self, space):
        if space in self.adjacent_spaces:
            return
        else:
            self.adjacent_spaces.append(space)
            if len(self.adjacent_spaces) > 4:
                raise Exception("TOO MANY ADJACENT SQUARES")

class SpaceManager():
    def __init__(self):
        self.spaces = []
    
    def add_space(self, new_space):
        (x, y) = (new_space.x, new_space.y)
        for space in self.spaces:
            if abs(space.x - x) + abs(space.y - y) == 1:
                space.add_adjacent(new_space)
                new_space.add_adjacent(space)
        self.spaces.append(new_space)

    def fetch_target_key_list(self):
        key_list = []
        for space in self.spaces:
            if space.content is not None and space.content.islower():
                key_list.append(space.content)
        return key_list
    
    def prune_dead_paths(self):
        starting_paths = []
        for space in self.spaces:
            if len(space.adjacent_spaces) == 1 and space.content is None:
                starting_paths.append(space)

        dead_cells = []
        for path in starting_paths:
            previous_step = path
            walker = path
            while True:
                if len(walker.adjacent_spaces) > 2:
                    break
                if walker.content is not None:
                    break
                
                if len(walker.adjacent_spaces) == 1 and walker.adjacent_spaces[0] not in dead_cells:
                    previous_step = walker
                    dead_cells.append(previous_step)
                    walker = walker.adjacent_spaces[0]
                elif len(walker.adjacent_spaces) == 1:
                    break

                elif walker.adjacent_spaces[0].x != previous_step.x or walker.adjacent_spaces[0].y != previous_step.y:
                    previous_step = walker
                    dead_cells.append(previous_step)
                    walker = walker.adjacent_spaces[0]
                elif walker.adjacent_spaces[1].x != previous_step.x or walker.adjacent_spaces[1].y != previous_step.y:
                    previous_step = walker
                    dead_cells.append(previous_step)
                    walker = walker.adjacent_spaces[1]
                else:
                    break

                dead_cells.append(walker)
            dead_cells.pop()

        dead_cells = list(set(dead_cells))
        len_cells = len(dead_cells)
        for dead_cell in dead_cells:
            self.spaces.remove(dead_cell)
        self.update_adjacencies()
        return len_cells

    def update_adjacencies(self):
        spaces = self.spaces
        self.spaces = []
        for space in spaces:
            space.adjacent_spaces = []
            self.add_space(space)
    
    def print_map(self, players=None):
        os.system("cls")
        max_x = 0
        max_y = 0
        for i in self.spaces:
            if i.x > max_x:
                max_x = i.x
            if i.y > max_y:
                max_y = i.y

        max_x += 2
        max_y += 2

        row = ["#"] * max_y
        game_map = []
        for i in range(max_x):
            game_map.append(row.copy())
        
        for space in self.spaces:
            content = space.content
            if content is None:
                content = " "
            game_map[space.x][space.y] = content
        if players is not None:
            for player in players:
                game_map[player.current_space.x][player.current_space.y] = "@"

        game_rows = []
        for row in game_map:
            game_rows.append("".join(row))
        print("\n".join(game_rows))






def parse_map(input_map):
    """
    Returns all the spaces
    """
    inputs = input_map.split("\n")
    space_manager = SpaceManager()
    for input_row in enumerate(inputs):
        row_data = input_row[1]
        row_number = input_row[0]
        for column_num in range(0, len(row_data)):
            content = row_data[column_num]
            if content == "#":
                continue
            
            new_space = Space(row_number, column_num, content)

            if content == "@":
                player = Player(new_space)
            space_manager.add_space(new_space)
    return [space_manager, player]


def run_simulation(space_manager, player):
    # Solution - At every fork, we create a new player from the current player
    player.give_key_target(space_manager.fetch_target_key_list())

    active_players = [player]
    active_steps_taken = [0]
    print(active_players)
    total_steps_taken = []
    current_minimum = 999999
    previous_states = set()
    counter = 0
    while len(active_players) > 0:
        player_num = active_steps_taken.index(min(active_steps_taken))
        player = active_players[player_num]
        for adjacent_space in player.current_space.adjacent_spaces:
            if player.steps_taken > current_minimum:
                # A faster path has been found elsewhere
                continue
            new_player = copy.copy(player)
            new_player.inventory = player.inventory.copy()
            attempt = new_player.attempt_move_to_space(adjacent_space)

            # If the movement failed, or we move to an already reached state
            # Do not keep the player moving
            if attempt is True:
                current_state = new_player.return_state()
                if current_state not in previous_states:
                    active_players.append(new_player)
                    active_steps_taken.append(new_player.steps_taken)
                    previous_states.add(current_state)
            elif attempt is False:
                pass
            else:
                total_steps_taken.append(attempt)
                current_minimum = min(total_steps_taken)



        #print(min(active_steps_taken), len(active_players))
        active_players.pop(player_num)
        active_steps_taken.pop(player_num)
        if len(active_steps_taken) > 0:
            time_counter = min(active_steps_taken)
            if counter < time_counter:
                space_manager.print_map(active_players)
                #for i in active_players:
                #    print(i.return_state())
            
            counter = time_counter
    print("TARGET LIST")
    print(space_manager.fetch_target_key_list())
    return total_steps_taken
    


if __name__ == "__main__":
    input_map = """########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""


    with open("data\\q18input.txt") as f:
        input_map = f.read()
    [space_manager, player] = parse_map(input_map)
    cells_pruned = 1
    while cells_pruned > 0:
        cells_pruned = space_manager.prune_dead_paths()
    space_manager.print_map()
    steps_taken = run_simulation(space_manager, player)

    print(f"Shortest path {min(steps_taken)}")