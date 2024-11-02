from config import *

import pygame
from pygame.locals import *

import random
import player
from Spritesheet import Spritesheet
from scale import scale_image


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def scale(arr, k):
    return [x * k for x in arr]

def main():
    running = True
    tilesheet = Spritesheet('assets/texture/TX Tileset Grass.png', 16)
    camera_x = 0
    camera_y = 0
    tiles = {}
    player1 = player.Player()
    for i in range(500):
        for j in range(500):
            x = random.randint(0, tilesheet.w)
            y = random.randint(0, tilesheet.h)
            tile = scale_image(tilesheet.get_image(x, y), TILE_SIZE)
            tiles[i, j] = tile
    while running:
        keys = pygame.key.get_pressed()
        player1.move(keys)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        for x in range(camera_x, camera_x + WIDTH):
            for y in range(camera_y, camera_y + HEIGHT):
                pos_x = (x - camera_x) * TILE_SIZE
                pos_y = (y - camera_y) * TILE_SIZE
                screen.blit(tiles[y, x], tiles[y, x].get_rect(topleft=(pos_x, pos_y)))
        player1.update()
        screen.blit(player1.image,player1.rect)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
