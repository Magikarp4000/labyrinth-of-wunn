from config import *
import pygame
from pygame.locals import *
from pygame.math import Vector2
from Spritesheet import Spritesheet
from scale import scale_image

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        spritesheet = Spritesheet("assets/Player/Player.png", 32)
        self.speed = PLAYER_SPEED
        self.strength = 1
        self.pos = Vector2(20, 20)
        self.image = scale_image(spritesheet.get_image(0, 0), PLAYER_SIZE)
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))

    def move(self, keys):
        direction = Vector2(0, 0)
        if keys[K_s]:
            direction.y += 1
        if keys[K_w]:
            direction.y -=1
        if keys[K_d]:
            direction.x += 1
        if keys[K_a]:
            direction.x -= 1
        
        if direction.length() > 0:
            direction = direction.normalize() * self.speed
        self.pos += direction
    
    def update(self, *args, **kwargs):
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))