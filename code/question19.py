from question9 import Computer, TerminateSequence
import math

def question_19a():
    with open("data\\q19input.txt") as f:
        input_data = f.read()
    intcode_program = input_data.split(",")
    intcode_program = list(map(int, intcode_program))

    row = ["."]*50
    mapping = []
    for _ in range(50):
        mapping.append(row.copy())
    
    tractors = 0
    for x in range(0,50):
        for y in range(0,50):
            computer = Computer(intcode_program,[])
            computer.set_input([x,y])
            output = computer.execute_until_output()
            if output == 1:
                mapping[y][x] = "#"
                tractors += 1

    print("\n".join(["".join(i) for i in mapping]))
    print(tractors)


def draw_area(x_start, y_start, theta1, theta2):
    offset = 0
    with open("data\\q19input.txt") as f:
        input_data = f.read()
    intcode_program = input_data.split(",")
    intcode_program = list(map(int, intcode_program))

    row = ["."]*(100 + 2 * offset)
    mapping = []
    for _ in range(100 + 2 * offset):
        mapping.append(row.copy())
    
    tractors = 0
    for x in range(-offset,100 + offset):
        for y in range(-offset,100 + offset):
            x_val = x + x_start
            y_val = y + y_start

            theta_from_start = math.atan(y_val/ x_val)
            #print(theta_from_start)
            if theta_from_start > theta1 and theta_from_start< theta2:
                mapping[y+offset][x+offset] = "X"
                tractors += 1
                
            #computer = Computer(intcode_program,[])
            #computer.set_input([x_val, y_val])
            #output = computer.execute_until_output()
            #if output == 1:
            #    if mapping[y+offset][x+offset] != "X":
            #        mapping[y + offset][x + offset] = "O"
            #    else:
            #        mapping[y + offset][x + offset] = "#"
    if tractors == 10000:
        print(f"Starting at {x_start-offset}:{y_start-offset} - Solution {x_start*10000+y_start}")
        #print("\n".join(["".join(i) for i in mapping]))
        return x_start*10000+y_start
    return None

def calculate_thetas(x, current_estimate, intcode_program):
    # Calculate the two thetas
    tractor_ranges = []

    # Add buffer for rounding
    y_start = int(x * math.tan(current_estimate[0])) - 10
    y_end = int(x * math.tan(current_estimate[1])) + 10
    for y in range(y_start,y_end):
        computer = Computer(intcode_program,[])
        computer.set_input([x,y])
        output = computer.execute_until_output()
        if output == 1:
            tractor_ranges.append(y)
    (min_y, max_y) = (min(tractor_ranges), max(tractor_ranges))

    # In Radians
    theta1 = math.atan(min_y / x)
    theta2 = math.atan(max_y / x)
    new_estimate = (theta1, theta2)
    print(x)
    print((y_start,y_end))
    print((theta1, theta2))
    
    if x > 10000:
        return new_estimate

    new_estimate = calculate_thetas(x*5, new_estimate, intcode_program)
    return new_estimate
    

def question_19b():
    with open("data\\q19input.txt") as f:
        input_data = f.read()
    intcode_program = input_data.split(",")
    intcode_program = list(map(int, intcode_program))
    (theta1, theta2) = calculate_thetas(100, [0, math.pi/4], intcode_program)

    x = abs(int(math.sqrt(20000)/(math.tan(theta1) - math.tan(theta2))))
    y = int(x * math.tan(theta1))
    draw_area(x, y, theta1, theta2)

    # Should be mathematically possible, but rounding crap, let's just iterate
    while True:
        theta_top_right =  math.atan(y / (x + 100))
        theta_bottom_left = math.atan((y+100) / x)
        print(x,y)
        print(theta_top_right)
        print(theta1)
        print(theta_bottom_left)
        print(theta2)
        if theta_top_right < theta1:
            y += 1
        if theta_bottom_left > theta2:
            x += 1
        if theta_top_right >= theta1 and theta_bottom_left <= theta2:
            print(f"Done: {x, y}")
            break
    
    values = set()
    for x_offset in range(-50,0):
        for y_offset in range(-50,0):
            values.add(draw_area(x+x_offset, y+y_offset, theta1, theta2))
    values.remove(None)
    print(min(list(values)))

    

if __name__ == "__main__":
    question_19b()
    # Too low  1527783
    # Too high 15270783
    # Too high 15300784
