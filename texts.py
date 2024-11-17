from config import *
from utils import *


import pygame
from pygame.math import Vector2


class HouseText:
    def __init__(self, x, y, image: pygame.Surface):
        self.real_pos = Vector2(x, y)
        self.pos = Vector2(0, 0)

        self.image = image
        self.rect = self.image.get_rect()

        self.size = Vector2(self.image.get_width(), self.image.get_height())
    