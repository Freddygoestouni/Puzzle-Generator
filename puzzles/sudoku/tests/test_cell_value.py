"""
Tests for the Cell Value Enum Class.
"""

from ..cell_value import Cell_Value

def test_str():
    """
    Method to test the method to give the string representation of a Cell Value.

    The tests create a cell value and checks the string representation.
    """

    assert str(Cell_Value.EMPTY) == " "
    assert str(Cell_Value.ONE) == "1"
    assert str(Cell_Value.TWO) == "2"
    assert str(Cell_Value.THREE) == "3"
    assert str(Cell_Value.FOUR) == "4"
    assert str(Cell_Value.FIVE) == "5"
    assert str(Cell_Value.SIX) == "6"
    assert str(Cell_Value.SEVEN) == "7"
    assert str(Cell_Value.EIGHT) == "8"
    assert str(Cell_Value.NINE) == "9"

def test_seed():
    """
    Method to test the method to give the seed representation of a Cell Value.

    The tests create a cell value and checks the seed representation.
    """

    assert Cell_Value.EMPTY.seed() == "d"
    assert Cell_Value.ONE.seed() == "e"
    assert Cell_Value.TWO.seed() == "f"
    assert Cell_Value.THREE.seed() == "g"
    assert Cell_Value.FOUR.seed() == "h"
    assert Cell_Value.FIVE.seed() == "i"
    assert Cell_Value.SIX.seed() == "j"
    assert Cell_Value.SEVEN.seed() == "k"
    assert Cell_Value.EIGHT.seed() == "l"
    assert Cell_Value.NINE.seed() == "m"

def test_create():
    """
    Method to test the ways of creating a Cell Value.

    The tests create a cell value using different methods checking they are identical.
    """

    assert Cell_Value.EMPTY == Cell_Value(0)
    assert Cell_Value.ONE == Cell_Value(1)
    assert Cell_Value.TWO == Cell_Value(2)
    assert Cell_Value.THREE == Cell_Value(3)
    assert Cell_Value.FOUR == Cell_Value(4)
    assert Cell_Value.FIVE == Cell_Value(5)
    assert Cell_Value.SIX == Cell_Value(6)
    assert Cell_Value.SEVEN == Cell_Value(7)
    assert Cell_Value.EIGHT == Cell_Value(8)
    assert Cell_Value.NINE == Cell_Value(9)
