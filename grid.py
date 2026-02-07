import random
import numpy as np
import pygame as pg
from globals import SCREEN_RECT
from pygame import Vector2 as v2

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

	def create_grid_objects(self,obstaclesnum:int):
		#gonna make this a random object gen, we can change it if we want eventually
		obstacles = []
		for i in range(obstaclesnum):
			obstacles.append(v2(random.randint(0,self.gridsize-1),random.randint(0,self.gridsize-1)))
		for i in range(len(obstacles)):
			self.grid[int(obstacles[i].x)][int(obstacles[i].y)] = 1
		print(self.grid)
screen = pg.display.set_mode((800,800))
test = Gird(screen,16)
test.create_grid_objects(16)