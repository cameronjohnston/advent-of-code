import pandas as pd
from textwrap import wrap
import re
import numpy as np
from enum import Enum


# constants
SNAFU_VALS = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2,
}
SNAFU_OPTS = ['=', '-', '0', '1', '2']


# classes


# functions
def snafu2dec(s):
    s = s[::-1]
    res = 0
    for i, c in enumerate(s):
        multiplier = pow(5, i+1)
        res += SNAFU_VALS[c] * multiplier
    return res


def dec2snafu(d):
    res = {
        'dec': 0,  # the dec result thus far - will be added to at each step, in sync with the snafu result
        'snafu': '',
    }
    remaining_d = d
    power = 1
    # 1. find which 5's place we should start at in building the snafu result
    while remaining_d > pow(5, power) * 2.5:
        power += 1
    # now "power" should equal the highest snafu place required to represent this number.
    # so, loop through and find the appropriate symbol for each place:
    print('power = {}'.format(power))
    for p in range(power, 0, -1):
        # find the highest abs amount we can leave to be represented by the remaining places:
        max_remaining = pow(5, p) / 2.0
        for opt in SNAFU_OPTS:
            place_val = SNAFU_VALS[opt] * pow(5, p)  # how much this place would be worth with current option
            would_remain = abs(remaining_d - place_val)
            if would_remain > max_remaining:
                continue
            res['snafu'] += opt
            res['dec'] += place_val
            remaining_d -= place_val
            break
    return res['snafu']




file1 = open('day25_input.txt', 'r')
Lines = file1.readlines()

# initial parsing
total = 0
for n, l in enumerate(Lines):
    l = l.strip()
    total += snafu2dec(l)

print(total)
print(dec2snafu(total))
# for sanity check: this should equal the value printed 2 lines above:
# print(snafu2dec(dec2snafu(total)))

