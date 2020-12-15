"""
https://adventofcode.com/2020/day/14
"""

# PART 1
# Tip = write int as binary string: "{0:b}".format(37) -> '100101' but then we still have to zero-pad the front
raw = open('14_input.txt', 'r').readlines()
mask_dict = {}
mask_order = []
for line in raw:
    split = line.split(' = ')
    if split[0] == 'mask':
        mask_val = split[1].strip()
        mask_dict[mask_val] = []
        mask_order.append(mask_val)
    else:
        mem_loc = split[0]
        mem_val = int(split[1])
        mask_dict[mask_val].append((mem_loc, mem_val))


def make_36_bit(int_val):
    int_bin = "{0:b}".format(int_val)
    zeros_needed = 36 - len(int_bin)
    return '0' * zeros_needed + int_bin


def apply_mask(string_val, mask):
    non_x_mask_index = [i for i, v in enumerate(mask) if v != 'X']
    new_string_list = list(string_val)
    # Prob a cleaner way to do this but
    for i in non_x_mask_index:
        new_string_list[i] = mask[i]
    return ''.join(new_string_list)


mem_loc_dict = {}
for m in mask_order:
    operations = mask_dict[m]
    for op in operations:
        mem_loc = op[0]
        intended_write_val = make_36_bit(op[1])

        actual_write_val = apply_mask(intended_write_val, m)
        mem_loc_dict[mem_loc] = int(actual_write_val, 2)

print(f"Part 1: Sum of values written = {sum(mem_loc_dict.values())}")

# PART 2
def apply_mask_mem(string_val, mask):
    # Swap out all vals according to mask rules
    string_with_mask = list(string_val)
    for i, m in enumerate(mask):
        if m in ['X', '1']:
            string_with_mask[i] = m

    # Now calculate possible values:
    new_string = ''.join(string_with_mask)
    base_value = int(new_string.replace('X', '0'), 2)
    mem_vals = [base_value]
    two_i = [35 - i for i, v in enumerate(new_string) if v == 'X']
    for exp in two_i:
        mem_vals += [curr_v + 2 ** exp for curr_v in mem_vals]
    return mem_vals


def get_mem_int(mem_string):
    return int(mem_string.replace('mem[','').replace(']', ''))


mem_location_val = {}
for i, m in enumerate(mask_order):
    if i % 10:
        print(f"Mask number: {i}")
    operations = mask_dict[m]
    for op in operations:
        mem_int = get_mem_int(op[0])
        mem_locs_to_write = apply_mask_mem(make_36_bit(mem_int), m)
        val_to_write = op[1]
        for loc in mem_locs_to_write:
            mem_location_val[loc] = val_to_write

print(f"Part 2: Sum of values written = {sum(mem_location_val.values())}")
