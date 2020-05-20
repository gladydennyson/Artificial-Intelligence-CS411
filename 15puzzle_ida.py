from collections import deque
import timeit
import os
import psutil
from func_timeout import func_timeout, FunctionTimedOut
import itertools
from heapq import heappush, heappop, heapify


explorednodes = 0
b = []
final = ''

# Creating a node class to hold the state, corresponding action, its parent, its depth level and fscore
class Node:
	def __init__(self, state , action, parent, depth,fscore):
		
		self.state = state
		self.action = action
		self.parent = parent
		self.depth = depth
		self.fscore = fscore
		

# creating a movement function to move a node up, down, left, right
def movement(s): 

	output = list() # creating a list to store the output, which has all the movements in it

	
	m = eval(s.state)
	row = 0
	# searching for element 0 in the 2d array
	while 0 not in m[row]: row += 1
	col = m[row].index(0); 

	if row > 0: #if the row index of the blank space is anything more than 0, move up
		
		#swapping values
		x = m[row][col] 
		m[row][col] = m[row-1][col]
		m[row-1][col] = x

		output.append(Node(str(m),1,s,s.depth+1,0)) # appending the output with node having newstate,movement,parent,depth(parent's depth + 1) and fscore as 0
		
		#putting back the swapped values
		x = m[row][col]
		m[row][col] = m[row-1][col]
		m[row-1][col] = x

	if row <3: #if the row index of the blank space is anything less than 3, move down
		
		#swapping values
		x = m[row][col]
		m[row][col] = m[row+1][col]
		m[row+1][col] = x

		output.append(Node(str(m),2,s,s.depth+1,0)) # appending the output with node having newstate,movement,parent,depth(parent's depth + 1) and fscore as 0
		#putting back the swapped values
		x = m[row][col]
		m[row][col] = m[row+1][col]
		m[row+1][col] = x

	if col > 0: #if the column index of the blank space is anything more than 0, move left
		
		#swapping values
		x = m[row][col]
		m[row][col] = m[row][col-1] 
		m[row][col-1] = x

		output.append(Node(str(m),3,s,s.depth+1,0)) # appending the output with node having newstate,movement,parent,depth(parent's depth + 1) and fscore as 0
		
		#putting back the swapped value
		x = m[row][col]
		m[row][col] = m[row][col-1]
		m[row][col-1] = x


	if col < 3: #if the row index of the blank space is anything less than 3, move right
		
		#swapping values
		x = m[row][col]
		m[row][col] = m[row][col+1]
		m[row][col+1] = x

		output.append(Node(str(m),4,s,s.depth+1,0)) # appending the output with node having newstate,movement,parent,depth(parent's depth + 1) and fscore as 0
		
		#putting back the swapped value
		x = m[row][col]
		m[row][col] = m[row][col+1]
		m[row][col+1] = x
		

	return (output)

def check_if_goal(s,goal): # checking if the state is the goal state or not
	if s == goal:
		return 1
	else: 
		return 0



def idastar(s,choice,goal):
	
	if choice == '1':
		threshold = manhattandistance(s) #if heuristic is manhattan distance

	else:
		threshold = displacedtiles(s) # if heuristic is displaced tiles
		
	
	while 1: #run till goal is found
		outcome = depthlimited(s,choice,threshold,goal) #calling the depthlimited function 

		if type(outcome) is int: # when the function returns the minimum cost(minimum fscore), make this the threshold
			threshold = outcome
		else:                    #when the fuction returns the goalnode, return this goalnode and end the loop 
			return outcome
			break

		

