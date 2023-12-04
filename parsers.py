
from dataclasses import dataclass
import os
import re
from typing import Union

from exceptions import ColourNotRecognizedException
from models import RGBGame, EnginePartCandidate, EngineSchematicSymbol

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
            # Each drawing will be separated by a semicolon
            for game_str in all_games.split(';'):
                colour_counts = {}

                # Each colour drawn in that drawing will be separated by a comma
                for rgb_str in game_str.split(','):
                    rgb_str = rgb_str.strip()  # remove leading spaces

                    # Each colour drawn will be indicated as <num> <colour>
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


class AOCEngineSchematicParser(AOCInputParser):
    def parse(self, input_file: Union[str, None] = None):
        lines = super().parse(input_file)
        candidates = []
        symbols = []
        for i, l in enumerate(lines):

            # Find numbers and create an EnginePartCandidate for each
            numbers_matches = re.finditer(r'(\d+)', l)
            for m in numbers_matches:
                epc = EnginePartCandidate(part_num=int(m.group()), row_num=i, start_pos=m.start())
                candidates.append(epc)

            # Find symbols and create an EngineSchematicSymbol for each
            # symbols_matches = re.finditer(r'([!@#$%^&*/\-\+=])', l)
            symbols_matches = re.finditer(r'(\D)', l)
            for m in symbols_matches:
                if m.group() not in ('\n', '.'):
                    # If we reached here, we have a non-digit, non-decimal, non-end-line. AKA a symbol

                    # Check if it's a negative sign part of a number ... if so, this isn't considered a symbol
                    # if m.group() in ('+', '-') and l[m.start() + 1].isdigit():
                    #     continue

                    ess = EngineSchematicSymbol(symbol=m.group(), row_num=i, start_pos=m.start())
                    symbols.append(ess)

            # Below was a non-regex attempt ... produced the same result
            # for j, c in enumerate(l):
            #     if not c.isdigit() and c not in ('.', '\n'):
            #         ess = EngineSchematicSymbol(symbol=c, row_num=i, start_pos=j)
            #         symbols.append(ess)

        # print(candidates)
        # print(symbols)
        return candidates, symbols


class DummyAOCInputParser(AOCInputParser):
    def parse(self, input_file: Union[str,None]=None):
        return ['Dummy input']


