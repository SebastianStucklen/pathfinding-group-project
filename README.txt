PATHFINDER PROJECT

Installation:
No additional addons are required: everything is included within this folder.
After dowloading the folder, run the text in the "main" file to test the algorithms


How to run:
Open and run the main.py file. For default operation, simply run the file.
Click the pygame screen to queue up to the next pathfinding run. This can be done
during the current run or after it has finished, but will not proceed until
the current run has finished. Once all three pathfinding runs have finished, 
the first bar plot (total searched cells) will display. Close
this plot to see the next (path length). Close this plot to return the program
to its original state. It is possible to stop running additional pathfinding runs after
the. Instead of clicking the pygame screen, close it to skip to the remaining runs
and move straight to the (incomplete) plots.

Input parameters can be modified by passing keyword arguments to the
compare_algorithms function call on line 104 of the "main" file. These arguments are:

start: where the pathfinding algorithms start (pygame vector2, imput as v2(x,y))
end: where the pathfinding algorithms are trying to go (vector2)
obs_num: Number of obstacles, from 1 up to total number of cells in grid - 5
screensize: display screen width, between 100 and 1000 pixels
n_cells: Number of cells wide to make the pathfinding grid, between 4 and 128


Expected behavior:
Upon being run, the program will randomly generate a grid of obstacles.
It will attempt to find a path between the start and the goal using three different
pathfinding algorithms, and will animate each as it attempts to reach the goal. Checked
(non-obstacle) grid cells are marked with yellow circles, and the final path (if one is found)
is displayed as a gradient from blue (start) to red (goal). After
each pathfinding run, this path and all searched cells are shown until program is
clicked through to the next run. Once all three runs have finished, the program will
display two plots in succession: the number of searched vertices and the length of the path
for each algorithm. The plots display sequentially. Once the second has closed,
the program returns to its original state. 

Without running the algorithms, we cannot actually guarantee that any given
start/goal pair has a path between them, so some pathfinding runs
will result in no path being found. This will be printed to terminal, as will any
error messages or status updates. 

Bugs, quirks, and other things of note:
The parameters are not filtered. Looking for grid cells outside the
range of the program will crash the program. We have implemented some input filtering, but we cannot
guarantee there is not some combination of attributes that will behave unexpectedly.

Number of checked cells if off by +- 2, though path length is accurate (counting
number of cells included in path, including start and enpoints in the total length). We
believe this is an acceptable amount of error for qualitative comparisons of search 
length, but it is a bug nonetheless.

