"""
https://adventofcode.com/2020/day/14
"""

# PART 1
# Tip = write int as binary string: "{0:b}".format(37) -> '100101' but then we still have to zero-pad the front

raw = open('14_input.txt', 'r').readlines()
mask_dict = {}
for line in raw:
    split = line.split(' = ')
    if split[0] == 'mask':
        mask_val = split[1].strip()
        mask_dict[mask_val] = []
    else:
        mem_loc = split[0]
        mem_val = int(split[1])
        mask_dict[mask_val].append((mem_loc, mem_val))


