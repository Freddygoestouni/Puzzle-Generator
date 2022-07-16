"""
Tests for the Sudoku Class.
"""

from ..sudoku import Sudoku
from ..cell_value import Cell_Value
import random
import pytest
from io import StringIO
import sys

def test_from_seed():
    """
    Method to test the method to create a Sudoku from a given seed.

    The tests create a sudoku from a given seed and then check if all cells hold the correct values.
    """

    # Positive Case - Sudoku filled with one value
    for cell_value in [Cell_Value(value) for value in range(10)]:
        seed = "".join([cell_value.seed() * 81])

        sudoku = Sudoku(seed=seed)

        for index in range(81):
            row = index % 9 + 1
            column = int(index / 9) + 1

            assert sudoku.get_value(column, row) == cell_value

    # Positive Case - Sudoku with different randomly generated values
    for _ in range(100):
        cells = [Cell_Value(random.randint(0, 9)) for _ in range(81)]

        seed = "".join([cell.seed() for cell in cells])

        sudoku = Sudoku(seed=seed)

        for index in range(81):
            row = index % 9 + 1
            column = int(index / 9) + 1

            assert sudoku.get_value(column, row) == cells[index]

    # Negative Case - Too short seed length
    for length in range(0, 80):
        seed = "".join([Cell_Value.ONE.seed() * length])

        with pytest.raises(Exception) as exception:
            sudoku = Sudoku(seed=seed)
        assert "Invalid Seed" in str(exception.value)

    # Negative Case - Too long seed length
    for length in range(82, 200):
        seed = "".join([Cell_Value.ONE.seed() * length])

        with pytest.raises(Exception) as exception:
            sudoku = Sudoku(seed=seed)
        assert "Invalid Seed" in str(exception.value)

    # Negative case - Invalid seed characters
    for _ in range(100):
        seed = "".join([Cell_Value(random.randint(0, 9)).seed() * 81])

        for i in range(random.randint(1, 81)):
            index = random.randint(0, 80)
            character = chr(random.randint(0, 95))

            seed = list(seed)
            seed[index] = character
            seed = "".join(seed)

        with pytest.raises(Exception) as exception:
            sudoku = Sudoku(seed=seed)
        assert "Invalid Seed" in str(exception.value)

def test_get_seed():
    """
    Method to test the method to create a seed from a given Sudoku.

    The tests create a sudoku and compare the exepected seed to the given seed.
    """

    # Positive case - Check seed length
    sudoku = Sudoku()
    assert len(sudoku.get_seed()) == 81

    # Positive case - Sudoku filled with one value
    for cell_value in [Cell_Value(value) for value in range(10)]:
        expected_seed = "".join([cell_value.seed() * 81])

        sudoku = Sudoku()

        for index in range(81):
            row = index % 9 + 1
            column = int(index / 9) + 1

            sudoku.set_value(column, row, cell_value)

        assert sudoku.get_seed() == expected_seed

    # Positive Case - Sudoku with different randomly generated values
    for _ in range(100):
        cells = [Cell_Value(random.randint(0, 9)) for _ in range(81)]

        expected_seed = "".join([cell.seed() for cell in cells])

        sudoku = Sudoku()

        for index in range(81):
            row = index % 9 + 1
            column = int(index / 9) + 1

            sudoku.set_value(column, row, cells[index])

        assert sudoku.get_seed() == expected_seed

def test_clear():
    """
    Method to test the method to clear a Sudoku.

    The tests create a Sudoku and then clears it, checking all values are blank.
    """

    empty = Sudoku()

    # Positive case - empty sudoku
    sudoku = Sudoku()
    sudoku.clear()

    assert sudoku.get_seed() == empty.get_seed()

    for column in range(1, 10):
        for row in range(1, 10):
                assert sudoku.get_value(column, row) == Cell_Value.EMPTY

    # Positive case - non-empty sudoku (random)
    cells = [Cell_Value(random.randint(0, 9)) for _ in range(81)]
    seed = "".join([cell.seed() for cell in cells])
    sudoku = Sudoku(seed=seed)
    sudoku.clear()

    assert sudoku.get_seed() == empty.get_seed()

    for column in range(1, 10):
        for row in range(1, 10):
                assert sudoku.get_value(column, row) == Cell_Value.EMPTY

