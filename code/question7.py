
from execution_time import timeit
import itertools


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


def process_instruction(sequence, instruction, cursor, global_input, input_position):
    [opcode, p1, p2, p3] = process_opcode(str(instruction[0]))
    output = None
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
        if input_position > len(global_input):
            sequence[instruction[1]] = global_input[-1]
        else:
            sequence[instruction[1]] = global_input[input_position]
        input_position += 1
    elif opcode == 4:
        output = sequence[instruction[1]]
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
    return [sequence, cursor, input_position, output]


def generate_all_possible_sequences(min, max):
    return list(itertools.permutations(range(min,max+1)))


def process_sequence(sequence, phase_setting, input_signal):
    cursor = 0
    global_input = [phase_setting]+input_signal
    input_position = 0
    outputs = []
    while True:
        size = get_size(sequence[cursor])
        if (cursor + size) > len(sequence):
            break

        prior_cursor = cursor
        try:
            [sequence, cursor, input_position, output] = process_instruction(sequence, sequence[cursor:(cursor+size)], cursor, global_input, input_position)
            if output is not None:
                outputs.append(output)
                return [sequence, outputs, False]
        except TerminateSequence:
            return [sequence, outputs, True]

        if cursor == prior_cursor:
            cursor += size


@timeit
def question_7a():
    with open("data\\q7input.txt") as f:
        input_data = f.read()
    input_data = input_data.split(",")
    input_data = list(map(int, input_data))
    phase_settings = generate_all_possible_sequences(0, 4)
    final_signals = []
    for phase_setting in phase_settings:
        input_signal = [0]
        for computer in range(0,5):
            sequence = input_data.copy()
            [sequence, output_signal, terminated] = process_sequence(sequence, phase_setting[computer], input_signal)
            input_signal = output_signal
        final_signals.append(input_signal)
    
    print(f"Question 7a: {max(final_signals)}")


    

if __name__ == "__main__":
    question_7a()
