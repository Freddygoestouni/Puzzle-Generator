from ..puzzle import I_Puzzle, Difficulty, Page_Size
from .sudoku import Sudoku
from .seed_manager import *

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

    def generate(self, difficulty : Difficulty) -> None:
        '''
        Method to generate a sudoku puzzle.

        Parameters:
            - difficulty - the level of difficulty the generated puzzle should have (Difficulty enum)
        '''

        seed = get_seed()

        self.__puzzle.from_seed(seed)
        self.__solution.from_seed(seed)

        self.__solution.print_terminal()

        if difficulty == Difficulty.EASY:
            self.__generate_easy()

        self.__puzzle.print_terminal(size="big")


    def __generate_easy(self) -> None:
        '''
        Method to remove cells in the puzzle to create an easy sudoku.
        '''

        # Get a shuffled list of all indices of cells in the sudoku
        indices = list(range(81))
        random.shuffle(indices)

        # Loop through each of the indices
        for index in indices:
            # Get the coordinates of the index
            row = index % 9 + 1
            column = int(index / 9) + 1

            # If there is only one option for cell value with can be directly inferred, remove the cell value
            if len(self.__puzzle.cell_options(column, row)) == 1:
                self.__puzzle.set_value(column, row, Cell_Value.EMPTY)
