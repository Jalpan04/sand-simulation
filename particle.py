import colorsys
import random


def random_colour(hue_range,saturation_range,value_range):
    hue = random.uniform(*hue_range)
    saturation = random.uniform(*saturation_range)
    value = random.uniform(*value_range)
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
    return int(r * 255), int(g * 255), int(b * 255)

class SandParticle:
    def __init__(self):
        self.color =random_colour((0.1,0.12), (0.5,0.7), (0.7,0.9))

    def update(self, grid, row, column):
        if grid.in_cell_empty(row + 1, column):
            return row + 1, column
        else:
            offsets = [-1, 1]
            random.shuffle(offsets)
            for offset in offsets:
                new_column = column + offset
                if grid.in_cell_empty(row +1, new_column):
                    return row + 1, new_column

        return row, column


class RockParticle:
    def __init__(self):
        self.color = random_colour((0.0, 0.1), (0.1,0.3), (0.3, 0.5))


class WaterParticle:
    def __init__(self):
        self.color = random_colour((0.55, 0.65), (0.4, 0.6), (0.6, 0.9))

    def update(self, grid, row, column):
        if grid.in_cell_empty(row + 1, column):
            return row + 1, column

        offsets = [-1, 1]
        random.shuffle(offsets)
        for offset in offsets:
            if grid.in_cell_empty(row, column + offset):
                return row, column + offset
            if grid.in_cell_empty(row + 1, column + offset):
                return row + 1, column + offset
        return row, column


class FireParticle:
    def __init__(self):
        self.color = (255, 85, 0)
        self.life = random.randint(3, 7)

    def update(self, grid, row, column):
        self.life -= 1
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                r, c = row + dr, column + dc
                neighbor = grid.get_cell(r, c)
                if isinstance(neighbor, PlantParticle) or isinstance(neighbor, OilParticle):
                    grid.set_cell(r, c, FireParticle())
        if self.life <= 0:
            return -1, -1
        return row, column


class OilParticle:
    def __init__(self):
        self.color = (100, 60, 20)

    def update(self, grid, row, column):
        if isinstance(grid.get_cell(row + 1, column), WaterParticle):
            return row, column  # float

        if grid.in_cell_empty(row + 1, column):
            return row + 1, column

        for offset in [-1, 1]:
            if grid.in_cell_empty(row, column + offset):
                return row, column + offset
            if grid.in_cell_empty(row + 1, column + offset):
                return row + 1, column + offset
        return row, column


class GasParticle:
    def __init__(self):
        self.color = (150, 150, 255)

    def update(self, grid, row, column):
        if grid.in_cell_empty(row - 1, column):
            return row - 1, column

        for offset in [-1, 1]:
            if grid.in_cell_empty(row - 1, column + offset):
                return row - 1, column + offset
            if grid.in_cell_empty(row, column + offset):
                return row, column + offset
        return row, column


class PlantParticle:
    def __init__(self):
        self.color = (50, 200, 50)

    def update(self, grid, row, column):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            r, c = row + dr, column + dc
            if isinstance(grid.get_cell(r, c), WaterParticle):
                for pr, pc in directions:
                    nr, nc = row + pr, column + pc
                    if grid.in_cell_empty(nr, nc):
                        if random.random() < 0.01:
                            grid.set_cell(nr, nc, PlantParticle())
        return row, column




