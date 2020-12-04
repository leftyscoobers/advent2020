"""
PART 1
The automatic passport scanners are slow because they're having trouble detecting which passports have all required
fields. The expected fields are as follows:

byr (Birth Year)
iyr (Issue Year)
eyr (Expiration Year)
hgt (Height)
hcl (Hair Color)
ecl (Eye Color)
pid (Passport ID)
cid (Country ID)

Passport data is validated in batch files (your puzzle input). Each passport is represented as a sequence of key:value
pairs separated by spaces or newlines. Passports are separated by blank lines.

Count the number of valid passports - those that have all required fields. Treat cid as optional.
"""

# I hate this but I really just want to reformat everything onto 1 line per record, requires going through file twice.
raw_data = ['']
i = 0
with open('04_input.txt') as f:
    for line in f.readlines():
        if line != '\n':
            raw_data[i] = raw_data[i] + ' ' + line.strip()
        else:
            raw_data[i] = raw_data[i].strip()
            i += 1
            raw_data.append('')
f.close()

fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']

# cid is optional right now
record_of_fields = []
for record in raw_data:
    fields_contained = []
    for field in fields[:-1]:
        if field in record:
            fields_contained.append(field)
    record_of_fields.append(fields_contained)

counts_of_fields = [len(fields) for fields in record_of_fields]
present = [(record, count) for record, count in zip(raw_data, counts_of_fields) if count == len(fields)-1]
print(f"Part one: valid passports with cid optional = {len(present)}")  # 196

"""
PART 2
You can continue to ignore the cid field, but each other field has strict rules about what values are valid for 
automatic validation:

byr (Birth Year) - four digits; at least 1920 and at most 2002.
iyr (Issue Year) - four digits; at least 2010 and at most 2020.
eyr (Expiration Year) - four digits; at least 2020 and at most 2030.

hgt (Height) - a number followed by either cm or in:
If cm, the number must be at least 150 and at most 193.
If in, the number must be at least 59 and at most 76.

hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
pid (Passport ID) - a nine-digit number, including leading zeroes.
cid (Country ID) - ignored, missing or not.

Your job is to count the passports where all required fields are both present and valid according to the above rules. 
"""

# This is some tedious shit.

def test_year(f_val, low, high):
    return len(f_val) == 4 and (low-1) < int(f_val) < (high+1)

def test_byr(f_val):
    return test_year(f_val, 1920, 2002)

def test_iyr(f_val):
    return test_year(f_val, 2010, 2020)

def test_eyr(f_val):
    return test_year(f_val, 2020, 2030)

def get_num(string):
    return int(''.join([i for i in string if i.isdigit()]))

def test_hgt(f_val):
    n = get_num(f_val)
    if 'cm' in f_val:
        return 149 < n < 194
    elif 'in' in f_val:
        return 58 < n < 77
    else:
        return False

def test_hcl(f_val):
    alphanum = [i.isalnum() for i in f_val[1:]]
    return f_val[0] == '#' and len(f_val) == 7 and all(alphanum)

def test_ecl(f_val):
    return f_val in 'amb blu brn gry grn hzl oth'

def test_pid(f_val):
    return len(f_val) == 9 and all([i.isdigit() for i in f_val])

valid = []
for record, count in present:
    r_dict = dict([(f.split(":")[0], f.split(":")[1]) for f in record.strip().split(" ")])
    if all([test_byr(r_dict['byr']),
        test_iyr(r_dict['iyr']),
        test_eyr(r_dict['eyr']),
        test_hgt(r_dict['hgt']),
        test_hcl(r_dict['hcl']),
        test_ecl(r_dict['ecl']),
        test_pid(r_dict['pid'])
           ]):
        valid.append(record)

print(f"Records with fields both present and valid: {len(valid)}")  # 114
