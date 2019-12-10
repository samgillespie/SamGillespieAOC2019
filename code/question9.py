

from execution_time import timeit
import itertools

class TerminateSequence(Exception):
    pass


class Computer():
    def __init__(self, sequence, inputs):
        self.sequence_dict = self.convert_sequence_to_dictionary(sequence)
        self.cursor = 0
        self.inputs = inputs
        self.input_position = 0
        self.output = None
        self.relative_base = 0

    def fetch_sequence_entry(self, position):
        if position < 0:
            raise Exception()
        if position in self.sequence_dict:
            return self.sequence_dict[position]
        else:
            return 0

    def convert_sequence_to_dictionary(self, sequence):
        sequence_dict = {}
        for i in enumerate(sequence):
            sequence_dict[i[0]] = i[1]
        return sequence_dict            

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
        parameter_3 = int(mode[-5])
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
            9: 2,
            99: 1
        }
        return size[opcode]

    def process_instruction(self):
        cursor = self.cursor
        start_cursor = cursor
        size = self.get_size(self.sequence_dict[cursor])
        instruction = []
        for i in range(0, size):
            instruction.append(self.fetch_sequence_entry(cursor+i))
        
        inputs = self.inputs
        [opcode, p1, p2, p3] = self.process_opcode(str(instruction[0]))
        output = None
        if opcode == 99:
            raise TerminateSequence

        if p1 == 0:
            # Position mode
            value_1 = self.fetch_sequence_entry(instruction[1])
        elif p1 == 1:
            # Immediate mode
            value_1 = instruction[1]
        elif p1 == 2:
            # Relative mode
            value_1 = self.fetch_sequence_entry(self.relative_base + instruction[1]) 

        if len(instruction) > 2:
            if p2 == 0:
                value_2 = self.fetch_sequence_entry(instruction[2])
            elif p2 == 1:
                value_2 = instruction[2]
            elif p2 == 2:
                value_2 = self.fetch_sequence_entry(self.relative_base + instruction[2]) 

        if len(instruction) > 3:
            if p3 >= 2:
                value_3 = self.relative_base + instruction[3]
            else:
                value_3 = instruction[3]


        if opcode == 1:
            value = value_1 + value_2
            self.sequence_dict[value_3] = value
        elif opcode == 2:
            value = value_1 * value_2
            self.sequence_dict[value_3] = value
        elif opcode == 3:
            if p1 == 0 or p1 == 1:
                target_position = instruction[1]
            elif p1 == 2:
                target_position = self.relative_base + instruction[1]
        
            if self.input_position > len(inputs)-1:
                self.sequence_dict[target_position] = inputs[-1]
            else:
                self.sequence_dict[target_position] = inputs[self.input_position]
            self.input_position += 1
            
        elif opcode == 4:
            output = value_1
        elif opcode == 5:
            if value_1 != 0:
                cursor = value_2
        elif opcode == 6:
            if value_1 == 0:
                cursor = value_2
        elif opcode == 7:
            if value_1 < value_2:
                self.sequence_dict[value_3] = 1
            else:
                self.sequence_dict[value_3] = 0
        elif opcode == 8:
            if value_1 == value_2:
                self.sequence_dict[value_3] = 1
            else:
                self.sequence_dict[value_3] = 0
        elif opcode == 9:
            self.relative_base += value_1
        else:
            raise Exception(f"Invalid Opcode: {opcode}")
        
        if start_cursor == cursor:
            cursor = cursor+size

        self.cursor =  cursor
        return output

    def execute_until_output(self):
        while True:
            output = self.process_instruction()
            if output is not None:
                return output

    def execute_until_terminate(self):
        outputs = []
        while True:
            try:
                output = self.process_instruction()
            except TerminateSequence:
                break
            if output is not None:
                outputs.append(output)
        return outputs
        

def generate_all_possible_sequences(min, max):
    return list(itertools.permutations(range(min,max+1)))


@timeit
def question_9():
    with open("data\\q9input.txt") as f:
        input_data = f.read()
    input_data = list(map(int, input_data.split(",")))
    computer = Computer(input_data, [2])
    print(computer.execute_until_terminate())

if __name__ == "__main__":
    question_9()
