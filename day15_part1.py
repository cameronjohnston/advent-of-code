import pandas as pd
from textwrap import wrap
import re
import numpy as np

# constants
INPUT_FMT = 'Sensor at x=([0-9]+), y=([0-9]+): closest beacon is at x=([0-9]+), y=([^\s]+)'
KEY_Y_COORD = 2000000 # we care about this row


# classes
class Sensor(object):
    def __init__(self, x, y, cb_x, cb_y):
        self.x, self.y, self.cb_x, self.cb_y = int(x), int(y), int(cb_x), int(cb_y)
        # print('new sensor: {} {} {} {}'.format(x, y, cb_x, cb_y))

    def get_taxicab_distance(self):
        return abs(self.x - self.cb_x) + abs(self.y - self.cb_y)


# functions


file1 = open('day15_input.txt', 'r')
Lines = file1.readlines()

# initial parsing
sensors = []
# below dicts are in backwards format [y-coord][x-coord], for ease of use in finding solution
empty_pts = {}  # these cannot contain a beacon
beacon_pts = {}  # track beacons points - will need to exclude these from the empty pts at the end
for i, l in enumerate(Lines):
    l = l.strip()
    m = re.match(INPUT_FMT, l)
    if m:
        sensor = Sensor(m.groups(1)[0], m.groups(1)[1], m.groups(1)[2], m.groups(1)[3])
        sensors.append(sensor)
        if sensor.cb_y not in beacon_pts:
            beacon_pts[sensor.cb_y] = [sensor.cb_x]
        elif sensor.cb_x not in beacon_pts[sensor.cb_y]:
            beacon_pts[sensor.cb_y].append(sensor.cb_x)

# now, fill in the points which cannot have a beacon:
for s in sensors:
    # print('processing sensor with x {}'.format(s.x))
    dist = s.get_taxicab_distance()

    for j in range(s.y - dist, s.y + dist + 1):
        if j != KEY_Y_COORD:
            continue # not necessary, but just to save a bit of time, lol
        j_to_y = abs(j - s.y)  # current y-coord (j) is this far from sensor's y-coord
        length = dist - j_to_y  # length (both left and right) for current y-coord, of the area which is empty
        min_x, max_x = s.x - length, s.x + length
        # print('sensor with x {}: {} {} {} {}'.format(s.x, j_to_y, length, min_x, max_x))
        if j not in empty_pts:
            empty_pts[j] = [[min_x, max_x]]
        else:
            empty_pts[j].append([min_x, max_x])

row = empty_pts[KEY_Y_COORD]

# below thanks to this person:
# https://leetcode.com/problems/merge-intervals/solutions/330282/python3-easy-solution-28s-beats-100/
row = sorted(row, key=lambda x: x[0])
res=[row[0]]
for i in range(1,len(row)):
    if res[-1][-1]>=row[i][0]:
        res[-1][-1]=max(res[-1][1],row[i][1])
    else:
        res.append(row[i])

# empty_coords = []
cnt = 0
for i, (x1, x2) in enumerate(res):
    length = x2 - x1 + 1
    cnt += length

# now, subtract any points which actually contain beacons:
if KEY_Y_COORD in beacon_pts:
    for x in beacon_pts[KEY_Y_COORD]:
        for _, (x1, x2) in enumerate(res):
            if x1 <= x <= x2:
                cnt -= 1 # this space actually has a beacon, so we should remove it from the "empty" cnt

print(cnt)
