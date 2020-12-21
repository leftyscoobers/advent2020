"""
https://adventofcode.com/2020/day/19
"""

from itertools import chain # For flattening lists
from itertools import combinations

raw = open('19_input.txt').readlines()
rules = {}
msgs = []


for line in raw:
    if ':' in line:
        k, r = line.strip().split(': ')
        rules[k] = r.replace('"', '').split(' | ')
    elif len(line.strip()) > 0:
        msgs.append(line.strip())

# PART 2: Completely replace rules 8: 42 and 11: 42 31 with the following, which creates an infinite loop...
# Also note that rule 0 : 8 11.

rules['8'] = ['42', '42 8']
rules['11'] = ['42 31', '42 11 31']

def contains_num(list_of_rules):
    yes_num = [any(char.isdigit() for char in string) for string in list_of_rules]
    return any(yes_num)


def merge_rules(string):
    return string.replace(' ', '')


def flatten_rules(a):
    return list(chain.from_iterable(a))


def rule_str_to_list(strings):
    return [r.split(' ') for r in strings]


def try_substitute(original_rule, value_to_replace, replacement_rule):
    orig = rule_str_to_list(original_rule)
    if value_to_replace not in flatten_rules(orig):
        return original_rule
    else:
        new = []
        for o in orig:
            if o.count(value_to_replace) == 0:
                new.append(' '.join(o))
            elif o.count(value_to_replace) == 2:  # Both values in original set are to be replaced
                new += [''.join(list(t)) for t in combinations(replacement_rule*2, 2)]
            else:
                for r in replacement_rule:
                    new.append(' '.join([r if x == value_to_replace else x for x in o]))
        merged = [merge_rules(x) if not contains_num(x) else x for x in new]
        return merged

# Replace all the run numbers in the rules until all are only a's and b's.
# Note: finding rules for rule 0 takes a while (~1 min), but the rest is fast.
clean_rules = rules.copy()
cleaned_keys = set()
good_keys = [k for k, r in clean_rules.items() if not contains_num(r)]
cleaning = True
while cleaning:
    to_clean = [k for k in good_keys if k not in cleaned_keys]
    if len(cleaned_keys) == (len(clean_rules) - 1):  # Won't clean the last key - nothing left to clean.
        cleaning = False
    for k in clean_rules:
        if k not in good_keys:
            for clean_k in to_clean:
                rset = clean_rules[k]
                clean_rules[k] = try_substitute(rset, clean_k, clean_rules[clean_k])
                cleaned_keys.add(clean_k)
    good_keys = [k for k, r in clean_rules.items() if not contains_num(r)]
    print(f"Percent complete: {round(len(good_keys)/len(clean_rules)*100, 2)}")

# Finally, figure out which of the messages completely match an option for rule 0:
rule0 = set(clean_rules['0'])  # All rules are 24 char long.
msg_match0 = [m for m in msgs if m in rule0]

print(f"PART 1: messages that match rule 0 {len(msg_match0)}")  # 285
