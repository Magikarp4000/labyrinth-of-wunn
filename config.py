"""Config file."""
import math


FPS = 60

BASE_TILE_SIZE = 36

# Num of tiles in world
WORLD_WIDTH = 500
WORLD_HEIGHT = 400

# Screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 450

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

NUM_NPCS = 25