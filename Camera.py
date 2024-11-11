import pygame
from pygame.math import Vector2
from pygame.math import clamp

from config import *
from utils import *


class Camera:
    def __init__(self, obj, screen):
        self.obj = obj
        self.screen = screen

        self.pos = obj.pos
        self.real_pos = obj.real_pos / TILE_SIZE
        self.tl = self.real_pos - self.pos / TILE_SIZE
        self.br = self.real_pos + ((SCREEN_WIDTH, SCREEN_HEIGHT) - self.pos) / TILE_SIZE
        
        self.zoom = 1
        self.tile_size = TILE_SIZE
    
    def update_zoom(self, delta_zoom):
        self.zoom = clamp(self.zoom + delta_zoom * ZOOM_RATE, 1, MAX_ZOOM)
        self.tile_size = self.zoom * TILE_SIZE

    def update_obj(self):
        self.obj.real_pos.x = clamp(self.obj.real_pos.x, 0, WORLD_WIDTH)
        self.obj.real_pos.y = clamp(self.obj.real_pos.y, 0, WORLD_HEIGHT)
        
        if (self.obj.real_pos.x > CAMERA_PADDING_X / self.tile_size and
            self.obj.real_pos.x < WORLD_WIDTH - CAMERA_PADDING_X / self.tile_size):
            self.obj.pos.x = clamp(self.obj.pos.x, CAMERA_PADDING_X, SCREEN_WIDTH - CAMERA_PADDING_X)
        if self.obj.pos.x / self.tile_size >= self.obj.real_pos.x:
            self.obj.pos.x = self.obj.real_pos.x * self.tile_size
        if (SCREEN_WIDTH - self.obj.pos.x) / self.tile_size >= WORLD_WIDTH - self.obj.real_pos.x:
            self.obj.pos.x = SCREEN_WIDTH - (WORLD_WIDTH - self.obj.real_pos.x) * self.tile_size
        
        if (self.obj.real_pos.y > CAMERA_PADDING_Y / self.tile_size and 
            self.obj.real_pos.y < WORLD_HEIGHT - CAMERA_PADDING_Y / self.tile_size):
            self.obj.pos.y = clamp(self.obj.pos.y, CAMERA_PADDING_Y, SCREEN_HEIGHT - CAMERA_PADDING_Y)
        if self.obj.pos.y / self.tile_size >= self.obj.real_pos.y:
            self.obj.pos.y = self.obj.real_pos.y * self.tile_size
        if (SCREEN_HEIGHT - self.obj.pos.y) / self.tile_size >= WORLD_HEIGHT - self.obj.real_pos.y:
            self.obj.pos.y = SCREEN_HEIGHT - (WORLD_HEIGHT - self.obj.real_pos.y) * self.tile_size

        self.obj.pos.x = clamp(self.obj.pos.x, 0, SCREEN_WIDTH)
        self.obj.pos.y = clamp(self.obj.pos.y, 0, SCREEN_HEIGHT)

    def update(self):
        self.update_obj()

        self.pos = self.obj.pos
        self.real_pos = self.obj.real_pos

        self.tl = self.real_pos - self.pos / TILE_SIZE
        self.br = self.real_pos + ((SCREEN_WIDTH, SCREEN_HEIGHT) - self.pos) / self.tile_size
    
    def render(self, object, obj_size, padding=1):
        if (self.tl.x - padding <= object.real_pos.x and self.br.x + padding >= object.real_pos.x and
            self.tl.y - padding <= object.real_pos.y and self.br.y + padding >= object.real_pos.y):
            pos_x = self.pos.x - (self.real_pos.x - object.real_pos.x) * self.tile_size
            pos_y = self.pos.y - (self.real_pos.y - object.real_pos.y) * self.tile_size

            object.pos = Vector2(pos_x, pos_y)
            object.image = pygame.transform.scale(object.image, self.zoom * obj_size)
            object.rect = object.image.get_rect(center=object.pos)

            self.screen.blit(object.image, object.rect)

    def render_group(self, objects, obj_size, padding=1, func=None):
        for object in objects:
            self.render(object, obj_size, padding)
            if func is not None:
                func()
    
    def render_tiles(self, objects, obj_size, padding=2):
        for x in range(int(self.tl.x) - padding, int(self.br.x) + padding):
            for y in range(int(self.tl.y) - padding, int(self.br.y) + padding):
                if (y, x) in objects:
                    objects[y, x] = pygame.transform.scale(objects[y, x], self.zoom * obj_size)
                    pos_x = self.pos.x - (self.real_pos.x - x) * self.tile_size
                    pos_y = self.pos.y - (self.real_pos.y - y) * self.tile_size
                    self.screen.blit(objects[y, x], objects[y, x].get_rect(center=(pos_x, pos_y)))
