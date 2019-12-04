

from execution_time import timeit
import re

def meets_criteria(value, check_for_2digit_group=False):    
    str_value = str(value)
    
    for i in range(1, len(str_value)):
        if int(str_value[i-1]) > int(str_value[i]):
            return False

    re_expression = r"(\d)\1+"
    has_double = False
    matches = re.finditer(re_expression, str_value)
    for match in matches:
        match_string = match.group()

        if check_for_2digit_group is False and len(match_string) >= 2:
            has_double = True
        if check_for_2digit_group is True and len(match_string) == 2:
            has_double = True

    return has_double


@timeit
def question_x():
    
    print(meets_criteria(111111) == True)
    print(meets_criteria(223450) == False)
    print(meets_criteria(122355) == True)
    print(meets_criteria(123789) == False)

    input_start = 264360
    input_stop = 746325
    inputs = range(input_start, input_stop)
    valid_inputs_a = 0
    valid_inputs_b = 0
    for i in inputs:
        if meets_criteria(i, False):
            valid_inputs_a += 1
        if meets_criteria(i, True):
            valid_inputs_b += 1
    print(f"Question 4a: {valid_inputs_a}")
    print(f"Question 4b: {valid_inputs_b}")

if __name__ == "__main__":
    question_x()
