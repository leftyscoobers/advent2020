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


# PART 1: Find all msgs that match rule 0 (count)
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
        return list(set(merged))

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

# PART 2: Completely replace rules 8: 42 and 11: 42 31 with the following, which creates an infinite loop...

# rules['8'] = ['42', '42 8']
# rules['11'] = ['42 31', '42 11 31']

# Rule 8 is basically now some combination of 42's
# Rule 11 is now some combination of 42's followed by some combination of 31's, equal amounts of each.
# Rule 0 is 8 then 11.
# SO basically 42s * n then (42s * m then 31s * m) -> 42 * (n + m) then 31 * m, which really means we can have
# a bunch of 42s and then 31s but no mixing of these (like 42 42 42 31 42 = bad)

# Don't need to check any messages that we already verified (previous working messages still work):
msgs_remain = [m for m in msgs if m not in rule0] # 195
r31 = set(clean_rules['31'])
r42 = set(clean_rules['42'])

# There is no overlap between 31 and 42 sets, so let's map messages back to 42 and 31:
def parse_msg_by_8s(message):
    m_len = len(message)
    pieces = int(m_len / 8)
    return [message[i*8:(i*8 + 8)] for i in range(pieces)]


def convert_to_31_42(message):
    global r31
    global r42
    parsed = parse_msg_by_8s(message)
    converted = [31 if x in r31 else x for x in parsed]
    converted = [42 if x in r42 else x for x in converted]
    return converted


def msg_valid(message):
    conv = convert_to_31_42(message)

    # Check counts - can't have more 31's than 42s (or equal amounts)
    if conv.count(42) <= conv.count(31) or conv.count(31) == 0:
        return False

    # Want consecutive 42s, then 31s
    max_i_42 = max([i for i, v in enumerate(conv) if v == 42])
    min_i_31 = min([i for i, v in enumerate(conv) if v == 31])
    if max_i_42 < min_i_31:
        return True
    else:
        return False

good_messages = msg_match0.copy()
for m in msgs_remain:
    if msg_valid(m):
        good_messages.append(m)

print(f"PART 2: Messages that now match {len(good_messages)}")
