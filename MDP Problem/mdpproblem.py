import random
import numpy as np
from collections import defaultdict
import operator

filepath = 'custominput5_4.txt'
output = list()

walstr = list()
walls = list()

termst = list()
terminal_states = list()
t = list()

global reward
global discount_rate
global epsilon
global gamma


# reading from input file
fp = open(filepath)
    
for line in fp:
    output.append(line.split(':'))

for i in range(len(output)):
    
    #for the size description, split by , and store row and column value 
    if output[i][0].strip() == 'size':
        x = output[i][1].strip()
        elems = x.split(",")
        col = int(elems[0])
        row = int(elems[1])

    # for the walls description, split by double space and store wall coordinates
    if output[i][0].strip() == 'walls':
        x = output[i][1].strip()
        y = x.replace("  ",",")
        walstr = y.split(",")

        for i in range(len(walstr)):
            walls.append(int(walstr[i]))

    #storing the reward value
    if output[i][0].strip() == 'reward':
        x = output[i][1].strip()
        reward = float(x)

    #storing the discount rate 
    if output[i][0].strip() == 'discount_rate':
        x = output[i][1].strip()
        discount_rate = float(x)
        gamma = discount_rate

    #storing the epsilon value
    if output[i][0].strip() == 'epsilon':
        x = output[i][1].strip()
        epsilon = float(x)

    # for the terminal state description, replacing double space with comma and storing terminal state coordinates and terminal state rewards
    if output[i][0].strip() == 'terminal_states':
        x = output[i][1].strip()
        y = x.replace("  ",",")
        termst = y.split(",")

        for i in range(len(termst)):
            terminal_states.append(int(termst[i]))


#making a grid with value set as -0.04 for each cell -0.04

grid = [[float(reward) for i in range(0, col)] for r in range(0, row)]


#to make the coordinates where the wall exists as None in the grid
i = 0
while i < len(walls):
    grid[walls[i + 1] - 1][walls[i] - 1] = None
    i = i + 2

grid.reverse() # to get row 0 on bottom, not on top, to set grid values for terminal states

#to set the rewards for the terminal states in the grid
i = 0
while i < len(terminal_states):
    l = (terminal_states[i] - 1, terminal_states[i+1] - 1)
    t.append(l)
    grid[terminal_states[i + 1] - 1][terminal_states[i] - 1] = terminal_states[i+2]
    i = i + 3

grid.reverse() #setting the grid to how it was

orientations = [(1,0), (0, 1), (-1, 0), (0, -1)] # East, North, West, South

def turn_right(orientation):
    return orientations[orientations.index(orientation)-1 % len(orientations)]


def turn_left(orientation):
    return orientations[(orientations.index(orientation)+1) % len(orientations)]


def vector_add(a, b):

    return tuple(map(operator.add, a, b))


def argmax(seq, fn):

    return argmin(seq, lambda x: -fn(x))


def argmin(seq, fn):

    best = seq[0]; best_score = fn(best)
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score
    return best


class GridMDP():

    def __init__(self, grid, terminals, gamma, rows, cols, init=(0, 0)):
        grid.reverse()  # to get row 0 on bottom, not on top
        reward = {}
        states = set()
        self.rows = rows
        self.cols = cols
        self.grid = grid
        for x in range(cols):
            for y in range(rows):
                if grid[y][x]:
                    states.add((x, y))
                    reward[(x, y)] = grid[y][x]
        self.states = states
        actlist = orientations
        transitions = {}
        for s in states:
            transitions[s] = {}
            for a in actlist:
                transitions[s][a] = self.calculate_T(s, a)
        
        self.gamma = gamma
        self.reward = reward
        self.terminals = terminals
        self.transitions = transitions
        self.actlist = actlist
                

    def actions(self, state):

        if state in self.terminals:
            return [None]
        else:
            return self.actlist
        
    def calculate_T(self, state, action):
        if action:
            return [(0.8, self.go(state, action)),
                    (0.1, self.go(state, turn_right(action))),
                    (0.1, self.go(state, turn_left(action)))]
        else:
            return [(0.0, state)]

    def R(self, state):

        return self.reward[state]

    def T(self, state, action):
        return self.transitions[state][action] if action else [(0.0, state)]

    def go(self, state, direction):

        state1 = vector_add(state, direction)
        return state1 if state1 in self.states else state

    def to_grid(self, mapping):

        return list(reversed([[mapping.get((x, y), None)
                               for x in range(self.cols)]
                              for y in range(self.rows)]))

    def directionset(self, policy):
        chars = {(1, 0): 'E', (0, 1): 'N', (-1, 0): 'W', (0, -1): 'S', None: 'T'}
        return self.to_grid({s: chars[a] for (s, a) in policy.items()})


gridworld = GridMDP(grid, t, gamma, row, col)

def value_iteration(mdp, epsilon=0.001):

    U1 = {s: 0 for s in mdp.states}
    R, T, gamma = mdp.R, mdp.T, mdp.gamma
    iter = 0
    while True:
        U = U1.copy()
        delta = 0
        for s in mdp.states:
            U1[s] = R(s) + gamma * max(sum(p * U[s1] for (p, s1) in T(s, a))
                                       for a in mdp.actions(s))
            delta = max(delta, abs(U1[s] - U[s]))

        eval_output = gridworld.to_grid(U)
        print("\n")
        print ("Iteration", iter)

        for v in eval_output:

            print(v)

        if delta <= epsilon * (1 - gamma) / gamma:
            print("\n")
            print("Final value after convergence")
            result = gridworld.to_grid(U)
            for x in result:
                 print(x)
           
            return U
        iter += 1




def expected_utility(a, s, U, mdp):
    return sum([p * U[s1] for (p, s1) in mdp.T(s, a)])



def policy_iteration(mdp):

    U = {s: 0 for s in mdp.states}
    pi = {s: random.choice(mdp.actions(s)) for s in mdp.states}
    while True:
        U = policy_evaluation(pi, U, mdp)
        unchanged = True
        for s in mdp.states:
            a = argmax(mdp.actions(s), lambda a: expected_utility(a, s, U, mdp))
            if a != pi[s]:
                pi[s] = a
                unchanged = False
        if unchanged:
            return pi



def policy_evaluation(pi, U, mdp, k=30):

    R, T, gamma = mdp.R, mdp.T, mdp.gamma
    for i in range(k):
        for s in mdp.states:
            U[s] = R(s) + gamma * sum([p * U[s1] for (p, s1) in T(s, pi[s])])
    return U

value_iteration(gridworld)
print("\n")
print("Final Policy")
print("\n")

res = gridworld.directionset(policy_iteration(gridworld))
for o in res:
    print (o)

