import math
import random

# Importing cell value
from .cell_value import Cell_Value


class Sudoku:
    '''
    Class to hold the information on a Sudoku grid.

    Rows and Columns are a range from 1 to 9.
    '''

    def __init__(self, seed=None):
        '''
        Method to create an instance of the sudoku puzzle.

        Parameters:
            - seed (optional) - seed of a sudoku puzzle to be loaded in
        '''

        # Create an empty sudoku grid
        self.__grid = [[Cell_Value.EMPTY]*9 for i in range(9)]

        # Fill the sudoku based on a seed if one is given
        if seed is not None:
            self.from_seed(seed)

    def from_seed(self, seed:str) -> None:
        '''
        Method to load a sudoku puzzle grid from a given seed.

        Parameters:
            - seed - seed of a sudoku puzzle
        '''

        # Check the seed is the correct length
        if len(seed) != 81:
            raise Exception("Invalid Seed")

        # Check all the characters in the seed are valid
        if not set(seed).issubset(set([Cell_Value(value).seed() for value in range(10)])):
            raise Exception("Invalid Seed")

        # Loop through all cells in the sudoku grid
        for index in range(81):
            # Find the specific coordinates of the index
            row = index % 9 + 1
            column = int(index / 9) + 1

            # Set the cell value of the coordinates according to the seed
            self.set_value(column, row, Cell_Value(ord(seed[index]) - 100))

    def get_seed(self) -> str:
        '''
        Method to create a seed for the sudoku.

        Returns:
            - seed - seed of the sudoku puzzle as a string
        '''

        # String for the seed
        seed = ""

        # Loop through all cells in the grid
        for index in range(81):
            # Find the specific coordinates of the index
            row = index % 9 + 1
            column = int(index / 9) + 1

            # Get the seed of the cell value to add to the sudoku seed
            seed += str(self.get_value(column, row).seed())

        # Return the seed of the sudoku
        return seed

    def clear(self) -> None:
        '''
        Method to clear the sudoku by replacing all cells with an empty value.
        '''

        # Create an empty sudoku grid
        self.__grid = [ [Cell_Value.EMPTY]*9 for i in range(9)]

    def get_value(self, column:int, row:int) -> Cell_Value:
        '''
        Method to get a value of a specific cell of the sudoku.

        Parameters:
            - column - column index of the cell (integer between 1 and 9)
            - row - row index of the cell (integer between 1 and 9)

        Returns:
            - cell value - the value of the cell as the Cell_Value enum
        '''

        # Check that the parameters are valid
        if type(column) is not int or type(row) is not int or column not in range(1, 10) or row not in range(1, 10):
            raise Exception("Invalid Index")

        # Return the value stored in the grid
        return self.__grid[row-1][column-1]

    def set_value(self, column:int, row:int, value:Cell_Value) -> None:
        '''
        Method to set a value of a specific cell of the sudoku.

        Parameters:
            - column - column index of the cell (integer between 1 and 9)
            - row - row index of the cell (integer between 1 and 9)
            - value - value of the cell as a Cell_Value enum
        '''

        # Check that the value parameter is valid
        if type(value) is not Cell_Value:
            raise Exception("Invalid Value")

        # Check that the column and row coordinates are valid
        if type(column) is not int or type(row) is not int or column not in range(1, 10) or row not in range(1, 10):
            raise Exception("Invalid Index")

        # Update the grid with the new value
        self.__grid[row-1][column-1] = value

    def get_row_values(self, row:int, ignore=None) -> list:
        '''
        Method to get all unique values in a specified row of the sudoku.

        Parameters:
            - row - row index of the cell (integer between 1 and 9)
            - ignore (optional) - column index of a cell to ignore in the list of values

        Returns:
            - list of unique cell values in the specified row (excluding potential ignored column)
        '''

        # Check that the row coordinate is valid
        if type(row) is not int or row not in range(1, 10):
            raise Exception("Invalid Index")

        # Check that the ignore coordinate is valid
        if ignore is not None and (type(ignore) is not int or ignore not in range(1, 10)):
            raise Exception("Invalid Index")

        # Set for all the unique values in the row (using set to remove duplicates)
        values = set()

        # Loop through all the cells in the row
        for column in range(1, 10):
            # If the cell is being ignored, skip the column
            if ignore is not None and column == ignore: continue

            # Add the cell value to the set
            values.add(self.get_value(column, row))

        # Return the collection of values as a list
        return list(values)

    def get_column_values(self, column:int, ignore=None) -> list:
        '''
        Method to get all unique values in a specified column of the sudoku.

        Parameters:
            - column - column index of the cell (integer between 1 and 9)
            - ignore (optional) - row index of a cell to ignore in the list of values

        Returns:
            - list of unique cell values in the specified column (excluding potential ignored row)
        '''

        # Check that the column coordinate is valid
        if type(column) is not int or column not in range(1, 10):
            raise Exception("Invalid Index")

        # Check that the ignore coordinate is valid
        if ignore is not None and (type(ignore) is not int or ignore not in range(1, 10)):
            raise Exception("Invalid Index")

        # Set for all the unique values in the column (using set to remove duplicates)
        values = set()

        # Loop through all the cells in the column
        for row in range(1, 10):
            # If the cell is being ignored, skip the row
            if ignore is not None and row == ignore: continue

            # Add the cell value to the set
            values.add(self.get_value(column, row))

        # Return the collection of values as a list
        return list(values)

    def get_box_values(self, column:int, row:int, ignore=False) -> list:
        '''
        Method to get all unique values in a specified box of the sudoku.

        Parameters:
            - column - column index of the cell (integer between 1 and 9)
            - row - row index of the cell (integer between 1 and 9)
            - ignore (optional) - boolean whether to ignore cell in the list of values (default False)

        Returns:
            - list of unique cell values in the box of the specified cell (excluding potential ignored cell)
        '''

        # Check that the row and column coordinate is valid
        if type(column) is not int or type(row) is not int or column not in range(1, 10) or row not in range(1, 10):
            raise Exception("Invalid Index")

        # Check that the ignore coordinate is valid
        if type(ignore) is not bool:
            raise Exception("Invalid Ignore")

        # Set for all the unique values in the box (using set to remove duplicates)
        values = set()

        # Calculate the top left corner index of the box that contains the cell
        box_row = math.floor((row-1)/3) * 3 + 1
        box_column = math.floor((column-1)/3) * 3 + 1

        # Loop through all cells in the box
        for row_index in range(box_row, box_row + 3):
            for column_index in range(box_column, box_column + 3):
                # If the cell is being ignored, skip it
                if ignore and row_index == row and column_index == column: continue

                # Add the cell value to the set
                values.add(self.get_value(column_index, row_index))

        # Return the collection of values as a list
        return list(values)

    def cell_options(self, column:int, row:int) -> list:
        '''
        Method to get all valid options to be put in a specific box of the sudoku.

        Parameters:
            - column - column index of the cell (integer between 1 and 9)
            - row - row index of the cell (integer between 1 and 9)

        Returns:
            - list of valid options for the cell value of the specified cell
        '''

        # Check that the row and column coordinate is valid
        if type(column) is not int or type(row) is not int or column not in range(1, 10) or row not in range(1, 10):
            raise Exception("Invalid Index")

        # Create a set of all potential values
        options = set([Cell_Value(x) for x in range(1, 10)])

        # Remove any cell values present in the row, column and box
        options -= set(self.get_row_values(row, ignore=column))
        options -= set(self.get_column_values(column, ignore=row))
        options -= set(self.get_box_values(column, row, ignore=True))

        # Return the collection of valid values as a list
        return list(options)

    def valid(self, empty_as_valid=False) -> bool:
        '''
        Method to check whether the sudoku grid is valid.

        Parameters:
            - empty_as_valid (optional) - boolean indicating whether to accept empty squares as valid

        Returns:
            - bool - whether the existing sudoku grid is valid
        '''

        # Loop through all cells in the sudoku grid
        for column in range(1, 10):
            for row in range(1, 10):
                # Get the list of all valid options for the cell
                options = self.cell_options(column, row)

                # If specified to accept empty cells, add this to the valid list
                if empty_as_valid:
                    options += [Cell_Value.EMPTY]

                # Check that the actual cell value is in the list of valid options
                if self.get_value(column, row) not in options:
                    return False

        # If all cells have passed the check, return valid
        return True

    def fill(self, clear=False, find_all=False) -> None:
        '''
        Method to fill a sudoku with valid values, to create a valid filled in sudoku grid.

        Parameters:
            - clear (optional) - boolean for whether to clear the sudoku before filling it (default is False)
            - find_all (optional) - boolean for whether to find more than one sudoku value (default is False)

        Returns:
            - if find_all is True, it returns a list of valid seeds found
        '''

        # If the sudoku should be cleared else, check if the sudoku is valid
        if clear:
            self.clear()
        elif not self.valid(empty_as_valid=True):
            raise Exception("Existing Sudoku Grid is not Valid")

        # List of empty cells locations
        empty = []

        # Loop through all cells in the grid to identify the empty locations
        for column in range(1, 10):
            for row in range(1, 10):
                if self.get_value(column, row) == Cell_Value.EMPTY:
                    empty += [(column, row)]

        # If all the cells are already filled, return
        if len(empty) == 0:
            return

        # Randomly shuffle the cell locations
        random.shuffle(empty)

        # Initialise the list of all seeds if find_all is True
        if find_all:
            self.__seeds = list()

        # Call the recursive function to fill the sudoku grid
        if not self.__fill_backtrack(empty, find_all):
            # If it is looking for all seeds it returns them
            if find_all:
                # Get the list of all seeds, delete it from the object and return it
                seeds = self.__seeds
                del self.__seeds
                return seeds

            raise Exception("Could not find a valid sudoku grid")

    def __fill_backtrack(self, locations:list, find_all=False) -> bool:
        '''
        Recursive method to fill a sudoku with valid values, to create a valid filled in sudoku grid.

        Parameters:
            - locations - list of remaining locations in the sudoku which are empty (yet to be filled)
            - find_all (optional) - whether to find just one sudoku or many

        Returns:
            - bool - whether a valid sudoku has been created
        '''

        # Base Case - if the list of locations yet to be filled is empty (i.e. sudoku is full)
        if len(locations) == 0:
            self.print_terminal()

            # If all sudoku grids are to be found, add the current seed to the list, and carry on searching
            if find_all:
                self.__seeds += [self.get_seed()]
                return True

            return True

        # Get the next location to be filled off the list
        location = locations[0]
        column, row = location

        # Get the list of options for values which can go into the cell
        options = self.cell_options(column, row)

        # Shuffle the list of options
        random.shuffle(options)

        # Loop through the list of options
        for option in options:
            # Try setting the cell to that value
            self.set_value(column, row, option)

            # Check if all other empty cells still have a valid option after this cell has been set
            valid = True
            for location in locations[1:]:
                if len(self.cell_options(location[0], location[1])) == 0:
                    valid = False

            # If the sudoku can still be filled, recursively call the fill method with the list of remaining locations
            if valid and self.__fill_backtrack(locations[1:]):
                return True

            # If the chosen value did not result in a valid sudoku, replace it with an empty value
            self.set_value(column, row, Cell_Value.EMPTY)

        # If none of the options created a valid sudoku, return false
        return False

    def print_terminal(self, size="small") -> None:
        '''
        Method to print the sudoku to the terminal.

        Parameters:
            - size (optional) - either "small" or "big" (default is "small")
        '''

        # Call the respective method to either print a small or big version
        if size == "small":
            self.__print_terminal_small()
        elif size == "big":
            self.__print_terminal_big()
        else:
            raise ValueError("Invalid Size. Size parameter must either be 'small' or 'big' (default is 'small')")

    def __print_terminal_small(self) -> None:
        '''
        Method to print the sudoku to the terminal in the small format.

        Outputs:
            - terminal - sudoku in small format
        '''

        # Top border of the sudoku
        string = "┏━━━━━━━┳━━━━━━━┳━━━━━━━┓" + "\n"

        # Loop through each row of the sudoku
        for row in range(1, 10):
            # If the current row is the first of a new box
            if row in [4, 7]:
                string += "┣━━━━━━━╋━━━━━━━╋━━━━━━━┫" + "\n"

            # Loop through each column of the row
            for column in range(1, 10):
                # If the current column is the first of a new box
                if column in [1, 4, 7]:
                    string += "┃ "

                # Add the cell value to the string
                string += str(self.get_value(column, row)) + " "

            # Add the right border to the line
            string += "┃" + "\n"

        # Bottom border of the sudoku
        string += "┗━━━━━━━┻━━━━━━━┻━━━━━━━┛" + "\n"

        # Print the sudoku
        print(string)

    def __print_terminal_big(self) -> None:
        '''
        Method to print the sudoku to the terminal in the large format.

        Outputs:
            - terminal - sudoku in large format
        '''

        # Top border of the sudoku
        string = "┏━━━┯━━━┯━━━┳━━━┯━━━┯━━━┳━━━┯━━━┯━━━┓" + "\n"

        # Loop through each row of the sudoku
        for row in range(1, 10):
            # If the current row is the first of a new box add thick horizontal, else thin
            if row in [4, 7]:
                string += "┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫" + "\n"
            elif row in [2, 3, 5, 6, 8, 9]:
                string += "┠───┼───┼───╂───┼───┼───╂───┼───┼───┨" + "\n"

            # Loop through each column of the row
            for column in range(1, 10):
                # If the current column is the first of a new box
                if column in [1, 4, 7]:
                    string += "┃ "

                # Add the cell value to the string
                string += str(self.get_value(column, row)) + " "

                # If the current column is not the last of a box
                if column in [1, 2, 4, 5, 7, 8]:
                    string += "│ "

            # Add the right border to the line
            string += "┃" + "\n"

        # Bottom border of the sudoku
        string += "┗━━━┷━━━┷━━━┻━━━┷━━━┷━━━┻━━━┷━━━┷━━━┛" + "\n"

        # Print the sudoku
        print(string)
