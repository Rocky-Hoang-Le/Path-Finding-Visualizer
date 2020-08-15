# Path-Finding-Visualizer
This program will allow the user visualize the process of 5 different path finding algorithms.


# Instructions
When starting the program an instructions menu will be brought up to display how to use it.

Before the program starts the user can select the following options:

Change FPS - Allow user to change FPS which will affect the animation speed, default is 15 max is 120, change in increments of 5.

Change Grid size - Allow user to change grid size (number of rows and columns). default is 5 and change is increments of 5 (cannot change to certain sizes)
since the grid is created based on screen size, allowing certain sizes would give uneven cell sizes.

Change Heuristic - Allow user to change the distance formula method for the path finding functions that use heuristics.
Manhattan distance and Euclidean distance are the 2 options availible.

After the program starts there are 5 algorithms to choose from and pressing the corresponing key will start it:

1: A*

2: Greedy Best Search

3: Dijkstra

4: Breadth First Search

5: Depth First Search

# Node types

White - Neutral

Orange - Starting Node

Cyan - End Node

Silver - Visited node (Closed node)

Blue - Free node (Open node)

Yellow - Path node (Nodes that belong to the shortest path from start to end node)

# Notes 

Path finding will only start if the start and end nodes have been placed.


Plan on adding and displaying a timer to measure the speed of each algorithm

