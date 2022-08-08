from .sudoku import Sudoku
import random

# Seed file
file_name = "seeds.txt"

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

    # If the seed index is not specified, find a random index
    if index is None:
        index = random.randint(0, len(lines))

    # Read the line containing the requested seed
    seed = lines[index]

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
    if not typ(seed) == str or not Sudoku(seed).valid():
        raise Exception("Invalid Seed")

    # Open the seed file
    file = open(file_name, "a")

    # Check that the seed is not already in the file
    for line in file.readlines():
        if line == seed:
            raise Exception("Duplicate Seed")

    # Write the seed to the end of the file
    file.write(seed)

    # Close the seed file
    file.close()

def generate_seeds() -> None:
    '''
    Method to generate a valid sudoku seeds and add them to the seed list file
    '''

    sudoku = Sudoku()

    seeds = sudoku.fill(clear=True, find_all=True)
    print(seeds)

    for seed in seeds:
        save_seed(seed)

def mutate_seed(seed:str) -> list:


    seeds = list()
