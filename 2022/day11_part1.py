import pandas as pd
from textwrap import wrap
import re

# constants
NUM_ROUNDS = 20
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
    def __init__(self, number, items=None, op_func=None, operand=None, throw2_divisor=None, throw2_true=None, throw2_false=None):
        self.number = number
        self.items = items
        self.op_func = op_func
        self.operand = operand
        self.throw2_divisor = throw2_divisor
        self.throw2_true = throw2_true
        self.throw2_false = throw2_false
        self.inspect_cnt = 0

    def append_item(self, item):
        self.items.append(item)


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
        monkeys[monkey_num].items = items

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

# do the throwing
for _ in range(NUM_ROUNDS):
    for m in monkeys:
        monkey_num = m.number
        while len(m.items):
            m.inspect_cnt += 1
            item = int(m.items.pop(0))
            res = m.op_func(item, m.operand)
            old_w = int(res)
            new_w = int(old_w / 3)
            if new_w % m.throw2_divisor:
                monkeys[m.throw2_false].append_item(new_w)
            else:
                monkeys[m.throw2_true].append_item(new_w)

# now the easy part ... find the answer!
inspect_cnts = []
for m in monkeys:
    inspect_cnts.append(m.inspect_cnt)
inspect_cnts.sort(reverse=True)
print(inspect_cnts[0] * inspect_cnts[1])
