import copy

# Imports from other parts of the project
from .sudoku import Sudoku
from .cell_value import Cell_Value

def hard_solve_sudoku(puzzle: Sudoku) -> bool:
    '''
    Method to attempt to solve a sudoku puzzle and return whether it is possible.
    Uses features for which a hard puzzle solve can use.

    Parameters:
        - puzzle - sudoku to attempt to solve

    Returns:
        - Whether the sudoku puzzle was solved
    '''

    puzzle_copy = copy.deepcopy(puzzle)

    while(True):
        # Build the little numbers
        little_numbers = build_little_numbers(puzzle_copy)

        # Restrict down the little numbers
        little_numbers = simplify_cross_box(puzzle_copy, little_numbers)

        has_changed = False

        # Fill in any cells with only one option
        for column in range(1, 10):
            for row in range(1, 10):
                if puzzle_copy.get_value(column, row) == Cell_Value.EMPTY and len(little_numbers[column-1][row-1]) == 1:
                    puzzle_copy.set_value(column, row, little_numbers[column-1][row-1][0])
                    has_changed = True

        if not has_changed:
            break

    return puzzle_copy.number_of_clues() == 81
