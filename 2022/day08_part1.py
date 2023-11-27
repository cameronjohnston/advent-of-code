import pandas as pd
from textwrap import wrap
import re

# constants


# classes
class Tree(object):
    def __init__(self, height, neighbours=None):
        if neighbours is None:
            neighbours = {'left': [], 'above': [], 'right': [], 'below': []}
        self.height = height
        self.neighbours = neighbours

    def add_neighbour(self, direction, neighbour_height=0):
        self.neighbours[direction].append(neighbour_height)

    def is_visible(self, direction=None):
        if direction:
            return all(neighbour_height < self.height for neighbour_height in self.neighbours[direction])
        else:
            # for d in self.neighbours:
            #     if not all(self.neighbours[d][loc] < self.height for loc in self.neighbours[d]):
            #         return False
            # return True
            # for d in self.neighbours:
            #     if all(neighbour_height < self.height for neighbour_height in self.neighbours[d]):
            #         return
            return any(
                all(neighbour_height < self.height for neighbour_height in self.neighbours[direction])
                for direction in self.neighbours
            )


file1 = open('day08_input.txt', 'r')
Lines = file1.readlines()

trees = [] # 2d array of Trees

for i, l in enumerate(Lines):
    l = l.strip()
    trees.append([])
    for j, c in enumerate(l):
        height = int(c)
        new_tree = Tree(height)
        # add neighbours to new tree:
        # its neighbours will always be left & above due to order of parsing
        # also add new tree to neighbours (new tree will always be right & below)
        for k in range(j):
            new_tree.add_neighbour('left', trees[i][k].height)
            trees[i][k].add_neighbour('right', height)
        for k in range(i):
            new_tree.add_neighbour('above', trees[k][j].height)
            trees[k][j].add_neighbour('below', height)
        trees[i].append(new_tree)

# now the easy part ... find the answer!
visible_cnt = 0
for r in trees:
    for t in r:
        if t.is_visible():
            visible_cnt += 1

print(visible_cnt)
