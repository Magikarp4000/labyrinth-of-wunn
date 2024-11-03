from config import *

from character import Character
from collections import deque
from dialogue import Dialogue

import pygame
from pygame.math import Vector2

NPC_CLEAR_QUEUE = 1

class NPC(Character):
    def __init__(self, x, y):
        self.real_pos = Vector2(x, y)
        self.image = pygame.Surface((BASE_PLAYER_SIZE, BASE_PLAYER_SIZE))
        self.rect = self.image.get_rect(center=self.real_pos)
        self.sus = 0
        self.actions = deque()
        self.dialogue = Dialogue()

    def queue_action(self, action, flags):
        if flags & NPC_CLEAR_QUEUE:
            self.actions.clear()
        self.actions.append(action)
    
    def update(self):
        self.rect = self.image.get_rect(center=self.real_pos)
        
