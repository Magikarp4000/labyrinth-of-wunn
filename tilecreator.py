import pygame
from pygame.locals import *

from collections import deque


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WIDTH = 900
HEIGHT = 550
SIZE = 15
X = WIDTH // SIZE
Y = HEIGHT // SIZE
FPS = 60
SQUARE_COLOURS = {
    'empty': BLACK,
    'track': WHITE,
    'start': BLUE,
    'finish': GREEN
}
MOUSE_COLOURS = {
    'track': RED,
    'start': BLUE,
    'finish': GREEN
}

class _GUISquare:
    def __init__(self, x, y):
        self.image = pygame.Surface((SIZE, SIZE))
        self.rect = self.image.get_rect(center=(x * SIZE + SIZE / 2, y * SIZE + SIZE / 2))
        self.x = x
        self.y = y
        self.state = 'empty'
    
    def _update(self, mouse_state, left_down, right_down):
        if left_down:
            self.state = mouse_state
        elif right_down:
            self.state = 'empty'
    
    def update(self, *args, **kwargs):
        self.image.fill(SQUARE_COLOURS[self.state])
    
    def reset(self):
        self.state = 'empty'

class _CursorSquare():
    def __init__(self):
        self.image = pygame.Surface((SIZE, SIZE))
        self.rect = self.image.get_rect()
    
    def update(self, mouse_state, *args, **kwargs):
        x, y = _normalise(pygame.mouse.get_pos())
        self.rect = self.image.get_rect(center=(x * SIZE + SIZE / 2, y * SIZE + SIZE / 2))
        self.image.fill(MOUSE_COLOURS[mouse_state])

def _normalise(pos):
    return pos[0] // SIZE, pos[1] // SIZE

def _reset(sprites):
    for sprite in sprites:
        if isinstance(sprite, _GUISquare):
            sprite.reset()
    return sprites

def _get_squares(sprites):
    squares = []
    for sprite in sprites.values():
        if isinstance(sprite, _GUISquare):
            squares.append(sprite)
    return squares

def _get_squares_dict(sprites):
    return {(sq.x, sq.y): sq for sq in _get_squares(sprites)}

def _bfs(start, squares, mouse_state):
    delta_x = [0, 0, 1, -1]
    delta_y = [1, -1, 0, 0]
    queue = deque()
    visited = {(x, y): False for x in range(X) for y in range(Y)}
    queue.append(start)
    while queue:
        x, y = queue.popleft()
        if (x, y) not in visited or visited[x, y]:
            continue
        visited[x, y] = True
        for dx, dy in zip(delta_x, delta_y):
            nx = x + dx
            ny = y + dy
            if (nx, ny) in visited and squares[nx, ny].state == squares[start].state:
                queue.append((nx, ny))
    visited_list = []
    for pos in visited:
        if visited[pos]:
            visited_list.append(pos)
    return visited_list

def _gui():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((X * SIZE, Y * SIZE))
    sprites = {(x, y): _GUISquare(x, y) for x in range(X) for y in range(Y)}
    sprites.update({'cursor': _CursorSquare()})
    left_down, right_down = False, False
    mouse_state = 'track'
    mouse_action = 'brush'
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_RETURN:
                    running = False
                if event.key == K_SPACE:
                    sprites = _reset(sprites)
                if event.key == K_1:
                    mouse_state = 'track'
                elif event.key == K_2:
                    mouse_state = 'start'
                elif event.key == K_3:
                    mouse_state = 'finish'
                if event.key == K_f:
                    mouse_action = 'brush' if mouse_action == 'fill' else 'fill'
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    left_down = True
                elif event.button == 3:
                    right_down = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    left_down = False
                elif event.button == 3:
                    right_down = False
        # Update state
        x, y = _normalise(pygame.mouse.get_pos())
        to_update = [(x, y)]
        if mouse_action == 'fill':
            to_update = _bfs((x, y), _get_squares_dict(sprites), mouse_state)
        for pos in to_update:
            if pos in sprites:
                sprites[pos]._update(mouse_state, left_down, right_down)
        # Update graphics
        for sprite in sprites.values():
            sprite.update(mouse_state)
        for sprite in sprites.values():
            screen.blit(sprite.image, sprite.rect)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    return _get_squares(sprites)

def get_tilesheet():
    squares = _gui()
    tilesheet = []
    for square in squares:
        pos = (square.x, square.y)
        if square.state == 'track':
            track.append(pos)
        elif square.state == 'start':
            start.append(pos)
            track.append(pos)
        elif square.state == 'finish':
            finish.append(pos)
            track.append(pos)
    track = list(dict.fromkeys(track))
    return track, start, finish

print(get_track())