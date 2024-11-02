from config import *
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

        self.real_pos = Vector2(WIDTH / 2, HEIGHT / 2)
        self.pos = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        spritesheet = Spritesheet("assets/Player/Player.png", 32)
        self.image = scale_image(spritesheet.get_image(0, 0), self.size)
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))

        self.at_edge = False

    def update_zoom(self, zoom):
        self.zoom = zoom
        # self.speed = BASE_PLAYER_SPEED * zoom
        self.size = BASE_PLAYER_SIZE * zoom

    def move(self, keys):
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
            direction = direction.normalize() * self.speed
        
        self.real_pos += direction
        self.pos += direction * self.zoom
        self.at_edge = (self.pos.x < CAMERA_PADDING_X or self.pos.x > SCREEN_WIDTH - CAMERA_PADDING_X or 
                        self.pos.y < CAMERA_PADDING_Y or self.pos.y > SCREEN_HEIGHT - CAMERA_PADDING_Y)
        self.pos.x = clamp(self.pos.x, CAMERA_PADDING_X, SCREEN_WIDTH - CAMERA_PADDING_X)
        self.pos.y = clamp(self.pos.y, CAMERA_PADDING_Y, SCREEN_HEIGHT - CAMERA_PADDING_Y)
    
    def update(self, *args, **kwargs):
        self.image = scale_image(self.image, self.size)
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))
