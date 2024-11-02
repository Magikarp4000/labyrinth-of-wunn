import json

ACTION_WALK = 1
ACTION_RUN = 2
ACTION_SCREAM = 3
ACTION_SUICIDE = 4

class Action:
    def __init__(self):
        # Associated with one of ACTION_WALK, ... etc.
        # If the action if ACTION_WALK or ACTION_RUN etc. then location is set
        self.t = 0
        self.location = None

def detect_action(reply):
    obj = json.loads(reply)
    try:
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
    except:
        return None
