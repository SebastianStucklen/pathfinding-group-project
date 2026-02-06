import random
import numpy as np
import pygame as pg
from globals import SCREEN_RECT

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
