"""
https://adventofcode.com/2020/day/17
"""

# I think I can go back to convolutions for this one... (see problem 11)
# Difference from P11: 1) diff rules 2) grid grows infinitely 3) 3D

# Rule 1: If 1 and 2 or 3 neighbors == 1 then stay 1 else 0
# Rule 2: If 0 and 3 neighbors == 1 then 1 else 0

import numpy as np
from astropy.convolution import convolve

raw_data = open('17_test.txt', 'r').readlines()

# PART 1: 3-D grid with initial 2-D input. Set up for 2 D first, then convert.

# Preprocess to create matrix of 0, 1, null
data = []
swap_dict = {'.': 0, '#': 1}
for line in raw_data:
    line_clean_list = list(line.strip())
    line_swap = [swap_dict[v] for v in line_clean_list]
    data.append(line_swap)

grid_filter = np.ones((3, 3, 3))
grid_filter[1, 1, 1] = 0

# Remember to change to 3D
def zero_pad(grid):
    x, y, z = grid.shape
    zeros = np.zeros((x+2, y+2, z+2))
    x_range = slice(1, x+1)
    y_range = slice(1, y+1)
    z_range = slice(1, z+1)
    zeros[x_range, y_range, z_range] += grid
    return zeros

grid = np.array([data])
cycle = 1
while cycle < 7:
    print(cycle)
    new_grid = zero_pad(grid)
    filter_applied = convolve(new_grid, grid_filter, boundary='fill', fill_value=0.0, nan_treatment='fill', preserve_nan=True) * 26
    new_grid[filter_applied == 3] = 1  # Regardless of i_state, 3 neighbors = 1
    new_grid[filter_applied < 2] = 0  # Note keep initial state if n = 2 (and 1 if n = 3) else 0
    new_grid[filter_applied > 3] = 0
    grid = new_grid.copy()  # Could trim off rows or cols that are all zeros but do we actually care? Won't change the solution.
    print(grid)
    cycle += 1

cells_filled = np.sum(grid)
print(f"PART 1: Total cells filled {cells_filled}")

# PART 2: 4D cube. Consider 3^4 -1 neighbors. Would be nice to rewrite p1 to make dynamic and use for p2 but...
# just copy and adjust...

# DAMN IT. CONVOLVE ONLY WORKS FOR 1-3 D. :-(
grid_filter = np.ones((3, 3, 3, 3))
grid_filter[1, 1, 1, 1] = 0

# Remember to change to 3D
def zero_pad4(grid):
    x, y, z, w = grid.shape
    zeros = np.zeros((x+2, y+2, z+2, w+2))
    x_range = slice(1, x+1)
    y_range = slice(1, y+1)
    z_range = slice(1, z+1)
    w_range = slice(1, w+1)
    zeros[x_range, y_range, z_range, w_range] += grid
    return zeros

grid = np.array([[data]])
cycle = 1
while cycle < 7:
    print(cycle)
    new_grid = zero_pad4(grid)
    filter_applied = convolve(new_grid, grid_filter, boundary='fill', fill_value=0.0, nan_treatment='fill', preserve_nan=True) * 26
    new_grid[filter_applied == 3] = 1  # Regardless of i_state, 3 neighbors = 1
    new_grid[filter_applied < 2] = 0  # Note keep initial state if n = 2 (and 1 if n = 3) else 0
    new_grid[filter_applied > 3] = 0
    grid = new_grid.copy()  # Could trim off rows or cols that are all zeros but do we actually care? Won't change the solution.
    print(grid)
    cycle += 1

cells_filled = np.sum(grid)
print(f"PART 2: Total cells filled {cells_filled}")
