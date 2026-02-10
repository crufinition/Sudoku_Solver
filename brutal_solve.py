import pandas as pd
from time import time
from sudoku_env.sql_env import sudoku_sql
from sudoku_env.tools import *

# connect to SQLite database
db = sudoku_sql()

def brutal(puzzle, idx=0, info=False):
    ''' Solve the given puzzle using brutal force
    Iterate through all possible sombinations
    May optimize the process by directly eliminate impossible numbers

    ==== Parameters ====
    puzzle: current puzzle
    idx: current position
    start: the number to start guessing
    prev: previous index being guessed
    '''
    success_info = 'Result found, please check if it is indeed the solution'
    if puzzle[idx] == "0": # put in guesses

        # loop from start number
        for n in range(1, 10):
            puzzle[idx] = str(n)

            # validate for current guess
            if check(idx, puzzle): # legal board
                if idx != 80: # continue guessing
                    result = brutal(puzzle, idx=idx+1)
                    if result: # continue guessing and found solution
                        return result
                else: # solution found at the end of puzzle being guessed
                    if info:
                        print(success_info)
                    return ''.join(puzzle)

        # used up all possibilities
        # return to previous guess
        puzzle[idx] = '0'
        return False
        
    elif idx != 80: # continue guessing
        result = brutal(puzzle, idx+1)
        if result:
            return result
        
    else: # all empty cells fillled
        if info:
            print(success_info)
        return ''.join(puzzle)

select_puzzle = pd.read_sql('''SELECT *
                            FROM sudoku
                            ORDER BY
                            RANDOM()
                            LIMIT 1
                            ''', db)

puzzle = select_puzzle['puzzle'][0]
solution = select_puzzle['solution'][0]

print_puzzle(solution, "Solution")
print_puzzle(puzzle, "Original")

start_time = time()
result = brutal(list(puzzle))
end_time = time()

print_puzzle(result, "Result")

print(f"Correct solution: {solution == result}")
print(f"Required time: {end_time-start_time} seconds\n")
