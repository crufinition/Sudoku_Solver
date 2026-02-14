__all__ = [
    'print_puzzle',
    'row_idx',
    'col_idx',
    'grid_idx',
    'single_check',
    'check',
    'error_count'
    ]

# Display puzzle and solution
def print_puzzle(board, name="Board"):
    '''Display a Sudoku puzzle in a 9x9 format'''
    print(f"\n====== {name} ======")
    for col in range(9):
        for row in range(9):
            if board[9*col+row] == '0':
                print('.', end=' ')
            else:
                print(board[9*col+row], end=' ')
        print("|")

#### Indices look up
def row_idx(idx):
    '''Return the indices of the row of given index'''
    row = idx // 9
    return [9*row+i for i in range(9)]

def col_idx(idx):
    '''Return the indices of the column of given index'''
    col = idx % 9
    return [9*i+col for i in range(9)]

def grid_idx(idx):
    '''Return the indices of the grid of the given index'''
    grid = [0,0]
    col = idx % 9
    row = idx // 9
    grid = [row // 3, col // 3]
    return [27*grid[0]+3*grid[1]+9*r+c for r in range(3) for c in range(3)]

#### Validation
def single_check(bag):
    '''Return False only if the given row, column, or grid is illegal

    ==== Parameter ==== 
    bag: the numbers of a row, a column, or a grid'''
    candidates = [str(i) for i in range(1,10)]
    for i in bag:
        if i in candidates:
            candidates.remove(i)
        elif i != "0":
            return False
    return True

def check(idx, puzzle):
    '''Return False only if the given index leads to an illegal board'''
    if not single_check([puzzle[i] for i in row_idx(idx)]):
        return False
    if not single_check([puzzle[i] for i in col_idx(idx)]):
        return False
    if not single_check([puzzle[i] for i in grid_idx(idx)]):
        return False
    return True

#### Count
def error_count(idx, puzzle):
    '''Count the number of errors the given index makes'''
    number = puzzle[idx]
    row_err = sum([number == puzzle[i] for i in row_idx(idx)])-1
    col_err = sum([number == puzzle[i] for i in col_idx(idx)])-1
    grid_err = sum([number == puzzle[i] for i in grid_idx(idx)])-1
    total_err = row_err+col_err+grid_err
    return total_err