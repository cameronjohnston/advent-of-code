
from dataclasses import dataclass

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
