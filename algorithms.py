# File for the different pathfinding algorithms, each defined as a seperate
# function. Can split into multiple  iles for different algorithms later if 
# that ends up being easier to work on

# This could also be a class, but I'm not sure what doing that would add. 

from pygame import Vector2
import numpy as np
# Notes:
# queue.sort(key=,ascending)
# define key with function

def dijkstra(start,goal,grid):
    # Find shortest (or cheapest) path from
    # start to goal on the grid usin dijkstra's algorithm
    # From W3 (https://www.w3schools.com/dsa/dsa_algo_graphs_dijkstra.php), the steps required:


    # Initialize scanning grid of same size as rendering grid but all infinites
    # To do this, we multiply a grid of 1s by infinity
    # https://numpy.org/doc/2.2/reference/generated/numpy.ones.html
    # https://numpy.org/devdocs/reference/constants.html

    # Actually, we need searched (boolean) AND travel cost to be tracked, and will
    # soon need heuristic values (for A*), so we're making vertices a class and 
    # creating a matrix of those instead - IN PROGRESS

    scan = np.inf * np.ones(grid.shape())

    # Set starting position of grid to 0
    
    scan[start[0]][start[1]] = 0 

    # Setup is goal flag if starting position is not goal
    if start != goal:
        is_goal = False

    while is_goal == False:
    # Choose vertex with shortest distance to be start
        

    # For each neigbor, calculate distance to that neighbor from source if not obstacle
    

    # If distance is lower, then update the distance

    # Once all neighbors have been checked, vertex is "visited" and we never check it again.

    # Repeat until all vertices visited
        is_goal = True

    pass