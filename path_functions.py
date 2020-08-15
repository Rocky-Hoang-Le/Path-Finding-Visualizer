# Import required modules
import pygame  # This is needed here so the user can quit if they need to while this script is running
import math
from queue import PriorityQueue


# Functions for use with the path_finding functions

# Use manhattan distance to find distance between 2 points (no diagonals)
def find_manhattan_distance(start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    return abs(x1 - x2) + abs(y1 - y2)


# Use euclidean distance to find distance between two point (allows diagonals)
def find_euclidean_distance(start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


option = 1
def heuristic_to_use(start_pos, end_pos):
    if option == 1:
        return find_manhattan_distance(start_pos, end_pos)
    elif option == 2:
        return find_euclidean_distance(start_pos, end_pos)


# This function draws the lowest cost path_finding answer from end node to start node
def shortest_path(node_map, current_node, draw):
    while current_node in node_map:
        current_node = node_map[current_node]  # Set current node as the node before it/ neighbor node to it
        current_node.set_path()  # Turn the node into a path node
        draw()


# Path finding functions that will solve and draw its process
# Informed search functions are first

# This function finds the shortest path using A star (Informed Search)
def a_star_path(draw, grid, start, end):
    # Setup initial node information
    node_map = {}  # A mapping to know which which node parent goes to which node neighbor
    unexplored_pq = PriorityQueue()  # Priority queue for indexing the lowest f_score node
    unexplored_pq.put(
        (0, start))  # Store unexplored nodes by its (f_score, Node object). Start node has init f_score of 0
    # g_score measures the cost/weight of the node path
    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0
    # f_score measures how optimal the node path is
    f_score = {node: float('inf') for row in grid for node in row}
    f_score[start] = heuristic_to_use(start.get_pos(), end.get_pos())

    while not unexplored_pq.empty():
        # Allow user to exit program while the algorithm is running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_node = unexplored_pq.get()[1]  # Set current node as lowest f_score node in queue

        # If the current node is the end node the path is found, begin drawing the shortest path
        if current_node == end:
            shortest_path(node_map, end, draw)
            return True

        # This block does the calculations determining the next optimal node to go too
        for relative_node in current_node.relative_nodes:
            temp_g_score = g_score[
                current_node]  # Have a temp g_score variable in case i want to use weighted cells later
            if relative_node not in g_score or temp_g_score < g_score[relative_node]:  # Check to see if the node has been considered and if so is that node better
                g_score[relative_node] = temp_g_score
                f_score[relative_node] = temp_g_score + heuristic_to_use(relative_node.get_pos(), end.get_pos())
                unexplored_pq.put((f_score[relative_node], relative_node))
                node_map[relative_node] = current_node  # Sets the neighbour nodes parent
                relative_node.set_free()  # Sets node as free which can be re-explored if necessary

        # Draw the updated node states and set the current node as a visited node
        draw()
        if current_node != start:
            current_node.set_visited()
    return False


# This function finds the path using Greedy First Search (Informed Search, does not guarantee shortest path)
def greedy_first_path(draw, grid, start, end):
    # Setup node information
    heuristic = {node: float('inf') for row in grid for node in row}  # Heuristic function
    heuristic[start] = heuristic_to_use(start.get_pos(), end.get_pos())  # Set init heuristic as the distance from start to end
    unexplored_nodes = PriorityQueue()  # Priority queue for indexing the lowest heuristic node
    unexplored_nodes.put((0, start))  # Set the heuristic of start node as 0
    node_map = {}  # Mapping to know what parent goes to what node

    while not unexplored_nodes.empty():
        # Allow user to exit program while the algorithm is running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_node = unexplored_nodes.get()[1]  # Set current node as lowest heuristic node

        # If current node is the path has been found
        if current_node == end:
            shortest_path(node_map, end, draw)
            return True

        # Check every relative node to see where the next path should be
        for relative_node in current_node.relative_nodes:
            if heuristic[relative_node] > heuristic_to_use(relative_node.get_pos(), end.get_pos()):  # Compare heuristic and set relative node heuristic to smaller one
                heuristic[relative_node] = find_manhattan_distance(relative_node.get_pos(), end.get_pos())
                unexplored_nodes.put((heuristic[relative_node], relative_node))
                node_map[relative_node] = current_node  # Change the parent node of this relative node
                relative_node.set_free()  # Set node as a free node which can be re-explored later if needed

        # Draw the updated node states and set current node as visited node
        draw()
        if current_node != start:
            current_node.set_visited()
    return False


# This function finds the shortest path using Dijkstra (Blind Search)
def dijkstra_path(draw, grid, start, end):
    # Setup initial node information
    node_distances = {node: float('inf') for row in grid for node in row}  # Set all node distances as infinity
    node_distances[start] = 0  # Set starting node distance as 0
    unexplored_nodes = PriorityQueue()  # Priority queue for indexing the lowest distance node
    unexplored_nodes.put((0, start))  # Store unexplored nodes by its (distance, Node object). Start node has init distance of 0
    node_map = {}  # A mapping to know which which node parent goes to which node neighbor

    while not unexplored_nodes.empty():
        # Allow user to exit program while the algorithm is running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_node = unexplored_nodes.get()[1]  # Set current node as lowest distance node in queue

        # If current node is the path has been found
        if current_node == end:
            shortest_path(node_map, end, draw)
            return True

        # Check every relative node to see where the next path should be
        for relative_node in current_node.relative_nodes:
            # Get new distance based on current nodes distance and distance to next node
            new_dist = node_distances[current_node] + heuristic_to_use(current_node.get_pos(), relative_node.get_pos())

            # If new distances is shorter then the distance given to the relative node update the distance of the relative node and add to queue
            if new_dist < node_distances[relative_node]:
                node_distances[relative_node] = new_dist
                unexplored_nodes.put((node_distances[relative_node], relative_node))
                node_map[relative_node] = current_node  # Set the parent of this relative node
                relative_node.set_free()  # Set node as free which can be re-explored later if needed

        # Draw the updated node states and set current node as a visited node
        draw()
        if current_node != start:
            current_node.set_visited()
    return False


# This function finds the shortest path using Breadth First search (Blind Search)
def breadth_first_path(draw, grid, start, end):
    # Setup node information
    node_distances = {node: float('inf') for row in grid for node in row}  # Set all node distances as infinity
    node_distances[start] = 0  # Set starting node distance as 0
    unexplored_nodes = [start]  # Regular queue that will index whether or not the node has been visited
    node_map = {}  # A mapping to know which which node parent goes to which node neighbor
    while unexplored_nodes:
        # Allow user to exit program while the algorithm is running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_node = unexplored_nodes.pop(0)  # Set current node as the first found non-visited node

        # If current node is the path has been found
        if current_node == end:
            shortest_path(node_map, end, draw)
            return True

        # Check every relative node to see where the next path should be
        for relative_node in current_node.relative_nodes:
            if 0 < node_distances[relative_node]:  # Check to see if the node is visited and if its the start node if not add it to queue
                node_distances[relative_node] = 0
                unexplored_nodes.append(relative_node)
                node_map[relative_node] = current_node  # Set the parent node of this relative node
                relative_node.set_free()  # Set node as a free node for re-exploration if needed

        # Draw the updated node states and set current node as visited
        draw()
        if current_node != start:
            current_node.set_visited()
    return False


# This functions finds the path using depth first search(Blind Search, does not guarantee shortest route)
def depth_first_path(draw, start, end):
    # Setup node information
    unexplored_nodes = [start]  # Stack for pulling the last node
    node_map = {}  # Mapping to know what node has what parent

    while unexplored_nodes:
        # Allow user to exit program while the algorithm is running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_node = unexplored_nodes.pop()  # Set current node as last node in stack

        # If current node is the path has been found
        if current_node == end:
            shortest_path(node_map, end, draw)
            return True

        # Check every relative node to see where the next path should be
        for relative_node in current_node.relative_nodes:
            if not relative_node.is_visited() and not relative_node.is_start():  # Check to see if the node is visited and if its the start node if not add it to stack
                unexplored_nodes.append(relative_node)
                node_map[relative_node] = current_node  # Change the parent node of this relative node
                relative_node.set_free()  # Set node as a free node which can be re-explored if needed

        # Draw updated node states and set current node as visited
        draw()
        if current_node != start:
            current_node.set_visited()
    return False
