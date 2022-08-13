from enum import Enum

class Cell_Value(Enum):
    '''
    Enum Class to hold the information on a cell in a Sudoku grid.

    Can have a value of either a number between 1 and 9 or blank.
    '''

    EMPTY = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9

    def __str__(self):
        '''
        Method to return the string representation of the cell value.
        '''

        # If the cell value is empty return a blank string, else return the number
        if self.value == 0:
            return " "
        else:
            return str(self.value)

    def seed(self):
        '''
        Method to return the seed representation of the cell value.
        '''

        # Return a character dependent on the integer value of the value
        return chr(self.value + 100)
