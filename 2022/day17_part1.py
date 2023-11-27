import pandas as pd
from textwrap import wrap
import re
import numpy as np
from enum import Enum


# constants
INPUT_FMT = ''
WIDTH = 7
BUFFER_ROWS = 3
NUM_ROCKS = 2022


# classes
class Rock(object):
    def __init__(self, rock_num, bl_loc):
        if rock_num % 5 == 1:
            self.shape = np.ones((1, 4))
        if rock_num % 5 == 2:
            self.shape = np.concatenate((np.array([[0, 1, 0]]), np.ones((1, 3)), np.array([[0, 1, 0]])))
        if rock_num % 5 == 3:
            self.shape = np.concatenate((np.ones((1, 3)), np.array([[0, 0, 1]]), np.array([[0, 0, 1]])))
        if rock_num % 5 == 4:
            self.shape = np.ones((4, 1))
        if rock_num % 5 == 0:
            self.shape = np.ones((2, 2))
        self.bl_loc = bl_loc  # location of bottom-left corner

    def can_move(self, direction, points):
        for i, p in np.ndenumerate(self.shape):
            if not p:
                continue  # empty space in the rock - does not affect whether it can move
            # print(self.bl_loc)
            # print(i)
            # print(self.shape)
            x = self.bl_loc[1] + i[1]
            y = self.bl_loc[0] + i[0]
            if direction == '<':
                if points[y, x - 1]:
                    return False  # something solid is to the left
            if direction == '>':
                if points[y, x + 1]:
                    return False  # something solid is to the right
            if direction == 'v':
                if points[y - 1, x]:
                    return False  # something solid is below
        return True  # if we made it here, there is no point obstructing the rock & direction

    def move(self, direction):
        if direction == '<':
            self.bl_loc = [self.bl_loc[0], self.bl_loc[1] - 1]
        if direction == '>':
            self.bl_loc = [self.bl_loc[0], self.bl_loc[1] + 1]
        if direction == 'v':
            self.bl_loc = [self.bl_loc[0] - 1, self.bl_loc[1]]

    def add_to_pts(self, points, max_h):
        for i, p in np.ndenumerate(self.shape):
            if p:  # avoid overwriting a pre-existing rock with air in this rock's area!
                points[self.bl_loc[0] + i[0], self.bl_loc[1] + i[1]] = p
            # print('max_h: {}; bl_loc: {}; self.shape: {}'.format(max_h, self.bl_loc, self.shape))
        return points, max(max_h, self.bl_loc[0] + np.size(self.shape, 0) - 1)


# functions



file1 = open('day17_input.txt', 'r')
Lines = file1.readlines()

# initial parsing
for i, l in enumerate(Lines):
    l = l.strip()
    n = 0  # index in input which contains the next jet direction
    rock_cnt = max_height = 0
    pts = np.full((1, 9), 1)  # start with just the floor ... it'll be extended just below
    # insert v's to represent downward moves between jet streams
    i = 1
    while i < len(l) + 1:
        l = l[:i] + 'v' + l[i:]
        i += 2
    # print(l)
    while rock_cnt < NUM_ROCKS:
        rock_cnt += 1
        # a rock will always start with jetstream movement (i.e. > or <, not v)
        while l[n] == 'v':
            n += 1
        # supplement existing space with higher walls
        while np.size(pts, 0) <= max_height + 7:
            pts = np.concatenate((pts, np.array([[1, 0, 0, 0, 0, 0, 0, 0, 1]])))
        # print(pts)
        new_bl_loc = [max_height + 4, 3]  # new rock appears after 3 empty rows + 2 empty spaces to its left
        # print('Rock {}: bl_loc {}'.format(rock_cnt, new_bl_loc))
        r = Rock(rock_cnt, new_bl_loc)
        while True:
            if r.can_move(l[n], pts):
                r.move(l[n])
                # print('Rock {} moved {}. bl_loc {}'.format(rock_cnt, l[n], r.bl_loc))
            elif l[n] == 'v':
                break
            else:
                # print('Cannot move {}'.format(l[n]))
                pass
            # increment to next char
            if n == len(l) - 1:
                # print('---- reached end of chars ----')
                n = 0
            else:
                n += 1
        pts, max_height = r.add_to_pts(pts, max_height)
        # print(pts)
        # print('End of rock {}, max_height: {}'.format(rock_cnt, max_height))
    print(max_height)


