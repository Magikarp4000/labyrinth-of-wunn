"""Config file."""

import math


FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

INF = 10**9

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
NUM_HOUSES = 10
HOUSE_WIDTH = TILE_SIZE * 3
HOUSE_HEIGHT = TILE_SIZE * 4
HOUSE_PADDING_X = WORLD_WIDTH // 4
HOUSE_PADDING_Y = WORLD_HEIGHT // 4
MAX_HOUSE_CHECK = 10**6

PLAYER_SPEED = 3
PLAYER_SIZE = 64
PLAYER_HEALTH = 100
PLAYER_DMG = 10
ADMIN_SPEED = 10

CAMERA_PADDING_X = SCREEN_WIDTH / 3
CAMERA_PADDING_Y = SCREEN_HEIGHT / 3

MAX_ZOOM = 5
ZOOM_RATE = 0.5
START_ZOOM = 1

NUM_NPCS = 25
NPC_SPEED = 1.5
NPC_RUN_SPEED = 4
NPC_SIZE = PLAYER_SIZE
NPC_HEALTH = 30
NPC_DMG = 10
RANDOM_CHANCE = 0.01
RANDOM_WALK_CHANCE = 0.002
TARGET_DURATION = 3
NPC_SPAWN_RADIUS = 30
NPC_DIALOGUE_CHANCE = 0.001
NPC_DIALOGUE_TIME = 5
NPC_DEATH_TIME = 5

SCREAM_SPREAD = 5
DIE_SPREAD = 8

#Dialogue
DLG_X = SCREEN_WIDTH / 20
DLG_Y = SCREEN_HEIGHT * 2 / 3
DLG_WIDTH = SCREEN_WIDTH - (2 * DLG_X)
DLG_HEIGHT = SCREEN_HEIGHT - DLG_Y - 20
DLG_SPACING = 25

DLG_BOX_PAD_LEFT = 10
DLG_BOX_PAD_RIGHT = 25
DLG_BOX_PAD_Y = 5

NPC_DLG_FONT_SIZE = 15
NPC_DLG_SPACING = 20
NPC_DLG_WIDTH = 300

FONT_SIZE = 25

LOCATIONS = ['shop', 'office', 'haunted house', 'cinema', 'cafe']

ACTION_WALK = 1
ACTION_RUN = 2
ACTION_SCREAM = 3
ACTION_DIE = 4

MID_QUAD_0 = math.pi / 4
MID_QUAD_1 = 3 * math.pi / 4
MID_QUAD_2 = -3 * math.pi / 4
MID_QUAD_3 = -math.pi / 4

RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3

INFO_PADDING_X = 20
INFO_PADDING_Y = 20

# Admin
ADMIN_TEXT_SIZE = 40
ADMIN_TEXT_LIFE = 3
HITBOX_WIDTH = 2
