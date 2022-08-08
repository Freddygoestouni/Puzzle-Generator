from .sudoku import Sudoku
from .cell_value import Cell_Value
import random
import re
import os

# Seed file
file_name = os.path.join("puzzles", "sudoku", "seeds.txt")

def get_seed(index:int=None) -> str:
    '''
    Method to load a seed from the list of valid seeds stored in the seeds file.

    Parameters:
        - index (optional) - index of the seed, if none given, it chooses a random index

    Returns:
        - the seed loaded from the seed file
    '''

    # Open the seed file
    file = open(file_name, "r")

    # Get a list of all the seeds
    lines = file.readlines()

    # Check the input for index is valid
    if index is not None:
        if type(index) is not int or index < 0 or index >= len(lines):
            file.close()
            raise Exception("Invalid Index")

    # If the seed index is not specified, find a random index
    if index is None:
        index = random.randint(0, len(lines) - 1)

    # Read the line containing the requested seed
    seed = lines[index]

    # Remove the line ending character (if present)
    seed = seed.replace("\n", "")

    # Close the seed file
    file.close()

    # Return the seed
    return seed

def save_seed(seed:str) -> None:
    '''
    Method to save a seed into the list of valid seeds stored in the seeds file.
    This checks if the seed is valid and is already in the file before saving it.

    Parameters:
        - seed - valid seed of a sudoku
    '''

    # Check that the seed is valid
    if not type(seed) == str or not Sudoku(seed).valid():
        raise Exception("Invalid Seed")

    # Open the seed file for reading
    file = open(file_name, "r")

    # Check that the seed is not already in the file
    for line in file.readlines():
        if seed in line:
            file.close()
            raise Exception("Duplicate Seed")

    # Close the seed file
    file.close()

    # Open the seed file for appending
    file = open(file_name, "a")

    # Write the seed to the end of the file
    file.write(seed + "\n")

    # Close the seed file
    file.close()

def generate_seeds() -> None:
    '''
    Method to generate a valid sudoku seeds and add them to the seed list file
    '''

    sudoku = Sudoku()

    seeds = sudoku.fill(clear=True, find_all=True)

    for seed in seeds:
        save_seed(seed)

def mutate_seed(seed:str):
    '''
    Method to generate a valid sudoku seeds and add them to the seed list file

    Parameters:
        - seed - seed to mutate
    '''

    # List of seed forms of all cell values
    values = [Cell_Value(i).seed() for i in range(1, 10)]

    # List of new mutated seeds found
    seeds = list()

    # Loop throguh all distinct pairs of values to try swapping
    for val_one in values:
        for val_two in values:
            if val_one == val_two: continue

            # Swap the two values
            mutated = swap(seed, val_one, val_two)

            # Check if the seed is already found
            try:
                save_seed(mutated)
                seeds += [mutated]
            except:
                pass

    # Loop through the new seeds found and find mutated versions
    for seed in seeds:
        mutate_seed(seed)

def swap(seed:str, val_one:str, val_two:str) -> str:
    '''
    Method to swap two values from a seed to create a new seed

    Parameters:
        - seed - seed to mutate
        - val_one - first value to be used in the swap
        - val_two - second value to be used in the swap

    Returns:
        - mutated seed with the value swapped
    '''

    # Replace all instances of value one with value two
    mutated = seed.replace(val_one, val_two)

    # Convert the new seed to a list
    mutated = list(mutated)

    # Loop through all indices of value two and swap them with value one
    for index in [index.start() for index in re.finditer(pattern=val_two, string=seed)]:
        mutated[index] = val_one

    # Return the mutated seed in string form
    return "".join(mutated)
