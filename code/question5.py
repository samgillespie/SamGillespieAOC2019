
from execution_time import timeit

class TerminateSequence(Exception):
    pass


def process_opcode(mode):
    mode = str(mode)
    opcode = int(mode[-2:])
    if len(mode) <= 2:
        parameter_1 = 0
        parameter_2 = 0
        parameter_3 = 0
        return [opcode, parameter_1, parameter_2, parameter_3]
        
    parameter_1 = int(mode[-3])
    if len(mode) == 3:
        parameter_2 = 0
        parameter_3 = 0
        return [opcode, parameter_1, parameter_2, parameter_3]
    
    parameter_2 = int(mode[-4])
    if len(mode) == 4:
        parameter_3 = 0
        return [opcode, parameter_1, parameter_2, parameter_3]
    parameter_3 = mode[-5]
    return [opcode, parameter_1, parameter_2, parameter_3]

def get_size(mode):
    mode = str(mode)
    opcode = int(mode[-2:])
    size = {
        1: 4,
        2: 4,
        3: 2,
        4: 2,
        5: 3,
        6: 3,
        7: 4,
        8: 4,
        99: 1
    }
    return size[opcode]


def process_instruction(sequence, instruction, cursor, global_input):
    [opcode, p1, p2, p3] = process_opcode(str(instruction[0]))

    if opcode == 99:
        raise TerminateSequence

    if p1 == 0:
        value_1 = sequence[instruction[1]]
    elif p1 == 1:
        value_1 = instruction[1]

    if len(instruction) > 2:
        if p2 == 0:
            value_2 = sequence[instruction[2]]
        elif p2 == 1:
            value_2 = instruction[2]

    if len(instruction) > 3:
        if p3 == 0:
            value_3 = sequence[instruction[3]]
        elif p3 == 1:
            value_3 = instruction[3]

    if opcode == 1:
        value = value_1 + value_2
        sequence[instruction[3]] = value
    elif opcode == 2:
        value = value_1 * value_2
        sequence[instruction[3]] = value
    elif opcode == 3:
        sequence[instruction[1]] = global_input
    elif opcode == 4:
        print(f"Opcode 4 - Print: {sequence[instruction[1]]}")
    elif opcode == 5:
        if value_1 != 0:
            cursor = value_2
    elif opcode == 6:
        if value_1 == 0:
            cursor = value_2
    elif opcode == 7:
        if value_1 < value_2:
            sequence[instruction[3]] = 1
        else:
            sequence[instruction[3]] = 0
    elif opcode == 8:
        if value_1 == value_2:
            sequence[instruction[3]] = 1
        else:
            sequence[instruction[3]] = 0
    else:
        raise Exception(f"Invalid Opcode: {opcode}")    
    return [sequence, cursor]




@timeit
def question_5a():
    global_input = 1
    with open("data\\q5input.txt") as f:
        input_data = f.read()
    input_data = list(map(int, input_data.split(",")))
    test_data = input_data.copy()
    cursor = 0
    while True:
        size = get_size(test_data[cursor])
        if (cursor + size) > len(test_data):
            break

        prior_cursor = cursor
        try:
            [test_data, cursor] = process_instruction(test_data, test_data[cursor:(cursor+size)], cursor, global_input)
        except TerminateSequence:
            return

        if cursor == prior_cursor:
            cursor += size

@timeit
def question_5b():
    global_input = 5
    with open("data\\q5input.txt") as f:
        input_data = f.read()
    input_data = list(map(int, input_data.split(",")))
    test_data = input_data.copy()
    cursor = 0
    while True:
        size = get_size(test_data[cursor])
        if (cursor + size) > len(test_data):
            break

        prior_cursor = cursor
        try:
            [test_data, cursor] = process_instruction(test_data, test_data[cursor:(cursor+size)], cursor, global_input)            
        except TerminateSequence:
            return

        if cursor == prior_cursor:
            cursor += size


if __name__ == "__main__":
    question_5a()
    question_5b()