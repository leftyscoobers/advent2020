"""
PART 1
Instead of zones or groups, this airline uses binary space partitioning to seat people. A seat might be specified like
FBFBBFFRLR, where F means "front", B means "back", L means "left", and R means "right".

The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the plane (numbered 0
through 127). Each letter tells you which half of a region the given seat is in. Start with the whole list of rows; the
first letter indicates whether the seat is in the front (0 through 63) or the back (64 through 127). The next letter
indicates which half of that region the seat is in, and so on until you're left with exactly one row.

The last three characters will be either L or R; these specify exactly one of the 8 columns of seats on the plane
(numbered 0 through 7). The same process as above proceeds again, this time with only three steps. L means to keep the
lower half, while R means to keep the upper half.

So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.

Every seat also has a unique seat ID: multiply the row by 8, then add the column. In this example, the seat has ID
44 * 8 + 5 = 357.

Here are some other boarding passes:

BFFFBBFRRR: row 70, column 7, seat ID 567.
FFFBBBFRRR: row 14, column 7, seat ID 119.
BBFFBBFRLL: row 102, column 4, seat ID 820.

As a sanity check, look through your list of boarding passes. What is the highest seat ID on a boarding pass?
"""

data = open('05_input.txt', 'r').readlines()


def bin_to_int(bin_string):
    return int(bin_string, 2)


def get_row_col_from_raw(raw_seat):
    bin_seat = raw_seat.strip().replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1')
    row_bin = bin_seat[:7]
    col_bin = bin_seat[7:]
    return bin_to_int(row_bin), bin_to_int(col_bin)

seats = []
seat_ids = []
for seat in data:
    r, c = get_row_col_from_raw(seat)
    seats.append((r, c))
    seat_ids.append(r * 8 + c)

print(f"Part 1: max seat id is {max(seat_ids)}")

"""
PART2
It's a completely full flight, so your seat should be the only missing boarding pass in your list. However, there's a
catch: some of the seats at the very front and back of the plane don't exist on this aircraft, so they'll be missing
from your list as well.

Your seat wasn't at the very front or back, though; the seats with IDs +1 and -1 from yours will be in your list.

What is the ID of your seat?
"""

possible_seats = list(range(min(seat_ids), max(seat_ids)))
my_seat = [s for s in possible_seats if s not in seat_ids]

print(f"My seat id is: {my_seat[0]}")

# And, for the record:
my_col = my_seat[0] % 8
my_row = (my_seat[0] - my_col) / 8

print(f"Seat location: row {my_row} and col {my_col}")
