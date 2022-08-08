from enum import Enum

class Difficulty(Enum):
    '''
    Enum Class to hold the information on a puzzle's difficulty level.

    Can have a value of easy, medium, hard or extreme.
    '''

    UNDEFINED = 0
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXTREME = 4

    def __str__(self):
        '''
        Method to return the string representation of the difficulty.
        '''

        return str(self.name)

class Page_Size(Enum):
    '''
    Enum Class to hold the information on the page size of a pdf document.

    Can have a value of A3, A4 or A5.
    '''

    A3 = 1
    A4 = 2
    A5 = 3

class I_Puzzle:
    '''
    Interface Class for a puzzle detailing the specifications for methods each puzzle type must have.
    '''

    def __str__(self):
        raise NotImplementedError("Subclass has not implemented this method!")

    def to_pdf(self, include_solution : bool, page_size : Page_Size, filepath : str) -> None:
        '''
        Method to convert the puzzle with proper formatting to a pdf document which can then be used by a user.

        Parameters:
            - include_solution - boolean indicating whether to include the solution on the page
            - page_size - the size of the page the pdf should be (Page_Size enum)
            - filepath - string filepath denoting where to save the pdf document to
        '''

        raise NotImplementedError("Subclass has not implemented this method!")

    def puzzle_to_pdf(self, page_size : Page_Size, filepath : str) -> None:
        '''
        Method to convert the puzzle to a pdf document.

        Parameters:
            - page_size - the size of the page the pdf should be (Page_Size enum)
            - filepath - string filepath denoting where to save the pdf document to
        '''

        raise NotImplementedError("Subclass has not implemented this method!")

    def solution_to_pdf(self, page_size : Page_Size, filepath : str) -> None:
        '''
        Method to convert the puzzle's solution to a pdf document.

        Parameters:
            - page_size - the size of the page the pdf should be (Page_Size enum)
            - filepath - string filepath denoting where to save the pdf document to
        '''

        raise NotImplementedError("Subclass has not implemented this method!")

    def puzzle_to_terminal(self) -> None:
        '''
        Method to print the puzzle to the console.
        '''

        raise NotImplementedError("Subclass has not implemented this method!")

    def solution_to_terminal(self) -> None:
        '''
        Method to print the puzzle's solution to the console.
        '''

        raise NotImplementedError("Subclass has not implemented this method!")

    def generate(self, difficulty : Difficulty) -> None:
        '''
        Method to generate a puzzle.

        Parameters:
            - difficulty - the level of difficulty the generated puzzle should have (Difficulty enum)
        '''

        raise NotImplementedError("Subclass has not implemented this method!")
