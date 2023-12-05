
from dataclasses import dataclass
from typing import List, Tuple



@dataclass
class Digit:  # 2023 day 1
    text: str
    value: int

    @classmethod
    def digits(cls):
        return [
            cls('zero', 0), cls('one', 1), cls('two', 2), cls('three', 3), cls('four', 4),
            cls('five', 5), cls('six', 6), cls('seven', 7), cls('eight', 8), cls('nine', 9)
        ]

    @classmethod
    def get_digits(cls, string: str):
        ordered_digit_values = []
        for i in range(len(string)):
            for d in cls.digits():
                if string[i] == str(d.value) or string[i:i+len(d.text)] == d.text:
                    ordered_digit_values.append(d.value)
        return ordered_digit_values


@dataclass
class RGBGame:  # 2023 day 2
    id: int
    drawings: List[dict]

    def is_possible(self, max_counts: dict):
        for colour in self.__class__.colour_strings():
            for colour_counts in self.drawings:
                if colour in colour_counts and colour in max_counts:
                    if colour_counts[colour] > max_counts[colour]:
                        return False
        return True

    def min_balls_possible(self):
        min_for_colours = {}
        for colour in self.__class__.colour_strings():
            this_colour_counts = [
                d[colour] for d in self.drawings if colour in d
            ]
            min_for_colour = max(this_colour_counts)
            min_for_colours[colour] = min_for_colour
        return min_for_colours

    @classmethod
    def colour_strings(cls):
        return 'red', 'green', 'blue'


@dataclass
class EngineSchematicSymbol:
    symbol: str
    row_num: int
    start_pos: int

    def __post_init__(self):
        self.length = len(str(self.symbol))
        self.end_pos = self.start_pos + self.length


@dataclass
class EnginePartCandidate:
    part_num: int
    row_num: int
    start_pos: int

    def __post_init__(self):
        self.length = len(str(self.part_num))
        self.end_pos = self.start_pos + self.length

    def is_part(self, symbols):
        for s in symbols:
            if self.is_adjacent(s):
                return True
        return False

    def is_adjacent(self, s: EngineSchematicSymbol):
        if self.row_num-1 <= s.row_num <= self.row_num+1:
            if self.start_pos-1 <= s.start_pos <= self.end_pos:
                # print(f'TRUE: {self.part_num} row {self.row_num}:{self.start_pos}-{self.end_pos}; Symbol {s.symbol} {s.row_num}:{s.start_pos}')
                return True
        return False


@dataclass
class ScratchCard:
    id: int
    winning_nums: List[int]
    my_nums: List[int]

    def count_matches(self):
        matches = [n for n in self.my_nums if n in self.winning_nums]
        return len(matches)


@dataclass
class AlmanacMapRange:
    source_start: int
    destination_start: int
    length: int

    def get_destination_value(self, source_value):
        if self.source_start <= source_value < self.source_start + self.length:
            return source_value + (self.destination_start - self.source_start)
        return None  # There is no matching value

@dataclass
class AlmanacMap:
    source: str
    destination: str
    ranges: List[AlmanacMapRange]

    def get_destination_value(self, source_value):
        for r in self.ranges:
            destination_value = r.get_destination_value(source_value)
            if destination_value:
                return destination_value
        return source_value

@dataclass
class AlmanacSeed:
    start: int
    end: int
