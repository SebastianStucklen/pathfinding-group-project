

# Test comment

class Traveler:
    def __init__(self,position,cellsize,algorithm):
        '''traveler'''

        #Initialize grid and render positions
        self.position = position
        self.render_position = position * cellsize
        self.path = []
	
    def follow_path(self):        
        # Only act if there is a path to follow
        if self.path != []:

            # Move to next position in path, then remove that position from the path
            self.pos = self.path[0]
            self.path.pop(0)
	
    def find_path(self,algorithm,goal,grid):
        # Implement one of the algorithms to find the best path
        # THIS IS DRAFT SYNTAX AND LIKELY WON'T WORK YET
        path = algorithm(self.pos,goal,grid)
        self.path = path

    def draw(self):
        # Many options to choose from here TODO
        pass


        