def test_get_set_value():
    """
    Method to test the methods to get and set a value from a given Sudoku.

    The tests create a blank sudoku and then sets and gets cell values in the Sudoku grid.
    """

    # Positive case - get values in blank Sudoku
    sudoku = Sudoku()

    for index in range(81):
        row = index % 9 + 1
        column = int(index / 9) + 1

        assert sudoku.get_value(column, row) == Cell_Value.EMPTY

    # Positive case - set random cells values in Sudoku grid and get value to check
    cells = [Cell_Value.EMPTY for _ in range(81)]
    for _ in range(1000):
        index = random.randint(0, 80)
        row = index % 9 + 1
        column = int(index / 9) + 1

        cell_value = Cell_Value(random.randint(0, 9))

        sudoku.set_value(column, row, cell_value)
        cells[index] = cell_value

        for i in range(81):
            r = i % 9 + 1
            c = int(i / 9) + 1

            assert sudoku.get_value(c, r) == cells[i]

    # Negative case - set cell to invalid cell value
    invalid_values = [0, 'a', "long", Sudoku(), -100, 0.002, (1, 2), {"dog": 1}, True, None, [0, 1, 2]]

    for value in invalid_values:
        with pytest.raises(Exception) as exception:
            sudoku = Sudoku()
            sudoku.set_value(1, 1, value)
        assert "Invalid Value" in str(exception.value)

    # Negative case - set non existent cell to a valid cell value
    invalid_cells = [(-1, -1), (0, 0), (10, 10), (1, 10), (-1, 5), (1.0, 2.5), (1.0, 5), (5, 1.0), ("a", 8)]

    for location in invalid_cells:
        with pytest.raises(Exception) as exception:
            sudoku = Sudoku()
            sudoku.set_value(location[0], location[1], Cell_Value.ONE)
        assert "Invalid Index" in str(exception.value)

    # Negative case - get non existent cell to a valid cell value
    for location in invalid_cells:
        with pytest.raises(Exception) as exception:
            sudoku = Sudoku()
            _ = sudoku.get_value(location[0], location[1])
        assert "Invalid Index" in str(exception.value)

def test_get_row_values():
    """
    Method to test the method to create a get a list of values in a row from a given Sudoku.

    The tests create a sudoku and compares the inserted values to the list of values in a row
    """

    # Positive case - empty sudoku
    sudoku = Sudoku()
    for row in range(1, 10):
        values = sudoku.get_row_values(row)

        assert len(values) == 1
        assert values[0] == Cell_Value.EMPTY

    # Positive case - sudoku where all values are the same cell value. (Generated using seed)
    for cell_value in [Cell_Value(value) for value in range(10)]:
        seed = "".join([cell_value.seed() * 81])

        sudoku = Sudoku(seed=seed)

        for row in range(1, 10):
            values = sudoku.get_row_values(row)

            assert len(values) == 1
            assert values[0] == cell_value

    # Positive case - sudoku where all values are random cell values
    cells = [Cell_Value(random.randint(0, 9)) for _ in range(81)]
    seed = "".join([cell.seed() for cell in cells])
    sudoku = Sudoku(seed=seed)

    for row in range(1, 10):
        values = sudoku.get_row_values(row)

        expected = list(set([sudoku.get_value(column, row) for column in range(1, 10)]))

        assert len(values) == len(expected)
        assert set(values) == set(expected)

    # Positive case - sudoku where all values are random cell values with ignore
    cells = [Cell_Value(random.randint(0, 9)) for _ in range(81)]
    seed = "".join([cell.seed() for cell in cells])
    sudoku = Sudoku(seed=seed)

    for row in range(1, 10):
        for ignore in range(1, 10):
            values = sudoku.get_row_values(row, ignore=ignore)

            columns = list(range(1, 10))
            columns.remove(ignore)
            expected = list(set([sudoku.get_value(column, row) for column in columns]))

            assert len(values) == len(expected)
            assert set(values) == set(expected)

    # Negative case - invalid row number
    for row in [-10, -1, 0, 10, 11, 1.0, 2.5, "One", Cell_Value.ONE, Sudoku()]:
        with pytest.raises(Exception) as exception:
            sudoku = Sudoku()
            sudoku.get_row_values(row)
        assert "Invalid Index" in str(exception.value)

    # Negative case - invalid ignore column number
    for ignore in [-10, -1, 0, 10, 11, 1.0, 2.5, "One", Cell_Value.ONE, Sudoku()]:
        with pytest.raises(Exception) as exception:
            sudoku = Sudoku()
            sudoku.get_row_values(random.randint(1, 9), ignore=ignore)
        assert "Invalid Index" in str(exception.value)

