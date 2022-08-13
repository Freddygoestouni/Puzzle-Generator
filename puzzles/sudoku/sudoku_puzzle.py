import math

from ..puzzle import I_Puzzle, Difficulty, Page_Size
from .sudoku import Sudoku
from .seed_manager import *
from .sudoku_pdf import Sudoku_PDF
from .create_difficulty import *

class Sudoku_Puzzle(I_Puzzle):

    def __init__(self):
        '''
        Method to initialise a sudoku puzzle. This creates a blank sudoku grid.
        '''

        # Create blank sudoku puzzle and solution
        self.__puzzle = Sudoku()
        self.__solution = Sudoku()

        # Set the difficulty level of the puzzle as undefined
        self.__difficulty = Difficulty.UNDEFINED

    def __str__(self):
        return "Sudoku puzzle. Difficulty: " + str(self.__difficulty) + " Puzzle seed: " + str(self.__puzzle.get_seed()) + " Solution seed: " + str(self.__solution.get_seed())

    def puzzle_to_terminal(self, size="small"):
        '''
        Method to print the puzzle to the console.

        Parameters:
            - size (optional) - how big the printed puzzle should be (either "small" or "big")
        '''

        self.__puzzle.print_terminal(size=size)

    def solution_to_terminal(self, size="small"):
        '''
        Method to print the solution to the console.

        Parameters:
            - size (optional) - how big the printed solution should be (either "small" or "big")
        '''

        self.__solution.print_terminal(size=size)

    def generate(self, difficulty : Difficulty, seed=None) -> None:
        '''
        Method to generate a sudoku puzzle.

        Parameters:
            - difficulty - the level of difficulty the generated puzzle should have (Difficulty enum)
            - seed (optional) - the seed to use for the puzzle, if not included it uses a random one
        '''

        # Set the difficulty of the puzzle as a class variable
        self.__difficulty = difficulty

        # Check that the seed given is valid
        if seed is not None and (type(seed) is not str or not Sudoku(seed).valid()):
            raise Exception("Invalid seed parameter. Must be a valid seed.")

        # If the seed is not given, find a random one
        if seed is None:
            seed = get_seed()

        # Create sudoku grids using the seed for the puzzle and solution
        self.__puzzle.from_seed(seed)
        self.__solution.from_seed(seed)

        # Remove squares depending on the difficulty requested
        if difficulty == Difficulty.EASY:
            self.__puzzle = generate_easy(self.__puzzle)
        elif difficulty == Difficulty.MEDIUM:
            self.__puzzle = generate_medium(self.__puzzle)
        elif difficulty == Difficulty.HARD:
            self.__puzzle = generate_hard(self.__puzzle)
        elif difficulty == Difficulty.EXTREME:
            self.__puzzle = generate_extreme(self.__puzzle)

    def to_pdf(self, include_solution : bool, page_size : Page_Size, filepath : str):
        '''
        Method to convert the sudoku puzzle with proper formatting to a pdf document which can
        then be used by a user.

        Parameters:
            - include_solution - boolean indicating whether to include the solution on the page
            - page_size - the size of the page the pdf should be (Page_Size enum)
            - filepath - string filepath denoting where to save the pdf document to
        '''

        # Set up a PDF document with the specified page size
        pdf = Sudoku_PDF(page_size)

        # Insert the sudoku puzzle to the PDF document
        pdf.insert_puzzle(self.__difficulty,
                                     self.__solution.get_seed(),
                                     self.__puzzle,
                                     self.__solution if include_solution else None)

        # Output the PDF document to the specified filepath
        pdf.output(filepath, "F")
