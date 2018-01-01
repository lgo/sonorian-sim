import math
from opensimplex import opensimplex


def seamless_noise(noise_generator, x, y, dx, dy, xyOffset):
    """

    noise_generator is an opensimplex.OpenSimplex instance.

    x is in [0..1]
    y is in [0..1]

    the returned value is in [0..1]
    """
    s = x
    t = y

    nx = xyOffset + math.cos(s * 2.0 * math.pi) * dx / (2.0 * math.pi)
    ny = xyOffset + math.cos(t * 2.0 * math.pi) * dy / (2.0 * math.pi)
    nz = xyOffset + math.sin(s * 2.0 * math.pi) * dx / (2.0 * math.pi)
    nw = xyOffset + math.sin(t * 2.0 * math.pi) * dy / (2.0 * math.pi)

    n = noise_generator.noise4d(nx, ny, nz, nw)
    return (n + 1.0) * .5


# if __name__ == "__main__":
#     seed = 0
#     noise_gen = simplex.OpenSimplex(seed)
#     seamless_noise(noise_gen, )
#     pass
