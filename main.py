import pygame, sys
from simulation import Simulation

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 6
FPS = 120
GREY = (29, 29, 29)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sand sim")

clock = pygame.time.Clock()
simulation = Simulation(WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE)

while True:
    simulation.handle_controls()

    buttons = pygame.mouse.get_pressed()
    if buttons[0]:
        pos = pygame.mouse.get_pos()
        row = pos[1] // CELL_SIZE
        colum = pos[0] // CELL_SIZE
        simulation.add_particle(row, colum)

    simulation.update()

    window.fill(GREY)
    simulation.draw(window)

    pygame.display.flip()
    clock.tick(FPS)