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

    def add_neighbour(self, direction, neighbour_height=0, insert=False):
        if insert:
            self.neighbours[direction].insert(0, neighbour_height)
        else:
            self.neighbours[direction].append(neighbour_height)

    def is_visible(self, direction=None):
        if direction:
            return all(neighbour_height < self.height for neighbour_height in self.neighbours[direction])
        else:
            return any(
                all(neighbour_height < self.height for neighbour_height in self.neighbours[direction])
                for direction in self.neighbours
            )

    def get_scenic_score(self, debug=False):
        scenic_score = 1
        for d in self.neighbours:
            this_dir_score = 0
            for n in self.neighbours[d]:
                this_dir_score += 1
                if n >= self.height:
                    break
            if this_dir_score > 0:
                scenic_score *= this_dir_score
        return scenic_score


file1 = open('day08_input.txt', 'r')
Lines = file1.readlines()

trees = [] # 2d list of Trees

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
            # inserting at the start of the list (asot appending to the end) ensures that
            # we will end up with the closest neighbour trees at the start
            new_tree.add_neighbour('left', trees[i][k].height, insert=True)
            trees[i][k].add_neighbour('right', height)
        for k in range(i):
            new_tree.add_neighbour('above', trees[k][j].height, insert=True)
            trees[k][j].add_neighbour('below', height)
        trees[i].append(new_tree)

# now the easy part ... find the answer!
best_scenic_score = 0
for r in trees:
    for t in r:
        s = t.get_scenic_score()
        if s > best_scenic_score:
            best_scenic_score = s

print(best_scenic_score)
