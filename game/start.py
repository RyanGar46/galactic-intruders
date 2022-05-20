import sys

import pygame
from pygame.locals import *
from pygame.math import Vector2

import game.objects
from game.util import get_texture, get_font

pygame.init()

HEIGHT = 450
WIDTH = 400
FPS = 60

# Colors
WHITE = 255, 255, 255
GREEN = 0, 255, 0

FramePerSec = pygame.time.Clock()

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic Intruders")
pygame.display.set_icon(get_texture("icon"))

all_sprites = pygame.sprite.Group()
entities = []
enemies = []
texts = []

ENEMIES_X = 11
ENEMIES_Y = 5

FONT = get_font("main", 32)
FONT_SMALL = get_font("main", 16)

GAME_WON = False

def add_entity(entity):
    if isinstance(entity, pygame.sprite.Sprite):
        all_sprites.add(entity)
    entities.append(entity)


def remove_entity(entity):
    if isinstance(entity, pygame.sprite.Sprite):
        all_sprites.remove(entity)
    entities.remove(entity)


def create_enemies():
    for y in range(ENEMIES_Y):
        for x in range(ENEMIES_X):
            size = Vector2(32, 16)

            # Calculate value
            if y == 4 or y == 3:
                enemy_type = 1
            elif y == 2 or y == 1:
                enemy_type = 2
            else:
                enemy_type = 3

            enemies.append(game.objects.Enemy(int(size.x), int(size.y),
                                              Vector2((x * size.x) + (WIDTH // 2) - (ENEMIES_X * size.x // 2),
                                                      (y * size.y) + 30),
                                              10,
                                              enemy_type * 10,
                                              enemy_type))


def start():
    global GAME_WON
    PLAYER = game.objects.Player(32, 16, Vector2(WIDTH // 2, HEIGHT - 32), 10)
    create_enemies()
    score_text_title, score_text = game.objects.Text.get_multicolored_text(FONT_SMALL, [
        {
            "text": "SCORE: ",
            "color": WHITE
        },
        {
            "text": "000",
            "color": GREEN
        }
    ], Vector2(0, 0))

    while True:
        # Check win conditions
        if PLAYER.kills >= ENEMIES_X * ENEMIES_Y and not GAME_WON:
            GAME_WON = True
            game_win()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # leftclick, middleclick, rightclick
        mouse = pygame.mouse.get_pressed()

        PLAYER.check_input(keys, mouse)

        for enemy in enemies:
            enemy.update()

        # Update score
        score_text.set_text(str(PLAYER.score))

        display_surface.fill((0, 0, 0))

        for entity in entities:
            display_surface.blit(entity.surf, entity.rect)

        pygame.display.update()
        FramePerSec.tick(FPS)


def game_win():
    completion_text = game.objects.Text(FONT, "You Won!", (255, 255, 255), Vector2(WIDTH // 4, HEIGHT // 2))
