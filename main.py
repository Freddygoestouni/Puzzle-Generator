from puzzles.sudoku.sudoku_puzzle import Sudoku_Puzzle
from puzzles.sudoku.seed_manager import *
from puzzles.puzzle import Difficulty, Page_Size
import argparse

parser = argparse.ArgumentParser(description="Puzzle Generator")
parser.add_argument("puzzle", nargs=1, help="Name of the puzzle. Options are: Sudoku, Wordsearch, ...")
args = parser.parse_args()

if args.puzzle[0] == "Sudoku":

    difficulty = get_difficulty()

    page_size = get_page_size()

    puzzle = Sudoku_Puzzle()

    puzzle.generate(difficulty)

    puzzle.to_pdf(False, page_size, "test.pdf")

if args.puzzle[0] == "Generate":
    mutate_seed("fihkmjglelmgehfjikkejlgifmhigmjlhekfjflikehgmehkmfgljihligekmfjgkfhjmielmjefilkhg")

def get_page_size() -> Page_Size:
    '''
    Method to get the page size from the user.

    Returns:
        - Page size given by the user
    '''

    # Dictionary of the page size options with user input -> Page_Size object
    sizes = {"A3" : Page_Size.A3,
                "A4" : Page_Size.A4,
                "A5" : Page_Size.A5 }

    # Ask the user for the page size
    user_input = input("Input a page size for the PDF document. Options are: A3, A4 and A5: ")

    # If they give bad input, repeat till they give valid input
    while user_input not in sizes.keys():
        user_input = input("Invalid page size. Options are: A3, A4 and A5: ")

    # Return the page size given by the user input
    return sizes[user_input]

def get_difficulty() -> Difficulty:
    '''
    Method to get the difficulty from the user.

    Returns:
        - Difficulty given by the user
    '''

    # Dictionary of the page size options with user input -> Page_Size object
    difficulties = {"Easy" : Difficulty.EASY,
                           "Medium" : Difficulty.MEDIUM,
                           "Hard" : Difficulty.HARD,
                           "Extreme" : Difficulty.EXTREME }

    # Ask the user for the page size
    user_input = input("Input a difficulty for the puzzle. Options are: Easy, Medium, Hard and Extreme: ")

    # If they give bad input, repeat till they give valid input
    while user_input not in difficulties.keys():
        user_input = input("Invalid difficulty. Options are: Easy, Medium, Hard and Extreme: ")

    # Return the difficulty given by the user input
    return difficulties[user_input]
