
import copy
import os
import time
import itertools


player_spawners = ["+", "-", "*", "/"]

class Player():
    def __init__(self):
        self.previous_nodes = []
        self.current_nodes = []
        self.path = []
        self.inventory = list()
        self.target_keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.steps_taken = 0
        self.robots_count = 0
        
    def give_key_target(self, list_of_keys_needed):
        self.target_keys = list_of_keys_needed

    def add_robot(self, node):
        self.previous_nodes.append(node)
        self.current_nodes.append(node)
        self.path.append([node.name])
        self.robots_count += 1
    
    def available_robot_movements(self, previous_states, target_order=[]): 
        """
        returns [(node, distance)]
        """
        available_movements = []
        valid_movements = 0
        for robot_num in range(self.robots_count):
            robot_node = self.current_nodes[robot_num] 
            available_movement = []
            options = robot_node.node_paths
            
            for option in options:

                # If we are just heading to a previous state that can be reached with fewer steps, bail out
                move_state = self.return_predicted_state(robot_num, option.destination_node.name)
                movement_cost = self.steps_taken + option.distance 
                if move_state in previous_states and previous_states[move_state] <= movement_cost:
                    #print("HERE WE ARE")
                    continue
                
                if target_order != []:
                    target_node = target_order[len(self.inventory)+1]
                    print(f"trying to move to {target_node}")
                    if option.destination_node.name != target_node:
                        continue

                if self.is_valid_movement(option):
                    available_movement.append(option)
                    valid_movements += 1
            
            available_movements.append(available_movement)
        if valid_movements == 0:
            return None

        return available_movements
            
    def return_state(self):
        return (tuple([(i.name) for i in self.current_nodes]), tuple(sorted(self.inventory)))

    def return_predicted_state(self, robot_num, new_position):
        nodes = [(i.name) for i in self.current_nodes]
        nodes[robot_num] = new_position
        return (tuple(nodes), tuple(sorted(self.inventory)))

    def print_robot_info(self):
        for robot_num in range(self.robots_count):
            print(f"ROBOT NUMBER {robot_num}")
            print(f"current_space {self.current_nodes[robot_num]}")
            print(f"previous_space {self.previous_nodes[robot_num]}")
            print(f"PATH {self.path[robot_num]}")
        print(f"Group Inventory {self.inventory}")
        print(f"Available Movements {self.available_robot_movements()}")


    def is_valid_movement(self, node_path):
        return node_path.can_traverse(self.inventory)
        
    def move_to_node(self, robot_num, node_path, node_manager):
        target_node_name = node_path.destination_node.name
        node = copy.copy(node_manager.nodes[target_node_name])
        self.steps_taken += node_path.distance

        #print(f"Moving from {self.current_nodes[robot_num].name} to {node.name}")
        
        self.previous_nodes[robot_num] = self.current_nodes[robot_num]
        self.current_nodes[robot_num] = node
        self.path[robot_num].append(node.name)
        # pick up key
        if node.name.islower() and node.name not in self.inventory:
            # If we pick up a thing, we need to split the players
            self.last_robot_moved = -1
            self.inventory.append(node.name)
            # Check for win state
            if set(self.inventory) == set(self.target_keys):
                print((self.inventory, self.steps_taken))            
                return self.steps_taken
        return True


class Node():
    def __init__(self, space, content):
        self.name = content
        self.space = space
        self.reachable_nodes = []
        self.node_paths = []

    def add_reachable_node(self, node, distance):
        self.reachable_nodes.append((node, distance))

    def add_node_path(self, node_destination, distance, gates):
        self.node_paths.append(NodePath(self, node_destination, distance, gates))


class NodePath():
    def __init__(self, node1, node2, distance, gates):
        self.origin_node = node1
        self.destination_node = node2
        self.gates = gates
        self.distance = distance
        print(f"Created Node Path from {self.origin_node.name} to {self.destination_node.name} through gates {self.gates}")
    
    def can_traverse(self, inventory):
        for gate in self.gates:
            if gate.lower() not in inventory:
                return False
        return True


