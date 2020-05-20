from collections import deque
import timeit
import os
import psutil
from func_timeout import func_timeout, FunctionTimedOut

# Creating a node class to hold the state, corresponding action and its parent
class Node:
	def __init__(self, state , action, parent):
		
		self.state = state
		self.action = action
		self.parent = parent

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

		output.append(Node(str(m),1,s)) # adding the newstate, movement variable and parent state into the output
		
		#putting back the swapped values
		x = m[row][col]
		m[row][col] = m[row-1][col]
		m[row-1][col] = x

	if row <3: #if the row index of the blank space is anything less than 3, move down
		
		#swapping values
		x = m[row][col]
		m[row][col] = m[row+1][col]
		m[row+1][col] = x

		output.append(Node(str(m),2,s)) # adding the newstate, movement variable and parent state into the output

		#putting back the swapped values
		x = m[row][col]
		m[row][col] = m[row+1][col]
		m[row+1][col] = x

		
    	
    	
	if col > 0: #if the column index of the blank space is anything more than 0, move left
		
		#swapping values
		x = m[row][col]
		m[row][col] = m[row][col-1] 
		m[row][col-1] = x

		output.append(Node(str(m),3,s)) # adding the newstate, movement variable and parent state into the output
		
		#putting back the swapped value
		x = m[row][col]
		m[row][col] = m[row][col-1]
		m[row][col-1] = x
		
  
	if col < 3: #if the row index of the blank space is anything less than 3, move right
		
		#swapping values
		x = m[row][col]
		m[row][col] = m[row][col+1]
		m[row][col+1] = x

		output.append(Node(str(m),4,s)) # adding the newstate, movement variable and parent state into the output
		
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

def bfs(s,goal):

	queue = deque([s]) #adding the initial node in the queue
	print(queue)
	while queue: # till the queue has some elements
		node = queue.popleft() #popping topmost element of the queue
		
		check = check_if_goal(node.state,goal) #check if that element is the goal or not

		if(check == 1):
			goalnode = node
			return goalnode
		
		if node.state not in explored: # if not , check if that node is explored or not, if not explored proceed
			
			explored.append(node.state) #add the node to explored
			result = movement(node) # get children of node


			for val in result: #for all the children append it to the queue
				queue.append(val)



def path_finder(m,goalnode):

	
	count = 0
	temp = goalnode #storing goalnode in temp variable
	
	while m != temp.state:  #checking if that state is the end state or not, 
	#if not storing the action taken for that. Proceeding up to the parent node and doing the same 
		count += 1
		
		temp = temp.parent
		# moves.insert(0,movetaken) #insert movetaken into moves list
	return count



if __name__ == '__main__':

	goalnode = Node # making goalnode as an empty object of Node
	explored = []   # creating an array named explored to store the explored nodes
	moves = list()  #creating a list to store the movements taken

	m1 = []
	m1 = [int(i) for i in input().split()] #taking input from user
	m2 = [1, 2, 3, 4,5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0] #end state
	
	a = []
	b = []
	a = [m1[i:i+4] for i in range(0, len(m1), 4)] #making into 2d array
	b = [m2[i:i+4] for i in range(0, len(m2), 4)] #making into 2d array
	initial = str(a)
	final = str(b)
	# print(initial)
# 
	start = timeit.default_timer() #starting timer
	try:
		finalgoal = func_timeout(30, bfs, args=(Node(initial,None,None),final)) #calling bfs function, if it exceeds 30s, go to exception
		count = path_finder(initial, finalgoal) #backtracing to find the path
		print("Moves:")

		print(count) #printing the move values

	

	except FunctionTimedOut: #exceeded time limit
		print ("solution cannot be found")

	
	

