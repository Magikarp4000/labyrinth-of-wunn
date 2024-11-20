from config import *
from utils import *


import pygame
from pygame.math import Vector2


class HouseText:
    def __init__(self, x, y, image: pygame.Surface):
        self.real_pos = Vector2(x, y)
        self.pos = Vector2(0, 0)

        self.orig_image = image
        self.image = image
        self.rect = self.image.get_rect()

        self.size = Vector2(self.image.get_width(), self.image.get_height())


class NPCText(pygame.sprite.Sprite):
    def __init__(self, obj, offset, image, birth):
        super().__init__()
        self.obj = obj
        self.offset = offset
        self.birth = birth

        self.real_pos = obj.real_pos + self.offset
        self.pos = obj.pos

        self.orig_image = image
        self.image = image

        self.size = Vector2(image.get_width(), image.get_height())
    
    def update(self, now, *args, **kwargs):
        self.real_pos = self.obj.real_pos + self.offset
        self.pos = self.obj.pos
        if now - self.birth > NPC_DIALOGUE_TIME:
            self.kill()
