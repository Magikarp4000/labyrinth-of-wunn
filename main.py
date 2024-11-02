import pygame
from pygame.locals import *
from pygame.math import Vector2
from pygame.math import clamp

import random
import math

from config import *
from Player import Player
from Spritesheet import Spritesheet
from scale import scale_image


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

music = pygame.mixer.Sound("assets/music/m.wav")
music.play(-1)

def move_camera(pressed):
    direction = Vector2(0, 0)
    if pressed[K_RIGHT] or pressed[K_d]:
        direction.x += PLAYER_SPEED
    if pressed[K_LEFT] or pressed[K_a]:
        direction.x -= PLAYER_SPEED
    if pressed[K_UP] or pressed[K_w]:
        direction.y -= PLAYER_SPEED
    if pressed[K_DOWN] or pressed[K_s]:
        direction.y += PLAYER_SPEED
    if direction.length() > 0:
        direction = direction.normalize() * PLAYER_SPEED
    return direction

def gen_world():
    tilesheet = Spritesheet('assets/texture/TX Tileset Grass.png', 16)
    tiles = {}
    for i in range(WORLD_HEIGHT):
        for j in range(WORLD_WIDTH):
            x, y = 12, 14
            while (x, y) == (12, 14) or (x, y) == (15, 14):
                x = random.randint(0, tilesheet.w - 1)
                y = random.randint(0, tilesheet.h - 1)
            tile = scale_image(tilesheet.get_image(x, y), TILE_SIZE)
            tiles[i, j] = tile
    return tiles

def render_tiles(tiles, camera):
    for x in range(int(camera.x), int(camera.x) + WIDTH + 1):
        for y in range(int(camera.y), int(camera.y) + HEIGHT + 1):
            pos_x = (x - camera.x) * TILE_SIZE
            pos_y = (y - camera.y) * TILE_SIZE
            screen.blit(tiles[y, x], tiles[y, x].get_rect(topleft=(pos_x, pos_y)))

def main():
    camera = Vector2(WORLD_WIDTH / 2, WORLD_HEIGHT / 2)

    tiles = gen_world()

    sprites = pygame.sprite.Group()
    player = Player()
    sprites.add(player)

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        keys = pygame.key.get_pressed()

        # Camera movement
        camera += move_camera(keys)
        camera.x = clamp(camera.x, 0, WORLD_WIDTH - WIDTH - 1)
        camera.y = clamp(camera.y, 0, WORLD_HEIGHT - HEIGHT - 1)

        # Player movement
        player.move(keys)

        # Update sprites
        sprites.update()

        # Rendering
        render_tiles(tiles, camera)
        screen.blit(player.image, player.rect)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
