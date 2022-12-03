import pandas as pd

file1 = open('day03_input.txt', 'r')
Lines = file1.readlines()


def char_to_priority(c):
    if c.isupper():
        return ord(c) - 38
    else:
        return ord(c) - 96


total = 0

three_lines = []

for l in Lines:
    l = l.rstrip()
    three_lines.append(l)
    if len(three_lines) == 3:
        shared = list(set(three_lines[0]) & set(three_lines[1]))
        print(shared)
        shared = list(set(three_lines[2]) & set(shared))
        print(shared)
        total += char_to_priority(shared[0])
        three_lines = []

print(total)
