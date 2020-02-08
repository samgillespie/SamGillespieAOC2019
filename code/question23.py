
from execution_time import timeit
from intcode import Computer, TerminateSequence
import itertools

COMPUTER_NUM = 50

class Computers():
    def __init__(self, computers = []):
        self.computers = computers
        self.queues = []
        self.idle = set()
    
    def add_computer(self, computer):
        self.computers.append(computer)

    def set_instruction(self, index, x, y):
        if index == 255:
            print(f"Question 23a Answer: {y}")
            raise Exception("We're done here")
        self.queues[index].append([x, y])
        if index in self.idle:
            self.idle.remove(index)


def execute_computer(computers, index):
    computer = computers.computers[index]
    outp = computer.execute_until_output_multiple_values(3)
    if outp[0] == "Awaiting Input":
        computers.idle.add(index)
        return
    return outp



def run_computers(computers):
    while True:
        for index in range(COMPUTER_NUM):
            if index in computers.idle:
                continue
            print(f"Running computer {index}")
            computer = computers.computers[index]
            queue = computers.queues[index]
            print(computer.cursor)
            
            if len(queue) == 0:
                queue = [[-1]]
            
            while len(queue) > 0:
                value = queue.pop(0)
                queue = computers.queues[index]
                computer.set_input(value)
                
                results = execute_computer(computers, index)
                if results is not None:
                    print(f"Received instruction {[results[0], results[1], results[2]]}")
                    computers.set_instruction(results[0], results[1], results[2])

@timeit
def question_23():
    with open("data\\q23input.txt") as f:
        input_data = f.read()
    intcode_program = input_data.split(",")
    intcode_program = list(map(int, intcode_program))
    
    test_intcode = [3,60,1005,60,18,1101,0,1,61,4,61,104,1011,104,1,1105,1,22,1101,0,0,61,3,62,1007,62,0,64,1005,64,22,3,63,1002,63,2,63,1007,63,256,65,1005,65,48,1101,0,255,61,4,61,4,62,4,63,1105,1,22,99]
    intcode_program = test_intcode

    computers = Computers([])
    for i in range(0,COMPUTER_NUM):
        print(f"Adding computer {i}")
        computer = Computer(intcode_program, [i])
        computer.execute_until_input()
        computers.add_computer(computer)
        computers.queues.append([])
    run_computers(computers)    
    

    



if __name__ == "__main__":
    question_23()
