
from abc import ABC, abstractmethod
from dataclasses import dataclass

from models import Digit
from parsers import AOCInputParser, DummyAOCInputParser
from timer import timeit

@dataclass
class AOCSolver:
    input_parser: AOCInputParser

    def solve(self):
        parsed = self.input_parser.parse()
        if hasattr(self, 'solve_part1'):
            print('Solving part 1...')
            part1_sol = self.solve_part1(parsed)
            print(f'Part 1 solution: {part1_sol}')
        if hasattr(self, 'solve_part2'):
            print('Solving part 2...')
            part2_sol = self.solve_part2(parsed)
            print(f'Part 2 solution: {part2_sol}')

@dataclass
class StraightThruAOCSolver(AOCSolver):
    @timeit
    def solve_part1(self, parsed):
        print(f'Part1: the file contains: {parsed}')

    @timeit
    def solve_part2(self, parsed):
        print(f'Part2: the file contains: {parsed}')


class AOC2023Day1Solver(AOCSolver):

    def sum_two_digit_numbers(self, digits):
        print(f'Digits: {digits}')
        two_digit_nums = [
            line_digits[0] * 10 + line_digits[len(line_digits)-1]
            for line_digits in digits
        ]
        print(f'two_digit_nums: {two_digit_nums}')
        sum_of_nums = sum(two_digit_nums)
        print(f'Sum of nums is {sum_of_nums}')
        return sum_of_nums

    @timeit
    def solve_part1(self, parsed):
        digits = [
            [int(c) for c in line if c.isdigit()]
            for line in parsed
        ]
        return self.sum_two_digit_numbers(digits)

    @timeit
    def solve_part2(self, parsed):
        digits_in_lines = [
            Digit.get_digits(l) for l in parsed
        ]
        return self.sum_two_digit_numbers(digits_in_lines)


AOC_SOLVERS = {
    2022: {
        32: [StraightThruAOCSolver(AOCInputParser(2022, 32))],
        33: [StraightThruAOCSolver(AOCInputParser(2022, 32)),
             StraightThruAOCSolver(AOCInputParser(2022, 32))],
    },
    2023: {
        1: [AOC2023Day1Solver(AOCInputParser(2023, 1))]
    }
}
