
from abc import ABC, abstractmethod
from dataclasses import dataclass
import time

from models import Digit
from parsers import (AOCInputParser, DummyAOCInputParser
    , AOCRGBGameParser
    , AOCEngineSchematicParser
    , AOCScratchCardParser
    , AOCAlmanacParser
                     )
from timer import timeit

@dataclass
class AOCSolver:
    input_parser: AOCInputParser

    def solve(self):
        try:
            parsed = self.input_parser.parse()
        except Exception as e:
            print(f'Found {e.__class__.__name__} during parsing: {e}')
            return

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


class AOC2023Day2Solver(AOCSolver):
    @timeit
    def solve_part1(self, parsed):
        total = 0
        for game in parsed:
            if game.is_possible({
                'red': 12, 'green': 13, 'blue': 14
            }):
                total += game.id
        return total

    @timeit
    def solve_part2(self, parsed):
        total = 0
        for game in parsed:
            multiplied = 1
            for v in (game.min_balls_possible()).values():
                multiplied *= v
            # print(f'ID {game.id} multiplied is {multiplied}')
            total += multiplied
        return total


class AOC2023Day3Solver(AOCSolver):
    @timeit
    def solve_part1(self, parsed):
        candidates, symbols = parsed
        total = 0
        for c in candidates:
            if c.is_part(symbols):
                total += c.part_num
        return total

    @timeit
    def solve_part2(self, parsed):
        candidates, symbols = parsed
        total = 0
        for s in symbols:
            if s.symbol != '*':
                print(f'Skipping {s.symbol}')
                continue
            adj_cnt = 0
            multiply_result = 1
            for c in candidates:
                if c.is_adjacent(s):
                    adj_cnt += 1
                    multiply_result *= c.part_num
            if adj_cnt == 2:
                print(f'FOUND: {s.symbol} {s.row_num}:{s.start_pos}')
                total += multiply_result
            else:
                print(f'FALSE: {s.symbol} {s.row_num}:{s.start_pos}')
        return total


class AOC2023Day4Solver(AOCSolver):
    @timeit
    def solve_part1(self, parsed):
        total = 0
        for card in parsed:
            winning_nums_cnt = card.count_matches()
            if winning_nums_cnt:
                total += pow(2, winning_nums_cnt-1)
        return total

    @timeit
    def solve_part2(self, parsed):
        won_cards = []
        print(f'Starting with {len(parsed)} cards')
        for i, card in enumerate(parsed):
            winning_nums_cnt = card.count_matches()
            print(f'{card.id} has {winning_nums_cnt} wins')
            if winning_nums_cnt:
                copies_of_this = len([c for c in won_cards if c.id == card.id])
                for j in range(i+1, i+1+winning_nums_cnt):
                    print(f'Adding {copies_of_this+1} cards of {parsed[j].id}')
                    for _ in range(copies_of_this+1):
                        won_cards.append(parsed[j])

        return len(parsed) + len(won_cards)


class AOC2023Day5Solver(AOCSolver):
    @timeit
    def solve_part1(self, parsed):
        seeds, almanac_maps = parsed
        print(almanac_maps)
        source, destination = 'seed', None
        values = {
            'seed': seeds
        }
        while destination != 'location':
            # Find the relevant map
            almanac_map = [m for m in almanac_maps if m.source == source]
            if len(almanac_map):
                time.sleep(0.1)
                almanac_map = almanac_map[0]
                destination = almanac_map.destination
                print(f'Found {source} {destination}')

                # Initialize empty array for values in destination
                values[destination] = []

                # Loop thru and populate destination values
                for k in values[source]:
                    # get the destination value
                    destination_value = almanac_map.get_destination_value(k)
                    values[destination].append(destination_value)

                source = destination

        print(values)
        return min(values['location'])


AOC_SOLVERS = {
    2022: {
        32: StraightThruAOCSolver(AOCInputParser(2022, 32)),
        33: StraightThruAOCSolver(AOCInputParser(2022, 32)),
    },
    2023: {
        1: AOC2023Day1Solver(AOCInputParser(2023, 1)),
        2: AOC2023Day2Solver(AOCRGBGameParser(2023, 2)),
        3: AOC2023Day3Solver(AOCEngineSchematicParser(2023, 3)),
        4: AOC2023Day4Solver(AOCScratchCardParser(2023, 4)),
        5: AOC2023Day5Solver(AOCAlmanacParser(2023, 5))
    }
}
