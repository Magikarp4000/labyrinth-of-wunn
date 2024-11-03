import pygame
from pygame.locals import *
from pygame.math import Vector2
from pygame.math import clamp

import random
import math

from config import *
from player import Player
from Spritesheet import Spritesheet
from utils import scale_image


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Game:
    def __init__(self):
        self.music = pygame.mixer.Sound("assets/music/m.wav")
        self.music.play(-1)

        self.zoom = 1
        self.tile_size = BASE_TILE_SIZE
        self.camera_speed = BASE_CAMERA_SPEED

        self.camera = Vector2(WORLD_WIDTH / 2, WORLD_HEIGHT / 2)
        self.camera_pos = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.tiles = self.gen_world()
    
    def move_camera(self, pressed):
        direction = Vector2(0, 0)
        if pressed[K_RIGHT] or pressed[K_d]:
            direction.x += self.camera_speed
        if pressed[K_LEFT] or pressed[K_a]:
            direction.x -= self.camera_speed
        if pressed[K_UP] or pressed[K_w]:
            direction.y -= self.camera_speed
        if pressed[K_DOWN] or pressed[K_s]:
            direction.y += self.camera_speed
        if direction.length() > 0:
            direction = direction.normalize()
        return direction

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

    def render_tiles(self):
        start_x = self.camera.x - self.camera_pos.x / self.tile_size
        end_x = self.camera.x + (SCREEN_WIDTH - self.camera_pos.x) / self.tile_size
        start_y = self.camera.y - self.camera_pos.y / self.tile_size
        end_y = self.camera.y + (SCREEN_HEIGHT - self.camera_pos.y) / self.tile_size

        for x in range(int(start_x), int(end_x) + WIDTH + 1):
            for y in range(int(start_y), int(end_y) + HEIGHT + 1):
                self.tiles[y, x] = scale_image(self.tiles[y, x], self.tile_size)
                pos_x = self.camera_pos.x - (self.camera.x - x) * self.tile_size
                pos_y = self.camera_pos.y - (self.camera.y - y) * self.tile_size
                screen.blit(self.tiles[y, x], self.tiles[y, x].get_rect(topleft=(pos_x, pos_y)))

    def update_zoom(self, d_zoom):
        self.zoom = clamp(self.zoom + d_zoom, 1, MAX_ZOOM)
        self.camera_speed = self.zoom * BASE_CAMERA_SPEED
        self.tile_size = self.zoom * BASE_TILE_SIZE

    def update_camera(self, keys, at_edge):
        direction = self.move_camera(keys)
        if at_edge:
            self.camera_pos += direction * self.camera_speed
            self.camera_pos.x = clamp(self.camera_pos.x, 0, WORLD_WIDTH - WIDTH - 1)
            self.camera_pos.y = clamp(self.camera_pos.y, 0, WORLD_HEIGHT - HEIGHT - 1)
        self.camera += direction * BASE_CAMERA_SPEED

    def main(self):
        sprites = pygame.sprite.Group()
        player = Player()
        sprites.add(player)

        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == MOUSEWHEEL:
                    self.update_zoom(event.y * 0.3)
            keys = pygame.key.get_pressed()

            # Player movement
            player.move(keys)
            
            # Camera movement
            self.update_camera(keys, player.at_edge)
            
            player.update_zoom(self.zoom)
            # Update sprites
            sprites.update()

            # Rendering
            self.render_tiles()
            screen.blit(player.image, player.rect)
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.main()
