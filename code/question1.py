
from .execution_time import timeit


def calculate_fuel(list_of_modules):
    total_fuel = 0
    for module in list_of_modules:
        try:
            int(module)
        except:
            continue
        total_fuel += int(int(module)/3)-2
    return total_fuel

def calculate_fuel_with_recursion(list_of_modules):
    total_fuel = 0
    for module in list_of_modules:
        try:
            int(module)
        except:
            continue
        fuel = int(int(module)/3)-2
        if fuel > 0:
            new_fuel = calculate_fuel_with_recursion([fuel])
            fuel += new_fuel
            total_fuel += fuel

    return total_fuel


@timeit
def question_1():
    with open("data\\q1input.txt") as f:
        input_data = f.read()
    input_data = input_data.split("\n")

    print(f"Question 1 Answer: {calculate_fuel(input_data)}")
    print(f"Question 2 Answer: {calculate_fuel_with_recursion(input_data)}")


if __name__ == "__main__":
    question_1()
