import pandas as pd
import numpy as np
from time import time
from sudoku_env.sql_env import sudoku_sql
from sudoku_env.tools import *
from copy import deepcopy

### Solving using all known strategies
### If no strategy works, do one assumption each time
### The goal is to minimize the required number of assumptions
### We need a candidate table for this solver

# connect to SQLite database
db = sudoku_sql()

def clean_candidates(puzzle, candidates, show=False):
    new_candidates = deepcopy(candidates)
    for i in range(81):
        if puzzle[i] == '0':
            for idx in row_idx(i)+col_idx(i)+grid_idx(i):
                if idx == i:
                    continue
                else:
                    num = puzzle[idx]
                    try:
                        new_candidates[i].remove(num)
                    except:
                        pass
        else:
            new_candidates[i] = []
    
    if show:
        for idx in range(81):
            print(f'{''.join(new_candidates[idx]):8s}', end='| ')
            if idx%9 == 8:
                print('')
    return new_candidates

#### STRATEGY FUNCTIONS STARTS FROM HERE
def last_free(puzzle, candidates):
    '''Insert the only candidate of each cell into the puzzle
    
    Containing strategies: Last Free Cell, Last Possible Number, Naked Single'''
    new_puzzle = deepcopy(puzzle)
    new_candidates = deepcopy(candidates)
    for idx in range(81):
        if len(candidates[idx]) == 1:
            assert new_puzzle[idx] == '0'
            new_puzzle[idx] = candidates[idx][0]
            new_candidates[idx] = []
    return new_puzzle, new_candidates

def hidden(puzzle, candidates):
    '''Insert the candidate that appears in exactly one position in a row, column, or grid

    Containind strategies: Cross Hatching, Hidden Single'''
    new_puzzle = deepcopy(puzzle)
    new_candidates = deepcopy(candidates)
    groups = [col_idx(i) for i in range(9)]\
            +[row_idx(9*i) for i in range(9)]\
            +[grid_idx(9*3*r+3*c) for r in range(3) for c in range(3)]
    for group in groups: # check rows, columns, and grids
        for i in range(1,10):
            num = str(i)
            found = False
            for idx in group:
                if num in new_candidates[idx]:
                    if not found:
                        found = True
                        the_idx = idx
                    else:
                        found = False
                        break
            if found:
                new_puzzle[the_idx] = num
                new_candidates[idx] = []
    return new_puzzle, new_candidates

#### END OF STRATEGIES


def strategic(puzzle, show=False):
    candidates = [[str(i) for i in range(1,10)] for idx in range(81)]
    count = 0
    while True:
        candidates = clean_candidates(puzzle, candidates, show)
        new_puzzle, new_candidates = last_free(puzzle, candidates)
        #new_puzzle, new_candidates = puzzle, candidates
        if new_puzzle != puzzle:
            count += 1
            puzzle = new_puzzle
            candidates = new_candidates
            if show:
                print(f'Progressed count: {count}')
        else:
            new_puzzle, new_candidates = hidden(puzzle, candidates)
            if new_puzzle != puzzle:
                count += 1
                puzzle = new_puzzle
                candidates = new_candidates
            else:
                if show:
                    print('End of solving without assumptions')
                return new_puzzle, new_candidates


n = 10000
select_puzzle = pd.read_sql(f'SELECT * FROM sudoku LIMIT {n}', db)

#puzzle = select_puzzle['puzzle'][0]
#puzzle = list(puzzle)
#puzzle[47] = '6'
#solution = select_puzzle['solution'][0]

#print_puzzle(solution, "Solution")
#print_puzzle(puzzle, "Original")

puzzles = select_puzzle['puzzle']
solutions = select_puzzle['solution']

count = 0

for i in range(n):
    puzzle = puzzles[i]
    solution = solutions[i]
    result, candidates = strategic(list(puzzle))
    #print_puzzle(result)

    #print(f'Successfully solved: {result==list(solution)}')

    if result==list(solution):
        count += 1

print(f'Total number of puzzles : {n}')
print(f'Successfully solved     : {count}')
print(f'Success rate            : {count/n}')
#print_puzzle(result)