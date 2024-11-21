from config import *
from utils import *

from collections import deque
from dialogue import Dialogue

from Spritesheet import Spritesheet
from animation import Animation

import pygame
from pygame.math import Vector2
from pygame.math import clamp

import random
import time


class NPC(pygame.sprite.Sprite):
    def __init__(self, id, x, y):
        super().__init__()
        self.id = id

        self.actions = deque()
        self.killed = False
        self.health = NPC_HEALTH
        self.dmg = NPC_DMG
        self.speed = NPC_SPEED / TILE_SIZE
        self.prev_speed = self.speed

        self.dialogue = None

        spritesheet = Spritesheet("assets/Cute_Fantasy_Free/Enemies/Skeleton.png", 32)

        self.down = (Animation(spritesheet, 5, [18, 19, 20, 21, 22, 23]), Animation(spritesheet, 5, [0]), Animation(spritesheet, 5, [36, 37, 38, 39]))
        self.right = (Animation(spritesheet, 5, [24, 25, 26, 27, 28, 29]), Animation(spritesheet, 5, [6]), Animation(spritesheet, 5, [42, 43, 44, 45]))
        self.up = (Animation(spritesheet, 5, [30, 31, 32, 33, 34, 35]), Animation(spritesheet, 5, [12]), Animation(spritesheet, 5, [48, 49, 50, 51]))

        self.kill_anim = Animation(spritesheet, 20, [36, 37, 38] + [39] * 8000)

        self.real_pos = Vector2(x, y)
        self.pos = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        self.size = NPC_SIZE

        self.image = scale_image(spritesheet.get_image(0, 0), self.size)
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))

        self.target = Vector2(random.randint(0, WORLD_WIDTH), random.randint(0, WORLD_HEIGHT))
        self.good_target = False
        self.last_target = 0
        self.stop_flag = False

        self.run = False
        self.orit = 0

        self.friend = 50

    def random_target(self):
        return Vector2(random.randint(0, WORLD_WIDTH - 1), random.randint(0, WORLD_HEIGHT - 1))
    
    def start(self):
        self.speed = self.prev_speed
    
    def stop(self):
        self.prev_speed = self.speed
        self.speed = 0

    def set_run(self):
        self.run = True
        self.speed = NPC_RUN_SPEED / TILE_SIZE
        self.last_target = time.time()
    
    def reset_run(self):
        self.run = False
        self.speed = NPC_SPEED / TILE_SIZE

    def set_target(self, target):
        self.target = Vector2(target)
        self.good_target = True

    def act(self, action):
        if action.t == ACTION_RUN:
            self.set_run()
        elif action.t == ACTION_SCREAM:
            self.set_run()
        elif action.t == ACTION_WALK:
            self.reset_run()
        elif action.t == ACTION_DIE:
            self.health = 0
        self.friend = action.friend

    def at_target(self):
        return self.real_pos.distance_to(self.target) < self.speed
    
    def retarget(self):
        self.stop_flag = False
        self.target = self.random_target()
        self.last_target = time.time()
        self.start()

    def update_pos(self, pos):
        self.pos = pos
    
    def update_disp(self, image, rect):
        self.image = image
        self.rect = rect

    def update(self, player_pos, now, *args, **kwargs):
        self.health = max(0, self.health)
        if self.health <= 0:
            self.killed = True
        
        if self.killed:
            img = self.kill_anim.get_image()
            self.image = scale_image(img, self.size)
            self.rect = self.image.get_rect(center=self.pos)
            return
        
        if self.at_target():
            if not self.stop_flag:
                self.stop_flag = True
                self.last_target = now
                self.real_pos = self.target
                self.good_target = False
                self.stop()

        if not self.good_target:
            if now - self.last_target > TARGET_DURATION and random.random() < RANDOM_CHANCE:
                self.retarget()

        direction = self.target - self.real_pos
        if self.run:
            direction = -(player_pos - self.real_pos)
            if now - self.last_target >= TARGET_DURATION and random.random() < RANDOM_WALK_CHANCE:
                self.run = False
                self.speed = NPC_SPEED / TILE_SIZE
                self.target = self.random_target()
        
        if direction.length() != 0:
            self.real_pos += direction.normalize() * self.speed
        self.real_pos.x = clamp(self.real_pos.x, 0, WORLD_WIDTH)
        self.real_pos.y = clamp(self.real_pos.y, 0, WORLD_HEIGHT)

        if self.speed != 0:
            ss_index = 0
        else:
            ss_index = 1
        self.orit = get_orient(direction)
        if self.orit == RIGHT:
            img = self.right[ss_index].get_image()
        if self.orit == UP:
            img = self.up[ss_index].get_image()
        if self.orit == LEFT:
            img = self.right[ss_index].get_image()
            img = pygame.transform.flip(img, 1, 0)
        if self.orit == DOWN:
            img = self.down[ss_index].get_image()
        self.image = img
