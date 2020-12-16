"""
https://adventofcode.com/2020/day/16
"""

import numpy as np

# PART 1: Identify invalid tickets and sum the invalid values (is this one per ticket...?)
# First, parse the file (tempted to split it manually and then read it separately but feels like cheating...)
raw_rules = open('16_input_rules.txt', 'r').readlines()
raw_tickets = [line.strip().split(',') for line in open('16_input_nearby.txt', 'r').readlines()]
my_ticket = ['101','179','193','103','53','89','181','139','137','97','61','71','197','59','67','173','199','211','191','131']


def make_range_pair(str_range):
    split = str_range.split('-')
    return int(split[0]), int(split[1])


def make_range_vals(range_pair):
    return np.arange(range_pair[0], range_pair[1] + 1)

# Note - it might be more efficient to record the min, max and INVLAID ranges?
field_rules = {}
for r in raw_rules:
    rule, str_ranges = r.strip().split(': ')
    all_ranges = str_ranges.split(' or ')
    field_rules[rule] = [make_range_pair(x) for x in all_ranges]

nearby = [[int(v) for v in values] for values in raw_tickets]

# Now, for part 1, we only care about the total acceptable values, not by field
all_valid_values = set()
for ranges in field_rules.values():
    for r in ranges:
        all_valid_values.add(list(make_range_vals(r)))
