# https://adventofcode.com/2020/day/4
import sys
import re

input = sys.stdin


# part 1
passports = input.read().split('\n\n')
passports = [p.replace(' ', '\n').split('\n') for p in passports]
passports = [{f.split(':')[0]: f.split(':')[1] for f in p if ':' in f} for p in passports]


required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

def has_all_required_fields(passport):
    return set(passport.keys()) & set(required_fields) == set(required_fields)

print(sum(map(has_all_required_fields, passports)))

# part 2
required_fields = {'byr': '19[2-9]\d|200[012]',
                   'iyr': '201\d|2020',
                   'eyr': '202\d|2030',
                   'hgt': '(1[5-8]\d|19[0-3])cm|(59|6\d|7[0-6])in',
                   'hcl': '#[0-9a-f]{6}',
                   'ecl': 'amb|blu|brn|gry|grn|hzl|oth',
                   'pid': '\d{9}'}

print(sum(has_all_required_fields(p) and
          all(re.compile('^' + required_fields[f] + '$').match(p[f]) for f in required_fields)
          for p in passports))
