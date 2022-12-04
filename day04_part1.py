import pandas as pd

file1 = open('day04_input.txt', 'r')
Lines = file1.readlines()


def line_to_assignments(line):
    s1, s2 = line.split(',')
    e1 = {
        'start': int(s1.split('-')[0]),
        'finish': int(s1.split('-')[1]),
    }
    e2 = {
        'start': int(s2.split('-')[0]),
        'finish': int(s2.split('-')[1]),
    }
    return e1, e2


total = 0

for l in Lines:
    l = l.rstrip()
    elf1, elf2 = line_to_assignments(l)
    if ((elf1['start'] >= elf2['start'] and elf1['finish'] <= elf2['finish'])
            or (elf2['start'] >= elf1['start'] and elf2['finish'] <= elf1['finish'])):
        total += 1

print(total)
