# Sudoku Solver
This project is a comprehensive toolkit for analyzing and solving Sudoku puzzle.
It features a SQL-backed data environment for managing large datasets and a collection of optimized utility functions for grid manipulation.

## Features
- Automated SQL Initialization: Automatically convert raw `.csv` Sudoku data into a SQLite database for efficient querying.
- Brutal Solver: Solve Sudoku using a recursive function.
- Q-Learning Solver: An agent repeatedly explore a Sudoku puzzle to find the solution.

## Project Structure

```text
Sudoku_Solver/
├── sudoku_env/                # A custome Python package
|   ├── __init__.py       # Package initialization for clean imports
|   ├── sql_env.py        # SQL database management and CSV migration logic
|   ├── csv_env.py        # CSV data initialization
|   └── tools.py          # Core utility functions (indexing, printing, validation)
├── brutal_solver.py       # Solve Sudoku using a recursive function
└── q_learning_solver.py  # An agent repeatedly explore a Sudoku puzzle to find the solution.
```
