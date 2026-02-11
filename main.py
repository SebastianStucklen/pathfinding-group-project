import pygame as pg
from grid import Grid
from algorithms import Pathfinder
from pygame import Vector2 as v2
from matplotlib import pyplot
import seaborn
import pandas


def compare_algorithms(start = v2(0,0), end = v2(30,30), obs_num = 320,
					   screensize = 640, n_cells = 32):
	'''
	This is the main function that runs the comparison

	Input Parameters
	start: where the pathfinding algorithms start (pygame vector2, imput as v2(x,y))
	end: where the pathfinding algorithms are trying to go (vector2)
	obs_num: Number of obstacles, from 1 up to total number of cells in grid - 5
	screensize: display screen width, between 100 and 1000 pixels
	n_cells: Number of cells wide to make the pathfinding grid, between 4 and 128

	'''

	# Some imput filtering to minimize risk of loop crashes
	# Only allow code to run if obstacle count leaves at least 5 empty cells
	if obs_num > n_cells**2 - 5 or obs_num < 1:
		print('too many obstacles!')
		return
	
	# Screens must be reasonable in size
	if screensize > 1000 or screensize < 100:
		print('screen size too extreme!')
		return
	
	if n_cells > 128 or n_cells < 4:
		print('number of cells too extreme!')
		return
	
	screen = pg.display.set_mode((screensize,screensize))
	test = Grid(screen,n_cells)
	test.create_grid_objects(obs_num+1,start,end) #+1 for off-by-1 error
	test.draw()
	astar = Pathfinder(screen,start,end,test.grid,'A')
	dijkstra = Pathfinder(screen,start,end,test.grid,'D')
	greedy = Pathfinder(screen,start,end,test.grid,'G')

	

	def checker():
		# Finds a grid that does not obscure the chosen start/end points
		# Use the check-valid feature from one of the pathfinders to do this
		# This function is exclusively useful when called within compare_algorithms
		# and requires a pathfinder to work, so we define it within compare_algorithms 
		if astar.check_path_invalid() == False:
			test.reset_grid()
			test.create_grid_objects(obs_num+1,start,end) # +1 patches an off by 1 error somewhere
			return True
		else:
			return False
	
	# Generate a valid grid
	while checker():
		print('fixing')

	# Parameters for input tracking
	doExit = False
	state = 0
	move_allowed = False # Prevents absent-mindedly clicking through all 3 at once

	# Run the main animation loop to compare the three algorithms
	while not doExit:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				doExit = True #lets you quit program
			if event.type == pg.MOUSEBUTTONDOWN and move_allowed == True:
				state+=1
				move_allowed = False
		
		if state == 0:
			test.draw()
			dijkstra.run_pathfinding()
			state +=1
			move_allowed = True

		if state == 2:
			test.draw()
			greedy.run_pathfinding()
			state +=1
			move_allowed = True

		if state == 4:
			test.draw()
			astar.run_pathfinding()
			state +=1
			move_allowed = True
		
		if state == 6:
			doExit = True

		pg.display.flip()

	
	# Plot steps taken by each algorithm	
	path_dict = {
	'algorithms':['astar','dijkstra','greedy'],
	'steps':[len(astar.path),len(dijkstra.path),len(greedy.path)],
	'search_steps':[astar.search_steps,dijkstra.search_steps,greedy.search_steps]
	}
	path_frame = pandas.DataFrame(path_dict)

	seaborn.barplot(path_frame,x='algorithms',y='search_steps')
	pyplot.title('Total Searched Steps by Algorithm')
	pyplot.show()

	seaborn.barplot(path_frame,x='algorithms',y='steps')
	pyplot.title('Path Length by Algorithm')
	pyplot.show()


# Pass kwargs to modify details of simulation
# Default parameters are chosen to highlight strengths/weaknesses of different algorithms.
compare_algorithms()
