#!/bin/python3
import random
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

if __name__ == "__main__":
    f = open("noise.json", "w")

    random.seed(0)

    h = w = 512

    #grid = white_noise_grid(4,4)
    #grid2 = smooth_grid(scale_grid(grid, 32))
    terrains = [ {'val': 0, 'amt': 0.4 },
                 {'val': 1, 'amt': 0.25 },
                 {'val': 2, 'amt': 0.14 },
                 {'val': 3, 'amt': 0.11 },
                 {'val': 4, 'amt': 0.05 },
                 {'val': 5, 'amt': 0.05 } ]

    perlin = perlin_noise_grid(w,h, 1/4, range(-5, -2))

    f.write(json_grid("white", truncate_grid_data(perlin, terrains)))

    zoom = zoom_grid(perlin, 64, 180, 64, 64)
    #perlin = perlin_noise_grid(w,h, 1/4, range(-6, 1))

    f.write(json_grid("perlin", truncate_grid_data(zoom, terrains)))

    f.close()

