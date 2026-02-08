import random
import numpy as np
import pygame as pg
from globals import SCREEN_RECT
from pygame import Vector2 as v2
from obstacles import Cell

class Grid:
	'''Pygame Surface (screen)
	dimensions of grid as int. (16 for a 16x16 grid etc.)
	creates grid, places and initialized grid obstacles'''
	def __init__(self,window:pg.Surface,gridwh:int):
		self.SCREEN = window
		#size of each cell
		self.gridsize = gridwh
		self.cellsize = SCREEN_RECT.width/gridwh

		#create array
		temp = []
		for i in range(self.gridsize):
			temp.append([])
			for j in range(self.gridsize):
				temp[i].append(0)
		self.grid = np.array(temp)
		self.matrix = np.full(self.gridsize,self.gridsize)
		self.obstacles = []

	def create_grid_objects(self,obstaclesnum:int):
		'''generates and places grid obstacles'''
		grid = []
		#creates list of vectors for obstacle position
		for i in range(obstaclesnum):
			grid.append(v2(random.randint(0,self.gridsize-1),random.randint(0,self.gridsize-1)))
		#adds them to the self.grid, and creates list of obstacle objects
		for i in range(len(grid)):
			self.grid[int(grid[i].x)][int(grid[i].y)] = 1
			self.obstacles.append(Cell(v2(grid[i].x,grid[i].y),1,self.cellsize))


#test code:
# screen = pg.display.set_mode((800,800))
# test = Grid(screen,16)
# test.create_grid_objects(16)