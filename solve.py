

import argparse

import os

from parsers import InputFileFinder
from solvers import AOC_SOLVERS


def main():
    arg_parser = argparse.ArgumentParser(description='Solve ALL the puzzles, get ALL the stars!')
    arg_parser.add_argument('--year', '-y', type=int, help='Optional specify year', default=0)
    arg_parser.add_argument('--day', '-d', type=int, help='Optional specify day', default=0)

    args = arg_parser.parse_args()

    # Populate year/day if not specified
    year = args.year
    day = args.day
    if not args.year:
        input_file_finder = InputFileFinder()
        year = input_file_finder.year
        print(f'Defaulting to year {year}')
    if not args.day:
        input_file_finder = InputFileFinder(year=year)
        day = input_file_finder.day
        print(f'Defaulting to day {day}')
        
    if year not in AOC_SOLVERS:
        print(f'Found no solvers yet for {year}!')
        return
        
    if day not in AOC_SOLVERS[year]:
        print(f'Found no solver yet for {year} day {day}!')
        return

    solver = AOC_SOLVERS[year][day]
    solver.solve()



if __name__ == "__main__":
    main()
