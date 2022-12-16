import pandas as pd
from textwrap import wrap
import re
import numpy as np

# constants
INPUT_FMT = 'Sensor at x=([0-9]+), y=([0-9]+): closest beacon is at x=([0-9]+), y=([^\s]+)'
MAX_COORD = 4000000 # we care about this row


# classes
class Sensor(object):
    def __init__(self, x, y, cb_x, cb_y):
        self.x, self.y, self.cb_x, self.cb_y = int(x), int(y), int(cb_x), int(cb_y)
        # print('new sensor: {} {} {} {}'.format(x, y, cb_x, cb_y))

    def get_taxicab_distance(self):
        return abs(self.x - self.cb_x) + abs(self.y - self.cb_y)


# functions
def reduce_and_order(row):
    # below thanks to this person:
    # https://leetcode.com/problems/merge-intervals/solutions/330282/python3-easy-solution-28s-beats-100/
    row = sorted(row, key=lambda x: x[0])
    res=[row[0]]
    for i in range(1,len(row)):
        if res[-1][-1]>=row[i][0]:
            res[-1][-1]=max(res[-1][1],row[i][1])
        else:
            res.append(row[i])
    return res


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
        if j < 0 or j > MAX_COORD:
            continue  # save time - this point is irrelevant to the solution
        j_to_y = abs(j - s.y)  # current y-coord (j) is this far from sensor's y-coord
        length = dist - j_to_y  # length (both left and right) for current y-coord, of the area which is empty
        # since there are waaaaaay too many points to keep track of all of them ...
        # we will add entries to empty_pts[j] for start & end x-coords of each empty region,
        # where an empty region is a straight horizontal line
        min_x, max_x = s.x - length, s.x + length
        # print('sensor with x {}: {} {} {} {}'.format(s.x, j_to_y, length, min_x, max_x))
        if j not in empty_pts:
            empty_pts[j] = [[min_x, max_x]]
        else:
            empty_pts[j].append([min_x, max_x])

for j in empty_pts:
    res = empty_pts[j]
    res = reduce_and_order(res)
    # now search for the single point within requested range which is not definitely empty,
    # and therefore must contain the distress beacon:
    if res[0][0] > 0 or res[0][1] < MAX_COORD:
        # print('Distress beacon is in row {}: {}'.format(j, res))
        # sanity check: there should be exactly one value between the first and second start/end pairs:
        if res[1][0] - res[0][1] == 2:
            tuning_frequency = (res[0][1] + 1) * MAX_COORD + j
            print(tuning_frequency)
            break
        else:
            # highly unlikely we'd end up here ...
            print('Distress beacon is in row {}: {}'.format(j, res))

