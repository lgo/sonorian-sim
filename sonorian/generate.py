# FIXME(joey): This file has rotted and is not used.

import random
import png
from worldgen import white_noise_grid, scale_grid, smooth_grid, perlin_noise_grid


def json_grid(var, grid):
    return "%s = %s;" % (var, grid)


def zoom_grid(grid, x, y, h, w):
    newgrid = grid[y:y + h]
    for i in range(len(newgrid)):
        newgrid[i] = newgrid[i][x:x + w]
    newgrid = scale_grid(newgrid, len(grid) / h)
    return newgrid


def truncate_grid_data(grid, terrains):
    newgrid = []
    for row in grid:
        newrow = []
        for val in row:
            for terrain in terrains:
                if val <= terrain['amt']:
                    newval = terrain['val']
                    break
                else:
                    val -= terrain['amt']
            newrow.append(newval)
        newgrid.append(newrow)
    return newgrid

terrains = [
    # Ocean.
    {'val': 0, 'amt': 0.4, 'color': '#131391', 'rgb': (19, 19, 145)},
    # Shallow water.
    {'val': 1, 'amt': 0.25, 'color': '#2221FF', 'rgb': (34, 33, 255)},
    # Grass.
    {'val': 2, 'amt': 0.14, 'color': '#1BBF00', 'rgb': (27, 191, 0)},
    # Forest.
    {'val': 3, 'amt': 0.11, 'color': '#127F00', 'rgb': (18, 127, 0)},
    # Bush.
    {'val': 4, 'amt': 0.05, 'color': '#094000', 'rgb': (9, 64, 0)},
    # Mountain.
    {'val': 5, 'amt': 0.05, 'color': '#403B23', 'rgb': (64, 59, 35)}
]

def get_tile_rgb(cell):
    reminaing_cell = cell
    for terrain in terrains:
        reminaing_cell -= terrain['amt']
        if reminaing_cell <= 0:
            return terrain['rgb']
    # For now, we want to return the last terrain.
    return terrains[-1]['rgb']
    # raise Exception("Expected to have a valid terrain. cell=%f reminaing_cell=%f" % (
    #     cell, reminaing_cell))

def write_to_image(filename, grid):
    image_pixels = []
    for grid_row in grid:
        row = []
        for cell in grid_row:
            row += get_tile_rgb(cell)
        image_pixels.append(row)
    with open(filename, 'wb') as f:
        w = png.Writer(len(grid[0]), len(grid))
        w.write(f, image_pixels)

if __name__ == "__main__":
    random.seed(0)
    h = w = 512

    #grid = white_noise_grid(4,4)
    #grid2 = smooth_grid(scale_grid(grid, 32))

    perlin = perlin_noise_grid(w,h, 1/4, range(-5, -2))
    # perlin = perlin_noise_grid(w, h, 1.0 / 5.0, range(-6, -2))

    # zoom = zoom_grid(perlin, 64, 180, 64, 64)
    #perlin = perlin_noise_grid(w,h, 1/4, range(-6, 1))

    # with open("noise.json", "w") as f:
    #     f.write(json_grid("white", truncate_grid_data(perlin, terrains)))
    #     f.write(json_grid("perlin", truncate_grid_data(zoom, terrains)))

    write_to_image("perlin_noise1.png", perlin)
    # write_to_image("zoom_noise.png", perlin)
