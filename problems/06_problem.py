"""
https://adventofcode.com/2020/day/6
"""

"""
PART 1
For each group, count the number of questions to which anyone answered "yes". What is the sum of those counts?
"""

# Make group answers per line, like problem 4, but no need to sep by space
raw_data = ['']
i = 0
with open('06_input.txt') as f:
    for line in f.readlines():
        if line != '\n':
            raw_data[i] += line.strip()
        else:
            i += 1
            raw_data.append('')
f.close()

answer_sets = [set(list(a)) for a in raw_data]
answer_counts = [len(s) for s in answer_sets]

print(f"Part 1: There are {sum(answer_counts)} yes-answers.")

"""
PART 2
You don't need to identify the questions to which anyone answered "yes"; you need to identify the questions to which
everyone answered "yes"!
"""

# Too lazy to adjust the above. Add space back (prob 4) and use that to count people per group.
raw_data = ['']
i = 0
with open('06_input.txt') as f:
    for line in f.readlines():
        if line != '\n':
            raw_data[i] = raw_data[i] + ' ' + line.strip()
        else:
            raw_data[i] = raw_data[i].strip()
            i += 1
            raw_data.append('')
f.close()

# So inefficient but....
match_count = []
for group in raw_data:
    people = group.strip().count(' ') + 1
    count_dict = {}
    for s in list(group.strip()):
        if s not in count_dict:
            count_dict[s] = 1
        else:
            count_dict[s] += 1
    matches = len([x for x in count_dict.values() if x == people])
    match_count.append(matches)

print(f"Part 2: Yes Matches per Group {sum(match_count)}")
