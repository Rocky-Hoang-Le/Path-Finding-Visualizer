# Import required modules
import pygame
import color

# Setup FPS
FPS_CLOCK = pygame.time.Clock()
FPS = 15


# This function draws the grid
def draw_grid(window, rows, size):
    cell = size // rows
    columns = rows
    for row in range(rows):
        pygame.draw.line(window, color.GREY, (0, row * cell), (size, row * cell))
        for col in range(columns):
            pygame.draw.line(window, color.GREY, (col * cell, 0), (col * cell, size))


# This function will handle drawing everything else
def draw(window, grid, rows, size):
    for row in grid:
        for node in row:
            node.draw(window)
    draw_grid(window, rows, size)
    FPS_CLOCK.tick(FPS)
    pygame.display.update()
