

from execution_time import timeit
import pandas as pd


def create_matrix_operator(length):
    df = []
    for i in range(1,length+1):
        seq = sequence([0,1,0,-1], i)
        row = []
        for j in range(length):
            row.append(seq.send(None))
        df.append(row)
    return pd.DataFrame(df)


def extract_ones_position(integer):
    return abs(integer) % 10

def sequence(sequence_pattern, repeat_number):
    pattern_index = 0
    number_occurred = 1
    while True:
        if number_occurred >= repeat_number:
            pattern_index += 1
            number_occurred = 0        
            if pattern_index >= len(sequence_pattern):
                pattern_index = 0

        yield sequence_pattern[pattern_index]
        number_occurred += 1
        


def execute_phase(input_data, sequence_pattern):
    output = []
    for element_num in range(1, len(input_data)+1):
        generator = sequence(sequence_pattern, element_num)
        summation = 0
        for value in input_data:
            sequence_value = generator.send(None) * value
            summation += sequence_value
        output.append(extract_ones_position(summation))
    return output



def assemble_list_as_value(int_list):
    return "".join(map(str, int_list))


def calculate_offset(input_data, digits_to_skip):
    datalen = len(input_data)
    offset = digits_to_skip % datalen
    return input_data[offset:offset+8]


@timeit
def question_16a():
    with open("data\\q16input.txt") as f:
        input_data = f.read()
    

    input_data = "80871224585914546619083218645595"*10000
    input_data = list(map(int,list(input_data)))
    for i in range(0,100):
        print(i)
        input_data = execute_phase(input_data, [0,1,0,-1])
    print(assemble_list_as_value(input_data))

def question_16b():
    part_a_solution = "74608727092984117225488554779405012467436674564530073186253167855468009757406537939221716262764368124618687995931374115095325199580367437035793220898926419915005566828106364680417980752456693860303897506049113167085482332669866829805204830914751373128588737340088207520689634322276348986337314549631149122132256732352522087321233719828004869381958744548803900795953925855541413762750741129784619961087510635770430535329025019197154087230962893268649040873816286289787688438417745109573274967302546629701216129800804867837892404522245753913373117642249766266335489785134101349009071832229956086501209240163910201161195041969130533091665702047971622614"
    with open("data\\q16input.txt") as f:
        input_data = f.read()
    
    # part  
    input_data = list(map(int,list(input_data)))
    print(calculate_offset(input_data, 7460872))
    



if __name__ == "__main__":
    question_16a()

    # TOO low - 02200171
    # TOO low - 41769408