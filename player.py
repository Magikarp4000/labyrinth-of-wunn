from config import *
import pygame
from pygame.locals import *
from pygame.math import Vector2
from Spritesheet import Spritesheet
from scale import scale_image

class Player(pygame.sprite.Sprite):
    def __init__(self):
        sprsheet = Spritesheet("assets/Player/Player.png", 32)
        super().__init__()
        self.speed = 5
        self.strength = 1
        self.position = Vector2(20,20)
        self.image = scale_image(sprsheet.get_image(0,0),64)

        self.rect = self.image.get_rect(topleft=(self.position.x,self.position.y))
    def move(self, keys):
        direction = Vector2(0,0)
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
        
        self.position += direction
    def update(self):
        self.rect = self.image.get_rect(topleft=(self.position.x,self.position.y))