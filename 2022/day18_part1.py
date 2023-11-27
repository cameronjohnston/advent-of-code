import pandas as pd
from textwrap import wrap
import re
import numpy as np
from enum import Enum


# constants


# classes


# functions



file1 = open('day18_input.txt', 'r')
Lines = file1.readlines()

# initial parsing
pts = {}
for n, l in enumerate(Lines):
    l = l.strip()
    i, j, k = int(l.split(',')[0]), int(l.split(',')[1]), int(l.split(',')[2])
    # add to dict
    if i not in pts:
        pts[i] = {j: {k: 6}}
    elif j not in pts[i]:
        pts[i][j] = {k: 6}
    elif k not in pts[i][j]:
        pts[i][j][k] = 6
    # now update neighbours, plus this new entry
    for x in (i-1, i+1):
        if x in pts:
            if j in pts[x]:
                if k in pts[x][j]:
                    pts[x][j][k] -= 1  # because now there is a new face which is covered
                    pts[i][j][k] -= 1  # and also this face of new point is covered
    for y in (j-1, j+1):
        if y in pts[i]:
            if k in pts[i][y]:
                pts[i][y][k] -= 1  # because now there is a new face which is covered
                pts[i][j][k] -= 1  # and also this face of new point is covered
    for z in (k-1, k+1):
        if z in pts[i][j]:
            pts[i][j][z] -= 1  # because now there is a new face which is covered
            pts[i][j][k] -= 1  # and also this face of new point is covered

# now the easy part ... find the answer!
total_faces_showing = 0
for x in pts:
    for y in pts[x]:
        for z in pts[x][y]:
            total_faces_showing += pts[x][y][z]

print(total_faces_showing)




