# Path finding project
# Goal of this project is to create a path finder using a path finding algorithm
# For this project there will be 5 different algorithims
# A*, Greedy Best , Dijkstra, Breadth First, and Depth First
# The path finder will be visualized using pygame

# Import required modules
import pygame
import pygame_menu
import color
import draw_functions
import path_functions
from path_functions import *
from draw_functions import *

pygame.init()  # Initialize pygame stuff

# Create window of the program
SCREEN_SIZE = 900
WINDOW = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('Path finding algorithms')  # Set tile to window

# Create menu that will be drawn on top of the same window that will allow user to change settings before
menu = pygame_menu.Menu(SCREEN_SIZE, SCREEN_SIZE, 'Path Finder options', theme=pygame_menu.themes.THEME_SOLARIZED)


# The node class contains position, size, node type/color, position of other nodes relative to it,
# and the ability to draw itself
class Node:
    def __init__(self, row, col, grid_size, total_rows):
        self.row = row
        self.col = col
        self.x = row * grid_size
        self.y = col * grid_size
        self.color = color.WHITE
        self.relative_nodes = []
        self.grid_size = grid_size
        self.total_rows = total_rows

    # Return node position based on its row and column
    def get_pos(self):
        return self.row, self.col

    # Checks to see if the node is a barrier or wall
    def is_barrier(self):
        return self.color == color.BLACK

    def is_visited(self):
        return self.color == color.SILVER

    def is_start(self):
        return self.color == color.ORANGE

    def is_free(self):
        return self.color == color.BLUE

    # Resets the current node to neutral
    def reset(self):
        self.color = color.WHITE

    # Set the node as a visited node
    def set_visited(self):
        self.color = color.SILVER

    # Set the node as a free node
    def set_free(self):
        if self.color != color.CYAN:  # Fixes small visual bug where end node is covered by a free cell
            self.color = color.BLUE

    # Sets node as a barrier node
    def set_barrier(self):
        self.color = color.BLACK

    # Sets node as starting node
    def set_start(self):
        self.color = color.ORANGE

    # Sets node as end point node
    def set_end(self):
        self.color = color.CYAN

    # Sets the node as path node which are nodes with the lowest cost to the goal
    def set_path(self):
        if self.color != color.ORANGE:  # Makes it so the start node isn't covered by the path node
            self.color = color.GOLD

    # Draw the node
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.grid_size, self.grid_size))

    # Update information about the relative nodes around this node
    def update_relative_nodes(self, grid):
        self.relative_nodes = []
        # Check below for non barrier nodes
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.relative_nodes.append(grid[self.row + 1][self.col])
        # Check above for non barrier nodes
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.relative_nodes.append(grid[self.row - 1][self.col])
        # Check right for non barrier nodes
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.relative_nodes.append(grid[self.row][self.col + 1])
        # Check left for non barrier nodes
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.relative_nodes.append(grid[self.row][self.col - 1])

    # When comparing the nodes cost against another in a queue always return the other one as lower cost
    def __lt__(self, other):
        return False


# This function creates grid based on how many rows/columns(should be same) and size of the screen
def create_grid(rows, screen_size):
    columns = rows  # Num of columns is same as rows added for better readability
    grid = []
    cell_size = screen_size // rows

    for row in range(rows):
        grid.append([])
        for col in range(columns):
            node = Node(row, col, cell_size, rows)
            grid[row].append(node)
    return grid

# This functions returns which cell position the mouse clicked
def clicked_position(pos, rows, screen_size):
    cell_size = screen_size // rows
    y, x = pos

    row = y // cell_size
    col = x // cell_size
    return row, col

