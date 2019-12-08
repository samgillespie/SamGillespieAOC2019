
from execution_time import timeit
import itertools


class TerminateSequence(Exception):
    pass


class Computer():
    def __init__(self, sequence, inputs):
        self.sequence = sequence
        self.cursor = 0
        self.inputs = inputs
        self.input_position = 0
        self.output = None

    def set_input(self, inputs):
        self.inputs = inputs

    def process_opcode(self, mode):
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

    def get_size(self, mode):
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

    def process_instruction(self):
        sequence = self.sequence
        cursor = self.cursor
        start_cursor = cursor
        size = self.get_size(self.sequence[cursor])
        instruction = sequence[cursor:(cursor+size)]
        inputs = self.inputs
        
        [opcode, p1, p2, p3] = self.process_opcode(str(instruction[0]))
        
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

        if opcode == 1:
            value = value_1 + value_2
            sequence[instruction[3]] = value
        elif opcode == 2:
            value = value_1 * value_2
            sequence[instruction[3]] = value
        elif opcode == 3:
            if self.input_position > len(inputs)-1:
                sequence[instruction[1]] = inputs[-1]
            else:
                sequence[instruction[1]] = inputs[self.input_position]
            self.input_position += 1
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
        
        if start_cursor == cursor:
            cursor = cursor+size

        self.sequence = sequence
        self.cursor =  cursor
        
        
        return output

    def execute_until_output(self):
        while True:
            output = self.process_instruction()
            if output is not None:
                return output
        

def generate_all_possible_sequences(min, max):
    return list(itertools.permutations(range(min,max+1)))


@timeit
def question_7a():
    with open("data\\q7input.txt") as f:
        input_data = f.read()
    input_data = input_data.split(",")
    input_data = list(map(int, input_data))
    phase_settings = generate_all_possible_sequences(0, 4)
    final_signals = []

    for phase_setting in phase_settings:
        output_signal = 0
        for computer_num in range(0,5):
            input_signal = [phase_setting[computer_num], output_signal]
            computer = Computer(input_data.copy(), input_signal)
            output_signal = computer.execute_until_output()
            input_signal = output_signal
        final_signals.append(input_signal)
    
    print(f"Question 7a: {max(final_signals)}")


@timeit
def question_7b():
    with open("data\\q7input.txt") as f:
        input_data = f.read()
    input_data = input_data.split(",")
    input_data = list(map(int, input_data))

    phase_settings = generate_all_possible_sequences(5, 9)
    final_signals = []
    
    for phase_setting in phase_settings:
        halted = False
        
        computers = []
        for computer_num in range(0,5):
            computers.append(Computer(input_data.copy(), None))
        output_signal = 0
        while halted is False:
            for computer_num in range(0,5):
                input_signal = [phase_setting[computer_num], output_signal]
                computer = computers[computer_num]
                computer.set_input(input_signal)
                try:
                    output_signal = computer.execute_until_output()    
                except TerminateSequence:
                    halted = True
                    break
                if output_signal is None:
                    raise Exception

        final_signals.append(output_signal)
    print(f"Question 7b: {max(final_signals)}")


if __name__ == "__main__":
    question_7a()
    question_7b()