def test_get_column_values():
    """
    Method to test the method to create a get a list of values in a column from a given Sudoku.

    The tests create a sudoku and compares the inserted values to the list of values in a column
    """

    # Positive case - empty sudoku
    sudoku = Sudoku()
    for row in range(1, 10):
        values = sudoku.get_column_values(row)

        assert len(values) == 1
        assert values[0] == Cell_Value.EMPTY

    # Positive case - sudoku where all values are the same cell value. (Generated using seed)
    for cell_value in [Cell_Value(value) for value in range(10)]:
        seed = "".join([cell_value.seed() * 81])

        sudoku = Sudoku(seed=seed)

        for column in range(1, 10):
            values = sudoku.get_column_values(column)

            assert len(values) == 1
            assert values[0] == cell_value

    # Positive case - sudoku where all values are random cell values
    cells = [Cell_Value(random.randint(0, 9)) for _ in range(81)]
    seed = "".join([cell.seed() for cell in cells])
    sudoku = Sudoku(seed=seed)

    for column in range(1, 10):
        values = sudoku.get_column_values(column)

        expected = list(set([sudoku.get_value(column, row) for row in range(1, 10)]))

        assert len(values) == len(expected)
        assert set(values) == set(expected)

    # Positive case - sudoku where all values are random cell values with ignore
    cells = [Cell_Value(random.randint(0, 9)) for _ in range(81)]
    seed = "".join([cell.seed() for cell in cells])
    sudoku = Sudoku(seed=seed)

    for column in range(1, 10):
        for ignore in range(1, 10):
            values = sudoku.get_column_values(column, ignore=ignore)

            rows = list(range(1, 10))
            rows.remove(ignore)
            expected = list(set([sudoku.get_value(column, row) for row in rows]))

            assert len(values) == len(expected)
            assert set(values) == set(expected)

    # Negative case - invalid column number
    for column in [-10, -1, 0, 10, 11, 1.0, 2.5, "One", Cell_Value.ONE, Sudoku()]:
        with pytest.raises(Exception) as exception:
            sudoku = Sudoku()
            sudoku.get_column_values(column)
        assert "Invalid Index" in str(exception.value)

    # Negative case - invalid ignore row number
    for ignore in [-10, -1, 0, 10, 11, 1.0, 2.5, "One", Cell_Value.ONE, Sudoku()]:
        with pytest.raises(Exception) as exception:
            sudoku = Sudoku()
            sudoku.get_column_values(random.randint(1, 9), ignore=ignore)
        assert "Invalid Index" in str(exception.value)

def test_get_box_values():
    """
    Method to test the method to create a get a list of values in a box from a given Sudoku.

    The tests create a sudoku and compares the inserted values to the list of values in a box
    """

    # Transformation of coordinate to the top left box coordinate
    box_coordinates = {1:1, 2:1, 3:1, 4:4, 5:4, 6:4, 7:7, 8:7, 9:7}

    # Positive case - empty sudoku
    sudoku = Sudoku()
    for row in range(1, 10):
        for column in range(1, 10):
            values = sudoku.get_box_values(column, row)

            assert len(values) == 1
            assert values[0] == Cell_Value.EMPTY

    # Positive case - sudoku where all values are the same cell value. (Generated using seed)
    for cell_value in [Cell_Value(value) for value in range(10)]:
        seed = "".join([cell_value.seed() * 81])

        sudoku = Sudoku(seed=seed)

        for row in range(1, 10):
            for column in range(1, 10):
                values = sudoku.get_box_values(column, row)

                assert len(values) == 1
                assert values[0] == cell_value

    # Positive case - sudoku where all values are random cell values
    cells = [Cell_Value(random.randint(0, 9)) for _ in range(81)]
    seed = "".join([cell.seed() for cell in cells])
    sudoku = Sudoku(seed=seed)

    for row in range(1, 10):
        for column in range(1, 10):
            values = sudoku.get_box_values(column, row)

            expected = []
            for r in range(box_coordinates[row], box_coordinates[row]+3):
                for c in range(box_coordinates[column], box_coordinates[column]+3):
                    expected += [sudoku.get_value(c, r)]
            expected = list(set(expected))

            assert len(values) == len(expected)
            assert set(values) == set(expected)

    # Positive case - sudoku where all values are random cell values with ignore
    cells = [Cell_Value(random.randint(0, 9)) for _ in range(81)]
    seed = "".join([cell.seed() for cell in cells])
    sudoku = Sudoku(seed=seed)

    for row in range(1, 10):
        for column in range(1, 10):
            values = sudoku.get_box_values(column, row, ignore=True)

            expected = []
            for r in range(box_coordinates[row], box_coordinates[row]+3):
                for c in range(box_coordinates[column], box_coordinates[column]+3):
                    if r == row and c == column: continue
                    expected += [sudoku.get_value(c, r)]
            expected = list(set(expected))

            assert len(values) == len(expected)
            assert set(values) == set(expected)

    # Negative case - invalid column and row number
    for column in [-10, -1, 0, 10, 11, 1.0, 2.5, "One", Cell_Value.ONE, Sudoku()]:
        for row in [-10, -1, 0, 10, 11, 1.0, 2.5, "One", Cell_Value.ONE, Sudoku()]:
            with pytest.raises(Exception) as exception:
                sudoku = Sudoku()
                sudoku.get_box_values(column, row)
            assert "Invalid Index" in str(exception.value)

    # Negative case - invalid ignore
    for ignore in [-10, -1, 0, 1, 2, 10, 11, 1.0, 2.5, "One", Cell_Value.ONE, Sudoku()]:
        with pytest.raises(Exception) as exception:
            sudoku = Sudoku()
            sudoku.get_box_values(random.randint(1, 9), random.randint(1, 9), ignore=ignore)
        assert "Invalid Ignore" in str(exception.value)

