from collections import deque
import timeit
import os
import psutil
from func_timeout import func_timeout, FunctionTimedOut


explorednodes = 0
# Creating a node class to hold the state, corresponding action, its parent and its depth level
class Node:
	def __init__(self, state , action, parent, depth):
		
		self.state = state
		self.action = action
		self.parent = parent
		self.depth = depth

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

		output.append(Node(str(m),1,s,s.depth+1)) # appending the output with node having newstate,movement,parent and depth(parent's depth + 1)
		
		#putting back the swapped values
		x = m[row][col]
		m[row][col] = m[row-1][col]
		m[row-1][col] = x

	if row <3: #if the row index of the blank space is anything less than 3, move down
		
		#swapping values
		x = m[row][col]
		m[row][col] = m[row+1][col]
		m[row+1][col] = x

		output.append(Node(str(m),2,s,s.depth+1)) # appending the output with node having newstate,movement,parent and depth(parent's depth + 1)

		#putting back the swapped values
		x = m[row][col]
		m[row][col] = m[row+1][col]
		m[row+1][col] = x

	if col > 0: #if the column index of the blank space is anything more than 0, move left
		
		#swapping values
		x = m[row][col]
		m[row][col] = m[row][col-1] 
		m[row][col-1] = x

		output.append(Node(str(m),3,s,s.depth+1)) # appending the output with node having newstate,movement,parent and depth(parent's depth + 1)
		
		#putting back the swapped value
		x = m[row][col]
		m[row][col] = m[row][col-1]
		m[row][col-1] = x


	if col < 3: #if the row index of the blank space is anything less than 3, move right
		
		#swapping values
		x = m[row][col]
		m[row][col] = m[row][col+1]
		m[row][col+1] = x

		output.append(Node(str(m),4,s,s.depth+1)) # appending the output with node having newstate,movement,parent and depth(parent's depth + 1)
		
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

def dls(s,maxdepth,goal):

	global explorednodes
	explored = []	 # creating an empty list named explored to store the explored nodes
	stack = deque([s]) #creating a stack
	
	while stack:	#till the stack is not empty
		node = stack.pop()	#popright from stack
		# print (node.state)
		# yel = eval(node.state)
		# for i in range(4):
		# 	for j in range(4):
		# 		if 
		# 	print()

		explored.append(node.state)	#add the node to explored
		
		check = check_if_goal(node.state,goal) 	#check if that element is the goal or not
		if(check == 1):
			goalnode = node
			return goalnode

		else:
			if node.depth <= maxdepth:	#if the node's depth is less than or equal to the maximum depth
				result = movement(node)	#if yes, explore it's children
				
				for val in result: 	
					if val.state not in explored:
						stack.append(val) #for all the children that are not explored, append it to the stack
						explored.append(val.state) #add the child to explored

		explorednodes += 1	#increment count of explored nodes


def iddfs(s,maxdepth,goal): #iddfs fn 
	
	for i in range(maxdepth): #loop to run dls
		finale = dls(s,i,goal) #running dls in loop for every depth till it reaches maxdepth
		if finale is not None: # if solution is found , break from loop
			break
	return finale #return solution


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

	
	goalnode = Node # making goalnode as an empty object of Node
	moves = list()  #creating a list to store the movements taken
	
	m1 = []
	m1 = [int(i) for i in input().split()] #taking input from user
	m2 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0] #end state
	
	a = []
	b = []
	a = [m1[i:i+4] for i in range(0, len(m1), 4)] #making into 2d array
	b = [m2[i:i+4] for i in range(0, len(m2), 4)] #making into 2d array
	initial = str(a)
	final = str(b)
	
	
	process = psutil.Process(os.getpid())	#using Process class of psutil

	start = timeit.default_timer() #starting timer
	try:
		initial_memory = process.memory_info().rss / 1024.0 #computing memory usage
		finalgoal = func_timeout(30,iddfs, args=(Node(initial,None,None,0),20,final)) #running iddfs , setting the maxdepth as 20 
		final_memory = process.memory_info().rss / 1024.0	
		end = timeit.default_timer()	#ending the timer
		time = end - start # difference between start time and end time
		timeE = str(round(time, 3)) #rounding the time upto 3 values after point

		moves = path_finder(initial, finalgoal)
		print("Moves:")
		print(*moves)	#printing the move values
		print("No of Nodes expanded: "+str(explorednodes)) #printing number of nodes expanded
		print("Time Taken:\t"+timeE+"s") #printing time
		print("Memory usage\t"+str(final_memory-initial_memory)+" KB")	#printing memory usage
	
	except FunctionTimedOut: #exceeded time limit
		print ("solution cannot be found")

	
	

	
	



		
	

