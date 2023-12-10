
from abc import ABC, abstractmethod
from dataclasses import dataclass
import time
import traceback

from models import Digit, Range, AlmanacMapRange
from parsers import (AOCInputParser, DummyAOCInputParser, AOCRGBGameParser
    , AOCEngineSchematicParser, AOCScratchCardParser, AOCAlmanacParser
    , AOCBoatRaceParser, AOCPokerHandParser
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
            traceback.print_exception(e)
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
    final_destination = 'location'

    @timeit
    def solve_part1(self, parsed):
        seeds, almanac_maps = parsed[0], parsed[1]
        print(almanac_maps)
        source, destination = 'seed', None
        values = {
            'seed': seeds
        }
        while destination != self.final_destination:
            # Find the relevant map
            almanac_map = [m for m in almanac_maps if m.source == source]
            if len(almanac_map):
                # time.sleep(0.1)
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

    @timeit
    def solve_part2(self, parsed):
        seed_ranges, almanac_maps = parsed[2], parsed[1]
        source, destination = 'seed', None
        ranges = {
            'seed': seed_ranges
        }

        while destination != self.final_destination:
            # Find the relevant map
            almanac_map = [m for m in almanac_maps if m.source == source]
            if len(almanac_map):
                # time.sleep(0.1)
                almanac_map = almanac_map[0]
                destination = almanac_map.destination
                print(f'Found {source} {destination}')
                print(f'{source} ranges: {ranges[source]}')
                print(f'{source}-{destination} ranges: {almanac_map.ranges}')

                # Initialize empty array for ranges in destination
                destination_ranges = []
                ranges[destination] = []

                # Loop thru and populate destination values
                for sr in ranges[source]:

                    # Initialize - we will continually subtract from this until using it after the below loop
                    sr_orphans = [Range(sr.start, sr.end)]
                    # Loop thru almanac map ranges, and find the destination ranges
                    for amr in almanac_map.ranges:
                        # get the destination range
                        print(f'Adding {amr} + {sr}')
                        destination_range = amr + sr
                        if destination_range is not None:
                            print(f'Appending {destination} range {destination_range}')
                            destination_ranges.append(destination_range)

                        # Loop thru and get ranges which are now "orphaned", i.e. unmapped
                        print(f'Subtracting {sr_orphans} - {destination_range}')
                        sr_orphans_res = []
                        for sro in sr_orphans:
                            print(f'Subtracting {sro} - {destination_range}')
                            sub_res = sro - destination_range
                            if sub_res is None:
                                continue
                            elif isinstance(sub_res, tuple):
                                sr_orphans_res.extend(sub_res)
                            elif isinstance(sub_res, Range):
                                sr_orphans_res.append(sub_res)
                        # sr_orphans = [sro - destination_range for sro in sr_orphans]
                        print(f'Subtraction res: {sr_orphans_res}')
                        sr_orphans = sr_orphans_res.copy()

                    # Now sr_orphans contains any source range values which did not map to a destination value.
                    # In this case, we should map them to their same value:
                    print(f'{source}-{destination} orphans: {sr_orphans_res}')
                    destination_ranges.extend([
                        AlmanacMapRange(sro.start, sro.end, 0)
                        for sro in sr_orphans_res if sro is not None
                    ])

                # Complete the step: assign destination -> source; assign incremented values
                source = destination
                new_source_ranges = [Range(amr.start+amr.destination_offset, amr.end+amr.destination_offset)
                                     for amr in destination_ranges]
                ranges[destination] = new_source_ranges

        print(ranges)
        final_dest_range_starts = [r.start for r in ranges[self.final_destination]]
        return min(final_dest_range_starts)


class AOC2023Day6Solver(AOCSolver):
    @timeit
    def solve_part1(self, parsed):
        # Initialize
        total = 1
        for race in parsed[0]:
            total *= race.unique_record_breaks()

        return total

    @timeit
    def solve_part2(self, parsed):
        return parsed[1].unique_record_breaks()


class AOC2023Day7Solver(AOCSolver):
    @timeit
    def solve_part1(self, parsed):
        total = 0

        # Sort the parsed poker hands. Weakest hand will then be at the start.
        hands = parsed[0]
        hands.sort()

        # Now loop through and add the bid * rank to the total
        # Since list is zero-indexed ... rank will be the location + 1
        for i, hand in enumerate(hands):
            total += hand.bid * (i+1)

        return total

    @timeit
    def solve_part2(self, parsed):
        total = 0

        # Sort the parsed poker hands, with jokers. Weakest hand will then be at the start.
        hands = parsed[1]
        print(f'Sorting {hands}')
        hands.sort()
        print(f'Sorted {hands}')

        # Now loop through and add the bid * rank to the total
        # Since list is zero-indexed ... rank will be the location + 1
        for i, hand in enumerate(hands):
            total += hand.bid * (i+1)

        return total

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
        5: AOC2023Day5Solver(AOCAlmanacParser(2023, 5)),
        6: AOC2023Day6Solver(AOCBoatRaceParser(2023, 6)),
        7: AOC2023Day7Solver(AOCPokerHandParser(2023, 7)),
    }
}
