import pandas as pd
from textwrap import wrap
import re

# constants
CMD = '([^\s]+) ([^\s]+)'

# classes


file1 = open('day09_input.txt', 'r')
Lines = file1.readlines()


def move_h(h_loc, direction):
    if direction == 'L':
        return (h_loc[0] - 1, h_loc[1])
    if direction == 'U':
        return (h_loc[0], h_loc[1] + 1)
    if direction == 'R':
        return (h_loc[0] + 1, h_loc[1])
    if direction == 'D':
        return (h_loc[0], h_loc[1] - 1)


def move_t(h_loc, t_loc):
    new_t_loc = ()
    move_x = move_y = 0
    if h_loc[0] < t_loc[0]:
        move_x = -1
    if h_loc[0] > t_loc[0]:
        move_x = 1
    if h_loc[1] < t_loc[1]:
        move_y = -1
    if h_loc[1] > t_loc[1]:
        move_y = 1
    if abs(h_loc[0] - t_loc[0]) < 2 and abs(h_loc[1] - t_loc[1]) < 2:
        return t_loc
    else:
        return [t_loc[0] + move_x, t_loc[1] + move_y]


h_loc = t_loc = [0, 0]
t_loc_history = [t_loc]
for i, l in enumerate(Lines):
    l = l.strip()
    match = re.match(CMD, l)
    direction, num_moves = match.groups()
    for _ in range(int(num_moves)):
        h_loc = move_h(h_loc, direction)
        t_loc = move_t(h_loc, t_loc)
        if t_loc not in t_loc_history:
            t_loc_history.append(t_loc)

print(len(t_loc_history))

