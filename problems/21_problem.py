"""
https://adventofcode.com/2020/day/21
"""

from copy import deepcopy

# PART 1: You start by compiling a list of foods (your puzzle input), one food per line. Each line includes that food's
# ingredients list followed by some or all of the allergens the food contains. Each allergen is found in exactly one
# ingredient. Each ingredient contains zero or one allergen but not all allergens are marked.

# The first step is to determine which ingredients can't possibly contain any of the allergens in any food in your list.
# Answer how many times the safe ingredients appear (incl repeats).

raw = open('21_input.txt', 'r').readlines()

# Not sure how we want to use this yet...
ingr_allerg = []
all_allergens = set()
for line in raw:
    split_i_a = line.strip().split(' (contains ')
    ingred = set(split_i_a[0].split(' '))
    allerg = set(split_i_a[1].replace(')', '').replace(',', '').split(' '))
    all_allergens.update(allerg)
    ingr_allerg.append([ingred, allerg])


# First run through the list and find all possibilities
a_match = {}
for a in all_allergens:
    print(a)
    a_match[a] = set()
    # Get all lists with a
    contains_a = [l for l, ag in ingr_allerg if a in ag]
    if len(contains_a) == 1:
        a_match[a] = contains_a[0]
    else:
        ingr_match_a = contains_a[0]
        for s in contains_a[1:]:
            ingr_match_a = ingr_match_a.intersection(s)
        a_match[a] = ingr_match_a

# Now match everything we can (may be cases where we can't fully match)
matching = True
while matching:
    a_match_copy = a_match.copy()
    for a in all_allergens:
        possible = a_match_copy[a]
        if len(possible) == 1:  # Only 1 time in set, so perfect match between allergen and ingredient
            a_match[a] = list(possible)[0]
            # Now remove as option from the other allergens
            for alt_a in [x for x in all_allergens if x != a]:
                if a_match[a] in a_match[alt_a]:
                    a_match[alt_a].remove(a_match[a])
    if a_match_copy == a_match:  # Check if dicionary has changed, stop when no more changes
        matching = False

# Now try and answer the part 1 question:
avoid_ingredients = a_match.values()  # Might break if some values are still sets
safe_ingredients = 0
for i, a in ingr_allerg:
    safe = [x for x in i if x not in avoid_ingredients]
    safe_ingredients += len(safe)

print(f"Occurrence of safe ingredients: {safe_ingredients}")

# PART 2: Arrange ingredients alphabetically by allergen, comma sep, no spaces
sorted_allergens = sorted(a_match.keys())
sorted_ingr = [a_match[k] for k in sorted_allergens]
print(','.join(sorted_ingr))