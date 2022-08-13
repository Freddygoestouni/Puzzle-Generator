from puzzles.sudoku.sudoku_puzzle import Sudoku_Puzzle
from puzzles.sudoku.seed_manager import *
from puzzles.puzzle import Difficulty, Page_Size
import argparse


parser = argparse.ArgumentParser(description="Puzzle Generator")
parser.add_argument("puzzle", nargs=1, help="Name of the puzzle. Options are: Sudoku, Wordsearch, ...")
parser.add_argument("difficulty", nargs=1, help="Difficulty of the puzzle. Options are: Easy, Medium, Hard, Extreme.")
parser.add_argument("size", nargs=1, help="Size of the paper for the puzzle to be printed on. Options are: A3, A4, A5.")
args = parser.parse_args()

sizes = {"A3" : Page_Size.A3,
            "A4" : Page_Size.A4,
            "A5" : Page_Size.A5 }
page_size = sizes[args.size[0]]



if args.puzzle[0] == "Sudoku":
    puzzle = Sudoku_Puzzle()

    puzzle.generate(Difficulty.EASY)

    puzzle.to_pdf(True, page_size, "filepath")
    #
    # puzzle.puzzle_to_terminal()
    # puzzle.solution_to_terminal()

    #generate_seeds()

if args.puzzle[0] == "Generate":
    mutate_seed("fihkmjglelmgehfjikkejlgifmhigmjlhekfjflikehgmehkmfgljihligekmfjgkfhjmielmjefilkhg")
