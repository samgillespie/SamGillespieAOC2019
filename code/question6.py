

from execution_time import timeit

class orbit():
    def __init__(self, parent_orbit=None, name=None):
        self.parent_orbit = parent_orbit
        self.name = name


def convert_data_to_nested_classes(data):
    orbits = {}

    # Generate map
    for input_row in data:
        split_row = input_row.split(")")
        if split_row[1] not in orbits:
            child = orbit(name = split_row[1])
        else:
            child = orbits[split_row[1]]
    
        if split_row[0] not in orbits:
            parent = orbit(parent_orbit = None, name=split_row[1])
        else:
            parent = orbits[split_row[0]]
        child.parent_orbit = parent
        
        orbits[split_row[0]] = parent
        orbits[split_row[1]] = child
    return orbits


def count_orbits(orbits):
    counter = 0 
    for elem in orbits:        
        orbit_obj = orbits[elem]
        while orbit_obj.parent_orbit is not None:
            counter += 1
            orbit_obj = orbit_obj.parent_orbit
    return counter

def calculate_shortest_route(orbits, inputa, inputb):
    you = orbits[inputa]
    santa = orbits[inputb]

    you_path = []
    while you.parent_orbit is not None:
        you_path.append(you.parent_orbit)
        you = you.parent_orbit

    santa_path = []
    while santa.parent_orbit is not None:
        santa_path.append(santa.parent_orbit)
        santa = santa.parent_orbit
    
    find_overlap = set(you_path) & set(santa_path)
    solution = len(you_path) - len(find_overlap)  + len(santa_path)  - len(find_overlap)
    return solution

@timeit
def question_6():
    with open("data\\q6input.txt") as f:
        input_data = f.read()
    input_data = input_data.split("\n")
   
    orbits = convert_data_to_nested_classes(input_data)
    
    # Walk map
    

    print(f"Question 6a: {count_orbits(orbits)}")

    
    print(f'Question 6b: {calculate_shortest_route(orbits, "YOU", "SAN")}')
    

if __name__ == "__main__":
    question_6()
