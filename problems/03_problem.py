"""
PART 1

Due to the local geology, trees in this area only grow on exact integer coordinates in a grid. You make a map (your
puzzle input) of the open squares (.) and trees (#) you can see. For example:

..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#

These aren't the only trees, though; due to something you read about once involving arboreal genetics and biome
stability, the same pattern repeats to the right many times.

From your starting position at the top-left, check the position that is right 3 and down 1. Then, check the position
that is right 3 and down 1 from there, and so on until you go past the bottom of the map.

Starting at the top-left corner of your map and following a slope of right 3 and down 1, how many trees would you
encounter?
"""

data = []
binary_map = {'.': 0, '#': 1}
with open('03_input.txt', 'r') as f:
    for line in f.readlines():
        line_as_list = list(line.strip())
        as_binary = [binary_map[i] for i in line_as_list]
        data.append(as_binary)
f.close()

# Note that the below doesn't check if 0,0 is a tree. Not sure if that should be considered but doesn't affect me...
def calc_trees_hit(data, slope):
    data_cols = len(data[0])
    position = (0, 0)
    trees_hit = 0

    while position[0] < (len(data) - slope[0]):
        new_position = (position[0] + slope[0], position[1] + slope[1])
        if new_position[1] > (data_cols - 1):
            new_position = (new_position[0], new_position[1] - data_cols)
        trees_hit += data[new_position[0]][new_position[1]]
        position = new_position

    return trees_hit

slope = (1, 3)
print(f"Part 1 trees hit: {calc_trees_hit(data, slope)}")


p2_slopes = [(1,1), (1,3), (1,5), (1,7), (2,1)]
trees_per_slope = []

for slope in p2_slopes:
    trees_hit = calc_trees_hit(data, slope)
    trees_per_slope.append(trees_hit)

ans = 1
for t in trees_per_slope:
    ans *= t

print(f"Part 2 tree product: {ans}")