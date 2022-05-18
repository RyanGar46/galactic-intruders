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
            enemies.append(game.objects.Enemy(int(size.x), int(size.y),
                                              Vector2((x * size.x) + (WIDTH // 2) - (ENEMIES_X * size.x // 2),
                                                      (y * size.y) + 20), 10))


def start():
    global GAME_WON
    PLAYER = game.objects.Player(32, 16, Vector2(WIDTH // 2, HEIGHT - 32), 10)
    create_enemies()

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

        display_surface.fill((0, 0, 0))

        for entity in entities:
            display_surface.blit(entity.surf, entity.rect)

        pygame.display.update()
        FramePerSec.tick(FPS)


def game_win():
    completion_text = game.objects.Text(FONT, "You Won!", (255, 255, 255), Vector2(WIDTH // 4, HEIGHT // 2))
