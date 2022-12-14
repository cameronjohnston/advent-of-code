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
        else: # identical lists?
            return 'CONTINUE'


file1 = open('day13_input.txt', 'r')
Lines = file1.readlines()

# initial parsing
pairs = [[[2]], [[6]]] # divider packets
left = right = None
for i, l in enumerate(Lines):
    l = l.strip()
    if l == '':
        pairs.append((left, right))
        left = right = None
    elif left is None:
        left = ast.literal_eval(l)
    elif right is None:
        right = ast.literal_eval(l)
# at the end, left and right should be something, but not yet added... need to add them:
pairs.append((left, right))

# now do the comparisons, capturing all which are in the correct order
correct_order = []
correct_sum = 0
for i, p in enumerate(pairs):
    print('comparing pair {}...'.format(i))
    result = compare(p[0], p[1])
    if result == 'CORRECT':
        correct_order.append(i)
        correct_sum += i

# now the easy part ... find the answer!
print(correct_order)
print(correct_sum)
