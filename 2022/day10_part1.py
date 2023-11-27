import pandas as pd
from textwrap import wrap
import re

# constants
CMDS = {
    'noop': 'noop',
    'addx': 'addx ([^\s]+)',
}
ROW_LEN = 40

# classes


file1 = open('day10_input.txt', 'r')
Lines = file1.readlines()

register_hist = [1, 1]

for _, l in enumerate(Lines):
    l = l.strip()
    h = register_hist[len(register_hist)-1]
    noop = re.match(CMDS['noop'], l)
    if noop:
        register_hist.append(h)
    addx = re.match(CMDS['addx'], l)
    if addx:
        delta = int(addx.group(1))
        register_hist.append(h)
        register_hist.append(h+delta)

# now the easy part ... find the answer!
total = 0
for i in (20, 60, 100, 140, 180, 220):
    total += register_hist[i] * i

print(total)
print(register_hist)
