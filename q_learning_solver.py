import numpy as np
import pandas as pd
#from random import randint
from time import time
from sudoku_env.sql_env import sudoku_sql
from sudoku_env.tools import *

# connect to SQLite database

data = pd.read_sql('SELECT * FROM sudoku LIMIT 1', db)
puzzle = list(data['puzzle'][0])

print_puzzle(puzzle)


def reward(idx, puzzle):
    '''The hand crafted reward function'''
    return 1-2*error_count(idx, puzzle)

class Sudoku():
    def __init__(self, size=10, random=False):
        if random:
            sql_query = 'SELECT * FROM sudoku ORDER BY RANDOM() LIMIT ?'
        else:
            sql_query = 'SELECT * FROM sudoku LIMIT ?'
        db = sudoku_sql()
        self._data = db.read_sql(sql_query, db, param=[size])
        del db
        self._size = size
        self._puzzle_number = 0
        self._qtable = np.random.random([81,9])
        self._log = np.zeros(81)
    
    def next(self, seed=None):
        '''Move on to the next puzzle
        
        Set seed for reproducibility'''
        if seed:
            np.random.seed(seed)
        self._puzzle_number = np.random.randint(self._size)
        self.restart()
    
    def restart(self):
        '''Restart the current puzzle'''
        self._puzzle = self._data['puzzle'][self._puzzle_number]
        self._solution = self._data['solution'][self._puzzle_number]

class Agent1(Sudoku):
    def choose_action(self, epsilon=0.3):
        if np.random.random() < epsilon:
            return np.unravel_index(self._qtable.argmax(), (81,9))
        else:
            return np.random.randint(81), np.random.randint(9)
    
    def step(self, idx, number):
        if self._puzzle[idx] != '0':
            if self._log[idx] == 0:
                reward, end = -100, False
            else:
                reward, end = -100, True # MODDIFICATION REQUIRED
        else:
            self._puzzle[idx] = str(number+1)
            reward, end = 1-error_count(idx, puzzle), False
        self._log[idx] = 1