def depthlimited(s,choice,threshold,goal):


    global explorednodes
    explored = [] # creating an empty list named explored to store the explored nodes
    cost = set() #creating a set to add the fscores 
    stack = list([Node(s.state, None, None, 0, threshold)]) #creating a list called stack and adding its components 

    while stack: #till the stack is not empty

    	node = stack.pop() #popright from stack
    	explored.append(node.state) #adding to explored nodes

    	check = check_if_goal(node.state,goal) #check if that element is the goal or not
    	if(check == 1):
    		goalnode = node 
    		return goalnode
    	
    	if node.fscore > threshold: #if the current node's fscore is greater than the threshold value then save it in cost 
    		cost.add(node.fscore) 

    	else: # if the current node's fscore is smaller than or equal to the threshold, expand that node and explore its children 
    		result = movement(node) #explore its children
    		for val in result: 
    			if val.state not in explored: #check if child is already in explored

    				if choice == '1':

    					displacedt = manhattandistance(val) #if heuristic is manhattan distance
  					
    				else:
    					displacedt = displacedtiles(val) # if heuristic is displaced tiles
    					

    				val.fscore = displacedt + val.depth #since fscore = heuristic + distance between current node and start node
    				stack.append(val) #add to stack 
    				explored.append(val.state) #adding to explored nodes

    	explorednodes += 1 #increment count of explorednodes

    return min(cost) #return the minimum fscore value stored in costs


#to compute the displaced tiles heuristic in 15 puzzle
def displacedtiles(s):
	displaced = 0
	x = eval(s.state)
	for i in range(4):
		for j in range(4):
			 #checking for each value in matrix, if value of state matrix at index is same as value of goal matrix at that index
			if x[i][j] != b[i][j] and x[i][j]!=0:   
				displaced = displaced + 1 #incrementing the count of displaced tiles 
	return displaced

#to compute the manhattan distance heuristic 
def manhattandistance(s):
	dist = 0
	mat = eval(s.state)
	for i in range(4):
		for j in range(4):
			if mat[i][j] != 0:
				x, y = divmod(mat[i][j]-1, 4) # this gives the quotient and remainder of the division to x and y respectively.
				dist += abs(x - i) + abs(y - j) #subtracts current position with the position in goalstate and adds that to 'dist'

	return dist


def path_finder(m,goalnode):

	
	movetaken = ''
	temp = goalnode #storing goalnode in temp variable
	
	while m != temp.state:  #checking if that state is the end state or not, 
	#if not storing the action taken for that. Proceeding up to the parent node and doing the same 
		if(temp.action == 1):
			movetaken = 'U'
		elif(temp.action == 2):
			movetaken = 'D'
		elif(temp.action == 3):
			movetaken = 'L'
		else:
			movetaken = 'R'
		
		temp = temp.parent
		moves.insert(0,movetaken) #insert movetaken into moves list
	return moves



if __name__ == '__main__':

	global initial
	goalnode = Node # making goalnode as an empty object of Node
	moves = list()  #creating a list to store the movements taken
	global costs
	m1 = []
	m1 = [int(i) for i in input().split()] #taking input from user
	m2 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0] #end state
	print("Implement ida* search with heuristic ‘manhattan distance’      : Enter 1\n")
	print("Implement ida* search with heuristic ‘number of misplaced tile’: Enter 2")
	choice = input() #taking choice input from user
	a = []
	
	a = [m1[i:i+4] for i in range(0, len(m1), 4)] #making into 2d array
	b = [m2[i:i+4] for i in range(0, len(m2), 4)] #making into 2d array
	initial = str(a)
	final = str(b)
	
	
	
	process = psutil.Process(os.getpid())	#using Process class of psutil

	start = timeit.default_timer() #starting timer
	
	initial_memory = process.memory_info().rss / 1024.0 #computing memory usage
	finalgoal = idastar(Node(initial,None,None,0,0),choice,final)
	final_memory = process.memory_info().rss / 1024.0	
	end = timeit.default_timer()	#ending the timer
	time = end - start # difference between start time and end time
	timeE = str(round(time, 3)) #rounding the time upto 3 values after point

	moves = path_finder(initial, finalgoal)
	print("Moves:")
	print(*moves)	#printing the move values
	print("No of Nodes expanded: "+str(explorednodes)) #printing number of nodes expanded
	print("Time Taken:\t"+timeE+"s") #printing time
	print("Memory usage:\t"+str(final_memory-initial_memory)+" KB")	#printing memory usage
	
	
	
	

	
	



		
	

