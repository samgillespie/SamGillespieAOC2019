
from question9 import Computer, TerminateSequence
import os
import copy

clear = lambda: os.system('cls')


class Robot():
    def __init__(self, computer, ship_map):
        self.x = 0
        self.y = 0
        self.heading = "north"
        self.computer = computer
        self.ship_map = ship_map
        self.icons = "▲►▼◄"
        self.ship_map.robot = self

    def move(self):
        if self.heading == "north":
            self.computer.set_input([1])
            target = (self.x, self.y+1)
        elif self.heading == "south":
            self.computer.set_input([2])
            target = (self.x, self.y-1)
        elif self.heading == "west":
            self.computer.set_input([3])
            target = (self.x-1, self.y)
        elif self.heading == "east":
            self.computer.set_input([4])
            target = (self.x+1, self.y)
        else:
            raise Exception(f"Invalid heading is {self.heading}")
        
        result = self.computer.execute_until_output()

        if result == 0:
            self.ship_map.update_map(target[0], target[1], "#")
        elif result == 1:
            self.ship_map.update_map(target[0], target[1], ".")
            (self.x, self.y) = target
        elif result == 2:
            self.ship_map.update_map(target[0], target[1], "O")
            (self.x, self.y) = target
        return result
    
    def rotate_right(self):
        if self.heading == "north":
            self.heading = "east"
        elif self.heading == "east":
            self.heading = "south"
        elif self.heading == "south":
            self.heading = "west"
        elif self.heading == "west":
            self.heading = "north"

    def rotate_left(self):
        if self.heading == "north":
            self.heading = "west"
        elif self.heading == "west":
            self.heading = "south"
        elif self.heading == "south":
            self.heading = "east"
        elif self.heading == "east":
            self.heading = "north"
    
    def get_robot_position(self):
        if self.heading == "north":
            icon = self.icons[0]
        elif self.heading == "east":
            icon = self.icons[1]
        elif self.heading == "south":
            icon = self.icons[2]
        elif self.heading == "west":
            icon = self.icons[3]
        return (self.x, self.y, icon)
    



class ShipMap():
    map_data = {(0,0): "S"}
    robot = None

    def update_map(self, x, y, value):
        if (x, y) not in self.map_data:
            self.map_data[(x,y)] = value

    
    def print_map(self):
        coordinate_list = list(self.map_data.keys())
        x_data = [i[0] for i in coordinate_list]
        y_data = [i[1] for i in coordinate_list]
        (min_x, max_x) = (min(x_data), max(x_data))
        (min_y, max_y) = (min(y_data), max(y_data))
        x_length = max_x - min_x + 1 
        
        # Prepare list
        print_map = []
        for _ in range(max_y - min_y + 1):
            row = [" "] *x_length
            print_map.append(row)

        for map_key in self.map_data:
            x = map_key[0] - min_x
            y = map_key[1] - min_y

            print_map[y][x] = self.map_data[map_key]

        # Print robot position        
        robot_pos = self.robot.get_robot_position()
        x = robot_pos[0] - min_x
        y = robot_pos[1] - min_y
        print_map[y][x] = robot_pos[2]
        
        # Display map
        print_map.reverse()
        for row in print_map:
            print("".join(row))


def question_15_generate_map():
    with open("data\\q15input.txt") as f:
        input_data = f.read()
    intcode_program = input_data.split(",")
    intcode_program = list(map(int, intcode_program))

    # Create initial state
    computer = Computer(intcode_program, [2])
    ship_map = ShipMap()
    robot = Robot(computer, ship_map)


    # Keep attempting to move left and forward
    counter = 0
    while counter < 10000:
        counter += 1
        result1 = robot.move()
        robot.rotate_right()
        result2 = robot.move()

        # If both forward and right are walls, lets go left
        if result1 == 0 and result2 == 0:
            robot.rotate_right()
            robot.rotate_right()
        
        # If forward is a wall, and right is clear to go, lets go right
        elif result1 == 0 and result2 == 1:
            pass

        # if forward is not a wall and right is a wall, lets go forward
        elif result1 == 1 and result2 == 0:
            robot.rotate_left()

        # if forward is not a wall and right is not a wall, lets go right
        elif result1 == 1 and result2 == 1:
            pass
        os.system("cls")
        print(counter)
        if robot.x == 0 and robot.y == 0:
            ship_map.print_map()
            break



