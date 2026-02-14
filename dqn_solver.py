import numpy as np
import pandas as pd
import random as rd
import copy as cp
import math as m
#import matplotlib.pyplot as plt
import statistics as stat
#import gymnasium as gym

#print(np.__version__)
#print(pd.__version__)
print('Loading "sudoku.csv" ...')
data = pd.read_csv("sudoku.csv")
print('The file "sudoku.csv" successfully loaded.')

# Some call back functions are defined here
def convert_puzzle(puzzle, show=False):
    'convert the data into a nested list (2 dimensional)'
    result = []
    for i in range(9):
        row = []
        for j in range(9):
            row.append(int(puzzle[9*i+j]))
            if puzzle[9*i+j] == "0" and show:
                print(".", end=" ")
            elif show:
                print(puzzle[9*i+j], end=" ")
        result.append(row)
        if show:
            print("")
    return result
def cell(row, column):
    'Return the left most and the up most cell location'
    return [row-row%3, column-column%3]

class Sudoku:
    def __init__(self, puzzle=None):
        '''This is the basic class that provides the environment for several
        learning algorithms to run simulations'''
        if puzzle:
            self._form = np.array(puzzle, dtype=int)
        else:
            self._form = np.zeros((9,9), dtype=int)
        self._initial = self._form.copy()
        self._initial_loc_list = []
        self._blanks = 0
        for i in range(9):
            for j in range(9):
                if self._form[i,j] == 0:
                    self._initial_loc_list.append([i,j])
                    self._blanks += 1
        self._loc_list = cp.deepcopy(self._initial_loc_list)
    def __setitem__(self, key, value):
        assert self._form[key] == 0
        assert list(key) in self._loc_list
        self._form[key] = value
        self._loc_list.remove(list(key))
    def __getitem__(self, key):
        return self._form[key]
    def delete(self, row, column):
        self._form[row, column] = 0
        if [row, column] not in self._loc_list:
            self._loc_list.append([row, column])
            self._loc_list.sort()
    @property
    def show_puzzle(self):
        '''Print out the initial puzzle'''
        for i in self._initial:
            for j in i:
                if j != 0:
                    print(f"{j:d}", end=" ")
                else:
                    print(".", end=" ")
            print("")
        print("=================")
    @property
    def replay(self):
        self._form = self._initial.copy()
        self._loc_list = self._initial_loc_list.copy()
    @property
    def show(self):
        for i in self._form:
            for j in i:
                if j != 0:
                    print(f"{j:d}", end=" ")
                else:
                    print(".", end=" ")
            print("")
        print("=================")
    @property
    def form(self):
        return self._form
    @property
    def blanks(self):
        return self._blanks
    @property
    def puzzle(self):
        return self._initial
    def save(self, file_name, agent="None", success="None", episodes="None"):
        '''Make sure to call this method when the current form is the solution of the agent'''
        lines = ["Puzzle :\n"]
        for i in self._initial:
            line = ""
            for j in i:
                line += f"{j} " if j != 0 else ". "
            line += "\n"
            lines.append(line)
        lines.append("="*18+"\n")
        lines.append("Agent's Solution :\n")
        for i in A._form:
            line = ""
            for j in i:
                line += f"{j} " if j != 0 else ". "
            line += "\n"
            lines.append(line)
        lines.append("="*18+"\n")
        lines.append("\nLearning Information :\n")
        lines.append(f"--learning agent : {agent}\n")
        lines.append(f"--success : {success}\n")
        lines.append(f"--episodes = {episodes}\n")
        with open(file_name, "w") as fh:
            fh.writelines(lines)
#### test the class
'''
puzzle = Sudoku(convert_puzzle(data.loc[0]["puzzle"], False))
print(puzzle._loc_list[0])
puzzle.show
puzzle[0,0] = 1
print(puzzle._loc_list[0])
puzzle.show
loc = [0,2]
puzzle[*loc] = 5
print(puzzle._loc_list[0])
puzzle.show
puzzle.delete(0,0)
print(puzzle._loc_list[0])
puzzle.show
'''