def test_cell_options():
    """
    Method to test the method to get a list of valid options for a cell from a given Sudoku.

    The tests create a sudoku and compares the list of options to an expected list.
    """

    # Positive case - empty sudoku
    sudoku = Sudoku()
    for row in range(1, 10):
        for column in range(1, 10):
            options = sudoku.cell_options(column, row)

            assert len(options) == 9
            assert set(options) == set([Cell_Value(value) for value in range(1, 10)])

    # Positive case - sudoku where all values are the same cell value. (Generated using seed)
    for cell_value in [Cell_Value(value) for value in range(1, 10)]:
        seed = "".join([cell_value.seed() * 81])

        sudoku = Sudoku(seed=seed)

        for row in range(1, 10):
            for column in range(1, 10):
                options = sudoku.cell_options(column, row)

                assert len(options) == 8
                assert set(options) == set([Cell_Value(value) for value in range(1, 10)]) - set([cell_value])

    # Negative case - invalid column and row number
    for column in [-10, -1, 0, 10, 11, 1.0, 2.5, "One", Cell_Value.ONE, Sudoku()]:
        for row in [-10, -1, 0, 10, 11, 1.0, 2.5, "One", Cell_Value.ONE, Sudoku()]:
            with pytest.raises(Exception) as exception:
                sudoku = Sudoku()
                sudoku.cell_options(column, row)
            assert "Invalid Index" in str(exception.value)

