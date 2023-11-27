import pandas as pd

file1 = open('day03_input.txt', 'r')
Lines = file1.readlines()


def char_to_priority(c):
    if c.isupper():
        return ord(c) - 38
    else:
        return ord(c) - 96


total = 0

for l in Lines:
    l = l.rstrip()
    half_length = len(l) / 2
    # print(half_length)
    left_side = l[0: int(half_length)]
    right_side = l[int(half_length):len(l)]
    shared = list(set(left_side) & set(right_side))
    total += char_to_priority(shared[0])

print(total)
