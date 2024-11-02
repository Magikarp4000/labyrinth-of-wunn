import pygame
from config import *
class Spritesheet:
    def __init__(self, file, image_tilesize):
        self.spritesheet = pygame.image.load(file).convert_alpha()
        self.tilesize = image_tilesize

        width, height = self.spritesheet.get_size()
        self.w = width / TILE_SIZE
        self.h = height / TILE_SIZE

    def get_image(self, x, y):
        sprite = pygame.Surface((self.tilesize, self.tilesize))
        sprite.blit(self.spritesheet, (0, 0), 
                    (x * self.tilesize, y * self.tilesize, self.tilesize, self.tilesize))
        return sprite