class NodeManager():
    def __init__(self):
        self.nodes = {}

    def create_node(self, space):
        new_node = Node(space, space.content)
        self.nodes[space.content] = new_node
    
    def calculate_node_adjacency(self, node, space_manager):
        space = node.space
        new_node = Node(space, space.content)
        self.nodes[space.content] = new_node
        
        # tuple of (space, distance, gates)
        walker_list = [(i, 1, []) for i in space.adjacent_spaces]
        spaces_traversed = {}
        while len(walker_list) > 0:
            adjacent_space = walker_list[0]
            x = adjacent_space[0].x
            y = adjacent_space[0].y
            distance = adjacent_space[1]+1
            gates = adjacent_space[2].copy()
            
            if (x, y) in spaces_traversed:
                prev_distance = spaces_traversed[(x,y)]
                if distance >= prev_distance:
                    walker_list.pop(0)
                    continue

            spaces_traversed[(x, y)] = distance
            target_content = adjacent_space[0].content

            # Is this a key, or a door
            space_type = None
            if target_content is not None:
                if target_content in self.nodes and target_content != space.content:
                    space_type = "Key"
                    target_node = self.nodes[target_content]
                    new_node.add_node_path(target_node, adjacent_space[1], gates)
                elif target_content.isupper() and target_content != space.content:
                    space_type = "Gate"
                    gates.append(target_content)
            
            if space_type is None or space_type == "Gate":
                new_distance = distance + 1
                new_candidates = []
                for i in adjacent_space[0].adjacent_spaces:
                    if (i.x, i.y) in spaces_traversed and spaces_traversed[(i.x, i.y)] >= new_distance:
                        continue
                    new_candidates.append(i)

                new_elems = [(i, distance, gates) for i in new_candidates]
                walker_list += new_elems
            walker_list.pop(0)
        
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
                for current_space in player.current_space:
                    game_map[current_space.x][current_space.y] = "@"

        game_rows = []
        for row in game_map:
            game_rows.append("".join(row))
        print("\n".join(game_rows))
    
    def convert_to_node_space(self):
        node_manager = NodeManager()
        for i in self.spaces:
            if i.content is not None and (i.content.islower() or i.content in player_spawners):
                node_manager.create_node(i)
        
        for node_name in node_manager.nodes:
            node = node_manager.nodes[node_name]
            node_manager.calculate_node_adjacency(node, self)
        return node_manager


def parse_map(input_map):
    """
    Returns all the spaces
    """
    inputs = input_map.split("\n")
    spawner_index = 0
    space_manager = SpaceManager()
    for input_row in enumerate(inputs):
        row_data = input_row[1]
        row_number = input_row[0]
        for column_num in range(0, len(row_data)):
            content = row_data[column_num]
            if content == "#":
                continue

            if content == "@":
                content = player_spawners[spawner_index]
                spawner_index += 1

            new_space = Space(row_number, column_num, content)
            space_manager.add_space(new_space)
    return space_manager


def get_new_player_instance(player):
    new_player = copy.copy(player)
    new_player.inventory = player.inventory.copy()
    new_player.current_nodes = player.current_nodes.copy()
    new_player.previous_nodes = player.previous_nodes.copy()
    new_player.path = copy.deepcopy(player.path)
    return new_player


def is_duplicate(current_state, previous_states, step_count):
    if current_state in previous_states:
        saved_steps = previous_states[current_state]
        if step_count < saved_steps:
            return "valid"
        else:
            #print("invalid")
            return "invalid"
    return "valid"


