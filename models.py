
from dataclasses import dataclass, field
import operator
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
class Range:
    start: int
    end: int

    def __add__(self, other):
        # Check if other is None. If so... there is no overlap, so return None:
        if other is None:
            return None
        # Returns the range of values which are in BOTH self AND other
        res_start = max(self.start, other.start)
        res_end = min(self.end, other.end)
        return Range(res_start, res_end) if res_end >= res_start else None

    def __sub__(self, other):
        # Returns the range of values in self which are NOT in other

        # Check if other is None. If so... there is nothing to subtract, so return self:
        if other is None:
            return self

        # Get overlap, for use further below
        overlap = self.__add__(other)

        # 0. overlap is None -> there is nothing to subtract, so return self
        if overlap is None:
            return self

        # 1. overlap is in the middle of self -> need to return 2 Ranges!
        if overlap.start > self.start and overlap.end < self.end:
            return Range(self.start, overlap.start - 1), Range(overlap.end + 1, self.end)

        # 2. overlap is the whole self -> return None
        if overlap.start == self.start and overlap.end == self.end:
            return None

        # 3. overlap is at the start of self -> return part after overlap
        if overlap.start == self.start and overlap.end < self.end:
            return Range(overlap.end+1, self.end)

        # 4. overlap is at the end of self -> return part before overlap
        if overlap.start > self.start and overlap.end == self.end:
            return Range(self.start, overlap.start-1)


@dataclass
class AlmanacMapRange(Range):
    destination_offset: int  # Difference between the source value and destination value

    def get_destination_value(self, source_value):
        return (source_value + self.destination_offset
                if self.start <= source_value <= self.end
                else None
                )

    def __add__(self, other):
        range = Range(self.start, self.end)
        overlap_range = range.__add__(other)
        if overlap_range is not None:
            return AlmanacMapRange(overlap_range.start, overlap_range.end, self.destination_offset)
        else:
            return None


@dataclass
class AlmanacMapRange_old:
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


@dataclass
class BoatRace:
    time_ms: int
    record_mm: int

    def unique_record_breaks(self):
        delay_ms = 1
        halfway = self.time_ms // 2 + self.time_ms % 2
        while delay_ms <= halfway:
            if delay_ms * (self.time_ms - delay_ms) > self.record_mm:
                break  # No need to continue checking
            # If we reached here, we did not break the record -> increment and continue
            delay_ms += 1

        # Now the delay_ms will indicate the minimum delay which results in a record break
        # Find the count based on this
        print(f'halfway: {halfway}')
        res = (halfway - delay_ms) * 2
        if not self.time_ms % 2:  # Even number -> need to add one
            res += 1
        print(f'{self.time_ms}ms record of {self.record_mm}mm can be broken {res} times')
        return res


@dataclass
class PokerHand:
    cards_str: str  # 1 char per card
    bid: int = 0

    def __post_init__(self):
        # Assign the type and cards
        self.type_ = self.get_type()
        self.cards = self.get_cards()

    def get_counts(self):
        relevant_cards = self.get_cards()
        counts = {}
        while len(relevant_cards):
            card = relevant_cards[0]
            count = relevant_cards.count(card)
            counts[card] = count
            relevant_cards = [c for c in relevant_cards if c != card]

        return counts

    def get_type(self):
        counts = self.get_counts()

        # Now we have all the counts. Determine type and return.
        if len([k for k in counts if counts[k] == 5]):
            return 'five-of-a-kind'
        elif len([k for k in counts if counts[k] == 4]):
            return 'four-of-a-kind'
        elif len([k for k in counts if counts[k] == 3]):
            if len([k for k in counts if counts[k] == 2]):
                return 'full-house'
            else:
                return 'three-of-a-kind'
        elif len([k for k in counts if counts[k] == 2]) == 2:
            return 'two-pair'
        elif len([k for k in counts if counts[k] == 2]) == 1:
            return 'one-pair'
        else:
            return 'high-card'

    def get_cards(self):
        return [PlayingCard(c) for c in self.cards_str]

    def __gt__(self, other):
        # Determine whether self is the superior poker hand
        self_loc = self.types_ordered().index(self.type_)
        other_loc = other.types_ordered().index(other.type_)

        if self_loc < other_loc:
            return True
        elif self_loc > other_loc:
            return False
        else:
            for i in range(len(self.cards)):
                if self.cards[i] > other.cards[i]:
                    return True
                elif self.cards[i] < other.cards[i]:
                    return False
            return False  # Should only reach here if the hands are identical

    @classmethod
    def types_ordered(cls):
        return ['five-of-a-kind', 'four-of-a-kind', 'full-house'
                , 'three-of-a-kind', 'two-pair', 'one-pair', 'high-card']

