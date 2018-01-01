import png
import sys
import random
import seamless
from opensimplex import opensimplex

class NoiseMap(object):
    """
    Provides a lazily generated noise map.
    """

    def __init__(self, height, width, detail=10, seed=None, offset=0):
        """
        Parameters
        ----------
        height : int
        width : int
        detail : float (default=10)
            adjusts the granularitylevel of detail in the generated noise
        seed : int (default=None)
            if None, a random value is used
        offset : float (default=0)
        """
        if seed is None:
            seed = random.randint(0, sys.maxsize)

        self.height = height
        self.width = width
        self.detail = detail
        self.offset = offset
        self.seed = seed
        self.generator = opensimplex.OpenSimplex(self.seed)
        self.map = []

    def generate(self):
        """
        Generates the noise map.
        """
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(seamless.seamless_noise(
                    self.generator, x / self.width, y / self.height, self.detail, self.detail, self.offset))
            self.map.append(row)

    def save_map(self, filename):
        """
        Save the noise map to a file.
        """
        pixels = [[int(cell * 255) for cell in grid_row] for grid_row in self.map]
        with open(filename, 'wb') as f:
            w = png.Writer(len(self.map[0]), len(
                self.map), greyscale=True)
            w.write(f, pixels)


if __name__ == "__main__":
    nm = NoiseMap(512, 512, 10)
    nm.generate()
    nm.save_map("seamless_noise_10.png")

    nm = NoiseMap(512, 512, 15)
    nm.generate()
    nm.save_map("seamless_noise_15.png")
