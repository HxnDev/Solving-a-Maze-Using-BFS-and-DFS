





#################################################################################################################################
###         Hassan Shahzad
###         CS-D
###         Artificial Intelligence (Assignment # 1)
###         FAST-NUCES
###         chhxnshah@gmail.com
##################################################################################################################################


import sys
import copy                                     # Will be used to deep copy
####################################### GLOBAL VARIABLES #########################################################################

visited_indexes = []                            # Tuple that will contain the nodes already visited for BFS
visited_indexes1 = []                           # Tuple that will contain the nodes already visited for DFS
agent = "A"                                     # Wil be used later to find index of agent
goal_index = [(10,0)]                           # Storing the goal index of agent

##CREATING THE MAZE##
## For this we will use 2D arrays and graphs
## In the maze, "*" will represent empty cells while "#" will represent blocked cells

rows , cols = (12,12)                           # 12 rows and 12 columns
maze = []                                       # Declaring variables

for i in range(rows):                           # Loop iterating through rows
    col = []
    for j in range(cols):                       # Loop iterating through columns
        col.append("#")                         # Initially storing "#" to show every cell is blocked.
    maze.append(col)

## Now the empty spaces are filled according to the given space
## I was exhausted so i decided to simply hardcode it instead of mapping

maze[1][1] = "*"
maze[2][1] = "*"
maze[1][2] = "*"
maze[1][3] = "*"
maze[2][3] = "*"
maze[3][3] = "*"
maze[4][3] = "*"
maze[4][1] = "*"
maze[4][2] = "*"
maze[4][4] = "*"
maze[5][4] = "*"
maze[6][4] = "*"
maze[7][4] = "*"
maze[8][4] = "*"
maze[8][1] = "*"
maze[8][2] = "*"
maze[8][3] = "*"
maze[8][5] = "*"
maze[8][6] = "*"
maze[8][7] = "*"
maze[8][8] = "*"
maze[6][1] = "*"
maze[6][2] = "*"
maze[7][2] = "*"
maze[10][0] = "*"
maze[10][1] = "*"
maze[10][2] = "*"
maze[10][3] = "*"
maze[10][4] = "*"
maze[10][5] = "*"
maze[10][6] = "*"
maze[1][10] = "*"
maze[2][10] = "*"
maze[3][10] = "*"
maze[4][10] = "*"
maze[5][10] = "*"
maze[6][10] = "*"
maze[7][10] = "*"
maze[8][10] = "*"
maze[9][10] = "*"
maze[10][10] = "*"
maze[10][8] = "*"
maze[10][9] = "*"
maze[1][5] = "*"
maze[1][6] = "*"
maze[1][7] = "*"
maze[1][8] = "*"
maze[1][9] = "*"
maze[2][5] = "*"
maze[3][5] = "*"
maze[3][6] = "*"
maze[3][7] = "*"
maze[3][8] = "*"
maze[4][8] = "*"
maze[5][8] = "*"
maze[6][8] = "*"
maze[7][8] = "*"
maze[5][6] = "*"
maze[6][6] = "*"
maze[7][6] = "*"
maze[9][6] = "*"

## Finally the start state
maze[4][11] = "A"

agent_index = [(index, rows.index(agent)) for index, rows in enumerate(maze) if agent in rows]  # Storing the current index of agent
x = agent_index[0][0]                                                                           # Will store the x-coordinate of agent
y = agent_index[0][1]                                                                           # Will store the y-coordinate of agent

def printMatrix(mat) :                                                                          # Prints the formatted matrix
    for i in range(rows):
        for j in range(cols):
            print(mat[i][j],end = ' ')
        print()

def matrixToIndex(state):                                                                       # Takes matrix and returns index of actor
    temp = state.copy()
    idx = [(index, rows.index(agent)) for index, rows in enumerate(temp) if agent in rows]      # Getting the index of the Agent (A)
    x = idx[0][0]                                                                               # Will store the x-coordinate of agent
    y = idx[0][1]                                                                               # Will store the y-coordinate of agent
    return idx,x,y


######################################################################################################################################

################################################# CREATING NODES #####################################################################

class Node:
    def __init__(self, state, parent, operator, moves):                 # Default Constructor
        self.state = state
        self.parent = parent
        self.operator = operator
        self.moves = moves

def create_node(state, parent, operator, cost):                         # This function creates a node of current state
    return Node(state, parent, operator, cost)

def expand_node(node,n):                                                  # This function performs all possible operations
    expanded_nodes = []
   
    temp_state1 = move_up(node.state,n)
    
    if (temp_state1 is not None):
        temp_node1 = create_node(temp_state1,node,"up",node.moves+1)    # The state is expanded with upward operation
        expanded_nodes.append(temp_node1)                               # Appending the expanded nodes in the list

    temp_state2 = move_left(node.state,n)
    
    if (temp_state2 is not None):
        temp_node2 = create_node(temp_state2,node,"left",node.moves+1)  # The state is expanded with upward operation
        expanded_nodes.append(temp_node2)                               # Appending the expanded nodes in the list
    
    temp_state3 = move_right(node.state,n)
    
    if (temp_state3 is not None):
        temp_node3 = create_node(temp_state3,node,"right",node.moves+1) # The state is expanded with upward operation
        expanded_nodes.append(temp_node3)                               # Appending the expanded nodes in the list
    
    
    temp_state = move_down(node.state,n)                              
    
    if (temp_state is not None):
        temp_node = create_node(temp_state,node,"down",node.moves+1)    # The state is expanded with downward operation
        expanded_nodes.append(temp_node)                                # Appending the expanded nodes in the list       

    return expanded_nodes



def move_left(state,n):
    swap = copy.deepcopy(state)
    idx,x,y = matrixToIndex(swap)                                                                   # Returning index of actor

    if (swap[x][y-1] == "#" or y <= 0):                                                             # Checks for unallowed moves 
        return None
    else:
        swap[x][y-1] , swap[x][y] = swap[x][y] , swap[x][y-1]                                       # Moving the agent one cell left
        return swap

def move_right(state,n):
    swap = copy.deepcopy(state)
    idx,x,y = matrixToIndex(swap)                                                                   # Returning index of actor
    
    if (y >= n-1 or swap[x][y+1] == "#"):                                                            # Checks for unallowed moves
        return None
    else:
        swap[x][y+1] , swap[x][y] = swap[x][y] , swap[x][y+1]                                       # Moving the agent one cell left
        return swap

def move_up(state,n):

    swap = copy.deepcopy(state)
    idx,x,y = matrixToIndex(swap)                                                                   # Returning index of actor
    
    if (swap[x-1][y] == "#" or x <= 0 ):                                                            # Checks for unallowed moves
        return None
    else:
        
        swap[x-1][y] , swap[x][y] = swap[x][y] , swap[x-1][y]                                       # Moving the agent one cell above
        return swap


def move_down(state,n):

    swap = copy.deepcopy(state)
    idx,x,y = matrixToIndex(swap)                                                                   # Returning index of actor
    
    if (swap[x+1][y] == "#" or x >= n-1):                                                            # Checks for unallowed moves
        return None
    else:
        swap[x+1][y] , swap[x][y] = swap[x][y] , swap[x+1][y]                                       # Moving the agent one cell left
        return swap

######################################################################################################################################

################################################## BFS ALGORITHM #####################################################################

def bfs(start,n):
    
    temp_count =0
    temp_idx,x1,y1 = matrixToIndex(start) 
    
    if (temp_idx == goal_index):
        return [None]
    
    else:
        to_be_expanded = []                                                                         # Array of all nodes in one level/depth
        current_node = create_node(start,None,None,0)                                               # Starting node is stored 
        to_be_expanded.append(current_node)                                                         # Adding first node to the expanding array
        
        while (1):
            temp_expanded = []                                                                      # Storing the nodes not expanded
            size = len(to_be_expanded)                                                              # Number of nodes yet to be expanded

            for j in range(size) :
                index,x1,y1 = matrixToIndex (to_be_expanded[j].state)
                
                if (index in visited_indexes) :                                                     # Do not expand as has already been visited
                    continue

                # one expansion
                node_array = expand_node(to_be_expanded[j],n)
                
                # checking the 4 nodes and adding them to the temp array
                for k in range(len(node_array)):
                    idx,x,y = matrixToIndex(node_array[k].state)
                    
                    temp_count+=1

                    if (idx == goal_index):
                        print()
                        print("Algorithm Used: BFS (Breadth First Search)")
                        print()
                        print("Maze Solved!!!")
                        print("Final State is as follows: ")
                        print()
                        printMatrix(node_array[k].state)
                        print()
                        print("Number of explorations in BFS = ", temp_count)
                        return node_array[k]
                        

                    else :
                        temp_expanded.append(node_array[k])                                         # Node will be expanded later
                        visited_indexes.append(index)                                               # Index has been visited

            to_be_expanded.clear()                                                                  # Clearing the previous (already expanded) nodes
            to_be_expanded = temp_expanded.copy()                                                   # Copying over the newly generated nodes
            temp_expanded.clear()                                                                   # Clearing the temp array
    
    return None 

######################################################################################################################################

################################################## DFS ALGORITHM #####################################################################

def dfs(start,n):
    
    temp_idx,x1,y1 = matrixToIndex(start)                                                   # Getting current index of the agent
    
    if (temp_idx == goal_index):                                                            # If agent is already at goal state
        return [None]

    else:
        stack = []                                                                          # Stack containing all nodes to be expanded
        current_node = create_node(start,None,None,0)                                       # Starting node is stored 
        stack.append(current_node)
        count = 0
        
        while(1):
            count+=1
            
            to_be_expanded = stack.pop()                                                    # Popping the node from stack to expand
            idx,x,y = matrixToIndex(to_be_expanded.state)                                           
            
            if (idx == goal_index):                                                         # Checking if current index is goal state
                print()
                print("Algorithm Used: DFS (Depth First Search)")
                print()
                print("Maze Solved!!!")
                print("Final State is as follows: ")
                print()
                printMatrix(to_be_expanded.state)
                print()
                print("Number of explorations in DFS = ", count)
                return to_be_expanded                                                          

            else:
                visited_indexes1.append(idx)                                                # Storing visited nodes in an array
                
                # one expansion
                node_array = expand_node(to_be_expanded,n)                                    # Expanding the node that was popped earlier

                for k in range(len(node_array)):
                    idx,x,y = matrixToIndex (node_array[k].state)
                    if (idx in visited_indexes1):
                        continue
                    else:
                        stack.append(node_array[k])                                         # Pushing the expanded nodes into the stack

        return None
    

######################################################################################################################################

################################################# Implementation of Main done ########################################################
def main():
    
#    if (len(sys.argv) > 0):
#        n = int(sys.argv[1])
    n=12
    starting_state = maze

    result = bfs(starting_state,n)
    if result == None:
        print("No solution found")
    elif result == [None]:
        print  ("Start node was the goal!")
    else:
        print ("Total number of moves needed = ", result.moves)

# Un-Comment the following lines to see the stepwise execution of the moves taken by the actor
#        path = []
#        path.append(result.state)
#        current = result      
#        flag = True     
#        while (flag):
#            parent = current.parent
#            prev_state = parent.state
#            path.append(prev_state)
#            current = parent         
#            if (prev_state == starting_state):
#                flag = False              
#        path.reverse()      
#        for state in path:
#            printMatrix(state)
#            print()
    print()
    print()
    print("######################################################################################################################")
    print()

    result1 = dfs(starting_state,n)
    if result1 == None:
        print("No solution found")
    elif result1 == [None]:
        print  ("Start node was the goal!")
    else:
        print ("Total number of moves needed = ", result1.moves)
        print()
        
# Un-Comment the following lines to see the stepwise execution of the moves taken by the actor
#        path1 = []
#        path1.append(result1.state)
#        current1 = result1
        
#        flag1 = True
        
#        while (flag1):
#            parent = current1.parent
#            prev_state1 = parent.state
#            path1.append(prev_state1)
#            current1 = parent
            
#            if (prev_state1 == starting_state):
#                flag1 = False
                
#        path1.reverse()
        
#        for state in path1:
#            printMatrix(state)
#            print()

if __name__ == "__main__":
    main()

######################################################################################################################
################################################### THE END ##########################################################
######################################################################################################################




