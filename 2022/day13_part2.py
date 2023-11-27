import pandas as pd
from textwrap import wrap
import re
import ast


# constants


# functions
def compare(lhs, rhs):
    if isinstance(lhs, int) and isinstance(rhs, int):
        if lhs < rhs:
            return 'CORRECT'
        elif lhs > rhs:
            return 'INCORRECT'
        else:
            return 'CONTINUE'
    if isinstance(lhs, int) and isinstance(rhs, list):
        lhs = [lhs]
        return compare(lhs, rhs)
    if isinstance(lhs, list) and isinstance(rhs, int):
        rhs = [rhs]
        return compare(lhs, rhs)
    if isinstance(lhs, list) and isinstance(rhs, list):
        for i in range(len(lhs)):
            if i > len(rhs) - 1:
                # LHS still has value(s), RHS has run out
                return 'INCORRECT'
            res = compare(lhs[i], rhs[i])
            if res != 'CONTINUE':
                return res
        if len(lhs) < len(rhs):
            # LHS has run out of values, RHS still has value(s)
            return 'CORRECT'
        else:  # identical lists?
            return 'CONTINUE'


file1 = open('day13_input.txt', 'r')
Lines = file1.readlines()

# initial parsing
packets = [[[2]], [[6]]]  # divider packets
for i, l in enumerate(Lines):
    l = l.strip()
    if l != '':
        packets.append(ast.literal_eval(l))

# now do the comparisons, and order the packets
# bubble sort because it's easier than merge sort lol
print(len(packets))
swapped = False
while True:
    swapped = False
    for i in range(len(packets)):
        if i == len(packets) - 1:  # we've reached the end
            break
        result = compare(packets[i], packets[i + 1])
        if result == 'INCORRECT':
            packets[i], packets[i + 1] = packets[i + 1], packets[i]
            swapped = True
    if not swapped:  # we've completed the for loop with no swaps -> all in correct order
        break

# now the easy part ... find the answer!
ans = 1
for i, p in enumerate(packets):
    if p == [[2]] or p == [[6]]:
        ans *= i + 1
print(ans)
