import pandas as pd
from textwrap import wrap
import re
import numpy as np
from enum import Enum


# constants
OP_FMT = '([^\s]+): ([^\s]+) ([\+\-\*\/]+) ([^\s]+)'
NUM_FMT = '([^\s]+): ([0-9]+)'


# classes


# functions
def calc(monkey):
    m = monkeys[monkey]
    if 'operation' not in m:
        return m['op1']
    elif m['operation'] == '+':
        return calc(m['op1']) + calc(m['op2'])
    elif m['operation'] == '-':
        return calc(m['op1']) - calc(m['op2'])
    elif m['operation'] == '*':
        return calc(m['op1']) * calc(m['op2'])
    elif m['operation'] == '/':
        return calc(m['op1']) / calc(m['op2'])
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

# now find what root shouts
print(calc('root'))






