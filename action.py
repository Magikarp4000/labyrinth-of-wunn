import json
from config import *


class Action:
    def __init__(self):
        # Associated with one of ACTION_WALK, ... etc.
        # If the action if ACTION_WALK or ACTION_RUN etc. then location is set
        self.t = 0
        self.location = None

def detect_action(reply):
    try:
        obj = json.loads(reply)
        action = Action()
        if obj['action']['type'] == 'walk':
            action.t = ACTION_WALK
        elif obj['action']['type'] == 'run':
            action.t = ACTION_RUN
        elif obj['action']['type'] == 'scream':
            action.t = ACTION_SCREAM
        elif obj['action']['type'] == 'suicide':
            action.t = ACTION_SUICIDE

        action.location = obj['action']['location']
        action.friend = obj['action']['friendliness']
        return action
    except:
        return Action()

def detect_dialogue(reply):
    try:
        obj = json.loads(reply)
        return obj['dialogue']
    except:
        return "Bye bye!"
