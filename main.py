import pygame
from pygame.locals import *
from pygame.math import Vector2
from pygame.math import clamp

import random
import math

from config import *
from Player import Player
from Spritesheet import Spritesheet
from utils import scale_image


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# def get_direction(keys):
#     direction = Vector2(0, 0)
#     if keys[K_RIGHT] or keys[K_d]:
#         direction.x += self.camera_speed
#     if keys[K_LEFT] or keys[K_a]:
#         direction.x -= self.camera_speed
#     if keys[K_UP] or keys[K_w]:
#         direction.y -= self.camera_speed
#     if keys[K_DOWN] or keys[K_s]:
#         direction.y += self.camera_speed
#     if direction.length() > 0:
#         direction = direction.normalize()
#     return direction

class Camera:
    def __init__(self, obj):
        self.zoom = 1
        self.obj = obj
        self.pos = obj.pos
        self.real_pos = obj.real_pos / BASE_TILE_SIZE
    
    def update(self, zoom):
        self.zoom = zoom
        self.pos = self.obj.pos
        self.real_pos = self.obj.real_pos
        self.real_pos.x = clamp(self.real_pos.x, 0, WORLD_WIDTH - 1)
        self.real_pos.y = clamp(self.real_pos.y, 0, WORLD_HEIGHT - 1)

class Game:
    def __init__(self):
        pygame.mixer.init()
        self.music = pygame.mixer.Sound("assets/music/m.wav")
        self.music.play(-1)

        self.zoom = 1

        self.tile_size = BASE_TILE_SIZE
        self.tiles = self.gen_world()
    
    def gen_world(self):
        tilesheet = Spritesheet('assets/texture/TX Tileset Grass.png', 16)
        tiles = {}
        for i in range(WORLD_HEIGHT):
            for j in range(WORLD_WIDTH):
                x, y = 12, 14
                while (x, y) == (12, 14) or (x, y) == (15, 14):
                    x = random.randint(0, tilesheet.w - 1)
                    y = random.randint(0, tilesheet.h - 1)
                tile = scale_image(tilesheet.get_image(x, y), self.tile_size)
                tiles[i, j] = tile
        return tiles

    def render_tiles(self, camera):
        start_x = camera.real_pos.x - camera.pos.x / self.tile_size
        end_x = camera.real_pos.x + (SCREEN_WIDTH - camera.pos.x) / self.tile_size
        start_y = camera.real_pos.y - camera.pos.y / self.tile_size
        end_y = camera.real_pos.y + (SCREEN_HEIGHT - camera.pos.y) / self.tile_size

        for x in range(int(start_x), int(end_x) + WIDTH + 1):
            for y in range(int(start_y), int(end_y) + HEIGHT + 1):
                if (y, x) not in self.tiles:
                    continue
                self.tiles[y, x] = scale_image(self.tiles[y, x], self.tile_size)
                pos_x = camera.pos.x - (camera.real_pos.x - x) * self.tile_size
                pos_y = camera.pos.y - (camera.real_pos.y - y) * self.tile_size
                screen.blit(self.tiles[y, x], self.tiles[y, x].get_rect(center=(pos_x, pos_y)))

    def update_zoom(self, d_zoom):
        self.zoom = clamp(self.zoom + d_zoom * ZOOM_RATE, 1, MAX_ZOOM)
        self.tile_size = self.zoom * BASE_TILE_SIZE

    def main(self):
        sprites = pygame.sprite.Group()
        player = Player()
        sprites.add(player)

        camera = Camera(player)

        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == MOUSEWHEEL:
                    self.update_zoom(event.y)
            keys = pygame.key.get_pressed()

            # Player movement
            player.move(keys)
            player.update_zoom(self.zoom)
            
            # Camera movement
            camera.update(self.zoom)
            
            # Update sprites
            sprites.update()

            # Rendering
            self.render_tiles(camera)
            screen.blit(player.image, player.rect)
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.main()
