from ..puzzle import I_Puzzle, Difficulty, Page_Size
from .sudoku import Sudoku

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
