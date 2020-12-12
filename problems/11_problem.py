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

raw_data = open('11_input.txt', 'r').readlines()

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
# Ugh. Just go back to the matrix with strings
def count_seats(data):
    return sum([row.count('#') for row in data])

data = [list(line.strip()) for line in raw_data]
nrow = len(data)
ncol = len(data[0])
new_seats = [list(line.strip()) for line in raw_data]
orig_seats_filled = count_seats(data)
diff = 100
while diff != 0:
    for r in range(nrow):
        for c in range(ncol):
            if data[r][c] != '.':
                visible_filled_seats = 0
                # North
                r_ind = r - 1
                seat = '.'
                while r_ind >= 0 and seat == '.':
                    seat = data[r_ind][c]
                    r_ind -= 1
                if seat == '#':
                    visible_filled_seats += 1
                # South
                r_ind = r + 1
                seat = '.'
                while r_ind < nrow and seat == '.':
                    seat = data[r_ind][c]
                    r_ind += 1
                if seat == '#':
                    visible_filled_seats += 1
                # West
                c_ind = c - 1
                seat = '.'
                while c_ind >= 0 and seat == '.':
                    seat = data[r][c_ind]
                    c_ind -= 1
                if seat == '#':
                    visible_filled_seats += 1
                # East
                c_ind = c + 1
                seat = '.'
                while c_ind < ncol and seat == '.':
                    seat = data[r][c_ind]
                    c_ind += 1
                if seat == '#':
                    visible_filled_seats += 1
                # Northwest I hate this but I don't care enough to do it differently.
                r_ind = r - 1
                c_ind = c - 1
                seat = '.'
                while r_ind >= 0 and c_ind >= 0 and seat == '.':
                    seat = data[r_ind][c_ind]
                    r_ind -= 1
                    c_ind -= 1
                if seat == '#':
                    visible_filled_seats += 1
                # Northeast
                r_ind = r - 1
                c_ind = c + 1
                seat = '.'
                while r_ind >= 0 and c_ind < ncol and seat == '.':
                    seat = data[r_ind][c_ind]
                    r_ind -= 1
                    c_ind += 1
                if seat == '#':
                    visible_filled_seats += 1
                # Southwest
                r_ind = r + 1
                c_ind = c - 1
                seat = '.'
                while r_ind < nrow and c_ind >= 0 and seat == '.':
                    seat = data[r_ind][c_ind]
                    r_ind += 1
                    c_ind -= 1
                if seat == '#':
                    visible_filled_seats += 1
                # Southeast
                r_ind = r + 1
                c_ind = c + 1
                seat = '.'
                while r_ind < nrow and c_ind < ncol and seat == '.':
                    seat = data[r_ind][c_ind]
                    r_ind += 1
                    c_ind += 1
                if seat == '#':
                    visible_filled_seats += 1
                if visible_filled_seats == 0:
                    new_seats[r][c] = '#'
                if visible_filled_seats > 4:
                    new_seats[r][c] = 'L'
    new_filled = count_seats(new_seats)
    diff = new_filled - orig_seats_filled
    print(diff)
    orig_seats_filled = new_filled
    data = [row + [] for row in new_seats]  # list.copy() not working? Still pointing at old list. Ugh.

print(f"Part 2: Seats filled {new_filled}")
