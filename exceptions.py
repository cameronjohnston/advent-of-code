
from dataclasses import dataclass

@dataclass
class ColourNotRecognizedException(Exception):
    colour: str

    def __str__(self):
        return f'Unrecognized colour: {self.colour}'