class Agent1(Sudoku):
    @property
    def restart(self):
        self._Qtable = np.random.rand(9,9,9)
    def choose_action(self, greedy=False):
        loc = rd.choice(self._loc_list)
        #self._loc_list.remove(loc)
        row, column = loc
        if greedy or np.random.randint(100) > self._epsilon:
            num = np.argmax(self._Qtable[row, column])+1
        else: 
            num = rd.randint(1,9)
        return row, column, num
    def step(self, row, column, num):
        '''Modify the puzzle, and return a specific reward
        Let the agent learn single puzzle'''
        # count the number of each type of violations
        cell_row, cell_column = cell(row, column)
        reward = 1
        a = np.sum(self._form[row] == num)
        b = np.sum(self._form[:,column] == num)
        c = np.sum(self._form[cell_row : cell_row+3, cell_column : cell_column+3] == num)
        reward -= 2*(a+b+c)
        self[row, column] = num
        self._deltaQ[row, column, num-1] += reward
    def simulation(self, epsilon=30, alpha=0.1, agent_episodes=10000, interval=0):
        '''After running given episodes, run the final result
        so that user can view what agent has learned.'''
        #self.restart
        self._epsilon = epsilon
        self._alpha = alpha
        result_log = []
        if not interval:
            interval = agent_episodes
        episodes = 1
        while True:
            self._deltaQ = np.zeros([9,9,9])
            result = 0
            self.replay
            solved = False
            episodes_used = agent_episodes
            greedy = True if episodes % interval == 0 or solved == True else False
            for j in range(self._blanks):
                row, column, num = self.choose_action(greedy)
                self.step(row, column, num)
            self._Qtable += (1-self._alpha)*(self._deltaQ-self._Qtable)
            result_log.append(np.sum(self._deltaQ))
            if result_log[-1] == self._blanks: # stop when the solution is found
                print(f"Solution found at episode {episodes}, learning process terminated.")
                solved = True
                episodes_used = episodes
                break
            elif episodes == agent_episodes:
                break
            episodes += 1
        return result_log, episodes_used

epsilon = 10
alpha = 0.9
agent_episodes = 10000
interval = 0

n = rd.randint(0, 8999999)
print(f"The series number of the puzzle is :{n}")
puzzle = convert_puzzle('250041000631950480489602001016093820302418095908260307004386579763529148800100206'
, False)
#answer = convert_puzzle(data.loc[n]["solution"], False)
A = Agent1(puzzle)
#B = Agent1(answer)
A.restart
result_log, episodes = A.simulation(epsilon, alpha, agent_episodes, interval)
print("The puzzle to solve is :")
A.show_puzzle
#print("The answer should be :")
#B.show
print(f"Number of blanks to fill in : {A.blanks}")
#different = 0
#for i in range(9):
#    for j in range(9):
#        if A[i,j] != B[i,j]:
#            different += 1
print("The agent's solution is :")
A.show
#if different:
#    print("Result : Incorrect")
#    print(f"There are {different} different numbers.")
#else:
#    print("Result : Correct")
#    print("Feel free to check if the result and the answer match.")

epsilon = 1
alpha = 0.9
tests = 10
agent_episodes = 20000
interval = 10000

# print the puzzle
print_puzzle = True

# print the solution
print_answer = True

# print the agent's solution
print_result = True

# print the number of blanks
print_blanks = True

# print whether the agent has solved the puzzle
print_info = True

####
#n = 7839561
#print(f"The series number of the puzzle is :{n}")
#print("Number of blanks to fill in : 42")
blanks_log = []
episodes_log = []
####

report = [0,0]
simulation_log = []
all_result_log = []
for i in range(tests):
    n = rd.randint(0, 8999999)
    print(f"\n== Test number {i+1} ==")
    print(f"The series number of the puzzle is :{n}")
    puzzle = convert_puzzle(data.loc[n]["puzzle"], False)
    answer = convert_puzzle(data.loc[n]["solution"], False)
    #puzzle = convert_puzzle("000070100609000000500000000070020004008000060000000059030000800400600000000900000", False)
    A = Agent1(puzzle)
    blanks_log.append(A.blanks)
    A.restart
    result_log, episodes = A.simulation(epsilon, alpha, agent_episodes, interval)
    #results = np.zeros(len(agent_episodes))+np.array(result_log)
    all_result_log.append(result_log)
    B = Agent1(answer)
    if print_puzzle:
        print("The puzzle to solve is :")
        A.show_puzzle
    if print_answer:
        print("The answer should be :")
        B.show
    if print_blanks:
        print(f"Number of blanks to fill in : {A.blanks}")
    different = 0
    for j in range(9):
        for k in range(9):
            if A[j,k] != B[j,k]:
                different += 1
    if print_result:
        print("The agent's solution is :")
        A.show
    report[int(different>0)] += 1
    if print_info:
        if different:
            print("Result : Incorrect")
            print(f"There are {different} different numbers.")
        else:
            print("Result : Correct")
            print("Feel free to check if the result and the answer match.")
    if episodes < 10000:
        episodes_log.append(episodes)
    #### Save the result to a file (.txt)
    simulation_log.append([n, episodes])
    A.save(str(n)+".txt", agent="1", success=str(different==0), episodes=f"{episodes}")

history = []
with open("Simulation Log.txt", "r") as fh:
    for i in fh.readlines():
        history.append([int(j) for j in i.split()])
history += simulation_log
history.sort(key=lambda x:x[1])
with open("Simulation Log.txt", "w") as fh:
    fh.writelines([f"{i[0]:7d} {i[1]:7d}\n" for i in history])
print(f"Success rate: {report[0]/tests}")

