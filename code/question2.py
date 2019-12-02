
from execution_time import timeit


class TerminateSequence(Exception):
    pass

def process_instruction(sequence, instruction):
    if instruction[0] == 1:
        value = sequence[instruction[1]] + sequence[instruction[2]]
    elif instruction[0] == 2:
        value = sequence[instruction[1]] * sequence[instruction[2]]
    elif instruction[0] == 99:
        # If we terminate, throw this exception.  We can always catch up up the stack
        raise TerminateSequence
    else:
        raise Exception(f"Invalid Opcode: {instruction[0]}")
        
    sequence[instruction[3]] = value
    return sequence
    

def process_entire_sequence(sequence):
    length = int(len(sequence)/4)
    for i in range(0, length):
        start = i*4
        end = start+4
        instruction = sequence[start:end]
        try:
            sequence = process_instruction(sequence, instruction)
        except TerminateSequence:
            return sequence
    return sequence


def try_different_nouns_and_verbs(sequence, target_value):
    # Brute force approach
    for noun in range(0,99):
        for verb in range(0,99):
            test_sequence = sequence.copy()
            test_sequence[1] = noun
            test_sequence[2] = verb
            res = process_entire_sequence(test_sequence)
            if res[0] == target_value:
                return noun*100 + verb


@timeit
def question_2():
    with open("data\\q2input.txt") as f:
        input_data = f.read()
    input_data = list(map(int, input_data.split(",")))
    test_data = input_data.copy()
    test_data[1] = 12
    test_data[2] = 2
    new_sequence = process_entire_sequence(test_data.copy())
    print(f"Question 2a: {new_sequence[0]}")
    result = try_different_nouns_and_verbs(input_data.copy(), 19690720)
    print(f"Question 2b: {result}")


if __name__ == "__main__":
    question_2()
