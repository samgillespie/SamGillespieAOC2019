

from execution_time import timeit

###
# For an entire list
###
def deal_into_new_stack(deck):
    deck.reverse()
    return deck

def cut_deck(deck, interval):
    return deck[interval:] + deck[0:interval]

def deal_with_increment(deck, interval):
    new_order = [-1] * len(deck)
    new_position_cursor = 0
    while len(deck) > 0:
        new_order[new_position_cursor] = deck.pop(0)
        new_position_cursor += interval
        if new_position_cursor > len(new_order):
            new_position_cursor -= len(new_order)
    return new_order

def convert_instruction(deck, instruction):
    split = instruction.split(" ")
    if split[0] == "cut":
        return cut_deck(deck, int(split[1]))
    elif split[0] == "deal" and split[1] == "into":
        return deal_into_new_stack(deck)
    elif split[0] == "deal" and split[1] == "with":
        return deal_with_increment(deck, int(split[-1]))
    else:
        raise Exception(f"Cannot handle {instruction}")

####
# Tracking a single card
####
def deal_card_into_new_stack(size_of_deck, card_position):
    return size_of_deck - card_position - 1

def cut_card(size_of_deck, card_position, interval):
    if interval > 0 and card_position < interval:
        return size_of_deck - interval + card_position
    elif interval < 0 and card_position >= size_of_deck + interval:
        distance_from_end = size_of_deck - card_position
        print(f"distance from end {distance_from_end}")
        return abs(interval + distance_from_end)
    else:
        return card_position - interval

def deal_card_with_increment(size_of_deck, card_position, interval):
    return (card_position * interval) % size_of_deck

def convert_card_instruction(size_of_deck, card_position, instruction):
    split = instruction.split(" ")
    if split[0] == "cut":
        return cut_card(size_of_deck, card_position, int(split[1]))
    elif split[0] == "deal" and split[1] == "into":
        return deal_card_into_new_stack(size_of_deck, card_position)
    elif split[0] == "deal" and split[1] == "with":
        return deal_card_with_increment(size_of_deck, card_position, int(split[-1]))
    else:
        raise Exception(f"Cannot handle {instruction}")
####

def test_cases():
    # Test Case 1
    test_case_1 = ["deal with increment 7", "deal into new stack", "deal into new stack"]
    size_of_deck = 10
    deck = list(range(size_of_deck))
    card = 1
    for instruction in test_case_1:
        deck = convert_instruction(deck, instruction)
        card = convert_card_instruction(size_of_deck, card, instruction)
    #print(deck)
    assert(deck == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7])
    assert(card == 7)



    # Test all deal_card_with_increment
    answer = []
    for i in range(0,10):
        answer.append(deal_card_with_increment(size_of_deck, i, 3))
    print(answer)
    print([0, 3, 6, 9, 2, 5, 8, 1, 4, 7])

    #Test Case 2
    test_case_2 = ["deal into new stack", "cut -2", "deal with increment 7", "cut 8", "cut -4", "deal with increment 7", "cut 3", "deal with increment 9", "deal with increment 3", "cut -1"]
    size_of_deck = 10
    deck = list(range(size_of_deck))
    card = 1
    for instruction in test_case_2:
        deck = convert_instruction(deck, instruction)
        card = convert_card_instruction(size_of_deck, card, instruction)
        print(instruction)
        print(deck.index(1))
        print(card)
        print(deck)
        
        print("##########")
    print(deck)
    assert(deck == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6])


@timeit
def question_22():
    with open("data\\q22input.txt") as f:
        input_data = f.read()
    input_data = input_data.split("\n")
    
    part_a_deck = list(range(10007))
    for instruction in input_data:
        part_a_deck = convert_instruction(part_a_deck, instruction)
   
    part_b_card = 2020
    size_of_deck = 119315717514047
    
    # Rely on the shuffle having some kind of loops
    previous_states = set()
    iterations = 0
    while True:
        iterations += 1
        for instruction in input_data:
            part_b_card = convert_card_instruction(size_of_deck, part_b_card, instruction)
        if part_b_card in previous_states:
            break
        previous_states.add(part_b_card)
        print(iterations)
    
    print(iterations)


if __name__ == "__main__":
    question_22()
