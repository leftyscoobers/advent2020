"""
https://adventofcode.com/2020/day/24

Lobby hexagon tiles
"""

import numpy as np
from itertools import chain

raw = [line.strip() for line in open('24_input.txt', 'r').readlines()]

# PART 1: How many tiles are black after all the flipping?
# Two issues to handle: 1) Parsing the input and 2) Hexagon grid

# Use 3-axis to represent moves in hex-grid
translation = {'w': np.array([-1, -1, 0]),
               'nw': np.array([-1, 0, 1]),
               'ne': np.array([0, 1, 1]),
               'e': np.array([1, 1, 0]),
               'se': np.array([1, 0, -1]),
               'sw': np.array([0, -1, -1])}


reference = np.array([0]*3)

# Now parsing... Maybe this is janky but we can replace the two char directions with single char
swap = {'a': 'nw', 'b': 'ne', 'c': 'se', 'd': 'sw', 'e': 'e', 'w': 'w'}
moves = []
for line in raw:
    for k, v in swap.items():
        line = line.replace(v, k)
    moves.append(list(line))

# Now read each line of directions and record flips
flipped = set()
for m in moves:
    translations = [translation[swap[i]] for i in m]
    final_tile = tuple(np.sum(translations, axis=0))
    if final_tile in flipped:
        flipped.remove(final_tile)
        print("Back to white!")
    else:
        flipped.add(final_tile)

print(f"PART 1: There are {len(flipped)} black tiles.")  # 330

# PART 2: Basically Conway's game of life with hexagons.
# Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
# Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.

# Assume we start with the above initial layout of black and white from following the initial directions.
n = 100  # Days to flip

def flatten(some_list):
    return list(chain(*some_list))


def get_adjacent(hex_coord):
    return [tuple(np.array(trans) + hex_coord) for k, trans in translation.items()]


# Not breaking any speed recores but it works.
black = flipped.copy()
for day in range(n):
    print(f"Day {day + 1}")
    relevant_tiles = list(set(flatten([get_adjacent(c) for c in black]) + list(black)))

    new_black = black.copy()
    for t in relevant_tiles:
        adj = get_adjacent(t)
        adj_black = len([a for a in adj if a in black])
        # Check black
        if t in black and (adj_black == 0 or adj_black > 2):
            new_black.remove(t)
        elif t not in black and adj_black == 2:  # White
            new_black.add(t)

    black = new_black
    print(f"Now total black {len(black)}")

#  3711
