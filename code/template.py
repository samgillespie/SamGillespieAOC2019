

from execution_time import timeit


@timeit
def question_x():
    with open("data\\qxinput.txt") as f:
        input_data = f.read()
    input_data = input_data.split("\n")


if __name__ == "__main__":
    question_x()
