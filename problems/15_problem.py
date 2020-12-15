"""
https://adventofcode.com/2020/day/15
"""

# PART 1
# After start string, n = 0 if prev n never occurred before. n = last_n - last_time_seen for n that has occurred before
# Find n at 2020
start_str = '1,0,16,5,17,4'

def get_last_value(start_str, end_turn):
    start = [int(x) for x in start_str.split(',')]
    val_record = dict([(n, (-1,t+1)) for t, n in enumerate(start)]) # Keep only two most recent times observed.

    prev_value = start[-1]
    prev_turn = len(start)
    while prev_turn != end_turn:
        turn = prev_turn + 1
        if turn % 1e6 == 0:
            print(turn)
        if val_record[prev_value][0] == -1:
            value = 0
        else:
            previous_turn_pair = val_record[prev_value]
            value = previous_turn_pair[1] - previous_turn_pair[0]

        if value not in val_record.keys():
            val_record[value] = (-1, turn)
        else:
            old_val_par = val_record[value]
            val_record[value] = (old_val_par[1], turn)
        prev_turn = turn
        prev_value = value

    return value

p1_value = get_last_value(start_str, 2020)
print(f"Part 1: Value spoken at the 2020th turn is {p1_value}")

# PART 2
# Repeat but go to 30000000th number - takes < 1 min
p2_value = get_last_value(start_str, 3e7)
print(f"Part 1: Value spoken at the 30,000,000th turn is {p2_value}")
