import pygame
from pygame.locals import *
from pygame.math import Vector2

import random
import time

from config import *
from Camera import Camera
from Player import Player
from Spritesheet import Spritesheet
from utils import *
from dialogue import Dialogue
from npc import NPC
from action import *
from texts import *


TILESHEET_TILE_SIZE = 16
INVALID_TILES = [(12, 14), (15, 14)]

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

        self.in_dialogue = False
        self.in_typing = False
        self.typed_text = None
        self.wait = False

        self.npc_texts = pygame.sprite.Group()
        self.tiles, self.house_tiles, self.locations, self.house_texts = self.gen_world()
    
    def check_house(self, x, y, house_tiles):
        for i in range(x - HOUSE_WIDTH // TILE_SIZE, x + HOUSE_WIDTH // TILE_SIZE):
            for j in range(y - HOUSE_HEIGHT // TILE_SIZE, y + HOUSE_HEIGHT // TILE_SIZE):
                if (i, j) in house_tiles:
                    return True
        return False

    def gen_world(self):
        tilesheet = Spritesheet('assets/texture/TX Tileset Grass.png', TILESHEET_TILE_SIZE)
        house_image = pygame.image.load('assets/Cute_Fantasy_Free/Outdoor decoration/House.png')
        house_tiles = {}
        tiles = {}
        house_locations = {}
        house_texts = []

        # Tiles
        for i in range(WORLD_HEIGHT + 1):
            for j in range(WORLD_WIDTH + 1):
                x, y = INVALID_TILES[0]
                while (x, y) in INVALID_TILES:
                    x = random.randint(0, tilesheet.w - 1)
                    y = random.randint(0, tilesheet.h - 1)
                tile = scale_image(tilesheet.get_image(x, y), self.tile_size)
                tiles[i, j] = tile
        
        # Houses
        for _ in range(NUM_HOUSES):
            for _ in range(MAX_HOUSE_CHECK): # guarantees execution
                x = random.randint(HOUSE_PADDING_X, WORLD_WIDTH - HOUSE_PADDING_X - 1)
                y = random.randint(HOUSE_PADDING_Y, WORLD_HEIGHT - HOUSE_PADDING_Y - 1)
                if not self.check_house(x, y, house_tiles):
                    house_image = pygame.transform.scale(house_image, (HOUSE_WIDTH, HOUSE_HEIGHT))
                    house_tiles[y, x] = house_image
                    break
        
        # Special houses
        special_houses = random.sample(list(house_tiles.keys()), len(LOCATIONS))
        for idx, house in enumerate(special_houses):
            house_locations[LOCATIONS[idx]] = (house[1], house[0])
            text_image = singletext(f"{LOCATIONS[idx].title()}", house[1] - 3, house[0] - 4)[0]
            house_texts.append(HouseText(house[1], house[0], text_image))
        
        return tiles, house_tiles, house_locations, house_texts

    def display_text(self, text):
        text_images, text_rects = multitext(text, DIALOGUE_X, DIALOGUE_Y, SCREEN_WIDTH-(2*DIALOGUE_X), DIALOGUE_YSPACING, 'Arial', FONT_SIZE, BLACK)
        pygame.draw.rect(screen, WHITE, (DIALOGUE_X, DIALOGUE_Y, SCREEN_WIDTH-(2*DIALOGUE_X), SCREEN_HEIGHT-DIALOGUE_Y-20))
        for image, rect in zip(text_images, text_rects):
            screen.blit(image, rect)        
    
    def get_collision(self, base, sprites):
        collide = pygame.sprite.spritecollideany(base, sprites)
        return collide

    def get_collision_within_group(self, base, sprites):
        collides = pygame.sprite.spritecollide(base, sprites, dokill=False)
        for collide in collides:
            if collide != base:
                return collide
        return None

    def get_random(self, size):
        return random.random() * random.randint(-size, size)

    def player_attack(self):
        self.player.attack()
        collide = self.get_collision(self.player, self.npcs)
        if collide is not None:
            collide.health -= self.player.dmg
            collide.set_run()
            self.spread(collide)

    def get_npc_response(self, npc):
        if npc.dialogue is None:
            npc.dialogue = Dialogue()
        if 'user' not in npc.dialogue.memory:
            response = npc.dialogue.test("Hi! Briefly introduce yourself.")
        else:
            if self.typed_text is None:
                self.in_typing = True
                self.typed_text = ""
                response = None
            else:
                response = npc.dialogue.test(self.typed_text)
                self.typed_text = None
        return response
    
    def process_npc_response(self, npc, response):
        self.display_text(detect_dialogue(response))
        npc.act(detect_action(response))
        self.wait = True

    def interaction(self, collide):
        response = None
        if not self.wait:
            response = self.get_npc_response(collide)
        if response is not None:
            self.process_npc_response(collide, response)

    def get_npc_text_surfaces(self, text):
        return multitext(text, 0, 0, 300, spacing=20, font_size=15, pos='midbottom')

    def get_textobjects_from_surfaces(self, target, surfaces, birth):
        return [NPCText(target, Vector2(rect.x, rect.y) / TILE_SIZE, img, birth) for img, rect in zip(*surfaces)]

    def npc_pair_interaction(self, src, dest):
        if src.dialogue is None:
            src.dialogue = Dialogue()
        if dest.dialogue is None:
            dest.dialogue = Dialogue()
        
        try:
            prompt = src.dialogue.test(f"What do you want to say to me?", dest.id, save=False)
            prompt_dlg = detect_dialogue(prompt)
            response = dest.dialogue.test(prompt_dlg, src.id)
            response_dlg = detect_dialogue(response)
            src.dialogue.save(prompt=response_dlg, source=dest.id)
        except:
            print(f"Warning: Attempted NPC interaction between {src.id} and {dest.id} but could not generate response.")
            return None

        prompts = self.get_npc_text_surfaces(prompt_dlg)
        responses = self.get_npc_text_surfaces(response_dlg)
        
        now = time.time()
        prompt_texts = self.get_textobjects_from_surfaces(src, prompts, now)
        response_texts = self.get_textobjects_from_surfaces(dest, responses, now)

        return prompt_texts + response_texts

    def npc_interaction(self):
        for npc in self.npcs:
            if self.camera.in_frame(npc):
                collide = self.get_collision_within_group(npc, self.npcs)
                if collide is not None:              
                    if random.random() < NPC_DIALOGUE_CHANCE:
                        return self.npc_pair_interaction(npc, collide)
        return None
    
    def spread(self, source):
        for npc in self.npcs:
            if source.real_pos.distance_to(npc.real_pos) <= MAX_SPREAD_DIST:
                npc.set_run()

    def main(self):
        sprites = pygame.sprite.Group()
        self.player = Player()
        sprites.add(self.player)

        self.npcs = pygame.sprite.Group([NPC(identifier,
                                             self.player.real_pos.x + self.get_random(NPC_SPAWN_RADIUS),
                                             self.player.real_pos.y + self.get_random(NPC_SPAWN_RADIUS))
                                        for identifier in range(NUM_NPCS)])
        sprites.add(self.npcs)
        self.camera = Camera(self.player, screen, TILE_SIZE, WORLD_WIDTH, WORLD_HEIGHT, CAMERA_PADDING_X,
                        CAMERA_PADDING_Y, ZOOM_RATE, MAX_ZOOM)

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
                        collide = self.get_collision(self.player, self.npcs)
                        if collide is not None:
                            self.in_dialogue = not self.in_dialogue
                            self.wait = False
                # End of dialogue toggler
                if event.type == MOUSEWHEEL:
                    self.camera.update_zoom(event.y)
                if event.type == KEYDOWN:
                    if event.key == K_x:
                        self.player_attack()
            keys = pygame.key.get_pressed()

            # In dialogue
            if self.in_dialogue and not self.in_typing:
                self.interaction(collide)
            # Not in dialogue
            elif self.in_typing:
                self.display_text(self.typed_text)
            # General
            else:
                # NPC interaction
                npc_inter = self.npc_interaction()
                if npc_inter is not None:
                    for text in npc_inter:
                        self.npc_texts.add(text)
                        sprites.add(text)
                # Player movement
                self.player.move(keys, self.camera.zoom)
                # Update sprites
                now = time.time()
                sprites.update(player_pos=self.player.real_pos, now=now)
                # Update camera
                self.camera.update()
                # Render
                self.camera.render_tiles(self.tiles, Vector2(TILE_SIZE, TILE_SIZE), padding=2)
                self.camera.render_tiles(self.house_tiles, Vector2(HOUSE_WIDTH, HOUSE_HEIGHT), padding=5)

                self.camera.render(self.house_texts, padding=5)
                self.camera.render(self.npcs, Vector2(NPC_SIZE, NPC_SIZE))
                self.camera.render(self.npc_texts, padding=5)
                self.camera.render(self.player, Vector2(PLAYER_SIZE, PLAYER_SIZE))

                pos_text = singletext(f"Coords: ({round(self.player.real_pos[0], 1)}, {round(self.player.real_pos[1], 1)})",
                                      INFO_PADDING_X, INFO_PADDING_Y)
                screen.blit(*pos_text)
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.main()
