# EVERY ARRAY IS INDEXED Y,X!!!!!!!!! DO NOT FORGET THIS!!!!!!! 
import pygame as pg
from pygame import Vector2 as v2
import numpy as np
from vertex import Vertex
import pdb

class Pathfinder:
    # Implements the dijstra pathfinding algorithm using the steps outlined in
    #(https://www.w3schools.com/dsa/dsa_algo_graphs_dijkstra.php)
    # Substantial inspiration from 
    # https://www.redblobgames.com/pathfinding/a-star/introduction.html)
    # for this as well

    def __init__(self,screen:pg.Surface,start:v2,goal:v2,grid,algorithm:str):
        '''setup pathfinding algorithm scan'''
        # store world grid and initialize scanning grid
        self.grid = grid
        scan_matrix = []

        # Initialize screen grid parameters
        self.SCREEN = screen
        self.gridshape = len(self.grid)
        self.screen_width = self.SCREEN.get_width()
        self.cell_size = self.screen_width/self.gridshape

        # Algorithm to use
        self.algorithm = algorithm

        # Starting and goal positions
        self.start = start
        self.goal = goal

        # Goal flag and frontier costs
        self.goal_reached = False
        self.min_cost = 0
        
        # Path and queue lists
        self.path = []
        self.queue = []

        # Limits how long the program will spend trying to pass through walls
        self.search_limit = self.gridshape**2
        self.search_steps = 0
        # Rendering parameters for visualizing the algorithm
        self.radius = self.cell_size * 0.45
        self.offset = self.cell_size/2

        # Initialize square scanning matrix of same size as grid
        for y_pos in range(self.gridshape):

            # Fill rows with default vertices
            row = []
            for x_pos in range(self.gridshape):
                row.append(Vertex(x_pos,y_pos))

            # Append rows to vertex matrix
            scan_matrix.append(row)
        

        # Turn matrix into a np array
        self.scan_matrix = np.array(scan_matrix)
        
        # Assign total cost of 0 to starting vertex, goal flag for goal vertex
        self.scan_matrix[int(self.start.y),int(self.start.x)].total_cost = 0
        self.scan_matrix[int(self.goal.y),int(self.goal.x)].is_goal = True


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
            if self.grid[y,x] != 1: 
                neighbors.append(self.scan_matrix[y,x])

        return neighbors
          
    def return_path(self):
        '''From solved scan matrix, reconstruct the path from start to goal'''
        # Only does anything if path is no longer empty (because goal has been added)
        if len(self.path) != 0:

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
                        break

                # Repeat until we add something with total cost = 0, as that's the start point!
                if new_step.total_cost == 0:
                    finished = True
                    
                    # This is a backwards path, so spin it around. https://www.w3schools.com/python/ref_list_reverse.asp
                    self.path.reverse()

                    # This is a list of vertices, and we want coordinates, so overwrite path with a list of vectors
                    vector_list = []
                    for vertex in self.path:
                        vector_list.append(v2(vertex.x,vertex.y))
                    
                    self.path = vector_list

    def check_path_invalid(self):
        # Checks that start and end points are not obstacles to avoid running an obviously impossible sim
        # Exploiting properties of booleans
        # allows us to split this into a few legible lines instead of one giant one
        start_check = self.grid[int(self.start.y),int(self.start.x)] != 1
        goal_check = self.grid[int(self.goal.y),int(self.goal.x)] != 1

        if start_check == True and goal_check == True:
            return True
        else:
            return False
        #return (start_check and goal_check)
    
    def heuristic(self,vertex):
        '''Score for distance to goal'''
        #Manhattan distance for use in A*, greedy algorithms
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
            self.search_steps += 1
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
            
            #Show progress
            self.display_vertices()
            pg.time.delay(10)
            
        # If no path found 
        print('unexpected error')
        
    def run_pathfinding(self):

        # Check if this is a valid question, immediately break if so
        if self.check_path_invalid() == False:
            print('start or goal blocked')

            # Show the out of bounds problem
            self.display_vertices()
            return

        # If start is goal, no path needed
        if self.goal == self.start:
            print("you're already there!")
            return
        
        # Check if algorithm is actually useable before running anything
        if self.algorithm not in ['D','A','G']:
            print('invalid algorithm')
            return

        # Reset and initialize queue
        self.queue = []
        self.path = []
        self.queue.append(self.scan_matrix[int(self.start.y),int(self.start.x)])

        # Run algorithm until path found
        self.continuous_queue()

        # Reconstruct path from grid
        self.return_path()

        # Show path and announce success if path exists
        self.display_vertices()

        if len(self.path) > 0: print('path found!')

    def display_vertices(self):

        # Show all searched vertices in yellow
        for row in self.scan_matrix:
            for vertex in row:
                if vertex.searched == True:
                    pg.draw.circle(self.SCREEN,
                                   (200,200,0),
                                   (self.cell_size*vertex.pos.x+self.offset,self.cell_size*vertex.pos.y+self.offset),
                                   self.radius)

        # Show path as a gradient from the source if there is a path to show
        if len(self.path) > 0:
            path_gradient_step = 255/len(self.path)
            color_step = 0
            for coordinate in self.path:
                color_step += path_gradient_step
                pg.draw.circle(self.SCREEN,
                               (int(color_step),0,int(255-color_step)),
                               (self.cell_size*coordinate.x+self.offset,self.cell_size*coordinate.y+self.offset),
                               self.radius)
                
        # Redraw start and endpoints over old map, and updates display
        self.start_and_end()
        pg.display.update()
                
    def start_and_end(self):
        '''draw circles at start and endpoints'''
        pg.draw.circle(self.SCREEN, 'blue', (self.cell_size * self.start.x + self.offset, self.cell_size * self.start.y + self.offset),self.radius)
        pg.draw.circle(self.SCREEN, 'red', (self.cell_size * self.goal.x + self.offset, self.cell_size * self.goal.y + self.offset),self.radius)

    def traveler(self):
        pass
        



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

# Render code
            # a = 0
            # width = self.cell_size
            # pg.font.init()
            # font = pg.font.SysFont("Times New Roman", 22) 
            # pg.draw.rect(self.SCREEN,(a,50,50),(self.path[-1].pos.x*width,self.path[-1].pos.y*width,width,width))
            # text_surface = font.render(str(a), True,'black')
            # self.SCREEN.blit(text_surface,(self.path[-1].pos.x*width,self.path[-1].pos.y*width))
            # a += 5

 # Render code
                        # pg.draw.rect(self.SCREEN,(a,50,50),(neighbor.pos.x*width,neighbor.pos.y*width,width,width))
                        # text_surface = font.render(str(a), True,'black')
                        # self.SCREEN.blit(text_surface,(neighbor.pos.x*width,neighbor.pos.y*width))
                        # if a <= 235:
                        #     a+=5