import sys
import random
from opensimplex import opensimplex

import sonorian.chunk as chunk
import sonorian.seamless as seamless
import sonorian.noise_map as noise_map


class World(object):

    class State(object):
        """
        Serializable state of World.
        """

        def __init__(self):
            self.seed = None
            self.height_map = None

    def __init__(self, seed=None):
        """
        Parameters
        ----------
        seed : int (default=None)
            if None, a random value is used
        """
        if seed is None:
            seed = random.randint(0, sys.maxsize)

        self.state = World.State()
        self.state.seed = seed

        self.state.height_map = noise_map.NoiseMap(height=512, width=512, seed=seed)
        self.state.height_map.generate()

        # TODO(joey): Modify seed for height map.
        # self.height_map_generator = simpex.OpenSimplex(seed)

    def __repr__(self):
        return "<World>"

    def dump(self):
        # TODO(joey): We likely need to return child state.
        data = self.state.__dict__
        data['height_map'] =

    @classmethod
    def load(state):
        pass

    def reload_children():
        pass

    # def get_chunk(self, x, y):
    #     (chunk_x, chunk_y) = chunk.at_coord(x, y)
    #     c = chunk.Chunk(self, chunk_x, chunk_y)
    #     return c

if __name__ == "__main__":
    w = World(1)
    c = w.get_chunk(12,12)
    print("Chunk at 12,12: %s" % c)
    c = w.get_chunk(34,34)
    print("Chunk at 34,34: %s" % c)
