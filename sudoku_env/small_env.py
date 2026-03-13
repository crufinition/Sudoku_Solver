import random as rd
from copy import deepcopy

def is_valid(board, row, col, num):
    for i in range(4):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 2 * (row // 2), 2 * (col // 2)
    for i in range(2):
        for j in range(2):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def count_solutions(board):
    """Returns the number of solutions found (capped at 2 for efficiency)."""
    for row in range(4):
        for col in range(4):
            if board[row][col] == 0:
                count = 0
                for num in range(1, 5):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        count += count_solutions(board)
                        board[row][col] = 0
                        if count > 1: # Optimization: Stop if we find more than one
                            return count
                return count
    return 1 # Found a complete solution

def generate_unique_puzzle(empties=10, attempts=10000):
    assert 0<empties<16
    # 1. Start with a full board
    board = [[0 for _ in range(4)] for _ in range(4)]
    
    def fill(b):
        for r in range(4):
            for c in range(4):
                if b[r][c] == 0:
                    nums = list(range(1, 5)); rd.shuffle(nums)
                    for n in nums:
                        if is_valid(b, r, c, n):
                            b[r][c] = n
                            if fill(b): return True
                            b[r][c] = 0
                    return False
        return True
    
    fill(board)
    puzzle = [row[:] for row in board]
    solution = deepcopy(puzzle)
    
    #def try_removal(empties, puzzle)


    for j in range(attempts):
        x = deepcopy(empties)
        puzzle = deepcopy(solution)

        # 2. Try removing numbers one by one
        cells = [(r, c) for r in range(4) for c in range(4)]
        rd.shuffle(cells)
    
        for r, c in cells:
            removed_val = puzzle[r][c]
            puzzle[r][c] = 0
            x -= 1
        
            # Check if the board still has exactly 1 solution
            if count_solutions([row[:] for row in puzzle]) != 1:
                # If removing it creates multiple solutions, put it back
                puzzle[r][c] = removed_val
                x += 1
        
            if x == 0:
                return puzzle, solution
    print(f"I'm sorry, I failed to find the puzzle you want in {attempts} attempts.")
    return [],[]

# Test it
while True:
    n = int(input("\nNumber of blanks: "))
    unique_puzzle, solution = generate_unique_puzzle(n)
    print(f"A puzzle with {n} blanks:")
    for row in unique_puzzle:
        print(row)
    print("The solution is:")
    for row in solution:
        print(row)