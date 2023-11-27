import pandas as pd
from textwrap import wrap
import re
import numpy as np
from enum import Enum
from sympy import symbols, solve


# constants
OP_FMT = '([^\s]+): ([^\s]+) ([\+\-\*\/]+) ([^\s]+)'
NUM_FMT = '([^\s]+): ([0-9]+)'


# classes


# functions
def calc(monkey):
    m = monkeys[monkey]
    if monkey == 'humn':
        # print('humn returning humn')
        return 'humn'
    elif 'operation' not in m:
        return m['op1'] # should be just a number
    res1, res2 = calc(m['op1']), calc(m['op2'])
    if isinstance(res1, str):
        # print('res1 of {} is str: {}'.format(monkey, res1))
        if True:  # 'humn' in res1:
            # print('humn contained in {} res1; res2 is {}'.format(monkey, res2))
            return '({} {} {})'.format(res1, m['operation'], res2)
    elif isinstance(res2, str):
        # print('res2 of {} is str: {}'.format(monkey, res2))
        if True:  # 'humn' in res2:
            # print('humn contained in {} res2; res1 is {}'.format(monkey, res1))
            return '({} {} {})'.format(res1, m['operation'], res2)
    elif m['operation'] == '+':
        return res1 + res2
    elif m['operation'] == '-':
        return res1 - res2
    elif m['operation'] == '*':
        return res1 * res2
    elif m['operation'] == '/':
        return res1 / res2
    else:
        print('could not find operation for {}: {}'.format(monkey), m)



file1 = open('day21_input.txt', 'r')
Lines = file1.readlines()

# initial parsing
monkeys = {}
for n, l in enumerate(Lines):
    l = l.strip()
    op_match = re.match(OP_FMT, l)
    num_match = re.match(NUM_FMT, l)
    if op_match:
        monkey, op1, operation, op2 = op_match.groups()
        monkeys[monkey] = {
            'op1': op1, 'operation': operation, 'op2': op2
        }
    elif num_match:
        monkey, op1 = num_match.groups()
        monkeys[monkey] = {
            'op1': int(op1)
        }

# now find what humn must shout in order to make the root operations equal
root1, root2 = monkeys['root']['op1'], monkeys['root']['op2']
print('root1: {}'.format(calc(root1)))
print('root2: {}'.format(calc(root2)))


""" 
Below is attempt at a more "complete" solution using sympy.
But printing out the long equation above and then using an online
algebra solver to solve for humn works lol

# check which one is the long string containing humn...
equals_zero = None
if isinstance(root1, str):
    if "humn" in root1:
        equals_zero = root1 + ' - ' + root2
        equals_zero = equals_zero.replace('humn', 'x')
if isinstance(root2, str):
    if "humn" in root2:
        equals_zero = root2 + ' - ' + root1
        equals_zero = equals_zero.replace('humn', 'x')


x = symbols('x')
expr = equals_zero
sol = solve(expr)
print(sol)
"""







