"""
https://adventofcode.com/2020/day/18
"""

# PART 1: Order of operations go left to right, but still () first.
# Solve each equation-line and sum resulting values
# Sample format: 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))

import numpy as np

data = open('18_input.txt', 'r').readlines()

def reformat(line):
    return line.strip().replace('(', '( ').replace(')', ' )')


def solve_substring(subline):
    # Note substring is actually list-form of substring
    operate = {'+': (lambda x, y: x + y),
               '*': (lambda x, y: x * y)}

    value = int(subline[0])
    for i, v in enumerate(subline):
        if v in ['+', '*']:
            value = operate[v](value, int(subline[i+1]))
    return value


def advanced_solve(subline):
    # Note substring is actually list-form of substring
    # In "advanced", we do + before *
    operate = {'+': (lambda x, y: x + y),
               '*': (lambda x, y: x * y)}

    remaining = subline
    while '+' in remaining:
        for i, v in enumerate(remaining):
            if v == '+':
                value = operate[v](int(remaining[i-1]), int(remaining[i+1]))
                remaining = remaining[:(i-1)] + [str(value)] + remaining[(i+2):]
                break
    return np.prod([int(x) for x in remaining if x != '*'])


# Inefficient solver
def solve(line, advanced=False):
    lr = reformat(line)
    line_list = lr.split(' ')
    non_ints = ['+', '*']
    while any([v for v in line_list if v in non_ints]):
        # Find pairs of inner ()
        parens = [(i, c) for i, c in enumerate(line_list) if c in ['(', ')']]
        paren_pairs = []
        for i, p in enumerate(parens[:-1]):
            next_p = parens[i+1]
            if p[1] == '(' and next_p[1] == ')':
                paren_pairs.append((p[0], next_p[0]))

        # Just handle the first paren pair and repeat (slightly inefficient but prob ok for now)
        if len(paren_pairs) > 0:
            i1, i2 = paren_pairs[0]
            subline = line_list[(i1+1):i2]
            if advanced:
                temp_val = advanced_solve(subline)
            else:
                temp_val = solve_substring(subline)
            line_list = line_list[:i1] + [str(temp_val)] + line_list[(i2 + 1):]
        else:
            if advanced:
                value = advanced_solve(line_list)
            else:
                value = solve_substring(line_list)
            line_list = [value]

    return value

sums = []
for line in data:
    sums.append(solve(line))

print(f"PART 1: Sum of solutions {sum(sums)}")

# PART 2: Now fix so that addition comes before multiplication
p2_sums = []
for line in data:
    p2_sums.append(solve(line, advanced=True))

print(f"PART 2: Sum of advanced solutions {sum(p2_sums)}")