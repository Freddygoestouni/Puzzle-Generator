from fpdf import FPDF
import datetime

# Imports from other parts of the project
from .puzzle import Difficulty, Page_Size

class PDF(FPDF):
    '''
    Class for PDF documents containing the puzzles.
    '''

    def __init__(self, page_size : Page_Size) -> None:
        '''
        Method to create an instance of the PDF class.

        Parameters:
            - page_size - the page dimension (A3, A4 or A5)
        '''

        # Call the initialisation method of the parent class to initialise the pdf document
        super().__init__(format=str(page_size))

        # Set the page size as a class variable to be used when adding content to the pdf
        self.page_size = page_size

        # Define the font of the document
        self.font = "Times"

        # Set the title, subject, creator and author of the PDF document
        self.set_title("Puzzles")
        self.set_subject("A collection of programmatically generated puzzles")
        self.set_creator("Puzzle Generator v1.0")
        self.set_author("Puzzle Generator v1.0")

    def puzzle_title(self, puzzle_name : str, key_values : dict) -> None:
        '''
        Method to add information on the puzzle as the title of a page. This is standardised across all
        puzzles.

        Parameters:
            - puzzle_name - The name of the puzzle type
            - key_values - A dictionary of key value pairs of information to be included in the title
                                  (e.g. Difficulty, seed, instructions, ...)
        '''

        # Dictionary of the styling for the title
        styling = {
            Page_Size.A3 : {
                "title_height" : 40,
                "title_font_size" : 50,
                "other_height" : 10,
                "other_font_size" : 15,
                "gap" : 20
            },
            Page_Size.A4 : {
                "title_height" : 30,
                "title_font_size" : 35,
                "other_height" : 6,
                "other_font_size" : 11,
                "gap" : 15
            },
            Page_Size.A5 : {
                "title_height" : 20,
                "title_font_size" : 25,
                "other_height" : 4,
                "other_font_size" : 7,
                "gap" : 10
            }
        }

        # Set the font for the title of the puzzle
        self.set_font(family=self.font, style="", size=styling[self.page_size]["title_font_size"])

        # Write the puzzle title
        self.cell(w=0,
                     h=styling[self.page_size]["title_height"],
                     txt=puzzle_name,
                     border=0,
                     ln=1,
                     align="C")

        # Set the font for the key-value information of the puzzle
        self.set_font(family=self.font, style="", size=styling[self.page_size]["other_font_size"])

        # Loop through the dictionary, writing the key value pair information
        for key in key_values.keys():
            self.cell(w=0,
                         h=styling[self.page_size]["other_height"],
                         txt=f"{str(key)}: {str(key_values[key])}",
                         border=0,
                         ln=1,
                         align="L")

        # Add the gap between the title and the puzzle
        self.ln(h=styling[self.page_size]["gap"])

    def footer(self) -> None:
        '''
        Method to add the footer to the pdf document. This details the application name and the
        time that the puzzle was generated.
        '''

        # Dictionary of the styling for the footer
        styling = {
            Page_Size.A3 : {
                "height" : 14,
                "font_size" : 14,
            },
            Page_Size.A4 : {
                "height" : 11,
                "font_size" : 11,
            },
            Page_Size.A5 : {
                "height" : 8,
                "font_size" : 8,
            }
        }

        # Set the location for the footer
        self.set_y(-15)

        # Set the font for the footer
        self.set_font(self.font, style="", size=styling[self.page_size]["font_size"])

        # Write the text of the footer in the bottom right corner of the page
        self.cell(w=0,
                     h=styling[self.page_size]["height"],
                     txt=f"Generated by Puzzle Generator v1.0 at {datetime.datetime.now():%d-%m-%Y %H:%M}",
                     border=0,
                     ln=0,
                     align="R")