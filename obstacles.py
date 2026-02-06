import pygame as pg
from globals import SCREEN_SIZE


class Cell:
    def __init__(self,position,cell_type,cellsize):
        '''
        position: grid coordinates, pg Vector2 from grid coordinates
        cell_type, string, currenty either obstacle or empty
        grid_resolution, number of cells across for the grid
        '''
        # Position, size, type
        self.position = position*cellsize
        self.cell_width = cellsize
        self.cell_type = cell_type

        # What colors this cell can have
        self.colors = {'empty':(255,255,255),'obstacle':(0,0,0)}

        # Keep track of parameters as a pygame rectangle object
        # https://www.pygame.org/docs/ref/rect.html#pygame.Rect
        self.rect = pg.Rect(self.position[0],self.position[1],cell_width,cell_width)

    def display_cell(self,window:pg.Surface):
        '''
        Displays cell
        '''
        #https://www.pygame.org/docs/ref/draw.html#pygame.draw.rect
        pg.draw.rect(window,self.colors[self.cell_type],self.rect)