import pygame
from pygame.locals import *
from pygame.math import Vector2

import random

from config import *
from Camera import Camera
from Player import Player
from Spritesheet import Spritesheet
from utils import *
from dialogue import Dialogue
from npc import NPC
from action import *
from texts import HouseText


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

        self.nps = []
        self.tiles, self.house_tiles, self.locations, self.house_texts = self.gen_world()
    
    def check_house(self, x, y, house_tiles):
        for i in range(x - HOUSE_WIDTH // TILE_SIZE, x + HOUSE_WIDTH // TILE_SIZE):
            for j in range(y - HOUSE_HEIGHT // TILE_SIZE, y + HOUSE_HEIGHT // TILE_SIZE):
                if (i, j) in house_tiles:
                    return True
        return False

    def gen_world(self):
        tilesheet = Spritesheet('assets/texture/TX Tileset Grass.png', 16)
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

    def get_random(self, size):
        return random.random() * random.randint(-size, size)

    def interaction(self, collide):
        response = None
        if not self.wait:
            if collide.dialogue is None:
                collide.dialogue = Dialogue()
            if 'user' not in collide.dialogue.memory:
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
            if action.t == ACTION_RUN:
                collide.set_run()
            elif action.t == ACTION_SCREAM:
                collide.set_run()
                self.spread(collide)
            elif action.t == ACTION_WALK:
                collide.reset_run()
            elif action.t == ACTION_DIE:
                collide.health = 0
                self.spread(collide)
            collide.friend = action.friend
            self.wait = True

    def spread(self, source):
        for npc in self.npcs:
            if source.real_pos.distance_to(npc.real_pos) <= MAX_SPREAD_DIST:
                npc.set_run()

    def attack_event(self):
        self.player.attack()
        collide = self.get_collision(self.player, self.npcs)
        if collide is not None:
            collide.health -= self.player.dmg
            collide.set_run()
            self.spread(collide)
    
    def get_collision_within_group(self, base, sprites):
        collides = pygame.sprite.spritecollide(base, sprites, dokill=False)
        for collide in collides:
            if collide != base:
                return collide
        return None

    def npc_interaction(self):
        for npc in self.npcs:
            collide = self.get_collision_within_group(npc, self.npcs)
            if collide is not None:              
                if random.random() < NPC_DIALOGUE_CHANCE:
                    if npc.dialogue is None:
                        npc.dialogue = Dialogue()
                    if collide.dialogue is None:
                        collide.dialogue = Dialogue()
                    prompt = npc.dialogue.test(f"What do you want to say to me?", collide.id, save=False)
                    response = collide.dialogue.test(prompt, npc.id)
                    npc.dialogue.save(prompt=response, source=collide.id)
                    print(npc.id, prompt)
                    print(collide.id, response)

    def main(self):
        sprites = pygame.sprite.Group()

        self.player = Player()
        sprites.add(self.player)

        self.npcs = pygame.sprite.Group([NPC(i,
                                             self.player.real_pos.x + self.get_random(SPAWN_RADIUS),
                                             self.player.real_pos.y + self.get_random(SPAWN_RADIUS))
                                        for i in range(NUM_NPCS)])
        sprites.add(self.npcs)

        camera = Camera(self.player, screen, TILE_SIZE, WORLD_WIDTH, WORLD_HEIGHT, CAMERA_PADDING_X,
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
                    camera.update_zoom(event.y)
                if event.type == KEYDOWN:
                    if event.key == K_x:
                        self.attack_event()
            keys = pygame.key.get_pressed()
            # In dialogue
            if self.in_dialogue and not self.in_typing:
                self.interaction(collide)
            # Not in dialogue
            elif self.in_typing:
                self.display_text(self.typed_text)
            else:
                # NPC interaction
                self.npc_interaction()
                # Player movement
                self.player.move(keys, camera.zoom)
                # Update sprites
                sprites.update(self.player.real_pos)
                # Update camera
                camera.update()
                # Rendering
                camera.render_tiles(self.tiles, Vector2(TILE_SIZE, TILE_SIZE), padding=2)
                camera.render_tiles(self.house_tiles, Vector2(HOUSE_WIDTH, HOUSE_HEIGHT), padding=5)
                for text in self.house_texts:
                    camera.render(text, text.size, padding=5)
                camera.render_group(self.npcs, Vector2(PLAYER_SIZE, PLAYER_SIZE))
                camera.render(self.player, Vector2(PLAYER_SIZE, PLAYER_SIZE))
                pos_text = singletext(f"Coords: ({round(self.player.real_pos[0], 1)}, {round(self.player.real_pos[1], 1)})",
                                      INFO_PADDING_X, INFO_PADDING_Y)
                screen.blit(*pos_text)
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.main()
