import random
import math
from numpy import arange


def white_noise_grid(w, h):
    w = int(w)
    h = int(h)
    grid = [[random.random() for _ in range(w)] for _ in range(h)]
    return grid


def smooth_grid(grid):
    h = len(grid)
    w = len(grid[0])
    newgrid = [[0 for _ in range(w)] for _ in range(h)]
    for y in range(h):
        for x in range(w):
            total = 0
            for i in range(-1, 1):
                if y + i >= h or y + i < 0:
                    continue
                for j in range(-1, 1):
                    if x + j >= w or x + j < 0:
                        continue
                    total += grid[y + i][x + j] / \
                        (2 * (2 ** (abs(i) + abs(j))))
            newgrid[y][x] = total
    return newgrid


def scale_grid(grid, factor):
    if factor == 1:
        return grid

    h = len(grid)
    w = len(grid[0])

    n_h = int(h * factor)
    n_w = int(w * factor)
    newgrid = [[0 for _ in range(n_w)] for _ in range(n_h)]
    for y in range(n_h):
        scaled_y = (float(y) / n_h) * (h - 1.0)
        for x in range(n_w):
            scaled_x = (float(x) / n_w) * (w - 1.0)
            # if scaled_x > 2 and scaled_y > 1:
            #    pdb.set_trace()
            top_left = grid[int(math.floor(scaled_y))
                            ][int(math.floor(scaled_x))]
            top_right = grid[int(math.floor(scaled_y))
                             ][int(math.ceil(scaled_x))]
            bot_left = grid[int(math.ceil(scaled_y))
                            ][int(math.floor(scaled_x))]
            bot_right = grid[int(math.ceil(scaled_y))
                             ][int(math.ceil(scaled_x))]

            top = interpolate(top_left, top_right, scaled_x -
                              int(math.floor(scaled_x)))
            bot = interpolate(bot_left, bot_right, scaled_x -
                              int(math.floor(scaled_x)))
            midpoint = interpolate(
                top, bot, (scaled_y - int(math.floor(scaled_y))))

            newgrid[y][x] = midpoint
        0

    return newgrid


def perlin_noise_grid(w, h, persistence, octaves):

    grid = [[0 for _ in range(w)] for _ in range(h)]

    total_amp = 0
    # print(octaves)
    for octo in octaves:
        freq = 2.0 ** octo
        amp = persistence ** octo
        total_amp += amp
        tmp = white_noise_grid(w * freq, h * freq)
        tmp = scale_grid(tmp, 1 / freq)
        octo_grid = smooth_grid(tmp)
        for y in range(h):
            for x in range(w):
                grid[y][x] += octo_grid[y][x] * amp

    for y in range(h):
        for x in range(w):
            grid[y][x] /= total_amp

    return grid


def interpolate(a, b, x):
    ft = x * math.pi * 0.5
    f = (math.cos(ft))
    return a * (f) + b * (1.0 - f)


def count(grid):
    ocean = 0
    sea = 0
    grass = 0
    forest = 0
    mountain = 0
    peak = 0
    for row in grid:
        for tile in row:
            if (tile <= 0.25):
                ocean += 1
            elif (tile <= 0.5):
                sea += 1
            elif (tile <= 0.65):
                grass += 1
            elif (tile <= 0.8):
                forest += 1
            elif (tile <= 0.9):
                mountain += 1
            else:
                peak += 1
    return (ocean, sea, grass, forest, mountain, peak)


def distribution_test():
    ret = []
    for _ in range(250):
        perlin = perlin_noise_grid(
            500, 500, 1.0 / 4.0, [-2, -1, 0, 1, 2, 3, 4])
        ret.append(count(perlin))

    ocean = sea = grass = forest = mountain = peak = 0
    for (oc, se, gr, fo, mo, pe) in ret:
        ocean += oc
        sea += se
        grass += gr
        forest += fo
        mountain += mo
        peak += pe

    total = ocean + sea + grass + forest + mountain + peak

    print("ocean = %s;" % (ocean / total))
    print("sea = %s;" % (sea / total))
    print("grass = %s;" % (grass / total))
    print("forest = %s;" % (forest / total))
    print("mountain = %s;" % (mountain / total))
    print("peak = %s;" % (peak / total))


if __name__ == "__main__":
    distribution_test()
