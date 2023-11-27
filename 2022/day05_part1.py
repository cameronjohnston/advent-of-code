import pandas as pd
from textwrap import wrap
import re

# constants
MOVE_RE = 'move ([\d]*) from ([\d]*) to ([\d]*)'
CRATE_RE = '\[([A-Z])\]'
CHARS_PER_INPUT_COL = 4

file1 = open('day05_input.txt', 'r')
Lines = file1.readlines()

# dict with column numbers as its keys and a single array as each value.
# array will have the highest crate in each pile as its 0th element,
# next highest as 1st element, and so on.
crate_piles = {}

for l in Lines:
    if l == '':
        continue
    move_match = re.match(MOVE_RE, l)
    if not move_match:
        cols = wrap(l, CHARS_PER_INPUT_COL, drop_whitespace=False)
        col_num = 0
        for col in cols:
            col_num += 1
            crate_match = re.match(CRATE_RE, col)
            if crate_match:
                crate_char = crate_match.group(1)
                if col_num not in crate_piles or crate_piles[col_num] is None:
                    # first crate detected in this pile
                    crate_piles[col_num] = [crate_char]
                else:
                    # crate is below other crates already detected in this pile.
                    # need to add it to the pile:
                    crate_piles[col_num].append(crate_char)
    else:
        # should only reach here once in the "move" section of the input.
        # at this point we will have a populated crate_piles dict with arrays for piles
        num_to_move, source, target = move_match.groups()
        for n in range(int(num_to_move)):
            char_to_move = crate_piles[int(source)].pop(0)
            crate_piles[int(target)].insert(0, char_to_move)

# now just print out which crate is on top of each pile!
sol = ''
for pile_num in sorted(crate_piles):
    if len(crate_piles[pile_num]) == 0:
        sol += ' '
    else:
        sol += crate_piles[pile_num][0]
print(sol)
