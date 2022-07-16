

import argparse


parser = argparse.ArgumentParser(description="Puzzle Generator")
parser.add_argument("puzzle", nargs=1, help="Name of the puzzle. Options are: Sudoku, Wordsearch, ...")
parser.add_argument("difficulty", nargs=1, help="Difficulty of the puzzle. Options are: Easy, Medium, Hard, Extreme.")
args = parser.parse_args()
