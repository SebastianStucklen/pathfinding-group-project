import random
import numpy as np
import pygame as pg
from globals import SCREEN_RECT
from pygame import Vector2 as v2
from obstacles import Cell

class Gird:
	'''Grid'''
	#todo
	#will take cell number (width and height) and calculate size based on screen size (800x800)
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
		#gonna make this a random object gen, we can change it if we want eventually
		grid = []
		for i in range(obstaclesnum):
			grid.append(v2(random.randint(0,self.gridsize-1),random.randint(0,self.gridsize-1)))
		for i in range(len(grid)):
			self.grid[int(grid[i].x)][int(grid[i].y)] = 1
			self.obstacles.append(Cell(v2(grid[i].x,grid[i].y),1,self.cellsize))
		print(self.grid)
		#print(self.obstacles)



screen = pg.display.set_mode((800,800))
test = Gird(screen,16)
test.create_grid_objects(16)