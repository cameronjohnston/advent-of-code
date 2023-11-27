import pandas as pd
from textwrap import wrap
import re
import numpy as np
from enum import Enum


# constants
MAX_COORDINATES = (1000, 1000)
ORIGIN = (500, 0)


# classes
class Point(Enum):
    AIR = 0
    ROCK = 1
    SAND = 2


file1 = open('day14_input.txt', 'r')
Lines = file1.readlines()

# initial parsing
max_y = 0
points = np.zeros(MAX_COORDINATES)
for i, l in enumerate(Lines):
    l = l.strip()
    pts = l.split(' -> ')
    for i, p in enumerate(pts):
        # print(p)
        x, y = p.split(',')
        x, y = int(x), int(y)
        if y > max_y:
            max_y = y
        if i == 0:
            points[x][y] = Point.ROCK.value
            continue
        else:
            prev_x, prev_y = pts[i-1].split(',')
            prev_x, prev_y = int(prev_x), int(prev_y)
            # assuming no diaginal lines, i.e. a rock line is either straight horizontal or vertical
            if prev_x < x:
                for n in range(prev_x, x + 1):
                    points[n][y] = Point.ROCK.value
            elif prev_x > x:
                for n in range(x, prev_x + 1):
                    points[n][y] = Point.ROCK.value
            elif prev_y < y:
                for n in range(prev_y, y + 1):
                    points[x][n] = Point.ROCK.value
            elif prev_y > y:
                for n in range(y, prev_y + 1):
                    points[x][n] = Point.ROCK.value

# now add the "floor" line:
for n in range(MAX_COORDINATES[0]):
    points[n][max_y + 2] = Point.ROCK
# print(points[500][12])
# print(points[499][13])
# print(points[500][13])
# print(points[501][13])
# print(points[502][9])

# now, do the sand-dropping
sand_cnt = 0
falling_forever = False
while not falling_forever:
    cur_x, cur_y = ORIGIN
    currently_falling = True
    while currently_falling:
        if cur_y == MAX_COORDINATES[1] - 1:
            falling_forever = True
            break
        # print('({}, {}: below is: {} {} {}'.format(cur_x, cur_y,
        #     points[cur_x - 1][cur_y + 1], points[cur_x][cur_y + 1], points[cur_x + 1][cur_y + 1]))
        if points[cur_x][cur_y + 1] == Point.AIR.value:
            cur_y += 1
        elif points[cur_x - 1][cur_y + 1] == Point.AIR.value:
            cur_x -= 1
            cur_y += 1
        elif points[cur_x + 1][cur_y + 1] == Point.AIR.value:
            cur_x += 1
            cur_y += 1
        else:
            currently_falling = False
            points[cur_x][cur_y] = Point.SAND.value
            sand_cnt += 1
            print('Sand stopped at ({}, {})'.format(cur_x, cur_y))

print(sand_cnt)
