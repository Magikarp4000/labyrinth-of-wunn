import pygame
from config import *


pygame.font.init()

def times(k, arr):
    return tuple([x * k for x in arr])

def scale_image(image, size):
    return pygame.transform.scale(image, (size, size))

def singletext(text, x, y, font_name='Arial', font_size=FONT_SIZE, colour=BLACK, pos='topleft', antialias=False):
    font = pygame.font.SysFont(font_name, font_size)
    image = font.render(text, antialias, colour)
    if pos == 'topleft':
        rect = image.get_rect(topleft = (x, y))
    elif pos == 'topright':
        rect = image.get_rect(topright = (x, y))
    elif pos == 'bottomleft':
        rect = image.get_rect(bottomleft = (x, y))
    elif pos == 'bottomright':
        rect = image.get_rect(bottomright = (x, y))
    elif pos == 'center':
        rect = image.get_rect(center = (x, y))
    return image, rect

def multitext(text, x, y, w, spacing, font_name='Arial', font_size=FONT_SIZE, colour=BLACK, pos='topleft', antialias=False):
    images = []
    rects = []
    lines = []

    font = pygame.font.SysFont(font_name, font_size)
    prev = 0
    for i in range(1, len(text)):
        if font.size(text[prev: i])[0] >= w:
            lines.append(text[prev: i-1])
            prev = i-1
    lines.append(text[prev:])
    for line in lines:
        image, rect = singletext(line, x, y, font_name, font_size, colour, pos, antialias)
        images.append(image)
        rects.append(rect)
        y += spacing
    return images, rects

def get_quandrant(direction):
    if direction.x >= 0 and direction.y <= 0:
        return 0
    elif direction.x < 0 and direction.y <= 0:
        return 1
    elif direction.x < 0 and direction.y > 0:
        return 2
    else:
        return 3

def get_angle(direction):
    if direction.x == 0:
        return UP if direction.y < 0 else DOWN
    angle = math.atan(-direction.y / direction.x) # -y cause up is -ve and we want +ve
    quadrant = get_quandrant(direction)
    if quadrant == 1:
        angle += math.pi
    elif quadrant == 2:
        angle -= math.pi
    return angle

def get_orient(direction):
    angle = get_angle(direction)
    if MID_QUAD_3 < angle and angle <= MID_QUAD_0:
        return RIGHT # right
    elif MID_QUAD_0 < angle and angle <= MID_QUAD_1:
        return UP # up
    elif MID_QUAD_1 < angle or angle <= MID_QUAD_2:
        return LEFT # left
    else:
        return DOWN # down

def get_orient_discrete(direction):
    if direction.x > 0:
        return RIGHT
    elif direction.y < 0:
        return UP
    elif direction.x < 0:
        return LEFT
    elif direction.y > 0:
        return DOWN
    return None
