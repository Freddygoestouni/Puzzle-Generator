import copy

# Imports from other parts of the project
from .sudoku import Sudoku
from .cell_value import Cell_Value

def medium_solve_sudoku(puzzle: Sudoku) -> bool:
    '''
    Method to attempt to solve a sudoku puzzle and return whether it is possible.
    Uses features for which a medium puzzle solve can use.

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


def build_little_numbers(puzzle: Sudoku) -> list:
    '''
    Method to build the little numbers on all cells of the sudoku.

    Parameters:
        - puzzle - Sudoku puzzle to build options for

    Returns:
        - 2 d array where each cell is a list of options for the cell in question
    '''
    # Build out little numbers for all blank cells
    little_numbers = [[[] for j in range(9)] for i in range(9)]

    # Loop through all cells in the sudoku
    for column in range(1, 10):
        for row in range(1, 10):
            little_numbers[column-1][row-1] = puzzle.cell_options(column, row)

    return little_numbers

def simplify_cross_box(puzzle: Sudoku, little_numbers: list) -> list:
    '''
    Method to simplify (remove possibilities) the little numbers by considering
    if a number must be in a certain row in one box, restricting its position in
    other boxes horizontally or vertically aligned.

    Parameters:
        - puzzle - Sudoku puzzle being worked on
        - little_numbers - little numbers for the sudoku puzzle

    Returns:
        - little_numbers with any simplifications made using this method
    '''
    # Loop through all the cell values
    for value in range(1, 10):
        cell_value = Cell_Value(value)

        # Locations this value can exist in for each box
        locations = [[[] for j in range(3)] for i in range(3)]

        # List of cells whose options can be simplified
        get_rid = []

        # Loop through all the boxes
        for box_x in range(0, 3):
            for box_y in range(0, 3):
                # Get the top right coordinate
                column = box_x*3 + 1
                row = box_y*3 + 1

                box_locations = []

                # Loop through all cells in the box to see if they are a valid location
                for i in range(3):
                    for j in range(3):
                        cell_loc_col = column + i
                        cell_loc_row = row + j

                        # Dont consider a cell with a value as a valid option
                        if puzzle.get_value(cell_loc_col, cell_loc_row) not in (Cell_Value.EMPTY, cell_value): continue

                        if cell_value in puzzle.cell_options(cell_loc_col, cell_loc_row):
                            box_locations += [(cell_loc_col, cell_loc_row)]

                locations[box_x][box_y] = box_locations

                # Determine if the only options are all in a single row or column
                row_val = box_locations[0][1]
                col_val = box_locations[0][0]
                same_row = True
                same_col = True

                for location in box_locations:
                    same_col = same_col and col_val == location[0]
                    same_row = same_row and row_val == location[1]

                # If there is only one valid column, then remove this as an option for vertically aligned boxes
                if same_col:
                    # Loop through vertically aligned boxes to remove options
                    for y in range(3):
                        if y == box_y: continue

                        before = locations[box_x][y]
                        after = []

                        for option in before:
                            if option[0] != col_val:
                                after += [option]
                            else:
                                get_rid += [option]

                        locations[box_x][y] = after

                # If there is only one valid row, then remove this as an option for horizontally aligned boxes
                if same_row:
                    # Loop through vertically aligned boxes to remove options
                    for x in range(3):
                        if x == box_x: continue

                        before = locations[x][box_y]
                        after = []

                        for option in before:
                            if option[1] != row_val:
                                after += [option]
                            else:
                                get_rid += [option]

                        locations[x][box_y] = after

        # Remove the little numbers that have been simplified out
        for option in get_rid:
            cell = little_numbers[option[0]-1][option[1]-1]
            new = []

            for v in cell:
                if v != cell_value:
                    new += [v]

            little_numbers[option[0]-1][option[1]-1] = new

    return little_numbers
