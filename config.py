"""Config file."""
import math


FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BASE_TILE_SIZE = 36

# Num of tiles in world
WORLD_WIDTH = 70
WORLD_HEIGHT = 50

# Screen size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Num of tiles displayed on screen
WIDTH = math.ceil(SCREEN_WIDTH / BASE_TILE_SIZE)
HEIGHT = math.ceil(SCREEN_HEIGHT / BASE_TILE_SIZE)

BASE_PLAYER_SPEED = 3
BASE_PLAYER_SIZE = 64

BASE_CAMERA_SPEED = BASE_PLAYER_SPEED / BASE_TILE_SIZE
CAMERA_PADDING_X = SCREEN_WIDTH / 4
CAMERA_PADDING_Y = SCREEN_HEIGHT / 4

MAX_ZOOM = 5
ZOOM_RATE = 0.5

NUM_NPCS = 1

#Dialogue
DIALOGUE_X = SCREEN_WIDTH / 20
DIALOGUE_Y = SCREEN_HEIGHT * 3/5
DIALOGUE_YSPACING = 25
HOUSE_WIDTH = 120
HOUSE_HEIGHT = 168

FONT_SIZE = 25
