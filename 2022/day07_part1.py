import pandas as pd
from textwrap import wrap
import re

# constants
CMDS = {
    'ls': '\$ ls',
    'cd': '\$ cd ([^\s]+)',
    'dir': 'dir ([^\s]+)',
    'file': '([^\s]+) ([^\s]+)',
}


# classes
class File(object):
    def __init__(self, name, size, parent=None):
        self.name = name
        self.size = size
        self.parent = parent


class Directory(object):
    def __init__(self, name, parent=None, contents=None):
        if contents is None:
            contents = []
        self.name = name
        self.parent = parent
        self.contents = contents

    def add_content(self, c):  # c can be either a Directory or a File
        self.contents.append(c)

    def get_flattened_contents(self):  # gets all contents, including those any layers down
        all_contents = []
        for c in self.contents:
            all_contents.append(c)
            if isinstance(c, Directory):
                all_contents += c.get_flattened_contents()
        return all_contents

    def get_size(self):
        total_size = 0
        for c in self.contents:
            if isinstance(c, Directory):
                total_size += c.get_size()
            elif isinstance(c, File):
                total_size += c.size
        return total_size


file1 = open('day07_input.txt', 'r')
Lines = file1.readlines()

# sort of a hack... create a non-existent directory one level above the top level dir.
# this ensures we can have this dir to always refer back to while guaranteeing that
# it only ever contains one item: the actual top level dir.
above_top_level_dir = Directory('top_level')
curr_dir = Directory('/', above_top_level_dir)
above_top_level_dir.add_content(curr_dir)
for i, l in enumerate(Lines):
    l = l.strip()
    if re.match(CMDS['ls'], l):
        # loop until finding the next line starting with $ (or end-of-file), and
        # parse in subdirectories and files as contents of this directory
        j = i
        while j < len(Lines) - 1:
            j += 1
            ls_output_line = Lines[j]
            if ls_output_line[0] == '$':
                break
            if re.match(CMDS['dir'], ls_output_line):
                # create new directory within the current one
                match = re.match(CMDS['dir'], ls_output_line)
                d = Directory(match.group(1), curr_dir)
                curr_dir.add_content(d)
            elif re.match(CMDS['file'], ls_output_line):
                # create new file within the current one
                match = re.match(CMDS['file'], ls_output_line)
                f = File(match.group(2), int(match.group(1)), curr_dir)
                curr_dir.add_content(f)
    if re.match(CMDS['cd'], l):
        match = re.match(CMDS['cd'], l)
        target_dir = match.group(1)
        if target_dir == '/':
            curr_dir = above_top_level_dir.contents[0]  # top level dir
            continue
        if target_dir == '..':  # go up a level
            curr_dir = curr_dir.parent
            continue
        # if we made it here, it means we have to find the directory with desired name,
        # so that we can assign it as the curr_dir:
        for c in curr_dir.contents:
            if isinstance(c, Directory):
                if c.name == target_dir:
                    curr_dir = c
                    break

# now that we've parsed everything ... the easy part: getting the answer!
small_dirs = []  # Directories which are under the threshold
grand_total_size = 0
flattened_contents = above_top_level_dir.get_flattened_contents()
for c in flattened_contents:
    if isinstance(c, Directory):
        size = c.get_size()
        if size <= 100000:
            small_dirs.append(c)
            grand_total_size += size

print(grand_total_size)
