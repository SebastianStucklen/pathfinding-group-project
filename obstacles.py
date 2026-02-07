import pygame as pg
from globals import SCREEN_SIZE


class Cell:
    def __init__(self,position,cell_type,cellsize):
        '''
        position: grid coordinates, pg Vector2 from grid coordinates
        cell_type, int, currently 0 for empty, 1 for obstacle. Can add as needed
        grid_resolution, number of cells across for the grid
        '''
        # Position, size, type
        self.render_position = position*cellsize
        self.cell_width = cellsize
        self.cell_type = cell_type

        # What colors this cell can have
        self.colors = [(255,255,255),(0,0,0)]

        # Keep track of parameters as a pygame rectangle object
        # https://www.pygame.org/docs/ref/rect.html#pygame.Rect
        self.rect = pg.Rect(self.render_position[0],self.render_position[1],
                            self.cell_width,self.cell_width)

    def display_cell(self,window:pg.Surface):
        '''
        Displays cell
        '''
        #https://www.pygame.org/docs/ref/draw.html#pygame.draw.rect
        pg.draw.rect(window,self.colors[self.cell_type],self.rect)