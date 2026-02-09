# Vertex class for use by the pathfinding algorithms. This seems like the easiest way
# to keep track of the data, and makes setup and algorithm a bit easier

from numpy import inf, array

class Vertex:

    def __init__(self,x_pos,y_pos):
        '''initialize vertex with default parameters'''
        # Position for ease of use
        # Numpy array for now
        self.pos = array([x_pos,y_pos])

        # Search and is goal flags
        self.searched = False
        self.is_goal = False
         
        # Dijkstra's algorithm cost value (inf by default)
        self.cost = inf

    def get_neighbor_positions(self):
        '''return the four (POSSIBLE) coordinates for neighbor vertices'''
        # Unpack position
        x_pos,y_pos = self.pos

        # Manually return position vectors for each
        neighbors = [
            array([x_pos,y_pos+1]),
            array([x_pos,y_pos+1]),
            array([x_pos,y_pos+1]),
            array([x_pos,y_pos+1])
        ]

        return neighbors
