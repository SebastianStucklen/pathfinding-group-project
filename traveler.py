


class Traveler:
    def __init__(self,position,cellsize,algorithm):

        #Initialize grid and render positions
        self.position = position
        self.render_position = position * cellsize
        self.path = []
        pass
	
    def follow_path(self,direction):
	    # move 1 step along the path
        pass
	
    def find_path(self,algorithm,goal):
        # Implement one of the algorithms to find the best path
        path = []
        self.path = path

    def draw(self):
        # Many options to choose from here
        pass


        
