from question9 import Computer, TerminateSequence
from execution_time import timeit
import matplotlib.pyplot as plt
import numpy as np

class Robot():
    def __init__(self):
        self.facing = "up"
        self.position = (0, 0)

    def move(self):
        if self.facing == "up":
            self.position = (self.position[0]+1, self.position[1])
        elif self.facing == "right":
            self.position = (self.position[0], self.position[1]+1)
        elif self.facing == "down":
            self.position = (self.position[0]-1, self.position[1])
        elif self.facing == "left":
            self.position = (self.position[0], self.position[1]-1)

    def rotate(self, clockwise=True):
        if clockwise is True:
            if self.facing == "up":
                self.facing = "right"
            elif self.facing == "right":
                self.facing = "down"
            elif self.facing == "down":
                self.facing = "left"
            elif self.facing == "left":
                self.facing = "up"
        else:
            if self.facing == "up":
                self.facing = "left"
            elif self.facing == "left":
                self.facing = "down"
            elif self.facing == "down":
                self.facing = "right"
            elif self.facing == "right":
                self.facing = "up"



@timeit
def question_11a():
    with open("data\\q11input.txt") as f:
        input_data = f.read()
    intcode_program = input_data.split(",")
    intcode_program = list(map(int, intcode_program))
    robot_moving = True
    comp = Computer(intcode_program,[1])
    white_spaces = set()
    currently_white_spaces = set()
    robot = Robot()
    while robot_moving:
        
        if robot.position in currently_white_spaces:
            comp.set_input([1])
        else:
            comp.set_input([0])

        try:
            result1 = comp.execute_until_output()
            result2 = comp.execute_until_output()
        except TerminateSequence:
            robot_moving = False
            break
            
        if result1 == 1:
            white_spaces.add(robot.position)
            currently_white_spaces.add(robot.position)
        elif result1 == 0 and robot.position in currently_white_spaces:
            currently_white_spaces.remove(robot.position)

        if result2 == 0:
            robot.rotate(False)
        elif result2 == 1:
            robot.rotate(True)
        robot.move()
    print(white_spaces)
    print(f"Number of spaces painted white now {len(currently_white_spaces)}")
    print(f"Number of spaces painted white {len(white_spaces)}")


@timeit
def question_11b():
    with open("data\\q11input.txt") as f:
        input_data = f.read()
    intcode_program = input_data.split(",")
    intcode_program = list(map(int, intcode_program))
    robot_moving = True
    comp = Computer(intcode_program,[1])
    currently_white_spaces = set()
    currently_white_spaces.add((0,0))
    robot = Robot()
    while robot_moving:
        
        if robot.position in currently_white_spaces:
            comp.set_input([1])
        else:
            comp.set_input([0])

        try:
            result1 = comp.execute_until_output()
            result2 = comp.execute_until_output()
        except TerminateSequence:
            robot_moving = False
            break
            
        if result1 == 1:
            currently_white_spaces.add(robot.position)
        elif result1 == 0 and robot.position in currently_white_spaces:
            currently_white_spaces.remove(robot.position)

        if result2 == 0:
            robot.rotate(False)
        elif result2 == 1:
            robot.rotate(True)
        robot.move()
    x = [i[0] for i in currently_white_spaces]
    y = [i[1] for i in currently_white_spaces]
    print(f"Number of spaces painted white now {len(currently_white_spaces)}")
    ybins = max(y) - min(y) + 1
    xbins = max(x) - min(x) + 1
    heatmap, xedges, yedges = np.histogram2d(y, x, bins=(ybins, xbins))
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    plt.clf()
    plt.imshow(heatmap.T, extent=extent, origin='lower')
    plt.show()


if __name__ == "__main__":    
    question_11b()
