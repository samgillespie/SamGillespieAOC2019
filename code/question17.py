from question9 import Computer, TerminateSequence
import copy


class Scaffolding():
    def __init__(self, input_list):
        self.path = []
        self.spaces_touched = set()
        self.prev_direction = ""
        self.input_map = input_list
        self.ymax = len(self.input_map)
        self.xmax = len(self.input_map[0])
        self.cursor = self.find_start()
        self.direction = "R"
    
    def direction_to_walk(self):
        if self.direction == "R":
            return (1, 0)
        elif self.direction == "L":
            return (-1, 0)
        elif self.direction == "U":
            return (0, -1)
        elif self.direction == "D":
            return (0, 1)

    def check_right(self):
        if self.direction == "R":
            return (0, 1)
        elif self.direction == "L":
            return (0, -1)
        elif self.direction == "U":
            return (1, 0)
        elif self.direction == "D":
            return (-1, 0)

    def check_left(self):
        if self.direction == "R":
            return (0, -1)
        elif self.direction == "L":
            return (0, 1)
        elif self.direction == "U":
            return (-1, 0)
        elif self.direction == "D":
            return (1, 0)
        
    def apply_rotation(self, left_or_right):
        print(f"Weird case {self.direction}, {left_or_right}")
        if self.direction == "R" and left_or_right == "L":
            self.direction = "U"
        elif self.direction == "R" and left_or_right == "R":
            self.direction = "D"
        elif self.direction == "L" and left_or_right=="R":
            self.direction = "U"
        elif self.direction == "L" and left_or_right=="L":
            self.direction = "D"
        elif self.direction == "U" and left_or_right == "L":
            self.direction = "L"
        elif self.direction == "U" and left_or_right == "R":
            self.direction = "R"
        elif self.direction == "D" and left_or_right == "L":
            self.direction = "R"
        elif self.direction == "D" and left_or_right == "R":
            self.direction = "L"
        else:
            raise Exception(f"Weird case {self.direction}, {left_or_right}")

        
    def find_start(self):
        for y in range(self.ymax):
            for x in range(self.xmax):
                if self.input_map[y][x] == "^":
                    return (x, y)
        raise Exception("Start not found")

    def calculate_path(self):
        steps = 0
        path = []
        (x, y) = self.cursor
        while True:
            print("Walking down")
            walk_dir = self.direction_to_walk()
            (x,y) = (x + walk_dir[0], y + walk_dir[1])
            stop = False
            if y >= self.ymax - 1:
                stop = True
            elif x >= self.xmax:
                stop = True
            elif x < 0:
                stop = True
            elif y < 0:
                stop = True
            
            if stop is False and self.input_map[y][x] == "#":
                steps += 1
                self.print_map((x,y))
            else:
                print("walk complete")
                self.cursor = (x - walk_dir[0], y - walk_dir[1])
                (x, y) = self.cursor
                path.append(steps)
                steps = 0
                rotate = self.calculate_rotation(self.cursor)
                print(rotate)
                if rotate is not None:
                    path.append(rotate)
                else:
                    return path
    
    def calculate_rotation(self, cursor):
        left = self.check_left()
        right = self.check_right()
        
        yleft = cursor[1] + left[1]
        xleft = cursor[0] + left[0]

        yright = cursor[1] + right[1]
        xright = cursor[0] + right[0]
        if yleft <= self.ymax - 2 and yleft >= 0 and xleft <= self.xmax - 1 and xleft >= 0:
            if self.input_map[yleft][xleft] == "#":
                self.apply_rotation("L")
                return "L"
        if yright <= self.ymax - 2 and yright >= 0 and xright <= self.xmax - 1 and xright >= 0:
            if self.input_map[yright][xright] == "#":
                self.apply_rotation("R")
                return "R"
        else:
            return
        
    def print_map(self, cursor):
        import os
        os.system("cls")
        if self.direction == "R":
            icon = ">"
        elif self.direction == "L":
            icon = "<"
        elif self.direction == "U":
            icon = "^"
        elif self.direction == "D":
            icon = "v"

        imap = copy.deepcopy(self.input_map)
        imap[cursor[1]][cursor[0]] = icon
        print("\n".join(["".join(i) for i in imap]))
        



        


def calculate_intersections(input_list):
    row_count = len(input_list)
    col_count = len(input_list[0])
    intersections = []
    for y in range(1, row_count-2):
        for x in range(1, col_count-2):
            
            up = input_list[y-1][x]  == "#"
            down = input_list[y+1][x]  == "#"
            left = input_list[y][x-1]  == "#"
            right = input_list[y][x+1]  == "#"
            this = input_list[y][x]  == "#"
            if (up and down and left and right and this):
                print((x,y))
                input_list[y][x] = "O"
                intersections.append((x,y))

    alignment_parameter = find_intersections(intersections)
    input_list.pop()
    return alignment_parameter


def find_intersections(intersections):        
    alignment_parameter = 0
    for intersect in intersections:
        alignment_parameter += intersect[0] * intersect[1]
    return alignment_parameter





def question_17():
    with open("data\\q17input.txt") as f:
        input_data = f.read()
    intcode_program = input_data.split(",")
    intcode_program = list(map(int, intcode_program))
    computer = Computer(intcode_program,[])
    output = computer.execute_until_terminate()

    mapped = []
    for i in output:
        mapped.append(chr(i))
    
    mapped_data = []
    while True:
        try:
            ind = mapped.index("\n")
        except ValueError:
            break
        mapped_data.append(mapped[0:ind])
        mapped = mapped[ind+1:]

    #print(f"Question 17a: {calculate_intersections(mapped_data)}")
    scaffold = Scaffolding(mapped_data)
    path = scaffold.calculate_path()
    print(path)
if __name__ == "__main__":
    question_17()
# Ugh, don't have to consider all the paths through the scaffold