import pandas as pd
from textwrap import wrap
import re
import numpy as np
from enum import Enum


# constants


# classes




# functions



file1 = open('day20_input.txt', 'r')
Lines = file1.readlines()

# initial parsing
orig = []
locs = [[]]
for n, l in enumerate(Lines):
    l = l.strip()
    num = int(l)
    orig.append(num)

# now processing
cnt = len(orig)
for i, v in enumerate(orig):
    locs.append([i, v])

locs.pop(0)  # remove the empty array
for i, v in enumerate(orig):
    if not i % 100:
        print('processed {} values'.format(i))
    # skip zero
    if v == 0:
        # print('zero originally at {}'.format(i))
        continue
    # search for the value in locs
    for j, w in enumerate(locs):
        # print(w)
        if w[0] == i:
            # print('found {} from orig {} location, now at {} location'.format(v, i, j))
            # match found: this is the orig value we need to move left or right
            if v > 0:  # moving right
                for k in range(j, j+v):
                    locs[k % cnt], locs[(k+1) % cnt] = locs[(k+1) % cnt], locs[k % cnt]
            if v < 0:  # moving left
                for k in range(j, j+v, -1):
                    locs[k % cnt], locs[(k-1) % cnt] = locs[(k-1) % cnt], locs[k % cnt]
            break  # to avoid shifting twice!

# now the easy part: find the answer!
zero_loc = None  # first, find the zero
for i, v in enumerate(locs):
    if v[1] == 0:
        zero_loc = i
        # print('zero is at {}'.format(i))

# print(locs)
# print ('{} {} {}'.format(
#     locs[(zero_loc+1000) % cnt], locs[(zero_loc+2000) % cnt], locs[(zero_loc+3000) % cnt]))

sol = locs[(zero_loc+1000) % cnt][1] \
      + locs[(zero_loc+2000) % cnt][1] \
      + locs[(zero_loc+3000) % cnt][1]

print(sol)







