from character import Character
from collections import deque

NPC_CLEAR_QUEUE = 1

class NPC(Character):
    def __init__(self):
        self.sus = 0
        self.actions = deque()

    def queue_action(self, action, flags):
        if flags & NPC_CLEAR_QUEUE:
            self.actions.clear()
        self.actions.append(action)
