import pygame
from pygame.locals import *
from pygame.math import Vector2

import random

from config import *
from utils import *

from Spritesheet import Spritesheet
from main import TILESHEET_TILE_SIZE, INVALID_TILES
from Player import Player
from Camera import Camera


class TestEnvironment:
    def __init__(self, screen_width, screen_height):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        self.tile_size = TILE_SIZE
        self.tiles = self.gen_tiles()

        self.player = Player()
        self.camera = Camera(self.player, self.screen, self.tile_size, WORLD_WIDTH, WORLD_HEIGHT,
                             CAMERA_PADDING_X, CAMERA_PADDING_Y, ZOOM_RATE, MAX_ZOOM)
    
    def gen_tiles(self):
        tilesheet = Spritesheet('assets/texture/TX Tileset Grass.png', TILESHEET_TILE_SIZE)
        tiles = {}
        for i in range(WORLD_HEIGHT + 1):
            for j in range(WORLD_WIDTH + 1):
                x, y = INVALID_TILES[0]
                while (x, y) in INVALID_TILES:
                    x = random.randint(0, tilesheet.w - 1)
                    y = random.randint(0, tilesheet.h - 1)
                tile = scale_image(tilesheet.get_image(x, y), self.tile_size)
                tiles[i, j] = tile
        return tiles
    
    def main(self):
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == MOUSEWHEEL:
                    self.camera.update_zoom(event.y)
            keys = pygame.key.get_pressed()
            # Updates
            self.player.move(keys, self.camera.zoom)
            self.player.update()
            self.camera.update()
            # Render
            self.camera.render_tiles(self.tiles, Vector2(TILE_SIZE, TILE_SIZE), padding=2)
            self.camera.render(self.player, Vector2(PLAYER_SIZE, PLAYER_SIZE))
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()


if __name__ == '__main__':
    env = TestEnvironment(SCREEN_WIDTH, SCREEN_HEIGHT)
    env.main()
