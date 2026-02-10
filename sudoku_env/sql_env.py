import sqlite3 as sql
import pandas as pd
import os

__all__ = [
    'sudoku_sql'
]

def sudoku_sql():
    db_path = 'sudoku.db'
    csv_path = 'sudoku.csv'

    if not os.path.exists(db_path):
        print(f"Database not found. Initializing from {csv_path}...")

        data = pd.read_csv(csv_path)
        conn = sql.connect(db_path)
        table_name = 'sudoku'

        data.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Successfully converted '{csv_path}' to '{db_path}' table '{table_name}'.")
        conn.close()

        del data 
        print("Initialization complete. Dataframe cleared from memory.")

    return sql.connect('sudoku.db')

