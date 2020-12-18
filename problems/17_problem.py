"""
https://adventofcode.com/2020/day/17
"""

# I think I can go back to convolutions for this one... (see problem 11)
# Difference from P11: 1) diff rules 2) grid grows infinitely 3) 3D

# Rule 1: If 1 and 2 or 3 neighbors == 1 then stay 1 else 0
# Rule 2: If 0 and 3 neighbors == 1 then 1 else 0

import numpy as np
from itertools import combinations

raw_data = open('17_input.txt', 'r').readlines()

# Preprocess to create matrix of 0, 1 (then we can do math)
data = []
swap_dict = {'.': 0, '#': 1}
for line in raw_data:
    line_clean_list = list(line.strip())
    line_swap = [swap_dict[v] for v in line_clean_list]
    data.append(line_swap)

# PART 1: 3-D grid with initial 2-D input. Set up for 2 D first, then convert.
# Note: Did P1 using convolution but it falls apart in P2 with 4D b/c the library used doesn't support more than 3D. :(
# Starting over. Boo.

def zero_pad(grid, dimensions=2):
    gs = grid.shape
    g0 = [d + 2 for d in gs]
    zeros = np.zeros(g0)
    slices = [slice(1, d+1) for d in gs]
    zeros[tuple(slices)] += grid
    return zeros


def get_increment_combos(dimensions=2):
    possible_values = [-1, 0, 1] * dimensions
    all_combos = list(set(combinations(possible_values, dimensions)))
    all_combos.remove(tuple([0] * dimensions))
    return all_combos


def sum_dim(grid, increment):
    # Errr...assume the grid is double zero padded...
    max_i = [m - 1 for m in grid.shape]
    zeros = np.zeros(grid.shape)
    orig_slices = [slice(1, m) for m in max_i]
    slices = [slice(1 + i, max_i[ind] + i) for ind, i in enumerate(increment)]
    zeros[tuple(orig_slices)] += grid[tuple(slices)]
    return zeros


dimensions = 3
increments = get_increment_combos(dimensions)
grid = zero_pad(np.array([data]), dimensions)
cycle = 1
while cycle < 7:
    print(cycle)
    new_grid = zero_pad(grid, dimensions)
    sum_grid = np.zeros(new_grid.shape)
    for incr in increments:
        sum_grid += sum_dim(new_grid, incr)
    new_grid[sum_grid == 3] = 1  # Regardless of i_state, 3 neighbors = 1
    new_grid[sum_grid < 2] = 0  # Note keep initial state if n = 2 (and 1 if n = 3) else 0
    new_grid[sum_grid > 3] = 0
    grid = new_grid.copy()  # Could trim off rows or cols that are all zeros but do we actually care? Won't change the solution.
    cycle += 1
    cells_filled = np.sum(grid)
    print(cells_filled)

cells_filled = np.sum(grid)
print(f"PART 1: Total cells filled {cells_filled}")

# PART 2: Same deal but 4D. Would be nicer to write above as function but whatever.
dimensions = 4
increments = get_increment_combos(dimensions)
grid = zero_pad(np.array([[data]]), dimensions)
cycle = 1
while cycle < 7:
    print(cycle)
    new_grid = zero_pad(grid, dimensions)
    sum_grid = np.zeros(new_grid.shape)
    for incr in increments:
        sum_grid += sum_dim(new_grid, incr)
    new_grid[sum_grid == 3] = 1  # Regardless of i_state, 3 neighbors = 1
    new_grid[sum_grid < 2] = 0  # Note keep initial state if n = 2 (and 1 if n = 3) else 0
    new_grid[sum_grid > 3] = 0
    grid = new_grid.copy()  # Could trim off rows or cols that are all zeros but do we actually care? Won't change the solution.
    cycle += 1
    cells_filled = np.sum(grid)
    print(cells_filled)

cells_filled = np.sum(grid)
print(f"PART 1: Total cells filled {cells_filled}")