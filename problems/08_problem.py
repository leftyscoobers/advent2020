"""
https://adventofcode.com/2020/day/8
"""

"""
PART 1

The boot code is represented as a text file with one instruction per line of text. Each instruction consists of an 
operation (acc, jmp, or nop) and an argument (a signed number like +4 or -20).

acc increases or decreases a single global value called the accumulator by the value given in the argument. For 
example, acc +7 would increase the accumulator by 7. The accumulator starts at 0. After an acc instruction, the 
instruction immediately below it is executed next.

jmp jumps to a new instruction relative to itself. The next instruction to execute is found using the argument as an 
offset from the jmp instruction; for example, jmp +2 would skip the next instruction, jmp +1 would continue to the 
instruction immediately below it, and jmp -20 would cause the instruction 20 lines above to be executed next.

nop stands for No OPeration - it does nothing. The instruction immediately below it is executed next.

Run your copy of the boot code. Immediately before any instruction is executed a second time, what value is in the 
accumulator?
"""

raw = open('08_input.txt', 'r').readlines()

def parse_instructions(raw_line):
    split = raw_line.strip().split(' ')
    return split[0], int(split[1])

inst = [parse_instructions(i) for i in raw]


def run_program(instructions):
    i = 0
    index_set = set()
    accum_val = 0
    accum_list = [accum_val]

    while i not in index_set and i != len(instructions):
        index_set.add(i)
        instruction = inst[i]
        if instruction[0] == 'acc':
            accum_val += instruction[1]
            i += 1
        elif instruction[0] == 'nop':
            i += 1
        elif instruction[0] == 'jmp':
            i += instruction[1]
        else:
            break
        accum_list.append(accum_val)

    if i != len(instructions):
        stop_code = "Infinite loop."
    else:
        stop_code = "Hit exit."

    return stop_code, accum_val

code, accum_val = run_program(inst)
print(f"Part 1: Last accumulator score is {accum_val}") # 1331

"""
PART 2

Somewhere in the program, either a jmp is supposed to be a nop, or a nop is supposed to be a jmp. 

The program is supposed to terminate by attempting to execute an instruction immediately after the last instruction in 
the file. By changing exactly one jmp or nop, you can repair the boot code and make it terminate correctly.

What is the value of the accumulator after the program terminates?
"""

# Repeat what we alredy had but methodically swap out nops and jmps.
indices_to_swap = [i for i, command in enumerate(inst) if command[0] in ['nop', 'jmp']]
exit_ind = len(inst)

for swap_i in indices_to_swap:
    print(f"Swapping {swap_i}")
    # Swap out nop for jmp or jmp for nop as appropriate.
    swap_inst = inst.copy()
    curr_cmd, curr_n = swap_inst[swap_i]
    if curr_cmd == 'nop':
        swap_inst[swap_i] = ('jmp', curr_n)
    else:
        swap_inst[swap_i] = ('nop', curr_n)

    # Run program with swapped vals.
    i = 0
    index_set = set()
    accum_val = 0
    accum_list = [accum_val]

    while i not in index_set and i != exit_ind:
        index_set.add(i)
        instruction = swap_inst[i]
        if instruction[0] == 'acc':
            accum_val += instruction[1]
            i += 1
        elif instruction[0] == 'nop':
            i += 1
        elif instruction[0] == 'jmp':
            i += instruction[1]

        accum_list.append(accum_val)

    if i == exit_ind:
        print(f"Reached exit with swapped index {swap_i}")
        print (f"Accumulator value up to this point is {accum_val}")
        break
