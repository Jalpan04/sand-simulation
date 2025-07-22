
import pygame
import particle


class Grid:
    def __init__(self, width, height, cell_size):
        self.rows = height // cell_size
        self.cols = width // cell_size
        self.cell_size = cell_size
        self.cells = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def draw(self, window):
        for row in range(self.rows):
            for column in range(self.cols):

                particle = self.cells[row][column]
                if particle is not None:
                    color = particle.color
                    pygame.draw.rect(window, color,
                (column * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))

    def add_particle(self, row, colum,particle_type):
        if 0 <= row < self.rows and 0 <= colum < self.cols and self.in_cell_empty(row, colum):
            self.cells[row][colum] = particle_type()

    def remove_particle(self, row, colum):
        if 0 <= row < self.rows and 0 <= colum < self.cols:
            self.cells[row][colum] = None

    def in_cell_empty(self, row, colum):
        if 0 <= row < self.rows and 0 <= colum < self.cols:
            if self.cells[row][colum] is None:
                return True
        return False

    def set_cell(self, row, colum, particle):
        if not(0 <= row < self.rows and 0 <= colum < self.cols):
            return
        self.cells[row][colum] = particle

    def get_cell(self, row, colum):
        if 0 <= row < self.rows and 0 <= colum < self.cols:
            return self.cells[row][colum]
        return None

    def clear(self):
        for row in range(self.rows):
            for column in range(self.cols):
                self.remove_particle(row, column)
