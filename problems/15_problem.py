"""
https://adventofcode.com/2020/day/15
"""

# PART 1
# After start string, n = 0 if prev n never occurred before. n = last_n - last_time_seen for n that has occurred before
# Find n at 2020
start_str = '1,0,16,5,17,4'
start = [int(x) for x in start_str.split(',')]

# Initialize with start list
val_record = dict([(n, [t+1]) for t, n in enumerate(start)])

# Loop through and update the dict. (This feels so sloppy...)
prev_value = start[-1]
prev_turn = len(start)
while prev_turn != 2020:
    turn = prev_turn + 1
    if len(val_record[prev_value]) == 1:
        value = 0
    else:
        turn_last_saw = val_record[prev_value][-2]
        value = prev_turn - turn_last_saw
        if value not in val_record.keys():
            val_record[value] = []

    val_record[value].append(turn)

    prev_turn = turn
    prev_value = value

print(f"Part 1: Value spoken at the 2020th turn is {value}")

# PART 2
# Repeat but go to 30000000th number - just be lazy and copy the work above.
# Two issues - probably slow (yes) and currently collecting all turns for each number but only need the previous two
# NOTE - was slow but worked... took maybe 15 min. Good enough for today.
end = 30000000
val_record = dict([(n, [t+1]) for t, n in enumerate(start)])

prev_value = start[-1]
prev_turn = len(start)
while prev_turn != end:
    turn = prev_turn + 1
    if turn % 1e4:
        print(f"Turn {turn}")
    if len(val_record[prev_value]) == 1:
        value = 0
    else:
        turn_last_saw = val_record[prev_value][-2]
        value = prev_turn - turn_last_saw
        if value not in val_record.keys():
            val_record[value] = []

    val_record[value].append(turn)

    prev_turn = turn
    prev_value = value

print(f"Part 2: Value spoken at the {end}th turn is {value}")


