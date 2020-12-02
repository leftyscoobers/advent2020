"""
PART 1
To try to debug the problem, they have created a list (your puzzle input) of passwords (according to the corrupted
database) and the corporate policy when that password was set.

For example -
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc

Each line gives the password policy and then the password. The password policy indicates the lowest and highest number
of times a given letter must appear for the password to be valid.

How many passwords are valid according to their policies?
"""

data = open("02_input.txt", "r").readlines()


# Extract four things: 1. Min times, 2. Max times, 3. Letter of interest, 4. Given password
def parse_password(password_row):
    """
    :param password_row: String format min_times-max_times letter: password
    :return: Returns [int(min), int(max)], letter, password
    """
    minmax_letter_pass = [x.strip() for x in password_row.split(' ')]
    min_max = [int(x) for x in minmax_letter_pass[0].split('-')]
    letter = minmax_letter_pass[1].strip(':')

    return min_max, letter, minmax_letter_pass[2]


# Given password row (unparsed), check password
def password_test(password_row):
    """
    :param password_row: String to be parsed into pass rules and password
    :return: True if password follows rule else False
    """
    min_max, letter, password_string = parse_password(password_row)
    letter_count = password_string.count(letter)
    if letter_count >= min_max[0] and letter_count <= min_max[1]:
        return True
    else:
        return False


good_passwords_bool = [password_test(row) for row in data]

print(f"Good passwords in the data: {sum([1 for x in good_passwords_bool if x])}")


"""
PART 2
The Official Toboggan Corporate Policy actually works a little differently.

Each policy actually describes two positions in the password, where 1 means the first character, 2 means the second
character, and so on. (Be careful; Toboggan Corporate Policies have no concept of "index zero"!) Exactly one of these
positions must contain the given letter. Other occurrences of the letter are irrelevant for the purposes of policy
enforcement.

How many passwords are valid according to the new interpretation of the policies?
"""

def get_letters(password_string, position_list):
    """
    :param password_string: String version of password
    :param position_list: [pos1, pos2] (Note position is 1 indexed, not zero.)
    :return: [letter1, letter2]
    """
    password_list = list(password_string)
    if max(position_list) <= len(password_string):
        indices = [i - 1 for i in position_list]
        return [password_list[i] for i in indices]
    else:
        None



def toboggan_test(password_row):
    """
    :param password_row: String to be parsed into pass rules and password
    :return: True if password follows rule else False
    """
    positions, letter, password_string = parse_password(password_row)
    letters_at_positions =get_letters(password_string, positions)
    letter_sum = letters_at_positions.count(letter)

    if letter_sum == 1:
        return True
    else:
        return False


good_toboggan_bool = [toboggan_test(row) for row in data]

print(f"Good passwords in the data: {sum([1 for x in good_toboggan_bool if x])}")
