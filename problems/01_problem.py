"""
PART 1
Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input);
apparently, something isn't quite adding up.

Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.
"""

data = [int(x) for x in open("01_input.txt", "r").readlines()]
target_sum = 2020


def sum_pair(data, target):
    for x in data:
        y = target - x
        if y in data:
            return x, y
    return None, None


x1, y1 = sum_pair(data, target_sum)
print(f"Part 1: {x1 * y1}")


"""
PART 2
They offer you a second one if you can find three numbers in your expense report that meet the same criteria.
"""

def sum_three(data, target):
    for x in data:
        diff_target = target - x
        print(x)
        possible_matches = [i for i in data if i < diff_target]
        for y in possible_matches:
            print(y)
            y, z = sum_pair(possible_matches, diff_target)
            if y is not None and y in data and z in data:
                return x, y, z  # should also check that x, y, z are unique

x2, y2, z2 = sum_three(data, target_sum)
print(f"Part 2: {x2 * y2 * z2}")