##########
#   ^^^^^^^^
#   For generating the map
#
#
#   For operating the map
##########

class Player():
    def __init__(self, current_space, oxygenate=False):
        self.previous_step = None
        self.current_space = current_space
        self.steps_taken = 0
        self.oxygenate = oxygenate

    def return_state(self):
        return (self.current_space.x, self.current_space.y)

    def attempt_move_to_space(self, space):
        if self.previous_step is not None and self.previous_step.x == space.x and self.previous_step.y == space.y:
            return False        

        self.previous_step = self.current_space
        self.current_space = space

        if self.oxygenate == True:
            self.current_space.content = "O"

        self.steps_taken += 1

        # pick up key
        if space.content == "O":
            return True
        return False
        

class Space():
    def __init__(self, x, y, content):
        self.x = x
        self.y = y
        if content is None or content == '.':
            self.content = None
        elif content == "@":
            self.content = "."
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
    
    def get_space(self, x, y):
        for space in self.spaces:
            if space is None:
                continue
            print(space)
            if space.x == x and space.y == y:
                return space
        raise ValueError("Not Found")

    def add_space(self, new_space):
        (x, y) = (new_space.x, new_space.y)
        for space in self.spaces:
            if abs(space.x - x) + abs(space.y - y) == 1:
                space.add_adjacent(new_space)
                new_space.add_adjacent(space)
        self.spaces.append(new_space)

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
        


def parse_map(input_map, player_content="S"):
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

            if content == player_content:
                player = Player(new_space, content=="O")
            space_manager.add_space(new_space)
    return [player, space_manager]


def run_simulation(space_manager, player):
    # Solution - At every fork, we create a new player from the current player
    active_players = [player]
    active_steps_taken = [0]
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
            reached_target = new_player.attempt_move_to_space(adjacent_space)

            # If the movement failed, or we move to an already reached state
            # Do not keep the player moving
            if reached_target is True:
                print(f"TARGET REACHED IN {player.steps_taken} STEPS")
                active_players = []
                break
                
            elif reached_target is False:
                current_state = new_player.return_state()
                if current_state not in previous_states:
                    active_players.append(new_player)
                    active_steps_taken.append(new_player.steps_taken)
                    previous_states.add(current_state)

        active_players.pop(player_num)
        active_steps_taken.pop(player_num)
        if len(active_steps_taken) > 0:
            time_counter = min(active_steps_taken)
            if counter < time_counter:
                space_manager.print_map(active_players)
                #for i in active_players:
                #    print(i.return_state())
            
            counter = time_counter
    return total_steps_taken

def run_oxygen_simulation(space_manager, player):
    # Solution - At every fork, we create a new player from the current player
    active_players = [player]
    active_steps_taken = [0]
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
            new_player.attempt_move_to_space(adjacent_space)

            # If the movement failed, or we move to an already reached state
            # Do not keep the player moving           
            current_state = new_player.return_state()
            if current_state not in previous_states:
                active_players.append(new_player)
                active_steps_taken.append(new_player.steps_taken)
                previous_states.add(current_state)

        active_players.pop(player_num)
        last_stepcount = active_steps_taken.pop(player_num)
        if len(active_steps_taken) > 0:
            time_counter = min(active_steps_taken)
            if counter < time_counter:
                space_manager.print_map(active_players)
                #for i in active_players:
                #    print(i.return_state())
            
            counter = time_counter
    return last_stepcount
    

def question_15_navigate_to_O():
    # Take the output of the map previously to get this map
    with open("data\\q15map.txt") as f:
        input_data = f.read()
    [player, space_manager] = parse_map(input_data)
    run_simulation(space_manager, player)


def question_15_part_2():
    with open("data\\q15map.txt") as f:
        input_data = f.read()
    [player, space_manager] = parse_map(input_data, "O")
    steps = run_oxygen_simulation(space_manager, player)
    print(f"Total steps: {steps}")



if __name__ == "__main__":
    question_15_part_2()


