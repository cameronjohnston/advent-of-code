import pandas as pd
from textwrap import wrap
import re
from dijkstar import Graph, find_path


# constants


# classes
class Height(object):
    def __init__(self, c, x, y):
        self.char = c
        if c == 'S':
            self.char = 'a'
        if c == 'E':
            self.char = 'z'
        self.ascii = ord(self.char)
        self.val = x * 100 + y


file1 = open('day12_input.txt', 'r')
Lines = file1.readlines()

# initial parsing
heights = []
start_val = end_val = 0
for i, l in enumerate(Lines):
    l = l.strip()
    row = []
    for j, c in enumerate(l):
        h = Height(c, i, j)
        row.append(h)
        if c == 'S':
            start_val = h.val
        if c == 'E':
            end_val = h.val
    heights.append(row)

# now, build the graph
graph = Graph()
for i, row in enumerate(heights):
    for j, h in enumerate(row):
        # check if each neighbour is reachable. If so, add the edge
        if i > 0:
            if heights[i - 1][j].ascii - h.ascii < 2:
                graph.add_edge(h.val, heights[i - 1][j].val, 1)
        if i < len(heights) - 1:
            if heights[i + 1][j].ascii - h.ascii < 2:
                graph.add_edge(h.val, heights[i + 1][j].val, 1)
        if j > 0:
            if heights[i][j - 1].ascii - h.ascii < 2:
                graph.add_edge(h.val, heights[i][j - 1].val, 1)
        if j < len(row) - 1:
            if heights[i][j + 1].ascii - h.ascii < 2:
                graph.add_edge(h.val, heights[i][j + 1].val, 1)

# now the easy part ... find the answer!
path_info_res = find_path(graph, start_val, end_val)
print(path_info_res.total_cost)
