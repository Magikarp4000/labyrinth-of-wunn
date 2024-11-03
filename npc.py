from character import Character
from collections import deque
from dialogue import Dialogue

import pygame
from pygame.math import Vector2

NPC_CLEAR_QUEUE = 1

class NPC(Character):
    def __init__(self, x, y):
        self.sus = 0
        self.actions = deque()
        self.real_pos = Vector2(x, y)
        d = Dialogue()

    def queue_action(self, action, flags):
        if flags & NPC_CLEAR_QUEUE:
            self.actions.clear()
        self.actions.append(action)
