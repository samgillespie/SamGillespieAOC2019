

from execution_time import timeit


def do_parta_check(slices):
    slice_zeros = []
    min_zeros  = 999
    pos = -1
    for i in enumerate(slices):
        zeros = i[1].count("0")
        slice_zeros.append(zeros)
        if zeros < min_zeros:
            min_zeros = zeros
            pos = i[0]
    solution = slices[pos].count("1")* slices[pos].count("2")
    return solution
    
def resolve_slices(slices, width, height):
    # Use 3 for unresolves
    size = height*width
    solution_slice = ["3"] * width * height
    for image_slice in slices:
        for i in range(0, size):
            if solution_slice[i] != "3":
                continue
            
            if image_slice[i] != "2":
                solution_slice[i] = image_slice[i]
    
    for i in range(height):
        print(solution_slice[i*width:(i+1)*width])



@timeit
def question_8():
    with open("data\\q8input.txt") as f:
        input_data = f.read()
    input_data = list(input_data)

    width = 25
    height = 6
    size = width*height
    layers = len(input_data)/ (width*height)
    slices = []
    for i in range(int(layers)):
        slices.append(input_data[i*size:(i+1)*size])
    
    print(f"Question 8a solution: {do_parta_check}")
    resolve_slices(slices, width, height)

    


if __name__ == "__main__":
    question_8()
