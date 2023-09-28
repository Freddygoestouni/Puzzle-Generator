import math
import random

# Imports from other parts of the project
from .sudoku import Sudoku
from .cell_value import Cell_Value
from .generate_easy import *
from .generate_medium import *
from .generate_hard import *


def generate_easy(puzzle : Sudoku) -> Sudoku:
    '''
    Method to remove cells in the puzzle to create an easy sudoku.

    Parameters:
        - puzzle - full sudoku to remove cells from

    Returns:
        - puzzle with cells removed to a difficulty level easy
    '''

    # Remove direct, box, row and column inferable cell values
    puzzle = remove_direct_inference(puzzle)
    puzzle = remove_box_inference(puzzle)
    puzzle = remove_row_inference(puzzle)
    puzzle = remove_column_inference(puzzle)

    print(puzzle.number_of_clues())

    # Return the easy difficulty puzzle
    return puzzle

def generate_medium(puzzle : Sudoku) -> Sudoku:
    '''
    Method to remove cells in the puzzle to create an medium sudoku.

    Parameters:
        - puzzle - full sudoku to remove cells from

    Returns:
        - puzzle with cells removed to a difficulty level medium
    '''

    # Remove the cells to create an easy difficulty puzzle
    puzzle = generate_easy(puzzle)

    # Get a shuffled list of all indices of cells in the sudoku
    indices = list(range(81))
    random.shuffle(indices)

    # Loop through each of the indices
    for index in indices:

        # Get the coordinates of the index
        row = index % 9 + 1
        column = int(index / 9) + 1

        # Ignore the cell if it is already empty
        if puzzle.get_value(column, row) == Cell_Value.EMPTY:
            continue

        # Set the value to empty (temporarily if inference is not possible)
        cell_value = puzzle.get_value(column, row)
        puzzle.set_value(column, row, Cell_Value.EMPTY)

        # If the puzzle cannot be solved by the medium puzzle solver, add back in the cell value
        if not medium_solve_sudoku(puzzle):
            puzzle.set_value(column, row, cell_value)

    print(puzzle.number_of_clues())

    # Return the medium difficulty puzzle
    return puzzle

def generate_hard(puzzle : Sudoku) -> Sudoku:
    '''
    Method to remove cells in the puzzle to create an hard sudoku.

    Parameters:
        - puzzle - full sudoku to remove cells from

    Returns:
        - puzzle with cells removed to a difficulty level hard
    '''

    # Remove the cells to create an medium difficulty puzzle
    puzzle = generate_medium(puzzle)

    # Get a shuffled list of all indices of cells in the sudoku
    indices = list(range(81))
    random.shuffle(indices)

    # Loop through each of the indices
    for index in indices:

        # Get the coordinates of the index
        row = index % 9 + 1
        column = int(index / 9) + 1

        # Ignore the cell if it is already empty
        if puzzle.get_value(column, row) == Cell_Value.EMPTY:
            continue

        # Set the value to empty (temporarily if inference is not possible)
        cell_value = puzzle.get_value(column, row)
        puzzle.set_value(column, row, Cell_Value.EMPTY)

        # If the puzzle cannot be solved by the hard puzzle solver, add back in the cell value
        if not hard_solve_sudoku(puzzle):
            puzzle.set_value(column, row, cell_value)

    print(puzzle.number_of_clues())
    
    # Return the hard difficulty puzzle
    return puzzle

def generate_extreme(puzzle : Sudoku) -> Sudoku:
    '''
    Method to remove cells in the puzzle to create an extreme sudoku.

    Parameters:
        - puzzle - full sudoku to remove cells from

    Returns:
        - puzzle with cells removed to a difficulty level extreme
    '''

    # Remove the cells to create an hard difficulty puzzle
    puzzle = generate_hard(puzzle)

    # Return the extreme difficulty puzzle
    return puzzle
