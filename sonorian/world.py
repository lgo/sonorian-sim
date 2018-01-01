import seamless
import chunk
from opensimplex import opensimplex

"""
World.
"""

class World(object):

    def __init__(self, seed):
        self.seed = seed
        self.chunk_cache = {}

        # TODO(joey): Modify seed for height map.
        self.height_map_generator = simpex.OpenSimplex(seed)

    def __repr__(self):
        return "<World>"

    def get_chunk(self, x, y):
        (chunk_x, chunk_y) = chunk.at_coord(x, y)
        c = chunk.Chunk(self, chunk_x, chunk_y)
        return c

if __name__ == "__main__":
    w = World(1)
    c = w.get_chunk(12,12)
    print("Chunk at 12,12: %s" % c)
    c = w.get_chunk(34,34)
    print("Chunk at 34,34: %s" % c)
