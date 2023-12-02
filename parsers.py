
from dataclasses import dataclass
import os
import re
from typing import Union

from exceptions import ColourNotRecognizedException
from models import RGBGame

@dataclass
class InputFileFinder:
    input_path: str = os.path.join(os.path.dirname(__file__), 'input')
    ext: str = 'txt'
    year: int = 0
    day: int = 0

    def __post_init__(self):

        # If year is still 0, populate it with latest
        if not self.year:
            dirs = [d for d in os.listdir(self.input_path) if not os.path.isfile(d)]
            relevant_dirs = [int(d) for d in dirs if d.isdigit()]
            self.year = max(relevant_dirs)

        # # If day is still 0, populate it with latest
        # if not self.day:
        #     year_path = os.path.join(self.input_path, str(self.year))
        #     relevant_files = [int(f.split('.'[0])) for f in os.walk(self.year_path)[2]
        #                         if f.split('.'[0]).isdigit() and f.split('.'[1]) == self.ext
        #                       ]
        #     self.day = max(relevant_files)

        # If day is still 0, populate it with latest
        if not self.day:
            year_dir = os.path.join(self.input_path, str(self.year))
            files = [int(f.split('.')[0]) for f in os.listdir(year_dir) if 1==1
                        # and os.path.isfile(f)
                        and f.split('.')[1] == self.ext
                        and f.split('.')[0].isdigit()
                     ]
            # relevant_files = [f for f in files if f.endswith(self.ext) and ]
            self.day = max(files)

    def get(self):
        return os.path.join(self.input_path, str(self.year), f'{self.day}.{self.ext}')

@dataclass
class AOCInputParser:
    year: int = 0
    day: int = 0

    # Default parse: return the file lines as a list of str's
    def parse(self, input_file: Union[str,None]=None):
        if input_file is None:
            input_file = InputFileFinder(year=self.year, day=self.day).get()
        f = open(input_file, 'r')
        lines = f.readlines()
        return lines

class AOCRGBGameParser(AOCInputParser):
    def parse(self, input_file: Union[str, None] = None):
        lines = super().parse(input_file)
        games = []
        for l in lines:
            game_with_id, all_games = l.split(':')

            # Get ID
            id = int(re.match(r'Game ([\d]+)', game_with_id).groups()[0])

            # Get drawings
            drawings = []
            for game_str in all_games.split(';'):
                colour_counts = {}
                game_rgb_strs = game_str.split(',')
                for rgb_str in game_rgb_strs:
                    rgb_str = rgb_str.strip()
                    num, colour = re.match(r'([\d]+) ([\w]+)', rgb_str).groups()
                    if colour in RGBGame.colour_strings():
                        colour_counts[colour] = int(num)
                    else:
                        raise ColourNotRecognizedException(colour=colour)

                # Now we have a colour_counts dict representing a drawing. Append to the drawings:
                drawings.append(colour_counts)

            # Create the game and append
            game = RGBGame(id=id, drawings=drawings)
            games.append(game)

        return games


class DummyAOCInputParser(AOCInputParser):
    def parse(self, input_file: Union[str,None]=None):
        return ['Dummy input']


