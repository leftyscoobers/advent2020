"""
https://adventofcode.com/2020/day/12
"""

# Part 1: Start facing east at location (0,0)

inst = [[line.strip()[0], int(line.strip()[1:])] for line in open('12_input.txt')]

clockwise = ['N', 'E', 'S', 'W']

def turn(face, direction):
    clockwise = ['N', 'E', 'S', 'W']
    face_i = clockwise.index(face)
    dir = direction[0]
    deg = direction[1]
    if dir == 'R':
        new_face = clockwise[(face_i + int(deg/90)) % 4]
    elif dir == 'L':
        new_face = clockwise[(face_i + 3 * int(deg/90)) % 4]
    else:
        new_face = None
    return new_face


def new_position(dir, n, position):
    x = position[0]
    y = position[1]
    if d == 'N':
        y += n
    if d == 'S':
        y -= n
    if d == 'E':
        x += n
    if d == 'W':
        x -= n
    return (x, y)


face = 'E'
position = (0, 0)
positions = [position]
for d, n in inst:
    print(f"{d}, {n}")
    if d in ['R', 'L']:
        face = turn(face, (d, n))
        positions.append(position)
    if d == 'F':
        d = face
    position = new_position(d, n, position)
    print(position)

print(f"Distance = {abs(position[0]) + abs(position[1])}")

# PART 2
def waypoint_translation(dir, deg, waypoint):
    clockwise_mults = [(1,1), (1,-1), (-1, -1), (-1, 1)]
    translation = waypoint
    flips = int(deg/90)
    if flips % 2 == 1:
        translation = (waypoint[1], waypoint[0])
    if dir == 'R':
        mults = clockwise_mults[flips % 4]
    if dir == 'L':
        mults = clockwise_mults[(flips * 3) % 4]
    translation = (translation[0] * mults[0], translation[1] * mults[1])

    return translation


waypoint = (10,1)  # relative to ship location
position = (0, 0)
for d, n in inst:
    x = position[0]
    y = position[1]
    if d == 'F':
        position = (x + waypoint[0]*n, y + waypoint[1]*n)
    if d in ['R', 'L']:
        waypoint = waypoint_translation(d, n, waypoint)
    if d in ['N', 'E', 'S', 'W']:
        waypoint = new_position(d, n, waypoint)

print(position)
print(f"Part 1: New distance {abs(position[0]) + abs(position[1])}")
