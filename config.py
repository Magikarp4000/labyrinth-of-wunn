"""Config file."""
import math


FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

TILE_SIZE = 36

# Num of tiles in world
WORLD_WIDTH = 70
WORLD_HEIGHT = 50

# Screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Num of tiles displayed on screen
WIDTH = math.ceil(SCREEN_WIDTH / TILE_SIZE)
HEIGHT = math.ceil(SCREEN_HEIGHT / TILE_SIZE)

# House
HOUSE_WIDTH = TILE_SIZE * 3
HOUSE_HEIGHT = TILE_SIZE * 4
NUM_HOUSES = 10
MAX_HOUSE_CHECK = 500

PLAYER_SPEED = 3
PLAYER_SIZE = 64

CAMERA_SPEED = PLAYER_SPEED / TILE_SIZE
CAMERA_PADDING_X = SCREEN_WIDTH / 3
CAMERA_PADDING_Y = SCREEN_HEIGHT / 3

MAX_ZOOM = 5
ZOOM_RATE = 0.5

NUM_NPCS = 25
NPC_SPEED = 1.5
NPC_RUN_SPEED = 4
RANDOM_CHANCE = 0.01
RANDOM_WALK_CHANCE = 0.002

#Dialogue
DIALOGUE_X = SCREEN_WIDTH / 20
DIALOGUE_Y = SCREEN_HEIGHT * 3 / 5
DIALOGUE_YSPACING = 25

FONT_SIZE = 25

LOCATIONS = ['shop', 'office', 'haunted house', 'cinema', 'cafe']

ACTION_WALK = 1
ACTION_RUN = 2
ACTION_SCREAM = 3
ACTION_SUICIDE = 4

MID_QUAD_0 = math.pi / 4
MID_QUAD_1 = 3 * math.pi / 4
MID_QUAD_2 = -3 * math.pi / 4
MID_QUAD_3 = -math.pi / 4

RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3
