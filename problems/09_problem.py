"""
https://adventofcode.com/2020/day/9
"""

"""
PART 1

XMAS starts by transmitting a preamble of 25 numbers. After that, each number you receive should be the sum of any two
of the 25 immediately previous numbers. The two numbers will have different values, and there might be more than one
such pair.

The first step of attacking the weakness in the XMAS data is to find the first number in the list (after the preamble)
which is not the sum of two of the 25 numbers before it.

(Assuming this means the actual value, not the index of said number.)
"""

data = [int(line.strip()) for line in open('09_input.txt', 'r').readlines()]

def check_valid(value, check_list):
    for item in check_list:
        needed_for_sum = value - item
        if needed_for_sum in check_list:
            return True
    return False


def find_weakness(data, increment=25):

    input_ind_to_check = [i+increment for i in range(len(data)-increment)]

    for i in input_ind_to_check:
        check_list = data[(i-increment):i]
        valid = check_valid(data[i], check_list)
        if not valid:
            break

    return i, data[i]

i, v = find_weakness(data)
print(f"Breaks at index {i} and value {v}.")

"""
PART 2

The final step in breaking the XMAS encryption relies on the invalid number you just found: you must find a contiguous
set of at least two numbers in your list which sum to the invalid number from step 1.

To find the encryption weakness, add together the smallest and largest number in this contiguous range; in this example,
these are 15 and 47, producing 62.

"""

for i, n in enumerate(data):
    start = n
    end = n
    sum_vals = n
    next_i = i + 1
    while sum_vals < v:
        end = data[next_i]
        sum_vals += end
        next_i += 1

    if sum_vals == v:
        print(f"Found set: start = {start}, end = {end}")
        sum_slice = data[i:next_i]
        print(f"Part 2: min + max = {min(sum_slice) + max(sum_slice)}") # 75253258 too high
        break
