# File for the different pathfinding algorithms, each defined as a seperate
# function. Can split into multiple  iles for different algorithms later if 
# that ends up being easier to work on

# This could also be a class, but I'm not sure what doing that would add. 

import pygame as pg
from pygame import Vector2 as v2
import numpy as np
from vertex import Vertex
import pathfinding
from pathfinding.finder.a_star import AStarFinder as AStar
import pdb
# Notes:
# queue.sort(key=,ascending)
# define key with function

class DijkstraPathfinder:
    # Implements the dijstra pathfinding algorithm using the steps outlined in
    #(https://www.w3schools.com/dsa/dsa_algo_graphs_dijkstra.php)
    # TODO check if goal is unreachable

    def __init__(self,screen:pg.Surface,start:v2,goal:v2,grid):

        # Initialize various parameters
        self.SCREEN = screen

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
        
        self.path = []
        self.queue = []

    
        '''setup pathfinding algorithm scan'''
        # Initialize vertex scanning matrix
        gridshape = len(self.grid)

        # Iterate through columns
        for y_pos in range(gridshape):

            # Fill columns with default vertices
            column = []
            for x_pos in range(gridshape):
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
        neighbor_positions = []
        neighbor_positions = vertex.get_neighbor_positions(self.grid)
        neighbors = []
        for position in neighbor_positions:
            # Unpack position
            x,y = int(position.x),int(position.y)
            
            # Add vertex to neighbors if it corresponds to a non-obstacle
            if self.grid[x,y] != 1: 
                neighbors.append(self.scan_matrix[x,y])
                print(position)
        print('loop done')
        return neighbors

    def get_minimums(self):
        '''Find the values in the scan matrix with a minimum cost and return a list of all of them'''

        #Starting at current minimum cost, add 1 and check if any values in the matrix satisfy this
        # Empty queue
        self.queue = []
        
        # Run until we have the next minimum value
        while len(self.queue) == 0:

            # Iterate through all entries
            for column in self.scan_matrix:
                for vertex in column:
                    if vertex.total_cost == self.min_cost and vertex.searched == False:
                        self.queue.append(vertex)
            
            # Once any vertices are added, add 1 to minimum value
            self.min_cost += 1
            print(self.min_cost)


    def handle_queue(self):
        # Handle algorithm steps for each entry to check in the queue
        for vertex in self.queue:
        #if vertex.searched == True:
            
            neighbors = []
            neighbors = self.get_valid_neighbors(vertex)
            #print(len(neighbors))
            for neighbor in neighbors:
                new_cost = vertex.total_cost + neighbor.move_cost

                # For each, set total cost to movement cost + cost to get here if that's lower than the current total
                # Also check if it is the goal, and update the flag/add to path if so
                if neighbor.pos == self.goal: 
                    self.goal_reached = True
                    self.path.append(neighbor)

                if neighbor.total_cost > new_cost:
                    neighbor.total_cost = new_cost
            
            # Set searched flag to true for the vertex once this is done
            vertex.searched = True
                


    def return_path(self):
        '''From solved scan matrix, reconstruct the path from start to goal'''
        # Only does anything if path is no longer empty (because goal has been added)
        # print('return path')
        if len(self.path) != 0:
            a = 0
            pg.font.init()
            font = pg.font.SysFont("Times New Roman", 22) 
            finished = False
            while finished == False:
                # Check neighbors of most recently added item 
                new_step = self.path[-1]
        
                #neighbor_positions= new_step.get_neighbor_positions(self.grid)
                neighbors = self.get_valid_neighbors(new_step)
                neighbor_positions = []
                for neighbor in neighbors:
                        neighbor_positions.append(neighbor.pos)

                # Add the first neighbor we see with total cost = total cost - move cost
                for x,y in neighbor_positions:
                    possible_step = self.scan_matrix[int(x),int(y)]
                    if possible_step.total_cost == new_step.total_cost - new_step.move_cost:
                        self.path.append(possible_step)
                        pg.draw.rect(self.SCREEN,(a,50,50),(possible_step.pos.x*100,possible_step.pos.y*100,100,100))
                        text_surface = font.render(str(a), True,'black')
                        self.SCREEN.blit(text_surface,(possible_step.pos.x*100,possible_step.pos.y*100))
                        if a <= 235:
                            a+=20
                        break
                # Repeat until we add something with total cost = 0
                if new_step.total_cost == 0:
                    finished = True

                    # This is a backwards path, so spin it around. https://www.w3schools.com/python/ref_list_reverse.asp
                    self.path.reverse()

                    # This is a list of vertices, and we want coordinates, so we 
                    # overwrite path with a list of vectors
                    vector_list = []
                    for vertex in self.path:
                        vector_list.append(vertex.pos)
                    
                    self.path = vector_list
    def draw(self):
        for path in self.path:
            pg.draw.rect(self.SCREEN,'yellow',(path.x*100,path.y*100,100,100))

    def run_pathfinding(self):
        # Finds cheapest path 
        # Loop until goal reached, unless start is goal, in which case nothing happens
        # Check if this is a valid questioh

        if self.goal == self.start:
            self.goal_reached = True

        while self.goal_reached == False:
            #pdb.set_trace()
            print('running')
            # Create queue of equal-cost vertices to check
            self.get_minimums()

            # Iterate through queue, implementing the algorithm steps for each vertex
            self.handle_queue()

            # If we're at the goal, reconstruct and return the path
            if self.goal_reached == True: 
               
                self.return_path()
                print('test')
                print(self.path)



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