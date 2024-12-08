
from abc import ABC, abstractmethod
from dataclasses import dataclass
import time
import traceback

from models import Digit, Range, AlmanacMapRange, AsciiHashChar, NeighbouringDirection
from parsers import (AOCInputParser, DummyAOCInputParser, AOCRGBGameParser
    , AOCEngineSchematicParser, AOCScratchCardParser, AOCAlmanacParser
    , AOCBoatRaceParser, AOCPokerHandParser, AOCLRNodeNetworkParser
    , AOCCommaSeparatedParser, AOC2023Day19Parser
    , AOC2024Day1Parser, AOC2024Day2Parser, AOC2024Day3Parser, AOC2024Day4Parser
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


class AOC2023Day8Solver(AOCSolver):
    @timeit
    def solve_part1(self, parsed):
        return None
        lr_pattern, nodes = parsed[0], parsed[1]
        curr_node, move_cnt = 'AAA', 0  # nodes[first_node_name], 0
        nodes_started_at = {}
        while curr_node != 'ZZZ':
            nodes_started_at[curr_node] = 1
            for c in lr_pattern:
                next_node = nodes[curr_node][c]
                curr_node = next_node
                move_cnt += 1
                if curr_node == 'ZZZ':
                    break

        return move_cnt

    @timeit
    def solve_part2(self, parsed):
        lr_pattern, nodes = parsed[0], parsed[1]
        starting_nodes = [n for n in nodes if n[-1] == 'A']
        ending_nodes = {n:[] for n in nodes if n[-1] == 'Z'}
        curr_node_names = starting_nodes
        print(f'Starting with {curr_node_names}')

        move_cnt = 0
        while len(curr_node_names):
            for i, c in enumerate(lr_pattern):
                move_cnt += 1
                # time.sleep(2)
                next_node_names = []  # init to empty - will fill this below

                # Loop thru currently occupied nodes. Find the next node. Append to next nodes.
                for node in curr_node_names:
                    next_node_names.append(nodes[node][c])

                # Remove those ending in Z - no longer relevant
                not_ending_in_z = [n for n in next_node_names if n[-1] != 'Z']
                ending_in_z = [n for n in next_node_names if n[-1] == 'Z']
                for e in ending_in_z:
                    if i not in ending_nodes[e]:
                        ending_nodes[e].append(i)
                # print(f'Ending nodes: {ending_nodes}')

                curr_node_names = next_node_names
                if not move_cnt % 1000000:
                    print(f'{move_cnt}: occupying {curr_node_names}')
                if not len(not_ending_in_z):
                    break  # Done!
            # The following else-continue-break means
            # the outer while loop will break when the for loop breaks:
            else:
                continue
            break

            print(f'{move_cnt}: occupying {curr_node_names}')

        return move_cnt


class AOC2023Day15Solver(AOCSolver):
    @timeit
    def solve_part1(self, parsed):
        print(f'parsed: {parsed}')
        total = 0
        for s in parsed:
            print(f's: {s}')
            val = 0
            for c in s:
                print(f'c: {c}')
                hash_char = AsciiHashChar(val, c)
                val = hash_char.get_result_value()
            total += val

        return total


class AOC2023Day19Solver(AOCSolver):
    @timeit
    def solve_part1(self, parsed):
        workflows, parts = parsed[0], parsed[1]

        total = 0
        for p in parts:
            if p.is_accepted(workflows):
                print(f'Accepted {p} {p.scores_sum}')
                total += p.scores_sum

        return total

class AOC2024Day1Solver(AOCSolver):
    @timeit
    def solve_part1(self, parsed):
        return parsed[0] - parsed[1]

    @timeit
    def solve_part2(self, parsed):
        return parsed[0].similarity(parsed[1])


class AOC2024Day2Solver(AOCSolver):
    @timeit
    def solve_part1(self, parsed):
        safe_reports = [lr for lr in parsed if lr.is_safe()]
        return len(safe_reports)

    @timeit
    def solve_part2(self, parsed):
        safe_reports = [lr for lr in parsed if lr.is_safe_with_one_removal()]
        return len(safe_reports)


class AOC2024Day3Solver(AOCSolver):
    @timeit
    def solve_part1(self, parsed):
        res = 0
        for me in parsed:
            res += me.result()

        return res

    @timeit
    def solve_part2(self, parsed):
        res = 0
        for me in parsed:
            if me.should_do:
                res += me.result()

        return res

class AOC2024Day4Solver(AOCSolver):
    @timeit
    def solve_part1(self, parsed):
        res = 0
        special_word = 'XMAS'

        for i, c in enumerate(parsed):
            if c.char == special_word[0]:
                for direction, neighbour in c.neighbours.items():
                    if neighbour[:3] == special_word[1:]:
                        res += 1

        return res

    @timeit
    def solve_part2(self, parsed):
        res = 0

        for i, c in enumerate(parsed):
            if c.char == 'A':
                # Look for A's in the middle, with neighbouring M's and S's
                try:
                    al, ar, br, bl = (
                        c.neighbours[NeighbouringDirection.ABOVE_LEFT][0],
                        c.neighbours[NeighbouringDirection.ABOVE_RIGHT][0],
                        c.neighbours[NeighbouringDirection.BELOW_RIGHT][0],
                        c.neighbours[NeighbouringDirection.BELOW_LEFT][0],
                    )
                    if (al in 'MS'
                            and ar in 'MS'
                            and br in 'MS'
                            and bl in 'MS'
                    ):
                        if al != br and ar != bl:
                            # If we made it here, both diagonals are not matching,
                            # therefore they must spell "MAS" (using the "A" which we already know is in the middle).
                            res += 1

                except IndexError as e:
                    # There may not be any neighbours in a given direction.
                    # If this is the case, there must not be a "X-MAS" centered at this "A".
                    # In such cases, we want to ignore this "A" and move on:
                    pass

        return res

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
        8: AOC2023Day8Solver(AOCLRNodeNetworkParser(2023, 8)),
        15: AOC2023Day15Solver(AOCCommaSeparatedParser(2023, 15)),
        19: AOC2023Day19Solver(AOC2023Day19Parser(2023, 19)),
    },
    2024: {
        1: AOC2024Day1Solver(AOC2024Day1Parser(2024, 1)),
        2: AOC2024Day2Solver(AOC2024Day2Parser(2024, 2)),
        3: AOC2024Day3Solver(AOC2024Day3Parser(2024, 3)),
        4: AOC2024Day4Solver(AOC2024Day4Parser(2024, 4)),
    },
}
