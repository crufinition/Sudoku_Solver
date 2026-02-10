import pandas as pd

__all__ = [
    'sudoku_csv'
]

def sudoku_csv():
    return pd.read_csv("sudoku.csv")