class PokerHandWithJackAsJoker(PokerHand):

    def get_cards(self):
        return [(PlayingCard('joker') if c == 'J' else PlayingCard(c))
                for c in self.cards_str]

    def get_type(self):
        joker_card = PlayingCard('joker')
        joker_cnt = self.get_cards().count(joker_card)
        if not joker_cnt:
            return super().get_type()

        # If we reached here, there are joker(s) among us ...
        jokerless_cards_str = self.cards_str.replace('J', '')  # [c for c in self.cards_str if c != 'J']
        jokerless_hand = PokerHand(jokerless_cards_str)  # don't care about bid for this

        # Loop through counts of each card.
        # The optimal joker usage will be to assign them to that with the highest count
        most_frequent_cnt, most_frequent_card = 0, None
        for card, count in jokerless_hand.get_counts().items():
            if count > most_frequent_cnt:
                most_frequent_cnt, most_frequent_card = count, card

        # Now replace the jokers with this most frequent card
        if most_frequent_card is not None:
            joker_substituted_str = self.cards_str.replace('J', most_frequent_card.value_str)
            return PokerHand(joker_substituted_str).get_type()
        else:
            # 5 jokers in a hand!!! Make it the optimal hand of 5 aces:
            return PokerHand('AAAAA').get_type()

@dataclass
class PlayingCard:
    value_str: str  # should be only 1 char, unless it's a joker

    def __post_init__(self):
        if self.value_str.isdigit():
            self.value = int(self.value_str)
        else:
            self.value = self.str_values()[self.value_str]

    def __gt__(self, other):
        return self.value > other.value

    def __hash__(self):
        return hash(self.value_str)

    @classmethod
    def str_values(cls):
        return {'joker': 1, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}


@dataclass
class LRMapNode:
    name: str
    to_left: str
    to_right: str


@dataclass
class AsciiHashChar:
    starting_value: int
    char: str

    def get_result_value(self):
        res = self.starting_value
        res += ord(self.char)
        res *= 17
        res = res % 256
        return res


@dataclass
class MachinePart:
    scores: dict

    def __post_init__(self):
        values = [v for _, v in self.scores.items()]
        self.scores_sum = sum(values)

    def is_accepted(self, workflows):
        curr_workflow = workflows['in']
        while True:
            found = False  # have we found a true condition yet for this workflow?
            for c in curr_workflow.conditions:
                if c.is_true(self):
                    if c.target == 'R':
                        return False
                    elif c.target == 'A':
                        return True
                    else:
                        found = True
                        curr_workflow = workflows[c.target]
                        break
            # If we got here, either all conditions are False, or we found the True one:
            if not found:
                if curr_workflow.default_target == 'R':
                    return False
                elif curr_workflow.default_target == 'A':
                    return True
                else:
                    curr_workflow = workflows[curr_workflow.default_target]

@dataclass
class MachineWorkflowCondition:
    part_metric: str
    operation_str: str
    rhs: int
    target: str

    def __post_init__(self):
        ops = {
            '<': operator.lt,
            '<=': operator.le,
            '==': operator.eq,
            '!=': operator.ne,
            '>=': operator.ge,
            '>': operator.gt,
            '': lambda x, y: True
        }
        self.operation = ops.get(self.operation_str)

    def is_true(self, machine_part: MachinePart):
        lhs = machine_part.scores[self.part_metric]
        return self.operation(lhs, self.rhs)

@dataclass
class MachineWorkflow:
    name: str
    conditions: List[MachineWorkflowCondition]

    # def success_conditions(self):


@dataclass
class HailStone:
    start_pos: Tuple[int, int, int]
    velocity: Tuple[int, int, int]

    def intersection(self, other, axis=(True, True, False)):
        pass


@dataclass
class HistorianList:
    location_ids: List[int] = field(default_factory=list)

    def __sub__(self, other):
        res = 0

        # First, sort them, as then we can pair the items and get the total of abs differences:
        self.location_ids.sort()
        other.location_ids.sort()

        for i, loc_id in enumerate(self.location_ids):
            res += abs(loc_id - other.location_ids[i])
            print(f'{i}: {loc_id} {other.location_ids[i]} -> {res}')

        return res

    def similarity(self, other):
        res = 0

        # Loop thru
        for loc_id in self.location_ids:
            # Add similarity score = count * value
            res += loc_id * other.location_ids.count(loc_id)

        return res


# @dataclass
# class Galaxy:





