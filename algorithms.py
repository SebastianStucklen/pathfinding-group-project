# File for the different pathfinding algorithms, each defined as a seperate
# function. Can split into multiple  iles for different algorithms later if 
# that ends up being easier to work on

# This could also be a class, but I'm not sure what doing that would add. 

from pygame import Vector2
import numpy as np
from vertex import Vertex
# Notes:
# queue.sort(key=,ascending)
# define key with function


def initialize_scan(start,goal,grid:np.array):
    '''setup pathfinding algorithm scan'''
    # Initialize vertex scanning matrix
    gridshape = grid.shape()
    scan_matrix = np.array()

    # Iterate through columns
    for y_pos in range(gridshape[0]):

        # Fill columns with default vertices
        column = []
        for x_pos in range(gridshape[1]):
            column.append(Vertex(x_pos,y_pos))

        # Append column to vertex matrix
        scan_matrix.append()

    # Set starting position of grid to 0 and goal flag to true
    scan_matrix[start].cost = 0
    scan_matrix[goal].is_goal = True

    # Initialize other useful lists
    path = []
    queue = []

    return scan_matrix,path,queue

def get_valid_neighbors(vertex,scan_matrix,grid):
    '''For a vertex, returns a list its valid, accessible vertices to check'''
    pass

def get_minimums(scan_matrix,min_cost):
    '''Find the values in the scan matrix with a minimum cost and return a list of all of them'''

    #Starting at current minimum cost, add 1 and check if any values in the matrix satisfy this
    min_values = []

    # Use nditer for simplicity's sake https://www.w3schools.com/python/numpy/numpy_array_iterating.asp
    
    return min_cost,min_values


def dijkstra(start,goal,grid:np.array):
    # Find shortest (or cheapest) path from
    # start to goal on the grid usin dijkstra's algorithm
    # From W3 (https://www.w3schools.com/dsa/dsa_algo_graphs_dijkstra.php), the steps required:

    # Initialize scan_matrix, path list, checking queue
    scan_matrix,path,queue = initialize_scan(start,goal,grid)
    

    # Loop until goal reached
    if start != goal:
        goal_reached = False
    
    while goal_reached == False:

        # Choose vertex with shortest distance to be start
        vertex = get_minimums(scan_matrix)

        # Find its valid neighbors
        neighbors = get_valid_neighbors(vertex,scan_matrix,grid)
            
        # If distance is lower, then update the distance

        # Once all neighbors have been checked, vertex is "visited" and we never check it again.
        vertex.visited = True
        # Repeat until goal is reached

        if vertex.is_goal == True:
            goal_reached = True

    return path