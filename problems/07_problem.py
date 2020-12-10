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


new_color = ['shiny gold']
color_set = set(new_color)
good_rule_set = set()
while len(new_color) > 0:
    color_set_start = list(color_set)
    for color in new_color:
        match, no_match = split_rules_with_color(raw_data, color)
        good_rule_set |= set(match)
        first_bag = get_first_bag(match)
        color_set |= set(first_bag)

    new_color = [c for c in color_set if c not in color_set_start]

# From good rules, get set of colors:
print(f"PART 1: Count of outer bag colors is {len(color_set)-1}") # 208

"""
PART 2
How many individual bags are required inside your single shiny gold bag?
"""

# Note: all the rules seem to start with a unique color (e.g., shiny gold is at the beginning of one rule only)

# Ok, so we really do need to parse each rule, don't we? :-(
def parse_rule(rule):
    rule_clean = rule.strip().replace("contain ", ', ')
    rule_split = [r.strip() for r in rule_clean.split(',')]
    parent_color = ' '.join(rule_split[0].split(' ')[:2])
    child_list = []
    for part in rule_split[1:]:
        part_split = part.split(' ')
        if part_split[0] != 'no':
            count = int(part_split[0])
            part_color = ' '.join(part_split[1:3])
            child_list.append((count, part_color))

    return parent_color, child_list

parse_rule(raw_data[0])

# Make a dict of rules that go with parent
parent_rule_dict = dict(list(zip(get_first_bag(raw_data), raw_data)))
parsed_rule_dict = dict([(parse_rule(r)) for r in raw_data])


def get_children(parent):
    mult = parent[0]
    return [(mult*n, c) for n, c in parsed_rule_dict[parent[1]]]


def calc_bags(child_list):
    return sum([n for n, c in child_list])

parent = (1, 'shiny gold')
children = get_children(parent)
bags_per_level = [calc_bags(children)]
level = 0
while len(children) > 0:
    level += 1
    new_children = []
    for child in children:
        new_children += get_children(child)
    bags_per_level.append(calc_bags(new_children))
    children = new_children.copy()

print(f"Total bags: {sum(bags_per_level)}") # 1664
