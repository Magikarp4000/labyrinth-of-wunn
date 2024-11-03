from config import *
from animation import Animation
from utils import *

import pygame
from pygame.locals import *
from pygame.math import Vector2
from pygame.math import clamp
from Spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.speed = BASE_PLAYER_SPEED
        self.size = BASE_PLAYER_SIZE

        self.zoom = 1

        self.strength = 1

        self.real_pos = Vector2(WORLD_WIDTH / 2, WORLD_HEIGHT / 2)
        self.pos = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        spritesheet = Spritesheet("assets/Player/Player.png", 32)

        self.down = (Animation(spritesheet, 5, [18, 19, 20, 21, 22, 23]), Animation(spritesheet, 5, [0]))
        self.right = (Animation(spritesheet, 5, [24, 25, 26, 27, 28, 29]), Animation(spritesheet, 5, [6]))
        self.up = (Animation(spritesheet, 5, [30, 31, 32, 33, 34, 35]), Animation(spritesheet, 5, [12]))

        self.image = scale_image(spritesheet.get_image(0, 0), self.size)
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))

        self.orit = 0

        self.tick = 0
        self.moving = False

    def update_zoom(self, zoom):
        self.zoom = zoom
        self.size = BASE_PLAYER_SIZE * zoom

    def get_direction(self, keys):
        direction = Vector2(0, 0)
        if keys[K_s]:
            direction.y += self.speed
        if keys[K_w]:
            direction.y -= self.speed
        if keys[K_d]:
            direction.x += self.speed
        if keys[K_a]:
            direction.x -= self.speed
        if direction.length() > 0:
            direction = direction.normalize()
        return direction

    def move(self, keys):
        direction = self.get_direction(keys)
        self.real_pos += direction * BASE_CAMERA_SPEED
        self.pos += direction * self.speed * self.zoom

        if (self.real_pos.x > CAMERA_PADDING_X / BASE_TILE_SIZE and
            self.real_pos.x < WORLD_WIDTH - CAMERA_PADDING_X / BASE_TILE_SIZE):
            self.pos.x = clamp(self.pos.x, CAMERA_PADDING_X, SCREEN_WIDTH - CAMERA_PADDING_X)
        if (self.real_pos.y > CAMERA_PADDING_Y / BASE_TILE_SIZE and 
            self.real_pos.y < WORLD_HEIGHT - CAMERA_PADDING_Y / BASE_TILE_SIZE):
            self.pos.y = clamp(self.pos.y, CAMERA_PADDING_Y, SCREEN_HEIGHT - CAMERA_PADDING_Y)
        self.pos.x = clamp(self.pos.x, 0, SCREEN_WIDTH)
        self.pos.y = clamp(self.pos.y, 0, SCREEN_HEIGHT)

        self.real_pos.x = clamp(self.real_pos.x, 0, WORLD_WIDTH - 1)
        self.real_pos.y = clamp(self.real_pos.y, 0, WORLD_HEIGHT - 1)

        if direction.x > 0:
            self.orit = 0
        elif direction.x < 0:
            self.orit = 2
        elif direction.y < 0:
            self.orit = 1
        elif direction.y > 0:
            self.orit = 3
        if abs(direction.x) + abs(direction.y) > 0:
            self.moving = True
    
    def update(self, *args, **kwargs):
        if self.orit == 0:
            img = self.right[not self.moving].get_image(self.tick)
        if self.orit == 1:
            img = self.up[not self.moving].get_image(self.tick)
        if self.orit == 2:
            img = self.right[not self.moving].get_image(self.tick)
            img = pygame.transform.flip(img, 1, 0)
        if self.orit == 3:
            img = self.down[not self.moving].get_image(self.tick)
        self.image = scale_image(img, self.size)
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))
        self.tick += 1
        self.moving = False
