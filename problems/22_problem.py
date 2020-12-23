"""
https://adventofcode.com/2020/day/22
"""

# PART 1: Play war with only top card wins (no ties).
# Get Sum of 1 * bottom card, 2 * next card, 3 * next card, etc.

raw = open('22_input.txt', 'r').readlines()
deck0= {1: [], 2: []}

fill_player = 1
for line in raw:
    striped = line.strip()
    if "Player 1" in striped or len(striped) == 0:
        continue
    elif "Player 2" in striped:
        fill_player = 2
        continue
    deck0[fill_player].append(int(line))


def play_round(deck):
    p1_card = deck[1][0]
    p2_card = deck[2][0]

    if p1_card > p2_card:
        deck[1] = deck[1][1:] + [p1_card, p2_card]
        deck[2] = deck[2][1:]
    elif p2_card > p1_card:
        deck[1] = deck[1][1:]
        deck[2] = deck[2][1:] + [p2_card, p1_card]

    return deck


def play_game(start_deck):
    deck = start_deck.copy()
    if len(deck[1]) == 0 or len(deck[2]) == 0:
        return deck
    return play_game(play_round(deck))


def game_winner(finished_deck):
    return [k for k, d in finished_deck.items() if len(d) > 0][0]

part1_deck = play_game(deck0)
winner = game_winner(part1_deck)
winner_pts = [(i + 1) * x for i, x in enumerate(part1_deck[winner][::-1])]

print(f"Part 1: Sum of winner (player {winner}) points is {sum(winner_pts)}.")

# PART 2: Recursive combat.
# If cards + order is ever repeated, game 1 ends and p1 wins. (prevents infinite recursion)
# If both players have at least as many cards left as the value of the card just played, winner determined by
# playing a another game (recursion)
# Else play as before (highest top card wins)
# However winner of round is determined, continue as before - add winning cards in order to bottom of winner deck.
# "Outer" game ends when one player has all cards - total score as before.

# This is a mess but oh well.


def play_recursive_game(deck):

    seen_before = set()
    while len(deck[1]) != 0 and len(deck[2]) != 0:

        # Case: Already seen this set
        curr_deck = str(deck[1]), str(deck[2])  # ([], []) doesn't work
        # print(curr_deck)
        if curr_deck in seen_before:  # p1 wins
            print("Break infinite loop!")
            # Hacky but fake winning deck for p1
            return {1: [0], 2: []}
        seen_before.add(curr_deck)

        p1_card = deck[1][0]
        p2_card = deck[2][0]

        winner = 1  # Default p1
        if p2_card > p1_card:
            winner = 2

        # Case: Recursive play required, overwrite winner
        if len(deck[1]) > p1_card and len(deck[2]) > p2_card:
            # print("Start game within game.")
            sub_deck = {1: deck[1][1:(p1_card+1)], 2: deck[2][1:(p2_card+1)]}
            sub_deck = play_recursive_game(sub_deck)
            winner = game_winner(sub_deck)

        if winner == 1:
            deck[1] = deck[1][1:] + [p1_card, p2_card]
            deck[2] = deck[2][1:]
        else:
            deck[1] = deck[1][1:]
            deck[2] = deck[2][1:] + [p2_card, p1_card]

    return deck

part2_deck = play_recursive_game(deck0.copy())
winner = game_winner(part2_deck)
winner_pts = [(i + 1) * x for i, x in enumerate(part2_deck[winner][::-1])]

print(f"Part 2: Sum of winner (player {winner}) points is {sum(winner_pts)}.")  # 31835



import numpy as np
from copy import deepcopy
with open("22_input.txt", 'r') as f:
    decks = [list(map(int, sec.splitlines()[1:]))
                     for sec in f.read().split('\n\n')]

def play(d, part):
    if (m := max(d[0])) > max(d[1]) and m > len(d[0]) + len(d[1]):# p0 can't lose
        return 0, d[0]
    seen = set()
    while all(d):
        if (h := str(d)) in seen:
            return 0, d[0]
        seen.add(h)
        c1, c2 = d[0].pop(0), d[1].pop(0)
        w = c2 > c1
        if part == 2 and len(d[0]) >= c1 and len(d[1]) >= c2:
            w, _ = play([d[0][:c1], d[1][:c2]], 2)
        d[w] += [c2, c1] if w else [c1, c2]

    return (0, d[0]) if d[0] else (1, d[1])

score = lambda d: np.array(d).dot(range(len(d), 0, -1))

for r in (1,2):
    print(f'Part {r}:', score(play(deepcopy(decks), r)[1]))