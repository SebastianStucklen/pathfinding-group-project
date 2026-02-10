# File for the different pathfinding algorithms, each defined as a seperate
# function. Can split into multiple  iles for different algorithms later if 
# that ends up being easier to work on

# This could also be a class, but I'm not sure what doing that would add. 

import pygame as pg
from pygame import Vector2 as v2
import numpy as np
from vertex import Vertex
# import pathfinding
# from pathfinding.finder.a_star import AStarFinder as AStar
import pdb

class Pathfinder:
    # Implements the dijstra pathfinding algorithm using the steps outlined in
    #(https://www.w3schools.com/dsa/dsa_algo_graphs_dijkstra.php)

    def __init__(self,screen:pg.Surface,start:v2,goal:v2,grid,algorithm:str):
        '''setup pathfinding algorithm scan'''
        # Initialize various parameters
        self.SCREEN = screen

        # Algorithm to use
        self.algorithm = algorithm

        # Starting position
        self.start = start

        # Goal position
        self.goal = goal

        # world grid
        self.grid = grid

        # Matrix for implementing pathfinding
        scan_matrix = []

        # Goal flag
        self.goal_reached = False

        # Cost that defines the frontier
        self.min_cost = 0
        
        # Path and queue lists
        self.path = []
        self.queue = []

        # Limits how long the program will spend trying to pass through walls
        self.search_limit = len(self.grid)**2

        # Initialize square scanning matrix of same size as grid
        gridshape = len(self.grid)
        for x_pos in range(gridshape):

            # Fill columns with default vertices
            column = []
            for y_pos in range(gridshape):
                column.append(Vertex(x_pos,y_pos))

            # Append column to vertex matrix
            scan_matrix.append(column)
        

        # Turn matrix into a np array
        self.scan_matrix = np.array(scan_matrix)
        
        # Assign total cost of 0 to starting vertex, goal flag for goal vertex
        self.scan_matrix[int(self.start.x),int(self.start.y)].total_cost = 0
        self.scan_matrix[int(self.goal.x),int(self.goal.y)].is_goal = True


    def get_valid_neighbors(self,vertex):
        '''For a vertex, returns a list its valid, non-obstacle to check'''
        # Get positions of neighbors
        neighbor_positions = vertex.get_neighbor_positions(self.grid)

        # initialize neighbors list
        neighbors = []

        for position in neighbor_positions:
            # Unpack position
            x,y = int(position.x),int(position.y)
            
            # Add vertex to neighbors if it corresponds to a non-obstacle
            if self.grid[x,y] != 1: 
                neighbors.append(self.scan_matrix[x,y])
                #print(position)

        return neighbors

    def get_minimums(self):
        '''Find the values in the scan matrix with a minimum cost and return a list of all of them'''

        #Starting at current minimum cost, add 1 and check if any values in the matrix satisfy this
        # Empty queue
        self.queue = []
        
        # Run until we have the next minimum value
        for _ in range(self.search_limit):

            # Iterate through all entries in scan matrix
            for column in self.scan_matrix:
                for vertex in column:

                    # If this is an unscanned vertex, add it to the queue for scanning
                    if vertex.total_cost == self.min_cost and vertex.searched == False:
                        self.queue.append(vertex)
                        return
            
            # Once any vertices are added, add 1 to minimum value
            self.min_cost += 1


    def handle_queue(self):
        # Handle algorithm steps for each entry to check in the queue
        for vertex in self.queue:

            # Find neighbors of vertex in queue 
            neighbors = []
            neighbors = self.get_valid_neighbors(vertex)

            # For each calculate the new total movement cost from origin through current vertex to neighbor
            for neighbor in neighbors:
                new_cost = vertex.total_cost + neighbor.move_cost

                # If that cost is lower than its existing cost, update the total cost to the new value
                if neighbor.total_cost > new_cost:
                    neighbor.total_cost = new_cost

                # Also check if it is the goal, and update the flag/add to path if so
                if neighbor.pos == self.goal: 
                    self.goal_reached = True

                    # Add the neighbor as the only element of the path list
                    self.path.append(neighbor)
            
            # Set searched flag to true for the vertex once this is done so it is not checked again
            vertex.searched = True
                


    def return_path(self):
        '''From solved scan matrix, reconstruct the path from start to goal'''
        # Only does anything if path is no longer empty (because goal has been added)
        if len(self.path) != 0:

            # Render code
            a = 0
            width = 50
            pg.font.init()
            font = pg.font.SysFont("Times New Roman", 22) 
            pg.draw.rect(self.SCREEN,(a,50,50),(self.path[-1].pos.x*width,self.path[-1].pos.y*width,width,width))
            text_surface = font.render(str(a), True,'black')
            self.SCREEN.blit(text_surface,(self.path[-1].pos.x*width,self.path[-1].pos.y*width))
            a += 5

            # Iterate until path is found
            finished = False
            while finished == False:
                # Find neighbors of most recently added item in the path list
                new_step = self.path[-1]
                neighbors = self.get_valid_neighbors(new_step)

                # Iterate through each
                for neighbor in neighbors:

                    # If the neighbor is a productive step towards the goal, add it to the path
                    if neighbor.total_cost == new_step.total_cost - new_step.move_cost:
                        self.path.append(neighbor)

                        # Render code
                        pg.draw.rect(self.SCREEN,(a,50,50),(neighbor.pos.x*width,neighbor.pos.y*width,width,width))
                        text_surface = font.render(str(a), True,'black')
                        self.SCREEN.blit(text_surface,(neighbor.pos.x*width,neighbor.pos.y*width))
                        if a <= 235:
                            a+=5
                        break

                # Repeat until we add something with total cost = 0, as that's the start point!
                if new_step.total_cost == 0:
                    finished = True
                    
                    # This is a backwards path, so spin it around. https://www.w3schools.com/python/ref_list_reverse.asp
                    self.path.reverse()

                    # This is a list of vertices, and we want coordinates, so overwrite path with a list of vectors
                    vector_list = []
                    for vertex in self.path:
                        vector_list.append(vertex.pos)
                    
                    self.path = vector_list


    def draw(self):
        for path in self.path:
            pg.draw.rect(self.SCREEN,'yellow',(path.x*100,path.y*100,100,100))

    def check_path_invalid(self):
        # Checks that start and end points are not obstacles to avoid running an obviously impossible sim
        # Exploiting properties allows us to split this into a few legible lines instead of one giant one
        start_check = self.grid[int(self.start.x),int(self.start.y)] != 1
        goal_check = self.grid[int(self.goal.x),int(self.goal.y)] != 1
        return (start_check and goal_check)
    
    def heuristic(self,vertex):
        '''Score for distance to goal'''
        # Might be handy for a greedy-first implementation down the road
        # Unpack position values from vertex and goal
        vertex_x,vertex_y = vertex.pos
        goal_x,goal_y = self.goal

        # Score based on "manhattan distance" (based on how it's done here: https://www.redblobgames.com/pathfinding/a-star/introduction.html)
        score = abs(vertex_x-goal_x) + abs(vertex_y-goal_y)
        return score
    
    def sort_function(self,item):
        # For now, this function just returns the total cost
        if self.algorithm == 'A': return self.heuristic(item) + item.total_cost
        if self.algorithm == 'D': return item.total_cost
        if self.algorithm == 'G': return self.heuristic(item) 
        

    def continuous_queue(self):
        # Interate through queue until goal reached or entire grid has been searched
        for _ in range(self.search_limit):
            # Check if queue is empty, break if so
            if len(self.queue) == 0:
                print('path not found')
                return

            # Pull first item from queue
            vertex = self.queue[0]

            # Get its neighbors
            neighbors = self.get_valid_neighbors(vertex)
            #print(neighbors)

            # Iterate through all neighbors that haven't been searched yet
            for neighbor in neighbors:
                if neighbor.searched == False:

                    # Update cost 
                    new_cost = vertex.total_cost + neighbor.move_cost

                    # If that cost is lower than its existing cost, update the total cost to the new value
                    if neighbor.total_cost > new_cost:
                        neighbor.total_cost = new_cost

                    # add to queue if it isn't there already
                    if neighbor not in self.queue:
                        self.queue.append(neighbor)

                # Also check if it is the goal, update the flag/add to path if so, and stop pathfninding
                if neighbor.pos == self.goal: 
                    self.goal_reached = True
                    self.path.append(neighbor)
                    return
                
            # Flag vetex as searched, remove it from queue, and sort queue by score
            vertex.searched = True
            self.queue.pop(0)
            self.queue.sort(key=self.sort_function)
            
        # If no path found 
        print('unexpected error')
        
    def run_pathfinding(self):
        # Finds cheapest path 
        # Check if this is a valid question, immediately break if so
        if self.check_path_invalid() == False:
            print('invalid path')
            return

        # If start is goal, no path needed
        if self.goal == self.start:
            print("you're already there!")
            return
        
        # Check if algorithm is actually useable before running anything
        if self.algorithm not in ['D','A','G']:
            print('invalid algorithm')
            return

        # New approach: continuous queue
        # Instead of the for loop. let's make a new function that runs until goal is reached
        # Initialize queue
        self.queue.append(self.scan_matrix[int(self.start.x),int(self.start.y)])

        # Run algorithm until path found
        self.continuous_queue()

        # Reconstruct path from grid
        self.return_path()

        # Old stuff
                # Attempt to add a step for every possible square on the grid
        # for _ in range(self.search_limit):            

        #     # Create queue of equal-cost vertices to check
        #     self.get_minimums()

        #     # Iterate through queue, implementing the algorithm steps for each vertex
        #     self.handle_queue()

        #     # If we're at the goal, reconstruct and return the path
        #     if self.goal_reached == True: 
               
        #         self.return_path()
        #         print('path returned')
        #         return self.path
        # If we've made it this far, find and return the path (if any)

        
        #If no path found, say so
        #print('path not found')

        




# class AstarPathfinder:
#     '''Implementation of Astar Pathfinding'''
#     def __init__(self,window,start:v2,goal:v2,grid):
#         self.SCREEN = window
#         self.start = start
#         self.goal = goal
#         self.grid = grid
#     def find(self):
#         #allowing diagonal movement to kinda differentiate the algorithms
#         pathfinder = AStar(diagonal_movement=True)