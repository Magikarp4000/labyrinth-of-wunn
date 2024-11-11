import pygame
from pygame.locals import *
from pygame.math import Vector2
from pygame.math import clamp

import random
import math

from config import *
from Camera import Camera
from Player import Player
from Spritesheet import Spritesheet
from utils import *
from dialogue import Dialogue
from npc import NPC
from action import detect_dialogue, detect_action
from action import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Game:
    def __init__(self):
        self.in_dialogue = False
        try:
            pygame.mixer.init()
            self.music = pygame.mixer.Sound("assets/music/m.wav")
            self.music.play(-1)
        except:
            pass

        self.zoom = 1

        self.tile_size = TILE_SIZE
        self.tiles = self.gen_world()

        self.in_dialogue = False
        self.in_typing = False
        self.typed_text = None
        self.wait = False

        self.nps = []
        self.tiles, self.house_tiles, self.locations = self.gen_world()
    
    def check_house(self, x, y, house_tiles):
        for i5 in range(x-4,x+4):
            for i6 in range(y-4,y+4):
                if (i5,i6) in house_tiles:
                    return True
        return False

    def gen_world(self):
        tilesheet = Spritesheet('assets/texture/TX Tileset Grass.png', 16)
        house_image = pygame.image.load('assets/Cute_Fantasy_Free/Outdoor decoration/House.png')
        house_tiles = {}
        tiles = {}
        house_locations = {}
        for i in range(WORLD_HEIGHT + 1):
            for j in range(WORLD_WIDTH + 1):
                x, y = 12, 14
                while (x, y) == (12, 14) or (x, y) == (15, 14):
                    x = random.randint(0, tilesheet.w - 1)
                    y = random.randint(0, tilesheet.h - 1)
                tile = scale_image(tilesheet.get_image(x, y), self.tile_size)
                tiles[i, j] = tile
        for h1 in range(NUM_HOUSES):
            while True:
                x,y = random.randint(15,WORLD_WIDTH-16), random.randint(10,WORLD_HEIGHT-11)
                if not self.check_house(x, y, house_tiles):
                    house_image = pygame.transform.scale(house_image, (HOUSE_WIDTH,HOUSE_HEIGHT))
                    house_tiles[x,y] = house_image
                    break
        special_houses = random.sample(list(house_tiles.keys()), len(LOCATIONS))
        for idx, house in enumerate(special_houses):
            house_locations[LOCATIONS[idx]] = house
        return tiles, house_tiles, house_locations


    def render_tiles(self, camera):
        for x in range(int(camera.tl.x) - 4, int(camera.br.x) + WIDTH + 4):
            for y in range(int(camera.tl.y) - 4, int(camera.br.y) + HEIGHT + 4):
                if (x, y) in self.house_tiles:
                    self.house_tiles[x, y] = pygame.transform.scale(self.house_tiles[x,y], (HOUSE_WIDTH*self.zoom,HOUSE_HEIGHT*self.zoom))
                    pos_x = camera.pos.x - (camera.real_pos.x - x) * self.tile_size
                    pos_y = camera.pos.y - (camera.real_pos.y - y) * self.tile_size
                    screen.blit(self.house_tiles[x, y], self.house_tiles[x, y].get_rect(center=(pos_x, pos_y)))
                for location in self.locations:
                    if self.locations[location] == (x, y):
                        images, rects = multitext(location.title(), pos_x - self.tile_size / 2, pos_y - self.tile_size * 3, SCREEN_WIDTH, DIALOGUE_YSPACING, 'Arial', FONT_SIZE, BLACK)
                        screen.blit(images[0], rects[0])

    def display_text(self, text):
        text_images, text_rects = multitext(text, DIALOGUE_X, DIALOGUE_Y, SCREEN_WIDTH-(2*DIALOGUE_X), DIALOGUE_YSPACING, 'Arial', FONT_SIZE, BLACK)
        pygame.draw.rect(screen, WHITE, (DIALOGUE_X, DIALOGUE_Y, SCREEN_WIDTH-(2*DIALOGUE_X), SCREEN_HEIGHT-DIALOGUE_Y-20))
        for image, rect in zip(text_images, text_rects):
            screen.blit(image, rect)        
    
    def get_collision(self, player, sprites):
        collide = pygame.sprite.spritecollideany(player, sprites)
        return collide

    def get_random(self, size):
        return random.random() * random.randint(-size, size)

    def interaction(self, collide):
        response = None
        if not self.wait:
            if collide.dialogue is None:
                collide.dialogue = Dialogue()
                response = collide.dialogue.test("Hi! Briefly introduce yourself.")
            else:
                if self.typed_text is None:
                    self.in_typing = True
                    self.typed_text = ""
                    response = None
                else:
                    response = collide.dialogue.test(self.typed_text)
                    self.typed_text = None
        if response is not None:
            self.display_text(detect_dialogue(response))
            action = detect_action(response)
            if action.location in self.locations:
                collide.good_target = True
                collide.target = self.locations[action.location]
            if action.t == ACTION_RUN or action.t == ACTION_SCREAM:
                collide.run = True
                collide.speed = NPC_RUN_SPEED / TILE_SIZE
            elif action.t == ACTION_WALK:
                collide.run = False
                collide.speed = NPC_SPEED / TILE_SIZE
            elif action.t == ACTION_SUICIDE:
                collide.die()
            self.wait = True

    def main(self):
        sprites = pygame.sprite.Group()

        player = Player()
        sprites.add(player)

        self.npcs = pygame.sprite.Group([NPC(*(player.real_pos + (self.get_random(10), self.get_random(10))))
                                         for _ in range(NUM_NPCS)])
        sprites.add(self.npcs)

        camera = Camera(player, screen)

        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                # Dialogue toggler    
                if event.type == pygame.KEYDOWN:
                    if self.in_typing:
                        if event.key == pygame.K_RETURN:
                            self.in_typing = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.typed_text = self.typed_text[:-1]
                        else:
                            self.typed_text += event.unicode
                        continue
                    if event.key == pygame.K_SPACE:
                        collide = self.get_collision(player, self.npcs)
                        if collide is not None:
                            self.in_dialogue = not self.in_dialogue
                            self.wait = False
                # End of dialogue toggler
                if event.type == MOUSEWHEEL:
                    camera.update_zoom(event.y)
                if event.type == KEYDOWN:
                    if event.key == K_x:
                        player.attack()
                        kills = self.get_collision(player, self.npcs)
                        if kills is not None:
                            kills.die()
            keys = pygame.key.get_pressed()
            # In dialogue
            if self.in_dialogue and not self.in_typing:
                self.interaction(collide)
            # Not in dialogue
            elif self.in_typing:
                self.display_text(self.typed_text)
            else:
                # Player movement
                player.move(keys, camera.zoom)
                # Update sprites
                sprites.update(player.real_pos)
                # Update camera
                camera.update()
                # Rendering
                camera.render_tiles(self.tiles, Vector2(TILE_SIZE, TILE_SIZE))
                camera.render_tiles(self.house_tiles, Vector2(HOUSE_WIDTH, HOUSE_HEIGHT), padding=5)
                camera.render_group(self.npcs, Vector2(PLAYER_SIZE, PLAYER_SIZE))
                camera.render(player, Vector2(PLAYER_SIZE, PLAYER_SIZE))
            pygame.display.flip()
            print(clock.get_fps())
            clock.tick(FPS)

        pygame.quit()


if __name__ == '__main__':
    # print(math.atan(-math.sqrt(3)/1))
    game = Game()
    game.main()
