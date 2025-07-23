import pygame, sys, random
from grid import Grid
from particle import *

class Simulation:
    def __init__(self, width, height, cell_size):
        self.grid = Grid(width, height, cell_size)
        self.cell_size = cell_size
        self.mode = "sand"
        self.brush_size = 3

    def draw(self, window):
        self.grid.draw(window)
        self.draw_brush(window)

    def add_particle(self, row, colum):
        if self.mode == "sand":
            if random.random() < 0.15:
                self.grid.add_particle(row, colum, SandParticle)
        elif self.mode == "rock":
            self.grid.add_particle(row, colum, RockParticle)
        elif self.mode == "water":
            self.grid.add_particle(row, colum, WaterParticle)
        elif self.mode == "fire":
            self.grid.add_particle(row, colum, FireParticle)
        elif self.mode == "oil":
            self.grid.add_particle(row, colum, OilParticle)
        elif self.mode == "gas":
            self.grid.add_particle(row, colum, GasParticle)
        elif self.mode == "plant":
            self.grid.add_particle(row, colum, PlantParticle)

    def remove_particle(self, row, colum):
        self.grid.remove_particle(row, colum)

    def update(self):
        for row in range(self.grid.rows - 2, -1, -1):
            for column in range(self.grid.cols):
                particle = self.grid.get_cell(row, column)
                if hasattr(particle, "update"):
                    new_pos = particle.update(self.grid, row, column)
                    if new_pos != (row, column):
                        if new_pos == (-1, -1):
                            self.grid.remove_particle(row, column)  # fire burns out
                        else:
                            self.grid.set_cell(new_pos[0], new_pos[1], particle)
                            self.grid.remove_particle(row, column)

    def restart(self):
        self.grid.clear()

    def handle_controls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.handle_key(event)
        self.handle_mouse()

    def handle_key(self, event):
        if event.key == pygame.K_SPACE:
            self.restart()
        elif event.key == pygame.K_s:
            print("sand")
            self.mode = "sand"
        elif event.key == pygame.K_r:
            print("rock")
            self.mode = "rock"
        elif event.key == pygame.K_w:
            print("water")
            self.mode = "water"
        elif event.key == pygame.K_f:
            print("fire")
            self.mode = "fire"
        elif event.key == pygame.K_o:
            print("oil")
            self.mode = "oil"
        elif event.key == pygame.K_g:
            print("gas")
            self.mode = "gas"
        elif event.key == pygame.K_p:
            print("plant")
            self.mode = "plant"
        elif event.key == pygame.K_e:
            print("erase")
            self.mode = "erase"


    def handle_mouse(self):
        buttons = pygame.mouse.get_pressed()
        if buttons[0]:
            pos = pygame.mouse.get_pos()
            row = pos[1] // self.cell_size
            colum = pos[0] // self.cell_size

            self.apply_brush(row, colum)

    def apply_brush(self, row, colum):
        for r in range(self.brush_size):
            for c in range(self.brush_size):
                current_row = row + r
                current_colum = colum + c
                if self.mode == "erase":
                    self.grid.remove_particle(current_row, current_colum)
                else:
                    self.add_particle(current_row, current_colum)

    def draw_brush(self, window):
        mouse_pos = pygame.mouse.get_pos()
        row = mouse_pos[1] // self.cell_size
        colum = mouse_pos[0] // self.cell_size

        brush_visual_size = self.cell_size * self.brush_size

        # Assign colors per mode
        mode_colors = {
            "sand": (185, 142, 66),
            "rock": (100, 100, 100),
            "water": (66, 135, 245),
            "fire": (255, 85, 0),
            "oil": (100, 60, 20),
            "gas": (150, 150, 255),
            "plant": (50, 200, 50),
            "erase": (255, 105, 180)
        }

        color = mode_colors.get(self.mode, (255, 255, 255))  # default to white

        pygame.draw.rect(
            window,
            color,
            (colum * self.cell_size, row * self.cell_size, brush_visual_size, brush_visual_size),
            width=1  # make it just a border
        )
