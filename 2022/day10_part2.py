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
rows = []

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
row = ''
diff = 0
for n, v in enumerate(register_hist):
    if n==0:
        continue
    if abs(n-v-diff-1) > 1:
        row += '.'
    else:
        row += '#'
    if n % ROW_LEN == 0:
        print(row)
        row = ''
        diff += 40

print(register_hist)
