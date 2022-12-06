import pandas as pd
from textwrap import wrap
import re

file1 = open('day06_input.txt', 'r')
Lines = file1.readlines()

pos = 0
recent_chars = []

for l in Lines:
    l = l.strip()
    for pos in range(len(l)):
        four_chars = l[pos:pos+4]
        if len(set(four_chars)) == len(four_chars):
            print(four_chars)
            print(pos+4)
            break


