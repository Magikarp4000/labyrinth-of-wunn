import pygame
from pygame.math import Vector2
from pygame.math import clamp

from config import *
from utils import *


class Camera:
    def __init__(self, obj, screen: pygame.Surface, base_ratio, world_width, world_height, 
                 cam_pad_x, cam_pad_y, zoom_rate, max_zoom, zoom=1):
        self.obj = obj
        self.screen = screen
        self.base_ratio = base_ratio
        self.scr_width = screen.get_width()
        self.scr_height = screen.get_height()
        self.wld_width = world_width
        self.wld_height = world_height
        self.cam_pad_x = cam_pad_x
        self.cam_pad_y = cam_pad_y
        self.zoom_rate = zoom_rate
        self.max_zoom = max_zoom

        self.zoom = zoom
        self.ratio = self.base_ratio * zoom

        self.real_pos = obj.real_pos / self.ratio
        self.pos = obj.pos
        self.tl = self.real_pos - self.pos / self.ratio
        self.br = self.real_pos + ((self.scr_width, self.scr_height) - self.pos) / self.ratio
    
    def update_zoom(self, delta_zoom):
        self.zoom = clamp(self.zoom + delta_zoom * self.zoom_rate, 1, self.max_zoom)
        self.ratio = self.zoom * self.base_ratio

    def clamp_obj_pos(self):
        real_pos = self.obj.real_pos
        pos = self.obj.pos
        
        if (real_pos.x > self.cam_pad_x / self.ratio and
            real_pos.x < self.wld_width - self.cam_pad_x / self.ratio):
            pos.x = clamp(pos.x, self.cam_pad_x, self.scr_width - self.cam_pad_x)
        
        if pos.x / self.ratio >= real_pos.x:
            pos.x = real_pos.x * self.ratio
        
        if (self.scr_width - pos.x) / self.ratio >= self.wld_width - real_pos.x:
            pos.x = self.scr_width - (self.wld_width - real_pos.x) * self.ratio
        
        if (real_pos.y > self.cam_pad_y / self.ratio and 
            real_pos.y < self.wld_height - self.cam_pad_y / self.ratio):
            pos.y = clamp(pos.y, self.cam_pad_y, self.scr_height - self.cam_pad_y)
        
        if pos.y / self.ratio >= real_pos.y:
            pos.y = real_pos.y * self.ratio
        
        if (self.scr_height - pos.y) / self.ratio >= self.wld_height - real_pos.y:
            pos.y = self.scr_height - (self.wld_height - real_pos.y) * self.ratio

        pos.x = clamp(pos.x, 0, self.scr_width)
        pos.y = clamp(pos.y, 0, self.scr_height)

        return pos

    def update(self):
        self.obj.update_pos(self.clamp_obj_pos())

        self.real_pos = self.obj.real_pos
        self.pos = self.obj.pos

        self.tl = self.real_pos - self.pos / self.ratio
        self.br = self.real_pos + ((self.scr_width, self.scr_height) - self.pos) / self.ratio
    
    def in_frame(self, object, padding=0):
        return (self.tl.x - padding <= object.real_pos.x and self.br.x + padding >= object.real_pos.x and
                self.tl.y - padding <= object.real_pos.y and self.br.y + padding >= object.real_pos.y)

    def _render(self, object, obj_size, padding=1):
        if self.in_frame(object, padding):
            pos_x = self.pos.x - (self.real_pos.x - object.real_pos.x) * self.ratio
            pos_y = self.pos.y - (self.real_pos.y - object.real_pos.y) * self.ratio

            object.update_pos(Vector2(pos_x, pos_y))
            try:
                base_image = object.orig_image
            except:
                base_image = object.image
            image = pygame.transform.scale(base_image, self.zoom * obj_size)
            rect = image.get_rect(center=object.pos)
            object.update_disp(image, rect)

            self.screen.blit(object.image, object.rect)

    def render(self, objects, obj_size=None, padding=1):
        if not hasattr(objects, '__iter__'):
            objects = [objects]
        for object in objects:
            if obj_size is None:
                self._render(object, object.size, padding)
            else:
                self._render(object, obj_size, padding)
    
    def render_tiles(self, objects, obj_size, padding=1):
        for x in range(int(self.tl.x) - padding, int(self.br.x) + padding):
            for y in range(int(self.tl.y) - padding, int(self.br.y) + padding):
                if (y, x) in objects:
                    objects[y, x] = pygame.transform.scale(objects[y, x], self.zoom * obj_size)
                    pos_x = self.pos.x - (self.real_pos.x - x) * self.ratio
                    pos_y = self.pos.y - (self.real_pos.y - y) * self.ratio
                    self.screen.blit(objects[y, x], objects[y, x].get_rect(center=(pos_x, pos_y)))
