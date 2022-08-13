import math
import random

# Imports from other parts of the project
from .sudoku import Sudoku
from .cell_value import Cell_Value

def generate_easy(puzzle : Sudoku) -> Sudoku:
    '''
    Method to remove cells in the puzzle to create an easy sudoku.

    Parameters:
        - puzzle - full sudoku to remove cells from

    Returns:
        - puzzle with cells removed to a difficulty level easy
    '''

    # Remove direct, box, row and column inferable cell values
    puzzle = __remove_direct_inference(puzzle)
    puzzle = __remove_box_inference(puzzle)
    puzzle = __remove_row_inference(puzzle)
    puzzle = __remove_column_inference(puzzle)

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

def __remove_direct_inference(puzzle : Sudoku) -> Sudoku:
    '''
    Method to remove cells in the puzzle which can be directly inferred by looking at the row, column
    and box the cell is situated in.

    Parameters:
        - puzzle - sudoku to remove cells from

    Returns:
        - Sudoku with directly inferable cells removed
    '''

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

        # If there is only one option for cell value with can be directly inferred, remove the cell value
        if len(puzzle.cell_options(column, row)) == 1:
            puzzle.set_value(column, row, Cell_Value.EMPTY)

    # Return the puzzle without directly inferable cells
    return puzzle

def __remove_box_inference(puzzle : Sudoku) -> Sudoku:
    '''
    Method to remove cells in the puzzle which can be inferred by looking at options for each empty
    cell in the box it is situated in. It only removes a cell if the only place in the box for the value is
    the cell being looked at

    Parameters:
        - puzzle - sudoku to remove cells from

    Returns:
        - Sudoku with box inferable cells removed
    '''

    # Get a shuffled list of all indices of cells in the sudoku
    indices = list(range(81))
    random.shuffle(indices)

    # Loop through all cells
    for index in indices:
        # Get the coordinates of the index
        row = index % 9 + 1
        column = int(index / 9) + 1

        # Calculate the top left corner index of the box that contains the cell
        box_row = math.floor((row-1)/3) * 3 + 1
        box_column = math.floor((column-1)/3) * 3 + 1

        # Ignore the cell if it is already empty
        if puzzle.get_value(column, row) == Cell_Value.EMPTY:
            continue

        # Change the cell to be empty (temporary)
        cell_value = puzzle.get_value(column, row)
        puzzle.set_value(column, row, Cell_Value.EMPTY)

        # Loop through cells in the box finding if there is an empty cell which could hold the value
        for search_row in range(box_row, box_row + 3):
            for search_column in range(box_column, box_column + 3):
                # Skip if it is the current cell
                if search_column == column and search_row == row:
                    continue

                # Skip if the cell is not empty
                if puzzle.get_value(search_column, search_row) != Cell_Value.EMPTY:
                    continue

                # If the cell value is an option in this cell, it cannot be removed
                if cell_value in puzzle.cell_options(search_column, search_row):
                    puzzle.set_value(column, row, cell_value)
                    break
            else:
                continue
            break

    # Return the puzzle without box inferable cells
    return puzzle

def __remove_row_inference(puzzle : Sudoku) -> Sudoku:
    '''
    Method to remove cells in the puzzle which can be inferred by looking at options for each empty
    cell in the row it is situated in. It only removes a cell if the only place in the row for the value is
    the cell being looked at

    Parameters:
        - puzzle - sudoku to remove cells from

    Returns:
        - Sudoku with row inferable cells removed
    '''

    # Get a shuffled list of all indices of cells in the sudoku
    indices = list(range(81))
    random.shuffle(indices)

    # Loop through all cells
    for index in indices:
        # Get the coordinates of the index
        row = index % 9 + 1
        column = int(index / 9) + 1

        # Ignore the cell if it is already empty
        if puzzle.get_value(column, row) == Cell_Value.EMPTY:
            continue

        # Change the cell to be empty (temporary)
        cell_value = puzzle.get_value(column, row)
        puzzle.set_value(column, row, Cell_Value.EMPTY)

        # Loop through cells in the row finding if there is an empty cell which could hold the value
        for search_column in range(1, 10):
            # Skip if it is the current cell
            if search_column == column:
                continue

            # Skip if the cell is not empty
            if puzzle.get_value(search_column, row) != Cell_Value.EMPTY:
                continue

            # If the cell value is an option in this cell, it cannot be removed
            if cell_value in puzzle.cell_options(search_column, row):
                puzzle.set_value(column, row, cell_value)
                break

    # Return the puzzle without row inferable cells
    return puzzle

def __remove_column_inference(puzzle : Sudoku) -> Sudoku:
    '''
    Method to remove cells in the puzzle which can be inferred by looking at options for each empty
    cell in the column it is situated in. It only removes a cell if the only place in the column for the
    value is the cell being looked at

    Parameters:
        - puzzle - sudoku to remove cells from

    Returns:
        - Sudoku with column inferable cells removed
    '''

    # Get a shuffled list of all indices of cells in the sudoku
    indices = list(range(81))
    random.shuffle(indices)

    # Loop through all cells
    for index in indices:
        # Get the coordinates of the index
        row = index % 9 + 1
        column = int(index / 9) + 1

        # Ignore the cell if it is already empty
        if puzzle.get_value(column, row) == Cell_Value.EMPTY:
            continue

        # Change the cell to be empty (temporary)
        cell_value = puzzle.get_value(column, row)
        puzzle.set_value(column, row, Cell_Value.EMPTY)

        # Loop through cells in the column finding if there is an empty cell which could hold the value
        for search_row in range(1, 10):
            # Skip if it is the current cell
            if search_row == row:
                continue

            # Skip if the cell is not empty
            if puzzle.get_value(column, search_row) != Cell_Value.EMPTY:
                continue

            # If the cell value is an option in this cell, it cannot be removed
            if cell_value in puzzle.cell_options(column, search_row):
                puzzle.set_value(column, row, cell_value)
                break

    # Return the puzzle without column inferable cells
    return puzzle
