import pygame
from pygame.locals import *
from pygame.math import Vector2
from pygame.math import clamp

import random
import math

from config import *
from Player import Player
from Spritesheet import Spritesheet
from utils import *
from dialogue import Dialogue
from npc import NPC


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
        self.tl = self.real_pos - self.pos / BASE_TILE_SIZE
        self.br = self.real_pos + ((SCREEN_WIDTH, SCREEN_HEIGHT) - self.pos) / BASE_TILE_SIZE
    
    def update(self, zoom):
        self.zoom = zoom
        self.pos = self.obj.pos
        self.real_pos = self.obj.real_pos
        self.real_pos.x = clamp(self.real_pos.x, 0, WORLD_WIDTH - 1)
        self.real_pos.y = clamp(self.real_pos.y, 0, WORLD_HEIGHT - 1)
        self.tl = self.real_pos - self.pos / BASE_TILE_SIZE
        self.br = self.real_pos + ((SCREEN_WIDTH, SCREEN_HEIGHT) - self.pos) / BASE_TILE_SIZE

class Game:
    def __init__(self):
        self.in_dialogue = False
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
        for x in range(int(camera.tl.x), int(camera.br.x) + WIDTH + 1):
            for y in range(int(camera.tl.y), int(camera.br.y) + HEIGHT + 1):
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

        # npcs = [NPC(random.randint(0, WORLD_WIDTH - 1), random.randint(0, WORLD_HEIGHT - 1))
        #         for _ in range(NUM_NPCS)]
        # sprites.add(npcs)

        camera = Camera(player)

        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                #Dialogue toggler    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.in_dialogue = not self.in_dialogue
                        if self.in_dialogue:
                            background_snapshot = screen.copy()
                #End of dialogue toggler
                if event.type == MOUSEWHEEL:
                    self.update_zoom(event.y)
            keys = pygame.key.get_pressed()
            #Dialogue
            if self.in_dialogue:
                text_images, text_rects = multitext("Hello"*15,DIALOGUE_X,DIALOGUE_Y,SCREEN_WIDTH-(2*DIALOGUE_X), (SCREEN_HEIGHT-DIALOGUE_Y-20), DIALOGUE_YSPACING,'Arial',FONT_SIZE,BLACK)
                screen.blit(background_snapshot, (0,0))
                pygame.draw.rect(screen, (255,255,255), (DIALOGUE_X, DIALOGUE_Y, SCREEN_WIDTH-(2*DIALOGUE_X), SCREEN_HEIGHT-DIALOGUE_Y-20))
                for image, rect in zip(text_images, text_rects):
                    screen.blit(image, rect)
            else:
                # Player movement
                player.move(keys)
                player.update_zoom(self.zoom)

                # Camera movement
                camera.update(self.zoom)
                
                player.update_zoom(self.zoom)
                # Update sprites
                sprites.update()

                # Rendering
                self.render_tiles(camera)
                screen.blit(player.image, player.rect)
            #Rendering
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.main()
