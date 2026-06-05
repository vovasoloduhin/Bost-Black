import random
from settings import SHAPES

class Piece:
    def __init__(self, shape=None):
        self.shape = shape if shape else random.choice(SHAPES)

        self.selected = False

        self.preview_x = 0
        self.preview_y = 0

    @property
    def width(self):
        return len(self.shape[0])

    @property
    def height(self):
        return len(self.shape)