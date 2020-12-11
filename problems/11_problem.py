"""
https://adventofcode.com/2020/day/11
"""

"""
PART 1

Figure out seating in waiting area.

The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L), or an occupied seat (#).

All decisions are based on the number of occupied seats adjacent to a given seat (one of the eight positions immediately
up, down, left, right, or diagonal from the seat). The following rules are applied to every seat simultaneously:

If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
Otherwise, the seat's state does not change.
Floor (.) never changes; seats don't move, and nobody sits on the floor.

Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up 
occupied?
"""

import numpy as np
from astropy.convolution import convolve

raw_data = open('11_test.txt', 'r').readlines()

# Preprocess to create matrix of 0, 1, null
data = []
swap_dict = {'L': 0, '.': np.nan}
for line in raw_data:
    line_clean_list = list(line.strip())
    line_swap = [swap_dict[v] for v in line_clean_list]
    data.append(line_swap)

seats = np.array(data)
seat_filter = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

change_in_seats = 100  # Start with some > 0 number

# Start with a couple iterations
while change_in_seats != 0:
    seats_filled = np.nansum(seats)
    new_seats = seats.copy()
    filter_applied = convolve(new_seats, seat_filter, boundary='fill', fill_value=0.0, nan_treatment='fill', preserve_nan=True) * 8
    new_seats[filter_applied == 0] = 1  # No neighbors -> fill (doesn't matter if previously filled)
    new_seats[filter_applied >= 4] = 0  # Was filled and too many neighbors
    new_seats_filled = np.nansum(new_seats)
    change_in_seats = new_seats_filled - seats_filled
    seats = new_seats.copy()

print(f"PART 1: Total seats filled {new_seats_filled}")

"""
PART 2

Now, instead of considering just the eight immediately adjacent seats, consider the first seat in each of those eight 
directions. For example, the empty seat below would see eight occupied seats:

.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....

Also, people seem to be more tolerant than you expected: it now takes five or more visible occupied seats for an 
occupied seat to become empty (rather than four or more from the previous rules). 

Given the new visibility method and the rule change for occupied seats becoming empty, once equilibrium is reached, how 
many seats end up occupied?
"""

# So much for convolutions? Doesn't appear to help with this view angle bit.
def check_neighbors(slope_array):
    if len(slope_array) == 0:
        return 0
    else:
        count_neighbors = np.nansum(slope_array)
        if count_neighbors > 0:
            return 1
        else:
            return 0

# God damn. Just do it the messy way.
def check_diag(ns, ew, data):
    diag_sum = 0
    if len(ns) > 0 and len(ew) > 0 and np.sum(ns) > -1 and np.sum(ew) > -1:
        val_array = []
        for i in range(min(len(ns), len(ew))):
            val_at_seat = seats[ns[i]][ew[i]]
            val_array.append(val_at_seat)
        if np.nansum(val_array) > 0:
            diag_sum = 1
    return diag_sum

seats = np.array(data)
nrow = len(seats)
ncol = len(seats[0])

seats_filled = np.nansum(seats)
seat_diff = 100
i = 0
while i < 100 and seat_diff != 0:
    i += 1
    new_seats = seats.copy()
    for row in range(nrow):
        for col in range(ncol):
            if not np.isnan(new_seats[row][col]):
                if col > 0:
                    west = check_neighbors(seats[row][:col])
                    east = check_neighbors(seats[row][(col + 1):])
                else:
                    west = 0
                    east = 0
                if row > 0:
                    north = check_neighbors(seats[:row, col])
                    south = check_neighbors(seats[(row + 1):, col])
                else:
                    north = 0
                    south = 0

                n = np.arange(0, row)[::-1]
                s = np.arange(row+1, nrow)
                w = np.arange(0, col)[::-1]
                e = np.arange(col+1, ncol)

                north_west = check_diag(n, w, seats)
                north_east = check_diag(n, e, seats)
                south_west = check_diag(s, w, seats)
                south_east = check_diag(s, e, seats)

                total_neighbors_visible = west + east + north + south + north_west + north_east + south_west + south_east
                if total_neighbors_visible == 0:
                    new_seats[row][col] = 1
                elif total_neighbors_visible > 4:
                    new_seats[row][col] = 0
    new_seats_filled = np.nansum(new_seats)
    seat_diff = new_seats_filled - seats_filled
    seats = new_seats.copy()
    seats_filled = new_seats_filled
    print(seat_diff)