def test_valid():
    """
    Method to test the method to determine if the sudoku is valid or not.

    The tests create a sudoku and checks to see if the method can correctly identify if it is valid.
    """

    # Positive case - valid sudoku's (given by seed)
    # Sudoku 1 - empty (empty cells are valid)
    sudoku = Sudoku()
    assert sudoku.valid(empty_as_valid=True) == True

    # Sudoku 2 - valid sudoku seeds
    valid_seeds = ["ijelhkmfggkmifejlhhflmjgekijegklmihfkmhjifgellifeghkmjmgihklfjeehjfmilgkflkgejhim",
                           "eifhlmgkjkgmfijlhehjlgkefmiglkefhjimimekjghflfhjlmikegmehjgkilfjfimhlegklkgiefmjh",
                           "hgifjmklejlfikehmgemklghijflfjemighkgkhjlfmeimiekhgjfliemgfjlkhfhlmikegjkjghelfim",
                           "fihkmjglelmgehfjikkejlgifmhigmjlhekfjflikehgmehkmfgljihligekmfjgkfhjmielmjefilkhg",
                           "ekfhlgjimgilmjekfhhmjkfielgfhklemigjmgijkhfelljeigfmhkkfhgijlmejemfhlgkiilgemkhjf"]

    for seed in valid_seeds:
        sudoku = Sudoku(seed=seed)

        assert sudoku.valid() == True
        assert sudoku.valid(empty_as_valid=True) == True

    # Negative case - invalid sudoku's (given by seed)
    # Sudoku 1 - empty (empty cells are not valid)
    sudoku = Sudoku()
    assert sudoku.valid() == False

    # Sudoku 2 - same cell value in all cells
    for cell_value in [Cell_Value(value) for value in range(1, 10)]:
        seed = "".join([cell_value.seed() * 81])

        sudoku = Sudoku(seed=seed)

        assert sudoku.valid() == False
        assert sudoku.valid(empty_as_valid=True) == False

    # Sudoku 3 - duplicate row values
    seed = "ijelhkmfgikmifejlhhflmjgekijegklmihfkmhjifgellifeghkmjmgihklfjeehjfmilgkflkgejhim"
    sudoku = Sudoku(seed=seed)

    assert sudoku.valid() == False
    assert sudoku.valid(empty_as_valid=True) == False

    # Sudoku 4 - duplicate column values
    seed = "iielhkmfggkmifejlhhflmjgekijegklmihfkmhjifgellifeghkmjmgihklfjeehjfmilgkflkgejhim"
    sudoku = Sudoku(seed=seed)

    assert sudoku.valid() == False
    assert sudoku.valid(empty_as_valid=True) == False

    # Sudoku 5 - duplicate box values
    seed = "ijelhkmfggimifejlhhflmjgekijegklmihfkmhjifgellifeghkmjmgihklfjeehjfmilgkflkgejhim"
    sudoku = Sudoku(seed=seed)

    assert sudoku.valid() == False
    assert sudoku.valid(empty_as_valid=True) == False

    # Sudoku 6 - invalid sudoku seeds
    invalid_seeds = ["jfhijkmgelkemglhifimghefjlkfjmkligehhelfmgkjikgiehjlfmmijgfheklelkjimfhgghflkeimj",
                              "igehmkljfmjhiflkegkfkegjhimlmlgihefjgeijkfmhljhfmlegkiekmljifghhigfemjlkfljkhgime",
                              "hilgfekjmemgjkihlfjkfhlmiegkijegfmhlfelmihgkjmghkjlfiegjeimklfhifmlhjegklhkfegjmi",
                              "hegflmikjlkmgijhfefiejhkmgliflmkegjhejkhgiflmgmhljfeikmhikfljegkgfjehlmijleimgkhf",
                              "ffgjmlihklhmfkigjejkiheglfmmihegfkljgelkjhfmikjflimhegfgjmhkeilhmkilejgfilegfjmkh"]

    for seed in invalid_seeds:
        sudoku = Sudoku(seed=seed)

        assert sudoku.valid() == False
        assert sudoku.valid(empty_as_valid=True) == False

def test_print_terminal():
    """
    Method to test the method to get a list of valid options for a cell from a given Sudoku.

    The tests create a sudoku and compares the list of options to an expected list.
    """

    # Positive case - empty sudoku small print
    sudoku = Sudoku()
    # Capture the standard output stream
    capturedOutput = StringIO()
    sys.stdout = capturedOutput

    sudoku.print_terminal(size="small")

    characters = [character for character in capturedOutput]
    for char in characters:
        assert char.isdigit() == False
    # Make the standard output go back to the normal stream
    sys.stdout = sys.__stdout__

    # Positive case - empty sudoku large print
    sudoku = Sudoku()
    # Capture the standard output stream
    capturedOutput = StringIO()
    sys.stdout = capturedOutput

    sudoku.print_terminal(size="big")

    characters = [character for character in capturedOutput]
    for char in characters:
        assert char.isdigit() == False
    # Make the standard output go back to the normal stream
    sys.stdout = sys.__stdout__

    # Positive case - single value sudoku small print
    for cell_value in [Cell_Value(value) for value in range(1, 10)]:
        seed = "".join([cell_value.seed() * 81])
        sudoku = Sudoku(seed=seed)
        # Capture the standard output stream
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        sudoku.print_terminal(size="small")

        characters = [character for character in capturedOutput]
        for char in characters:
            assert char.isdigit() == False or int(char) == cell_value.value

        # Make the standard output go back to the normal stream
        sys.stdout = sys.__stdout__

    # Positive case - single value sudoku large print
    for cell_value in [Cell_Value(value) for value in range(1, 10)]:
        seed = "".join([cell_value.seed() * 81])
        sudoku = Sudoku(seed=seed)
        # Capture the standard output stream
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        sudoku.print_terminal(size="big")

        characters = [character for character in capturedOutput]
        for char in characters:
            assert char.isdigit() == False or int(char) == cell_value.value

        # Make the standard output go back to the normal stream
        sys.stdout = sys.__stdout__

    # Negative case - invalid size
    for size in [0, 1, 2, 2.0, True, False, "Large", None, Sudoku(), Cell_Value.ONE]:
        with pytest.raises(Exception) as exception:
            sudoku = Sudoku()
            sudoku.print_terminal(size=size)
        assert "Invalid Size" in str(exception.value)
