"""
https://adventofcode.com/2020/day/16
"""

import numpy as np

# PART 1: Identify invalid tickets and sum the invalid values (is this one per ticket...?)
raw_rules = open('16_input_rules.txt', 'r').readlines()
raw_tickets = [line.strip().split(',') for line in open('16_input_nearby.txt', 'r').readlines()]
my_ticket = [101,179,193,103,53,89,181,139,137,97,61,71,197,59,67,173,199,211,191,131]


def make_range_pair(str_range):
    split = str_range.split('-')
    return int(split[0]), int(split[1])


# Note - it might be more efficient to record the min, max and INVALID ranges?
field_rules = {}
for r in raw_rules:
    rule, str_ranges = r.strip().split(': ')
    all_ranges = str_ranges.split(' or ')
    field_rules[rule] = [make_range_pair(x) for x in all_ranges]

nearby = [[int(v) for v in values] for values in raw_tickets]  # 238 nearby tickets


# Could go through each range and "merge" to create a single set of valid ranges... but that seems annoying to make.
# Just make a set of valid numbers.
def make_range(range_pair):
    min_val = range_pair[0]
    max_val = range_pair[1]
    return [i + min_val for i in range(max_val - min_val + 1)]


all_valid = set()
for f, r_set in field_rules.items():
    print(f)
    for r in r_set:
        r_range = make_range(r)
        all_valid.update(r_range)

invalid_vals = []
bad_tickets = []
for i, t in enumerate(nearby):
    no_match = [v for v in t if v not in all_valid]
    if len(no_match) > 0:
        invalid_vals.append(no_match)
        bad_tickets.append(i)

print(f"Part 1: Sum of invalid values: {np.sum(invalid_vals)}")

# PART 2: Find which field belongs to which vals in each ticket
# Then multiply all "departure" values in my ticket for answer.

def match_to_range(array, range):
    return [v for v in array if range[0] <= v <= range[1]]


good_tix = [t for i, t in enumerate(nearby) if i not in bad_tickets]
matched_fields = dict([(i, []) for i in range(len(field_rules.keys()))])
for c in range(len(field_rules)):
    col_vals = set([row[c] for row in good_tix])
    for f, rules in field_rules.items():
        matched_vals = set()
        for r in rules:
            matched_vals.update(match_to_range(col_vals, r))
        if matched_vals == col_vals:
            print(f"{f} col {c}")
            matched_fields[c].append(f)

# Now need to do some elimination to figure out what matches where:
final_match = dict([(i, f[0]) for i, f in matched_fields.items() if len(f) == 1])
while len(final_match) < len(matched_fields):
    fields_already_matched = [f for i, f in final_match.items()]
    for i, flist in matched_fields.items():
        diff = [f for f in flist if f not in fields_already_matched]
        if len(diff) == 1:
            print(i, diff)
            final_match[i] = diff[0]


# Get departure fields
dep_ind = [i for i, f in final_match.items() if "departure" in f]
my_tix_vals = [v for i, v in enumerate(my_ticket) if i in dep_ind]

print(f"Part 2: My departure val product: {np.prod(my_tix_vals)}") # 589685618167
