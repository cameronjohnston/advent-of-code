
from abc import ABC, abstractmethod
from dataclasses import dataclass

from parsers import AOCInputParser, DummyAOCInputParser
from timer import timeit

@dataclass
class AOCSolver(ABC):
    input_parser: AOCInputParser

    @timeit
    @abstractmethod
    def solve(self):
        pass

@dataclass
class StraightThruAOCSolver(AOCSolver):
    @timeit
    def solve(self):
        print(f'The file contains: {self.input_parser.parse()}')

@dataclass
class DummyAOCSolver(AOCSolver):
    input_parser: AOCInputParser = DummyAOCInputParser
    def solve(self):
        print('I am a dummy!')
        return


AOC_SOLVERS = {
    2022: {
        32: StraightThruAOCSolver(input_parser=AOCInputParser()),
        33: StraightThruAOCSolver(input_parser=AOCInputParser()),
    },
    2023: {}
}
