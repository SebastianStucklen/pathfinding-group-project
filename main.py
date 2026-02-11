import pygame as pg
from grid import Grid
from algorithms import Pathfinder
from pygame import Vector2 as v2
from matplotlib import pyplot
import seaborn
import pandas

start = v2(0,0)
end = v2(30,30)
obs_num = 320

# test code:
screensize = 640
screen = pg.display.set_mode((screensize,screensize))
test = Grid(screen,32)
test.create_grid_objects(obs_num,start,end)
test.draw()
# testpath = Pathfinder(screen,v2(0,9),v2(15,5),test.grid,'G')
# testpath.run_pathfinding()
astar = Pathfinder(screen,start,end,test.grid,'A')
dijkstra = Pathfinder(screen,start,end,test.grid,'D')
greedy = Pathfinder(screen,start,end,test.grid,'G')



def checker():
	if astar.check_path_invalid() == False:
		test.reset_grid()
		test.create_grid_objects(obs_num,start,end)
		return True
	else:
		return False
	
def main():
	while checker():
		print('fixing')
	doExit = False
	state = 0
	while not doExit:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				doExit = True #lets you quit program
			if event.type == pg.MOUSEBUTTONDOWN:
				state+=1
		if state == 0:
			test.draw()
			astar.run_pathfinding()
			state +=1

		if state == 2:
			test.draw()
			dijkstra.run_pathfinding()
			state +=1

		if state == 4:
			test.draw()
			greedy.run_pathfinding()
			state +=1
		
		if state == 6:
			doExit = True

		pg.display.flip()

main()
path_dict = {
	'algorithms':['astar','dijkstra','greedy'],
	'steps':[len(astar.path),len(dijkstra.path),len(greedy.path)],
	'search_steps':[astar.search_steps,dijkstra.search_steps,greedy.search_steps]
	}
path_frame = pandas.DataFrame(path_dict)

seaborn.barplot(path_frame,x='algorithms',y='search_steps')
pyplot.show()
# Run multiple algorithms on the same grid
# Change grid while algorithm is running
# UI of some kind