def run_simulation(node_manager, player):
    # Node space. Consider each step all the options available.
    # Execute each step as a new instance
    players = [player]
    players_steps = [0]

    min_steps = 99999999
    previous_states = {}
    print("Beginning Simulation")
    best_player = None
    key_order = []
    counter = 0
    keys_collected = set()
    while len(players) > 0 and min(players_steps) < min_steps:
        player_num = players_steps.index(min(players_steps))
        active_player = players[player_num]
        options = active_player.available_robot_movements(previous_states)
        
        # Check to see if this is still vallid
        move_player = True
        active_player_state = active_player.return_state()
        if active_player_state in previous_states:
            if previous_states[active_player_state] < active_player.steps_taken:
                # print("Found a better way to get here")
                move_player = False

        if options is None:
            move_player = False

        if move_player is True:    
            # Run all situations
            for robot_num in range(active_player.robots_count):
                for option in options[robot_num]:
                    new_player = get_new_player_instance(active_player)
                    attempt = new_player.move_to_node(robot_num, option, node_manager)
                    if attempt is True:
                        current_state = new_player.return_state()
                        is_dup = is_duplicate(current_state, previous_states, new_player.steps_taken)
                        if is_dup == "valid":
                            previous_states[current_state] = new_player.steps_taken
                            players.append(new_player)
                            players_steps.append(new_player.steps_taken)
                    elif attempt != False and attempt < min_steps:
                        min_steps = attempt
                        key_order = new_player.inventory
                        best_player = new_player
                        print(f"Min steps found: {min_steps}")
                
        players.pop(player_num)
        players_steps.pop(player_num)
        if len(players_steps) > 0:
            time_counter = min(players_steps)
            if counter < time_counter:
                print(min(players_steps), len(players), len(previous_states))
                counter = time_counter
                if counter > 1500:
                    for player in players:
                        for item in player.inventory:
                            keys_collected.add(item)
        
        # for player in players:
            #print(player.inventory)
            #print(player.target_keys)


    return [key_order, min_steps, best_player]


def instantiate_player(node_manager):
    player = Player()
    for spawner in player_spawners:
        if spawner in node_manager.nodes:
            node = node_manager.nodes[spawner]
            player.add_robot(node)
    return player
        

def run_simulation_in_order(node_manager, player, key_order):
    step = 0
    for step in range(len(key_order)):
        player.give_key_target(key_order[0:step+1])
        [_, _, player] = run_simulation(node_manager, player)
        print(player.inventory)
        print(player.steps_taken)
    return [player.inventory, player.steps_taken]


if __name__ == "__main__":
    input_map = """#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba@#@BcIJ#
#############
#nK.L@#@G...#
#M###N#H###.#
#o#m..#i#jk.#
#############"""


    # with open("data\\q18input.txt") as f:
    #     input_map = f.read()
    # space_manager = parse_map(input_map)
    # cells_pruned = 1
    # while cells_pruned > 0:
    #     cells_pruned = space_manager.prune_dead_paths()
    # space_manager.print_map()
    # node_manager = space_manager.convert_to_node_space()
    # player = instantiate_player(node_manager)
    # player.give_key_target(space_manager.fetch_target_key_list())
    
    # # Use the order from the default map
    # [key_order, min_steps, _] = run_simulation(node_manager, player)
    


    with open("data\\q18binput.txt") as f:
        input_map = f.read()
    space_manager = parse_map(input_map)
    cells_pruned = 1
    while cells_pruned > 0:
        cells_pruned = space_manager.prune_dead_paths()
    space_manager.print_map()
    node_manager = space_manager.convert_to_node_space()
    player = instantiate_player(node_manager)
    player.give_key_target(space_manager.fetch_target_key_list())
    

    key_order = ['f', 's', 'w', 'a', 'm', 'd', 'z', 'r', 'e', 'c', 'k', 'o', 'p', 'j', 'q', 'b', 'l', 'y', 't', 'n', 'g', 'v', 'h', 'i', 'x', 'u']
    # Use the order from the default map
    [key_order, steps_taken] = run_simulation_in_order(node_manager, player, key_order)
    
    print(f"Shortest path {steps_taken}")
    
    