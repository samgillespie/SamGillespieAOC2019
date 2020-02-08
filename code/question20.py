
import copy
import os
import time

class Player():
    def __init__(self, current_space, x_size, y_size):
        self.previous_step = None
        self.current_space = current_space
        self.steps_taken = 0
        self.recursive_level = 0
        self.portals = portals
        self.x_size = x_size
        self.y_size = y_size
        
    def return_state(self):
        return {(self.current_space.x, self.current_space.y, self.recursive_level): self.steps_taken}

    def attempt_move_to_space(self, space):
        # Forbid the movement to a previous space, unless we have just picked up a key
        if self.previous_step is not None and self.previous_step.x == space.x and self.previous_step.y == space.y:
            return False        

        # Determine if we are traversing a portal
        if abs(space.x - self.current_space.x) > 1 or abs(space.y - self.current_space.y) > 1:
            # Are we in the edge area, then we pop out
            # Opposite, because we are looking at the future space
            if space.x < 5 or space.x > self.x_size - 7:
                self.recursive_level += 1
            elif space.y < 5 or space.y > self.y_size - 7:
                self.recursive_level += 1
            else:
                self.recursive_level -= 1

        if self.recursive_level < 0:
            return False

        self.previous_step = self.current_space
        self.current_space = space
        self.steps_taken += 1

        if self.current_space.content == "Z":
            if self.recursive_level == 0:
                return self.steps_taken
            else:
                return False
        
        return True


class Portals():
    def __init__(self):
        self.portal_coordinates = {}
        self.portals = {}

    def add_portal(self, name, coordinates):
        if name not in self.portal_coordinates:
            self.portal_coordinates[name] = set()
        self.portal_coordinates[name].add(coordinates)
    
    def convert_to_space_manager(self, space_manager):
        for portal_name in self.portal_coordinates:
            coords = list(self.portal_coordinates[portal_name])
            if len(coords) == 1 and portal_name == "AA":
                player_space = space_manager.get_space(coords[0][0], coords[0][1])
                player_space.content = "$"
                player = Player(player_space, space_manager.x_size, space_manager.y_size)
            elif len(coords) == 1 and portal_name == "ZZ":
                target_space = space_manager.get_space(coords[0][0], coords[0][1])
                target_space.content = "Z"
            else:
                portal1 = space_manager.get_space(coords[0][0], coords[0][1])
                portal1.content = "@"
                portal2 = space_manager.get_space(coords[1][0], coords[1][1])
                portal2.content = "@"
                portal1.add_adjacent(portal2)
                portal2.add_adjacent(portal1)
                self.portals[portal_name] = (portal1, portal2)
        return player


    def print_portals_to_map(self, donut_map):
        for i in self.portals:
            for (x,y) in self.portals[i]:
                donut_map[y][x] = "@"
        
        for row in donut_map:
            print("".join(row))



class Space():
    def __init__(self, x, y, donut_map, portals):
        self.content = donut_map[y][x]
        if self.content == " ":
            raise Exception("invalid Space")
        
        elif self.content == ".":
            self.x = x
            self.y = y
            self.adjacent_spaces = []

        elif self.content.isupper() is True:
            self.x = None
            self.y = None
            self.adjacent_spaces = []
            try:
                self.check_for_portals(x, y, donut_map, portals)
            except:
                raise Exception(f"Unhandled portal at {x,y} {donut_map[y][x]}")
        

    def check_for_portals(self,  x, y, donut_map, portals):
        # Left of the map
        if x == 0 or x == 1:
            portal_name = donut_map[y][0:2]
            portal_coords = (2, y)

        # Right of the map
        elif x == len(donut_map[0])-1 or x == len(donut_map[0])-2:
            portal_name = donut_map[y][-2:]
            portal_coords = (len(donut_map[0])-3, y)

        # Top of the map
        elif y == 0 or y == 1:
            portal_name = donut_map[0][x] + donut_map[1][x]
            portal_coords = (x, 2)

        # Bottom of the map
        elif y == len(donut_map)-1 or y == len(donut_map)-2:
            portal_name = donut_map[-2][x] + donut_map[-1][x]
            portal_coords = (x, len(donut_map)-3)

        # -> A
        #    B
        #    .
        elif donut_map[y+1][x].isupper() and donut_map[y+2][x] == ".":
            portal_name = donut_map[y][x] + donut_map[y+1][x]
            portal_coords = (x, y+2)
        
        #    A
        # -> B
        #    .
        elif donut_map[y-1][x].isupper() and donut_map[y+1][x] == ".":
            portal_name = donut_map[y-1][x] + donut_map[y][x]
            portal_coords = (x, y+1)
        
        # AB.
        # ^
        elif donut_map[y][x+1].isupper() and donut_map[y][x+2] == ".":
            portal_name = donut_map[y][x] + donut_map[y][x+1]
            portal_coords = (x+2, y)
    
        # AB.
        #  ^
        elif donut_map[y][x-1].isupper() and donut_map[y][x+1] == ".":
            portal_name = donut_map[y][x-1] + donut_map[y][x]
            portal_coords = (x+1, y)

        #    .
        # -> A
        #    B
        elif donut_map[y+1][x].isupper() and donut_map[y-1][x] == ".":
            portal_name = donut_map[y][x] + donut_map[y+1][x]
            portal_coords = (x, y-1)
        
        #    .
        #    A
        # -> B
        elif donut_map[y-1][x].isupper() and donut_map[y-2][x] == ".":
            portal_name = donut_map[y-1][x] + donut_map[y][x]
            portal_coords = (x, y-2)
        
        # .AB
        #  ^
        elif donut_map[y][x+1].isupper() and donut_map[y][x-1] == ".":
            portal_name = donut_map[y][x] + donut_map[y][x+1]
            portal_coords = (x-1, y)
    
        # .AB
        #   ^
        elif donut_map[y][x-1].isupper() and donut_map[y][x-2] == ".":
            portal_name = donut_map[y][x-1] + donut_map[y][x]
            portal_coords = (x-2, y)
        else:
            raise Exception(f"Unhandled portal at {x,y}")

        portals.add_portal(portal_name, portal_coords)


    def __str__(self):
        return f"{self.x}, {self.y}"
    
    def add_adjacent(self, space):
        if space in self.adjacent_spaces:
            return
        else:
            self.adjacent_spaces.append(space)
            if len(self.adjacent_spaces) > 5:
                raise Exception("TOO MANY ADJACENT SQUARES")

