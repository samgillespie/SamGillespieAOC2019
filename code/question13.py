
from execution_time import timeit
from question9 import Computer, TerminateSequence
import os

clear = lambda: os.system('cls')


class Game():
    def __init__(self):
        self.walls = set()
        self.blocks = set()
        self.paddle = ()
        self.ball = ()
    
    def add_block(self, x, y, block_type):
        if block_type == "wall" or block_type == 1:
            self.walls.add((x,y))
        elif block_type == "blocks" or block_type == 2:
            self.blocks.add((x,y))
        elif block_type == "paddle" or block_type == 3:
            self.paddle = (x,y)
        elif block_type == "ball" or block_type == 4:
            self.ball = (x,y)
            # If the ball is being moved, we return the direction we need to head
            if self.paddle != ():
                if self.paddle[0] > x:
                    return -1
                elif self.paddle[0] < x:
                    return 1
                else:
                    return 0

        elif block_type == "empty" or block_type == 0:
            pass
        else:
            raise Exception("invalid Type "+ block_type)
    
    def get_extents(self):
        wall_x = [i[0] for i in self.walls]
        wall_y= [i[1] for i in self.walls]
        block_x = [i[0] for i in self.blocks]
        block_y= [i[1] for i in self.blocks]
        x_min = min(min(wall_x), min(block_x))
        y_min = min(min(wall_y), min(block_y))
        x_max = max(max(wall_x), max(block_x))
        y_max = max(max(wall_y), max(block_y))
        return [x_min, x_max, y_min, y_max]

    def print(self):
        try:
            [x_min, x_max, y_min, y_max] = self.get_extents()

            rows = [" "]*(x_max - x_min + 1)
            game_scene = []
            for row in range(y_max - y_min + 1):
                game_scene.append(rows.copy())

            for (x, y) in self.walls:
                game_scene[y+y_min][x+x_min] = "#"
            for (x, y) in self.blocks:
                game_scene[y+y_min][x+x_min] = "▓"
            
            
            game_scene[self.paddle[1]+y_min][self.paddle[0]+x_min] = "-"
            game_scene[self.ball[1]+y_min][self.ball[0]+x_min] = "○"

        except:
            return
        
        game_rows = []
        for row in game_scene:
            game_rows.append("".join(row))
        print("\n".join(game_rows))




@timeit
def question_13():
    with open("data\\q13input.txt") as f:
        input_data = f.read()
    intcode_program = input_data.split(",")
    intcode_program = list(map(int, intcode_program))

    # Create initial state
    intcode_program[0] = 2
    computer = Computer(intcode_program, [2])
    game = Game()

    game_executing = True
    score = -9999
    try:
        while game_executing:
            x = computer.execute_until_output()
            y = computer.execute_until_output()
            block_type = computer.execute_until_output()
            if x == -1:
                score = block_type
                # When we get score, reset the game instance and print
            else:
                ball_pos = game.add_block(x, y, block_type)
                if ball_pos is not None:
                    computer.set_input([ball_pos])
                    game.print()
                    clear()
    except TerminateSequence:
        pass    

    print(score)


if __name__ == "__main__":
    question_13()


