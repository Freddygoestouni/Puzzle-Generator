import datetime

# Imports from other parts of the project
from ..pdf import PDF
from .sudoku import Sudoku
from ..puzzle import Difficulty, Page_Size

class Sudoku_PDF(PDF):
    '''
    Class for PDF documents containing the sudoku puzzles. This extends the PDF class.
    '''

    def __init__(self, page_size : Page_Size) -> None:
        '''
        Method to create an instance of the Sudoku_PDF class.

        Parameters:
            - page_size - the page dimension (A3, A4 or A5)
        '''

        # Call the initialisation method of the parent (PDF) class
        super().__init__(page_size)

        # Set the title of the class to Sudoku
        self.set_title("Sudoku")

    def insert_puzzle(self, difficulty : Difficulty, seed : str, puzzle : Sudoku, solution=None) -> None:
        '''
        Method to insert a sudoku puzzle into the document.

        Parameters:
            - difficulty - Difficulty of the puzzle to be added to the document
            - seed - Seed of the sudoku puzzle to be added to the document
            - puzzle - Sudoku puzzle to be added to the document
            - solution (optional) - Solution to the sudoku puzzle, if one is given
        '''

        # Add a new page to the PDF document
        self.add_page()

        # Add the puzzle title and difficulty + seed information to the PDF document
        self.puzzle_title("Sudoku Puzzle", {"Difficulty" : str(difficulty), "Seed" : seed})

        # Add the puzzle to the PDF document
        self.__add_puzzle(puzzle)

        # If requested, add the solution to the PDF document
        if solution is not None and type(solution) is Sudoku:
            self.__add_solution(solution)

    def __add_puzzle(self, puzzle : Sudoku) -> None:
        '''
        Method to add a puzzle to the current page of the PDF document.

        Parameters:
            - puzzle - Sudoku puzzle to be added to the page
        '''

        # Dictionary of the styling for the sudoku puzzle grid
        styling = {
            Page_Size.A3 : {
                "cell_dim" : 22,
                "font_size" : 45,
                "thin_width" : 0.6,
                "thick_width" : 1.2
            },
            Page_Size.A4 : {
                "cell_dim" : 15,
                "font_size" : 25,
                "thin_width" : 0.4,
                "thick_width" : 0.9
            },
            Page_Size.A5 : {
                "cell_dim" : 9,
                "font_size" : 18,
                "thin_width" : 0.3,
                "thick_width" : 0.6
            }
        }

        # Calculate the starting x coordinate of the sudoku puzzle so that it is centered
        start_x = (self.page_size.width() - styling[self.page_size]["cell_dim"] * 9) / 2

        # Call the local method to add the puzzle grid to the specified location with specified styling
        self.__add_sudoku_grid(puzzle, styling, start_x, self.get_y())

    def __add_solution(self, solution : Sudoku) -> None:
        '''
        Method to add a solution to the current page of the PDF document.

        Parameters:
            - solution - Sudoku solution to be added to the page
        '''

        # Dictionary of the styling for the sudoku solution grid
        styling = {
            Page_Size.A3 : {
                "cell_dim" : 5,
                "font_size" : 9,
                "thin_width" : 0.15,
                "thick_width" : 0.5
            },
            Page_Size.A4 : {
                "cell_dim" : 4,
                "font_size" : 7,
                "thin_width" : 0.1,
                "thick_width" : 0.4
            },
            Page_Size.A5 : {
                "cell_dim" : 3,
                "font_size" : 5,
                "thin_width" : 0.05,
                "thick_width" : 0.3
            }
        }

        # Calculate the starting x and y coordinates of the solution grid to place it in the bottom right
        start_x = self.page_size.width() - styling[self.page_size]["cell_dim"] * 10 - self.r_margin
        start_y = self.page_size.height() - styling[self.page_size]["cell_dim"] * 10 - self.b_margin

        # Call the local method to add the solution grid to the specified location with specified styling
        self.__add_sudoku_grid(solution, styling, start_x, start_y)

    def __add_sudoku_grid(self, sudoku : Sudoku, styling : dict, start_x : int, start_y : int) -> None:
        '''
        Method to add a sudoku grid to the PDF document in a specified location

        Parameters:
            - sudoku - Sudoku class containing the grid information to be added
            - styling - Dictionary of the styling to be used for the sudoku grid
            - start_x - Starting x coordinate for the sudoku grid
            - start_y - Starting y coordinate for the sudoku grid
        '''

        # Set the starting coordinates of the sudoku grid
        self.set_xy(start_x, start_y)

        # Find the current coordinates in the PDF document
        x, y = self.get_x(), self.get_y()

        # Set the font of the sudoku grid
        self.set_font(family=self.font, style="", size=styling[self.page_size]["font_size"])

        # Set the line width for the border of each cell
        self.set_line_width(styling[self.page_size]["thin_width"])

        # Loop through the sudoku grid, adding each value as a bordered cell in the document
        for row in range(1, 10):
            for column in range(1, 10):
                self.cell(w=styling[self.page_size]["cell_dim"],
                             h=styling[self.page_size]["cell_dim"],
                             txt=str(sudoku.get_value(column, row)),
                             border=1,
                             ln=0 if column < 9 else 1,
                             align="C")

            # Every time a new line is needed, set the x location to the starting x location given
            self.set_x(start_x)

        # Set the line width to the thicker value used to outline the groups of cells
        self.set_line_width(styling[self.page_size]["thick_width"])

        # Loop through the locations to place the thicker lines
        for i in [0, 3, 6, 9]:
            # Add a vertical line
            self.line(x + i * styling[self.page_size]["cell_dim"],
                          y,
                          x + i * styling[self.page_size]["cell_dim"],
                          y + 9 * styling[self.page_size]["cell_dim"])

            # Add a horizontal line
            self.line(x,
                          y + i * styling[self.page_size]["cell_dim"],
                          x + 9 * styling[self.page_size]["cell_dim"],
                          y + i * styling[self.page_size]["cell_dim"])
