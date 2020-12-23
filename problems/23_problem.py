"""
https://adventofcode.com/2020/day/23
"""

input_cups = 389125467  # Test input
# input_cups = 739862541

# PART 1: Answer with order of numbers after cup 1
# Test after n = 10: 92658374
# Test after n = 100: 67384529


def get_destination(cup_val, to_remove, max=9):
    dest = cup_val - 1
    if dest == 0:
        dest = 9
    if dest not in to_remove:
        return dest

    return get_destination(dest, to_remove)

# This is a mess. Not proud.
start = [int(i) for i in list(str(input_cups))]


def playgame(given, max_value, turns):
    if len(given) < max_value:
        p1 = given + list(range(max(given)-1, max_value+1))
    else:
        p1 = given.copy()
    ci = 0  # starting cup index
    turns = 100
    for n in range(turns):
        if n % 1e5 == 0:
            print(f"Round {n}")
            print(p1[:20])
        cup = p1[ci]
        remove_indices = [(ci + i) % max_value for i in range(1, 4)]
        remove_items = [p1[i] for i in remove_indices]
        d = get_destination(cup, remove_items)
        p1 = [x for i, x in enumerate(p1) if i not in remove_indices]
        di = p1.index(d)
        p1 = p1[:(di+1)] + remove_items + p1[(di+1):]

        new_cup_index = p1.index(cup)
        ci = (new_cup_index + 1) % max_value
    return p1

p1 = playgame(start, max(start), 100)

# Format for output
i1 = p1.index(1)
new_indices = [(9-i1 + i) % 9 for i in range(9)]
new_order = [str(x) for i, x in sorted(list(zip(new_indices, p1))) if x != 1]
print(''.join(new_order))


# PART 2: Now 1e6 cups and 10e6 turns.
# Find two cups after cup 1 and multiply for answer
# Test solution = 934001 * 159792 = 149245887792

# What happens if I just run the above function with no changes....?
p2 = playgame(start, 1000000, 10000000)