# Main function that will run the program
def main(window, screen_size):
    grid = create_grid(GRID_SIZE, screen_size)

    # Neutral values for the start and end node
    start = None
    end = None

    # Run the program
    run = True
    while run:
        draw(window, grid, GRID_SIZE, screen_size)  # Draw the visualizer
        events = pygame.event.get()  # Store events in a list so menu can reference it
        keys = pygame.key.get_pressed()  # Store keyboard events in a list for easier referencing

        # Allow user to call up menu if needed
        if keys[pygame.K_p]:
            menu.toggle()
        if menu.is_enabled():
            menu.mainloop(window)

        # This block checks if user has quit program or is placing nodes
        for event in events:
            if event.type == pygame.QUIT:
                run = False

            # Check for mouse clicks to see which nodes to place and where
            # Left click will place nodes
            if pygame.mouse.get_pressed()[0]:  # Left mouse click
                pos = pygame.mouse.get_pos()
                row, col = clicked_position(pos, GRID_SIZE, screen_size)
                node = grid[row][col]

                # Checks to see if start and end nodes have been placed yet
                # If not these nodes must be placed first before any other node
                # Start must be placed before end node
                if not start and node != end:
                    start = node
                    start.set_start()
                elif not end and node != start:
                    end = node
                    end.set_end()
                elif node != end and node != start:
                    node.set_barrier()

            # Right click will remove nodes
            elif pygame.mouse.get_pressed()[2]:  # Right mouse click
                pos = pygame.mouse.get_pos()
                row, col = clicked_position(pos, GRID_SIZE, screen_size)
                node = grid[row][col]
                node.reset()

                # Special check to reset start and/or end node if removed
                # If so they must be placed again before algorithm can work
                if node == start:
                    start = None
                elif node == end:
                    end = None

        # Start path finding functions

        # Pressing 1 will start A* path finding
        if keys[pygame.K_1] and start and end:
            for row in grid:
                for node in row:
                    node.update_relative_nodes(grid)
            a_star_path(lambda: draw(window, grid, GRID_SIZE, screen_size), grid, start, end)

        # Pressing 2 will start Greedy Besy Search
        if keys[pygame.K_2] and start and end:
            for row in grid:
                for node in row:
                    node.update_relative_nodes(grid)
            greedy_first_path(lambda: draw(window, grid, GRID_SIZE, screen_size), grid, start, end)

        # Pressing 3 will start Dijkstra path finding
        if keys[pygame.K_3] and start and end:
            for row in grid:
                for node in row:
                    node.update_relative_nodes(grid)
            dijkstra_path(lambda: draw(window, grid, GRID_SIZE, screen_size), grid, start, end)

        # Pressing 4 will start Breadth First Search path finding
        if keys[pygame.K_4] and start and end:
            for row in grid:
                for node in row:
                    node.update_relative_nodes(grid)
            breadth_first_path(lambda: draw(window, grid, GRID_SIZE, screen_size), grid, start, end)

        # Pressing 5 will start Depth First Search path finding
        if keys[pygame.K_5] and start and end:
            for row in grid:
                for node in row:
                    node.update_relative_nodes(grid)
            depth_first_path(lambda: draw(window, grid, GRID_SIZE, screen_size), start, end)


        # Pressing c will reset the screen and make all nodes neutral
        if keys[pygame.K_c]:
            start = None
            end = None
            grid = create_grid(GRID_SIZE, screen_size)

    pygame.display.quit()
    pygame.quit()



# Menu functions to change fps and grid size, and screen size and start program
# Funtion to call main window
def start_finder():
    menu.toggle()
    main(WINDOW, SCREEN_SIZE)

# This menu function allows user to change fps/ speed of animation
def change_fps(*args):
    global draw_functions
    draw_functions.FPS = args[1]

# This menu function allows user to change grid size
GRID_SIZE = 5  # Default size of the grid
def change_grid_size(*args):
    global GRID_SIZE
    GRID_SIZE = args[1]

# This function will allow user to change heuristic/ distance formula for the path finders
def change_heuristic(*args):
    global path_functions
    path_functions.option = args[1]

# Add menu options, text, etc
# Instructions and options string weirdly spaced to look better on the menu layout
instructions = 'Place nodes by clicking on the cells. ' \
               'Automatically start by placing start node and then end node before wall nodes. ' \
               'Clear nodes with right click, if start or end nodes are cleared it will force user to place start/end node again before starting.'
instructions_2 = 'After program starts press the corresponding number on the keyboard to run the specific algorithm'
options = '1: A*     2: Greedy Best Search     3: Dijkstra' \
          '         4: Breadth First Search     5: Depth First Search' \
          '         P: Menu'
menu.add_label(instructions, max_char= -1, font_size = 20)
menu.add_label(' ')
menu.add_label(instructions_2, max_char= -1, font_size = 20)
menu.add_label(' ')
menu.add_label(options, max_char= -1, font_size = 20)
menu.add_label(' ')
menu.add_selector('FPS :', [(f'{x}', x) for x in range (15, 121, 5)], onchange= change_fps)
menu.add_selector('GRID SIZE :', [(f'{x}', x) for x in range (5, 91, 5) if SCREEN_SIZE % x == 0], onchange= change_grid_size)
menu.add_selector('Heuristic :', [('Manhattan Distance', 1), ('Euclidean Distance', 2)], onchange= change_heuristic)
menu.add_button('Play', start_finder)

# Start program beginning with menu
if __name__ == '__main__':
    menu.mainloop(WINDOW)


