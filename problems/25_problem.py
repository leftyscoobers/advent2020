"""
https://adventofcode.com/2020/day/25
"""

# Test values
# k1 = 5764801
# k2 = 17807724

# My input
k1 = 8252394
k2 = 6269621

# PART 1: Find encryption key (assume subject is 7? unclear)


def find_loops(key, subject=7):
    v = 1
    loops = 0
    while v != key:
        loops += 1
        v *= subject
        v %= 20201227
    return loops


def transform(loops, subject=7):
    v = 1
    for l in range(loops):
        v *= subject
        v %= 20201227
    return v


def get_encryption(key1, key2, subject=7):
    l1 = find_loops(key1)
    l2 = find_loops(key2)
    e1 = transform(l1, key2)
    e2 = transform(l2, key1)
    if e1 != e2:
        print("Error: Encryption values don't match!")
        return
    return e1

print(f"PART 1: Encryption value {get_encryption(k1, k2)}")