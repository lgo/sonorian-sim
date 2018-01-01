import binascii

"""
Chunk.
"""

# CHUNK_SIZE is the size of discretely generated chunks.
CHUNK_SIZE = 30

def at_coord(x, y):
    """
    Get the chunk coordinate from a global coordinate.
    """
    return (x // CHUNK_SIZE, y // CHUNK_SIZE)


class Chunk(object):

    def __init__(self, world, x, y):
        self._world = world
        self.x = x
        self.y = y

        # Generate the chunk seed from the global seed.
        self.seed = binascii.crc32(b"%d.%d.%d" % (self._world.seed, x, y))

    def __repr__(self):
        return "<Chunk x=%d y=%d seed=%s>" % (self.x, self.y, self.seed)
