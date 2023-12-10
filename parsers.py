
from dataclasses import dataclass
import os
import re
from typing import Union

from exceptions import ColourNotRecognizedException
from models import (RGBGame, EnginePartCandidate, EngineSchematicSymbol
    , ScratchCard, AlmanacMap, AlmanacMapRange, Range, BoatRace
    , PokerHand, PokerHandWithJackAsJoker
)

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


class AOCScratchCardParser(AOCInputParser):
    def parse(self, input_file: Union[str, None] = None):
        lines = super().parse(input_file)
        cards = []
        for l in lines:
            card_with_id, all_nums_str = l.split(':')
            print(card_with_id)
            id = int(re.match(r'Card[ ]+([\d]+)', card_with_id).groups()[0])
            winning_nums_str, my_nums_str = all_nums_str.split('|')
            winning_nums = [int(num) for num in winning_nums_str.split(' ') if len(num)]
            my_nums = [int(num) for num in my_nums_str.split(' ') if len(num)]
            card = ScratchCard(id, winning_nums, my_nums)
            cards.append(card)
        return cards


class AOCAlmanacParser(AOCInputParser):
    def parse(self, input_file: Union[str, None] = None):
        lines = super().parse(input_file)
        almanac_maps = []
        for l in lines:
            # Expected to be first line
            if 'seeds:' in l:
                print(f'Parsing line {l}')
                seeds_str = l.split(':')[1]
                print(f'Parsing seeds: {seeds_str}')
                seeds = [int(s) for s in seeds_str.split(' ') if len(s)]
                seed_range_pairs = [(seeds[i], seeds[i+1]) for i in range(0, len(seeds), 2)]
                seed_ranges = [Range(p[0], p[0]+p[1]-1) for p in seed_range_pairs]
                source, destination = None, None

            # Blank lines: add new AlmanacMap, then skip this line
            if len(l) < 2:
                if source is not None:
                    almanac_map = AlmanacMap(source, destination, map_ranges)
                    almanac_maps.append(almanac_map)
                source = destination = None
                continue

            # Search for matches to new map header
            map_match = re.match(r'([a-zA-Z]+)-to-([a-zA-Z]+) map:', l)
            if map_match:
                source, destination = map_match.groups()
                map_ranges = []

            values_match = re.match(r'([\d]+) ([\d]+) ([\d]+)', l)
            if values_match:
                destination_start, source_start, length = tuple(int(x) for x in values_match.groups())
                map_ranges.append(AlmanacMapRange(source_start, source_start+length-1, destination_start-source_start))

        # After all lines: need to add the final AlmanacMap
        almanac_map = AlmanacMap(source, destination, map_ranges)
        almanac_maps.append(almanac_map)

        # Done parsing. Return seeds and AlmanacMaps
        # ... and seed_ranges, because hooray for pt2 requiring different parsing!
        print(f'Done parsing. {seeds}; {almanac_maps}; {seed_ranges}')
        return seeds, almanac_maps, seed_ranges


class AOCBoatRaceParser(AOCInputParser):
    def parse(self, input_file: Union[str, None] = None):
        lines = super().parse(input_file)
        races = []
        for l in lines:
            parts = l.split(':')
            print(f'Found {parts}')
            if parts[0] == 'Time':
                times = parts[1].split()
            elif parts[0] == 'Distance':
                distances = parts[1].split()

        # Now we should have times and distances
        print(f'{times}; {distances}')
        concatenated_times = concatenated_distances = ''
        for i in range(len(times)):
            race = BoatRace(int(times[i]), int(distances[i]))
            races.append(race)
            concatenated_times += times[i]
            concatenated_distances += distances[i]

        return races, BoatRace(int(concatenated_times), int(concatenated_distances))


class AOCPokerHandParser(AOCInputParser):
    def parse(self, input_file: Union[str, None] = None):
        lines = super().parse(input_file)
        hands = []
        hands_with_jokers = []
        for l in lines:
            cards_str, bid_str = l.split(' ')
            hand = PokerHand(cards_str, int(bid_str))
            hands.append(hand)
            print(f'About to create PokerHandWithJackAsJoker from {cards_str}')
            hand_with_jokers = PokerHandWithJackAsJoker(cards_str, int(bid_str))
            print(f'Appending {hand_with_jokers}')
            hands_with_jokers.append(hand_with_jokers)

        print(f'===== Done parsing')
        return hands, hands_with_jokers


class DummyAOCInputParser(AOCInputParser):
    def parse(self, input_file: Union[str,None]=None):
        return ['Dummy input']


