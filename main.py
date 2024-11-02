import pygame
from pygame.locals import *


W = 26
H = 18
TILE_SIZE = 32
WIDTH = W * TILE_SIZE
HEIGHT = H * TILE_SIZE
FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Spritesheet:
    def __init__(self, file, tilesize):
        self.spritesheet = pygame.image.load(file).convert()
        self.tilesize = tilesize

    def get_image(self, x, y):
        sprite = pygame.Surface((self.tilesize, self.tilesize))
        sprite.blit(self.spritesheet, (0, 0), 
                    (x * self.tilesize, y * self.tilesize, self.tilesize, self.tilesize))
        return sprite

def scale(image):
    return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))


def main():
    running = True
    tilesheet = Spritesheet('assets/tilesheet/tilesheet.png', 16)
    tiles = {}
    for i in range(WIDTH // TILE_SIZE):
        for j in range(HEIGHT // TILE_SIZE):
            tile = scale(tilesheet.get_image(6, 2))
            tiles[i*TILE_SIZE, j*TILE_SIZE] = tile
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        pygame.display.flip()
        for pos, tile in tiles.items():
            screen.blit(tile, tile.get_rect(topleft=pos))
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
