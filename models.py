
from dataclasses import dataclass
from typing import List


@dataclass
class RGBGame:
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
class Digit:
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
