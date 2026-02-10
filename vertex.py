# Vertex class for use by the pathfinding algorithms. This seems like the easiest way
# to keep track of the data, and makes setup and algorithm a bit easier

from numpy import inf, array
from pygame import Vector2 as v2

class Vertex:

    def __init__(self,x_pos,y_pos):
        '''initialize vertex with default parameters'''
        # Position for ease of use
        # Numpy array for now
        self.pos = v2(x_pos,y_pos)

        # Search and is goal flags
        self.searched = False
        self.is_goal = False
         
        # Dijkstra's algorithm cost value (inf by default) and terrain movement cost (1 for no1)
        self.total_cost = inf
        self.move_cost = 1

    def get_neighbor_positions(self,grid):
        '''return the up to four coordinates for valid neighbor vertices in the grid'''
        # Unpack position
        x_pos,y_pos = self.pos

        # Figure out grid limits  
        limits = len(grid)
        x_values = range(limits)
        y_values = range(limits)

        # Manually return position vectors for each
        neighbor_positions = []

        for displacement in [-1,1]:
            # If the displacement is within the area of the grid, it's a valid neighbor
            if x_pos + displacement in x_values: neighbor_positions.append(v2(x_pos+displacement,y_pos))
            if y_pos + displacement in y_values: neighbor_positions.append(v2(x_pos,y_pos+displacement))

        return neighbor_positions
