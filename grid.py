import random
import numpy as np
import pygame as pg
from pygame import Vector2 as v2
from obstacles import Cell
from pygame import Rect
from vertex import Vertex
from algorithms import Pathfinder


class Grid:
	'''Pygame Surface (screen)
	dimensions of grid as int. (16 for a 16x16 grid etc.)
	creates grid, places and initialized grid obstacles'''
	def __init__(self,window:pg.Surface,gridwh:int):
		self.SCREEN = window
		#size of each cell
		self.gridsize = gridwh
		self.cellsize = self.SCREEN.get_width()/gridwh

		#create array
		temp = []
		for i in range(self.gridsize):
			temp.append([])
			for j in range(self.gridsize):
				temp[i].append(0)
		self.grid = np.array(temp)
		self.obstacles = []


	def reset_grid(self):
		temp = []
		for i in range(self.gridsize):
			temp.append([])
			for j in range(self.gridsize):
				temp[i].append(0)
		self.grid = np.array(temp)
		self.obstacles = []


	def create_grid_objects(self,obstaclesnum:int,start:v2,end:v2):
		'''generates and places grid obstacles'''
		genlist = [start,end]
		#creates list of vectors for obstacle position
		for i in range(obstaclesnum):
			tempob = v2(random.randint(0,self.gridsize-1),random.randint(0,self.gridsize-1))
			if tempob not in genlist:
				genlist.append(tempob)
			else:
				is_invalid = True
				while is_invalid:
					tempob = v2(random.randint(0,self.gridsize-1),random.randint(0,self.gridsize-1))
					if tempob not in genlist:
						is_invalid = False
						genlist.append(tempob)
		#adds them to the self.grid, and creates list of obstacle objects
		del genlist[0]
		del genlist[1]
		templist = genlist
		for i in range(len(genlist)-1):
			if genlist[i].x == start.x and genlist[i].y == start.y:
				del templist[i]
			elif genlist[i].x == end.x and genlist[i].y == end.y:
				del templist[i]
		genlist = templist
		for i in range(len(genlist)):
			self.grid[int(genlist[i].x)][int(genlist[i].y)] = 1
			self.obstacles.append(Cell(v2(genlist[i].x,genlist[i].y),1,self.cellsize))
		# with open('output_file.txt', 'w') as file:
		# 	file.write(str(self.grid))

	def draw(self):
		self.SCREEN.fill('white')
		for i in range(len(self.grid)):
			for j in range(len(self.grid[i])):
				if self.grid[i][j] == 1:
					temp = Rect((j*self.cellsize),(i*self.cellsize),self.cellsize,self.cellsize)
					pg.draw.rect(self.SCREEN,'black',temp)
				# else:
				# 	temp = Rect((j*self.cellsize),(i*self.cellsize),self.cellsize,self.cellsize)
				# 	pg.draw.rect(self.SCREEN,'red',temp)


