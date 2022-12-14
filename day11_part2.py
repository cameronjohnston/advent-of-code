import pandas as pd
from textwrap import wrap
import re

# constants
NUM_ROUNDS = 10000
CMDS = {
    'monkey': 'Monkey ([0-9]+):',
    'start': 'Starting items: ([^\n]+)',
    'op': 'Operation: new = old ([\+\-\*\/]+) ([^\s]+)',
    'test': 'Test: divisible by ([0-9]+)',
    'test_true': 'If true: throw to monkey ([0-9]+)',
    'test_false': 'If false: throw to monkey ([0-9]+)',
}

# classes
class Monkey(object):
    def __init__(self, number, starting_items=[], mod_items=[], op_func=None, operand=None, throw2_divisor=None, throw2_true=None, throw2_false=None):
        self.number = number
        self.starting_items = starting_items
        self.mod_items = mod_items
        self.op_func = op_func
        self.operand = operand
        self.throw2_divisor = throw2_divisor
        self.throw2_true = throw2_true
        self.throw2_false = throw2_false
        self.inspect_cnt = 0

    def append_item(self, item):
        self.mod_items.append(item)


class Item(object):
    """
    "mod_values" is the key for part 2. This list will represent not the actual worry level
    of each item, but the result of "worry level % throw2_divisor" for each monkey, in order,
    aka modulus values (mod_values).
    Constructor will serve 2 purposes:
    1. initialize mod_values based on the starting values
    2. update the mod_values, including reducing them by calculating the modulus of them
        for each monkey's throw2_divisor
    """
    def __init__(self, monkeys, val=None, mod_vals=None):
        if val:
            self.mod_values = []
            for _ in range(len(monkeys)):
                self.mod_values.append(val)
        if mod_vals:
            self.mod_values = []
            for n, mv in enumerate(mod_vals):
                self.mod_values.append(mv % monkeys[n].throw2_divisor)

file1 = open('day11_input.txt', 'r')
Lines = file1.readlines()

monkeys = []
monkey_num = 0

for _, l in enumerate(Lines):
    l = l.strip()

    monkey_match = re.match(CMDS['monkey'], l)
    if monkey_match:
        monkey_num = int(monkey_match.group(1)[0])
        monkeys.append(Monkey(monkey_num))

    start_match = re.match(CMDS['start'], l)
    if start_match:
        comma_sep_items = start_match.groups(1)[0]
        items = comma_sep_items.split(", ")
        items = list(map(int, items))
        monkeys[monkey_num].starting_items = items

    op_match = re.match(CMDS['op'], l)
    if op_match:
        operator, operand = op_match.groups()
        if str(operand) == 'old':
            if operator == '+':
                monkeys[monkey_num].op_func = lambda x, y: x + x
            if operator == '-':
                monkeys[monkey_num].op_func = lambda x, y: x - x
            if operator == '*':
                monkeys[monkey_num].op_func = lambda x, y: x * x
            if operator == '/':
                monkeys[monkey_num].op_func = lambda x, y: x / x
        else:
            monkeys[monkey_num].operand = int(operand[0])
            if operator[0] == '+':
                monkeys[monkey_num].op_func = lambda x, y: x + y
            if operator[0] == '-':
                monkeys[monkey_num].op_func = lambda x, y: x - y
            if operator[0] == '*':
                monkeys[monkey_num].op_func = lambda x, y: x * y
            if operator[0] == '/':
                monkeys[monkey_num].op_func = lambda x, y: x / y

    test_match = re.match(CMDS['test'], l)
    if test_match:
        divisor = int(test_match.groups(1)[0])
        monkeys[monkey_num].throw2_divisor = divisor

    true_match = re.match(CMDS['test_true'], l)
    if true_match:
        throw2_true = int(true_match.groups(1)[0])
        monkeys[monkey_num].throw2_true = throw2_true

    false_match = re.match(CMDS['test_false'], l)
    if false_match:
        throw2_false = int(false_match.groups(1)[0])
        monkeys[monkey_num].throw2_false = throw2_false

# initialize the "mod" values
for m in monkeys:
    m.mod_items = []
    for i in m.starting_items:
        new_item = Item(monkeys, val=i)
        m.mod_items.append(new_item)

# do the throwing
for r in range(NUM_ROUNDS):
    # start by reducing to each modulus value
    for m in monkeys:
        for n, i in enumerate(m.mod_items):
            # Item constructor will take care of reducing each value to appropriate modulus
            m.mod_items[n] = Item(monkeys, val=None, mod_vals=i.mod_values)

    for m in monkeys:
        monkey_num = m.number
        while len(m.mod_items):
            m.inspect_cnt += 1
            item = m.mod_items.pop(0)
            this_mod_val = item.mod_values[monkey_num]
            operands = []
            for _ in monkeys:
                operands.append(m.operand)
            item.mod_values = list(map(m.op_func, item.mod_values, operands))
            this_res = item.mod_values[monkey_num]
            if this_res % m.throw2_divisor:
                monkeys[m.throw2_false].append_item(item)
            else:
                monkeys[m.throw2_true].append_item(item)

# now the easy part ... find the answer!
inspect_cnts = []
for m in monkeys:
    inspect_cnts.append(m.inspect_cnt)
inspect_cnts.sort(reverse=True)
print(inspect_cnts[0] * inspect_cnts[1])
