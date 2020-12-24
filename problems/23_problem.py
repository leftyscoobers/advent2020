"""
https://adventofcode.com/2020/day/23
"""

# input_cups = 389125467  # Test input
input_cups = 739862541

start = [int(i) for i in list(str(input_cups))]

# Started P1 with a simple solution that fell part in P2, so I refactored both to use a function with linked lists.

# PART 1: Answer with order of numbers after cup 1
# Test after n = 10: 92658374
# Test after n = 100: 67384529


def playgame(given, max_value, turns):

    # Initialize list
    cups = [0] * (max_value + 1)

    # Add given values to list in linked fashion
    cup = given[0]
    for g in given[1:]:
        cups[cup] = g
        cup = g

    # Fill in values past given values
    if max_value > len(given):
        for i in range(len(given) + 1, max_value + 1):
            cups[cup] = i
            cup = i

    cups[cup] = given[0]  # Makes list loop back to beginning

    # Now loop through rounds
    cup = given[0]  # Rest to starting cup
    for r in range(turns):
        # Set up remove items
        r1 = cups[cup]
        r2 = cups[r1]
        r3 = cups[r2]
        remove_items = (r1, r2, r3)

        # Find destination
        dest = cup - 1
        while dest in remove_items or dest < 1:
            dest -= 1
            if dest < 1:
                dest = max_value

        # Point current cup at the cup after the removed items (cutting them out)
        cups[cup] = cups[r3]

        # Insert removed items after destination
        # From dest -> cups[dest] to dest -> r1 -> r2 -> r3 -> dest_end
        cups[r3] = cups[dest]
        cups[dest] = r1

        cup = cups[cup]

    return cups

p1 = playgame(start, 9, 100)

answer_string = str(p1[1])
n = p1[1]
for i in range(2, 9):
    answer_string += str(p1[n])
    n = p1[n]

print(f"PART 1: Cups after 1 {answer_string}")


# PART 2: Now 1e6 cups and 10e6 turns.
# Find two cups after cup 1 and multiply for answer
# Test solution = 934001 * 159792 = 149245887792

p2 = playgame(start, 1_000_000, 10_000_000)

a1 = p2[1]
a2 = p2[a1]

print(f"PART 2: {a1} * {a2} = {a1 * a2}")


