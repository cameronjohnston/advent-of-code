
from dataclasses import dataclass
from typing import List


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
            if self.row_num-1 <= s.row_num <= self.row_num+1:
                if self.start_pos-1 <= s.start_pos <= self.end_pos+1:
                    print(f'TRUE: {self.part_num} on row {self.row_num}')
                    return True
        print(f'FALSE: {self.part_num} on row {self.row_num}')
        return False

@dataclass
class EngineSchematicSymbol:
    symbol: str
    row_num: int
    start_pos: int

    def __post_init__(self):
        self.length = len(str(self.symbol))
        self.end_pos = self.start_pos + self.length


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
