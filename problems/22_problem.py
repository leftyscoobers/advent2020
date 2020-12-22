"""
https://adventofcode.com/2020/day/22
"""

# PART 1: Play war with only top card wins (no ties).
# Get Sum of 1 * bottom card, 2 * next card, 3 * next card, etc.

raw = open('22_test.txt', 'r').readlines()
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


def apply_round_win(deck):
    p1_card = deck[1][0]
    p2_card = deck[2][0]

    if p1_card > p2_card:
        deck[1] = deck[1][1:] + [deck[1][0], deck[2][0]]
        deck[2] = deck[2][1:]
    elif p2_card > p1_card:
        deck[2] = deck[2][1:] + [deck[2][0], deck[1][0]]
        deck[1] = deck[1][1:]
    return deck


def play_game(start_deck):
    deck = start_deck.copy()
    if len(deck[1]) == 0 or len(deck[2]) == 0:
        return deck
    return play_game(apply_round_win(deck))

part1_deck = play_game(deck0)
winner = [k for k, d in part1_deck.items() if len(d) > 0][0]
winner_pts = [(i + 1) * x for i, x in enumerate(part1_deck[winner][::-1])]

print(f"Part 1: Sum of winner (player {winner}) points is {sum(winner_pts)}.")

# PART 2: Recursive combat.
# If cards + order is ever repeated, game 1 ends and p1 wins. (prevents infinite recursion)
# If both players have at least as many cards left as the value of the card just played, winner determined by
# playing a another game (recursion)
# Else play as before (highest top card wins)
# However winner of round is determined, continue as before - add winning cards in order to bottom of winner deck.
# "Outer" game ends when one player has all cards - total score as before.

# Let's ignore the infinite loop situation... and just see what happens.
# (I don't feel like figuring out how to store that.)

def play_recursive_game(start_deck, r=0):
    r +=1
    deck = start_deck.copy()
    print(deck)
    if len(deck[1]) == 0 or len(deck[2]) == 0:
        return deck
    if r == 20:
        return deck

    p1_card = deck[1][0]
    p2_card = deck[2][0]
    if len(deck[1]) > p1_card and len(deck[2]) > p2_card:
        print("Start game within game.")
        sub_deck = {1: deck[1][1:], 2: deck[1][1:]}
        deck = play_recursive_game(sub_deck, r=0)

    return play_recursive_game(apply_round_win(deck), r)

part2_deck = play_recursive_game(deck0)
winner = [k for k, d in part1_deck.items() if len(d) > 0][0]
winner_pts = [(i + 1) * x for i, x in enumerate(part1_deck[winner][::-1])]

print(f"Part 2: Sum of winner (player {winner}) points is {sum(winner_pts)}.")