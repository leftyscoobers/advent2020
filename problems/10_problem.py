"""
https://adventofcode.com/2020/day/10
"""

"""
PART 1

Each of your joltage adapters is rated for a specific output joltage (your puzzle input). Any given adapter can take an
input 1, 2, or 3 jolts lower than its rating and still produce its rated output joltage.

In addition, your device has a built-in joltage adapter rated for 3 jolts higher than the highest-rated adapter in your
bag. (If your adapter list were 3, 9, and 6, your device's built-in adapter would be rated for 12 jolts.)

Treat the charging outlet near your seat as having an effective joltage rating of 0.

If you use every adapter in your bag at once, what is the distribution of joltage differences between the charging
outlet, the adapters, and your device?

What is the number of 1-jolt differences multiplied by the number of 3-jolt differences?
"""

data = [int(i.strip()) for i in open(f'10_input.txt', 'r').readlines()]
data.sort()

# This is not well-planned for part 2, whatever that is... feels like it should be graph-like
first_adapt = [0] + data[:]
second_adapt = data[:] + [data[-1] + 3]  # device joltage = max in list + 3

diffs = [i_2 - i_1 for i_1, i_2 in zip(first_adapt, second_adapt)]
count_1 = diffs.count(1)
count_3 = diffs.count(3)

print(f"Part 1: {count_1 * count_3}")

"""
PART 2

To completely determine whether you have enough adapters, you'll need to figure out how many different ways they can be
arranged. Every arrangement needs to connect the charging outlet to your device. The previous rules about when adapters
can successfully connect still apply.

The first example above (the one that starts with 16, 10, 15) supports the following arrangements:

(0), 1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, (22)
(0), 1, 4, 5, 6, 7, 10, 12, 15, 16, 19, (22)
(0), 1, 4, 5, 7, 10, 11, 12, 15, 16, 19, (22)
(0), 1, 4, 5, 7, 10, 12, 15, 16, 19, (22)
(0), 1, 4, 6, 7, 10, 11, 12, 15, 16, 19, (22)
(0), 1, 4, 6, 7, 10, 12, 15, 16, 19, (22)
(0), 1, 4, 7, 10, 11, 12, 15, 16, 19, (22)
(0), 1, 4, 7, 10, 12, 15, 16, 19, (22)

What is the total number of distinct ways you can arrange the adapters to connect the charging outlet to your device?
"""

# Right.... graphs.
d2 = [0] + data[:] + [max(data) + 3]
gd = {}

for i, a in enumerate(d2):
    d2_remain = d2[(i+1):]
    gd[a] = [i for i in d2_remain if (i - a) < 4]


def get_paths(d, node, path = []):
    path = path + [node]
    if len(d[node]) == 0:
        return [path]
    paths = []
    for n in gd[node]:
        if n not in path:
            new_paths = get_paths(d, n, path)
            for np in new_paths:
                paths.append(np)
    return paths

p = get_paths(gd, 0)

print(f"Part 2: possible adapter paths {len(p)}")
