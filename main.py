import pygame
from pygame.locals import *


WIDTH = 800
HEIGHT = 600
FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == '__main__':
    main()
