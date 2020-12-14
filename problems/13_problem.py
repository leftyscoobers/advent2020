"""
https://adventofcode.com/2020/day/13
"""

# PART 1
data = open('13_input.txt', 'r').readlines()
timestamp = int(data[0])
bus_list = [int(b) for b in data[1].strip().split(',') if b != 'x']

times_to_check = [timestamp + i for i in range(max(bus_list) + 1)]

# Just brute force this
bus_depart = []
for t in times_to_check:
    for b in bus_list:
        if t % b == 0:
            bus_depart.append((b, t))
            break

win_time = min([t for b, t in bus_depart])
win_bus = [b for b, t in bus_depart if t == win_time][0]

print(f"Bus {win_bus} at time {win_time}.")
print(f"Part 1: {(win_time - timestamp) * win_bus}")

# PART 2
def good_time_check(time, bus_pairs):
    start_bus = bus_pairs[0][1]
    if time % start_bus == 0:
        check_mods = [(t, b - time % b) for t, b in bus_pairs[1:]]
        time_match = [t == mod for t, mod in check_mods]
        return all(time_match)
    else:
        return False

# Now split the bus list differently
string_bus = list(data[1].strip().split(','))
bus_min = [(t % int(b), int(b)) for t, b in enumerate(string_bus) if b != 'x']

position = 0
m = 1
max_mod_num = 1
list_to_check = [bus_min[0]]
index = 0
time_is_good = False
while not time_is_good:

    while len(list_to_check) != len(bus_min):
        t = position + m * max_mod_num
        if good_time_check(t, list_to_check):
            print(list_to_check)
            max_mod_num *= list_to_check[-1][1]  # Now increment by next bus as well
            index += 1
            list_to_check.append(bus_min[index])
            position = t
            print(f"Mod: {max_mod_num}, Pos: {position}")
            m = 1
        else:
            m += 1
            if m % 100 == 0:
                print(f"m status: {m}")

    t = position + m * max_mod_num
    time_is_good = good_time_check(t, list_to_check)
    m += 1
    if m % 100 == 0:
        print(f"m status: {m}")

print(f"Found time {t}")

