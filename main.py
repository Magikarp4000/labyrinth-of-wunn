from config import *

import pygame
from pygame.locals import *

import random


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Spritesheet:
    def __init__(self, file, image_tilesize):
        self.spritesheet = pygame.image.load(file).convert()
        self.tilesize = image_tilesize

        width, height = self.spritesheet.get_size()
        self.w = width / TILE_SIZE
        self.h = height / TILE_SIZE

    def convert(self, idx):
        """Return (row, col)"""
        return divmod(idx, self.w)

    def get_image(self, x, y):
        sprite = pygame.Surface((self.tilesize, self.tilesize))
        sprite.blit(self.spritesheet, (0, 0), 
                    (x * self.tilesize, y * self.tilesize, self.tilesize, self.tilesize))
        return sprite

def scale_image(image, size):
    return pygame.transform.scale(image, (size, size))

def scale(arr, k):
    return [x * k for x in arr]

def main():
    running = True
    tilesheet = Spritesheet('assets/texture/TX Tileset Grass.png', 16)
    camera_x = 0
    camera_y = 0
    tiles = {}
    for i in range(500):
        for j in range(500):
            x = random.randint(0, tilesheet.w)
            y = random.randint(0, tilesheet.h)
            tile = scale_image(tilesheet.get_image(x, y), TILE_SIZE)
            tiles[i, j] = tile
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        for x in range(camera_x, camera_x + WIDTH):
            for y in range(camera_y, camera_y + HEIGHT):
                pos_x = (x - camera_x) * TILE_SIZE
                pos_y = (y - camera_y) * TILE_SIZE
                screen.blit(tiles[y, x], tiles[y, x].get_rect(topleft=(pos_x, pos_y)))
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
