"""
Tests for the Seed Manager Class.
"""

from ..seed_manager import *
import os
import pytest

# List of valid unique seeds to be used in testing
seeds = ["ijelhkmfggkmifejlhhflmjgekijegklmihfkmhjifgellifeghkmjmgihklfjeehjfmilgkflkgejhim",
              "eifhlmgkjkgmfijlhehjlgkefmiglkefhjimimekjghflfhjlmikegmehjgkilfjfimhlegklkgiefmjh",
              "hgifjmklejlfikehmgemklghijflfjemighkgkhjlfmeimiekhgjfliemgfjlkhfhlmikegjkjghelfim",
              "fihkmjglelmgehfjikkejlgifmhigmjlhekfjflikehgmehkmfgljihligekmfjgkfhjmielmjefilkhg"]

def setup():
    """
    Method to setup the seeds file for the tests to be run.

    This will setup a fake seeds file for the tests to use instead.
    """

    # Create a new seeds file
    file = open(file_name, "w")

    # Add the seeds to the file
    file.write("\n".join(seeds))

    # Close the connection to the file
    file.close()

def set_down():
    """
    Method to reverse the setup for the test seeds file.

    This will remove the test seeds file.
    """

    # Remove the seeds file
    os.remove(file_name)

def test_get_seed():
    """
    Method to test getting a seed from the seed file.

    This replaces the contents of the seed file and checks to ensure that the method can read the
    new file correctly
    """

    # Call the setup function
    setup()

    # Positive case - valid indexes
    for i in range(len(seeds)):
        assert get_seed(index=i) == seeds[i]

    # Positive case - random seed
    for _ in range(100):
        assert get_seed() in seeds

    # Negative case - invalid index
    for index in [-3, -2, -1, 4, 5, 6, 1.0, "index", False]:
        with pytest.raises(Exception) as exception:
            get_seed(index=index)
        assert "Invalid Index" in str(exception.value)

    # Call the set down function to reverse the setup
    set_down()

def test_save_seed():
    """
    Method to test saving a seed to the seed file.

    This tries to save seeds to the file that are valid and invalid
    """

    # Call the setup function
    setup()

    # Positive case - Valid unique seed
    save_seed("ekfhlgjimgilmjekfhhmjkfielgfhklemigjmgijkhfelljeigfmhkkfhgijlmejemfhlgkiilgemkhjf")

    # Negative case - Duplicate seed
    for seed in seeds:
        with pytest.raises(Exception) as exception:
            save_seed(seed)
        assert "Duplicate Seed" in str(exception.value)

    # Negative case - Invalid seed
    for seed in [True, 1, 2.0, "sadnasdnasd", "ekfhlgjimgilmjekfkhmjkfielgfhklemigjmgijkhfelljeigfmhkkfhgijlmejemfhlgkiilgemkhjf"]:
        with pytest.raises(Exception) as exception:
            save_seed(seed)
        assert "Invalid Seed" in str(exception.value)

    # Call the set down function to reverse the setup
    set_down()

# Takes too long
# def test_mutate_seed():
#     """
#     Method to test getting all the valid mutations of a seed.
#
#     This checks that all valid mutations of a seed are found.
#     """
#
#     file = open(file_name, "w")
#     file.close()
#
#     # Mutate a short seed
#     mutate_seed("defg")
#
#     # Read the list of mutated seeds found
#     file = open(file_name, "r")
#     seeds = file.readlines()
#     file.close()
#
#     assert len(seeds) == 1

def test_swap():
    """
    Method to swapping two values in a seed.

    This checks that the values are swapped properly.
    """

    assert "aabb" == swap("bbaa", "a", "b")
    assert "aabb" == swap("bbaa", "b", "a")
    assert "aabb" == swap(swap("aabb", "a", "b"), "a", "b")
    assert "aabbccdd" == swap("bbaaccdd", "a", "b")
