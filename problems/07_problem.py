"""
https://adventofcode.com/2020/day/7
"""

"""
PART 1

Example bag rules:
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.

You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be
valid for the outermost bag?

This is a graph problem...
"""

raw_data = open('07_input.txt', 'r').readlines()


# rules with color and without
def split_rules_with_color(rule_list, color):
    return [r for r in rule_list if color in r], [r for r in rule_list if color not in r]


def get_first_bag(rule_list):
    return [' '.join(r.split(' ')[:2]) for r in rule_list]


good_rule_set = set()

# Inital colors
match, no_match = split_rules_with_color(raw_data, "shiny gold")
good_rule_set |= set(match)
while len(match) > 0:
    first_bag = get_first_bag(match)
    for color in first_bag:
        match, no_match = split_rules_with_color(no_match, color)
        good_rule_set |= set(match)

# From good rules, get set of colors:
good_color_list = [c for c in get_first_bag(list(good_rule_set))]
print(f"PART 1: Count of outer bag colors is {len(good_color_list)-1}")
