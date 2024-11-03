from config import *
from utils import *

from character import Character
from collections import deque
from dialogue import Dialogue

from Spritesheet import Spritesheet
from animation import Animation

import pygame
from pygame.math import Vector2
import random

NPC_CLEAR_QUEUE = 1

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sus = 0
        self.actions = deque()
        self.dialogue = None
        self.killed = False
        self.health = 100
        self.speed = BASE_NPC_SPEED / BASE_TILE_SIZE

        spritesheet = Spritesheet("assets/Cute_Fantasy_Free/Enemies/Skeleton.png", 32)

        self.down = (Animation(spritesheet, 5, [18, 19, 20, 21, 22, 23]), Animation(spritesheet, 5, [0]), Animation(spritesheet, 5, [36, 37, 38, 39]))
        self.right = (Animation(spritesheet, 5, [24, 25, 26, 27, 28, 29]), Animation(spritesheet, 5, [6]), Animation(spritesheet, 5, [42, 43, 44, 45]))
        self.up = (Animation(spritesheet, 5, [30, 31, 32, 33, 34, 35]), Animation(spritesheet, 5, [12]), Animation(spritesheet, 5, [48, 49, 50, 51]))

        self.killanim = Animation(spritesheet, 20, [36, 37, 38] + [39] * 100)

        self.real_pos = Vector2(x, y)
        self.pos = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        self.size = BASE_PLAYER_SIZE

        self.image = scale_image(spritesheet.get_image(0, 0), self.size)

        self.target = Vector2(random.randint(0, WORLD_WIDTH), random.randint(0, WORLD_HEIGHT))
        self.good_target = False

        self.run = False

    def queue_action(self, action, flags):
        if flags & NPC_CLEAR_QUEUE:
            self.actions.clear()
        self.actions.append(action)

    def update(self, player_pos):
        if self.killed:
            img = self.killanim.get_image(0)
            self.image = scale_image(img, self.size)
            self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))
            return
        
        if self.real_pos == self.target or not self.good_target:
            if random.random() < RANDOM_CHANCE:
                self.target = Vector2(random.randint(0, WORLD_WIDTH), random.randint(0, WORLD_HEIGHT))
        
        if self.real_pos == self.target:
            self.good_target = False

        if self.run:
            self.real_pos += -(player_pos - self.real_pos).normalize() * self.speed
            if random.random() < RANDOM_WALK_CHANCE:
                self.run = False
                self.speed = BASE_NPC_SPEED / BASE_TILE_SIZE
        else:
            self.real_pos += (self.target - self.real_pos).normalize() * self.speed

        ii = 0
        self.orit = 0
        if self.orit == 0:
            img = self.right[ii].get_image(0)
        if self.orit == 1:
            img = self.up[ii].get_image(0)
        if self.orit == 2:
            img = self.right[ii].get_image(0)
            img = pygame.transform.flip(img, 1, 0)
        if self.orit == 3:
            img = self.down[ii].get_image(0)
        self.image = scale_image(img, self.size)
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))
    
    def die(self):
        img = self.killanim.get_image(0)
        self.image = scale_image(img, self.size)
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))
        self.killed = True