class SpaceManager():
    def __init__(self, x_size, y_size):
        self.spaces = []
        self.x_size = x_size
        self.y_size = y_size
    
    def add_space(self, new_space):
        (x, y) = (new_space.x, new_space.y)
        for space in self.spaces:
            if abs(space.x - x) + abs(space.y - y) == 1:
                space.add_adjacent(new_space)
                new_space.add_adjacent(space)
        self.spaces.append(new_space)

    def get_space(self, x, y):
        for i in self.spaces:
            if i.x == x and i.y == y:
                return i
        raise IndexError(f"Space {x,y} not found")

    def update_adjacencies(self):
        spaces = self.spaces
        self.spaces = []
        for space in spaces:
            space.adjacent_spaces = []
            self.add_space(space)
    
    def print_map(self, players=[]):
        os.system("cls")
        max_x = 0
        max_y = 0
        for i in self.spaces:
            if i.x > max_x:
                max_x = i.x
            if i.y > max_y:
                max_y = i.y

        max_x += 3
        max_y += 3

        row = ["#"] * max_x
        game_map = []
        for i in range(max_y):
            game_map.append(row.copy())
        
        for space in self.spaces:
            content = space.content
            if content is None:
                content = " "
            game_map[space.y][space.x] = content

        for player in players:
            recursive_level = str(player.recursive_level)[-1]
            game_map[player.current_space.y][player.current_space.x] = recursive_level

        game_rows = []
        for row in game_map:
            game_rows.append("".join(row))
        print("\n".join(game_rows))


def parse_map(input_map):
    """
    Returns all the spaces
    """
    inputs = input_map.split("\n")
    portals = Portals()

    x_size = len(inputs[0])
    y_size = len(inputs)
    space_manager = SpaceManager(x_size, y_size)
    for x in range(x_size):
        for y in range(y_size):
            content = inputs[y][x]
            if content == " " or content == "#":
                continue
            
            new_space = Space(x, y, inputs, portals)
            if new_space.x is None and new_space.y is None:
                continue
            space_manager.add_space(new_space)

    return [space_manager, portals]



def navigate_maze(space_manager, player):
    # Solution - At every fork, we create a new player from the current player
    active_players = [player]
    active_steps_taken = [0]    
    current_minimum = 999999
    previous_states = {(player.current_space.x, player.current_space.y, 0): 0}
    counter = 0
    while len(active_players) > 0:
        player_num = active_steps_taken.index(min(active_steps_taken))
        player = active_players[player_num]
        for adjacent_space in player.current_space.adjacent_spaces:
            if player.steps_taken > current_minimum:
                # A faster path has been found elsewhere
                continue
            new_player = copy.copy(player)

            # Check to make sure someone else hasn't found a faster path
            pos = list(new_player.return_state().keys())[0]
            steps = previous_states[pos]
            if new_player.steps_taken > steps:
                # Now redundant, proceed
                break

            attempt = new_player.attempt_move_to_space(adjacent_space)

            # If the movement failed, or we move to an already reached state
            # Do not keep the player moving
            if attempt is True:
                current_state = new_player.return_state()
                pos = list(current_state.keys())[0]
                if pos in previous_states and previous_states[pos] < current_state[pos]:
                    # Another player has reached here more efficiently
                    pass
                else:
                    active_players.append(new_player)
                    active_steps_taken.append(new_player.steps_taken)
                    previous_states.update(current_state)
            elif attempt is False:
                pass
            else:
                # We have reached the target
                current_minimum = attempt

        active_players.pop(player_num)
        active_steps_taken.pop(player_num)
        if len(active_steps_taken) > 0:
            time_counter = min(active_steps_taken)
            if counter < time_counter:
                space_manager.print_map(active_players)
                
            counter = time_counter
    return current_minimum

if __name__ == "__main__":
    with open("data\\q20input.txt") as f:
        input_map = f.read()
    print(input_map)
    [space_manager, portals] = parse_map(input_map)
    space_manager.print_map()
    player = portals.convert_to_space_manager(space_manager)
    steps = navigate_maze(space_manager, player)
    print(f"Steps: {steps}")
