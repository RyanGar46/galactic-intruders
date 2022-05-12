import pygame
import sys
import game.objects
from pygame import Vector2
from pygame.locals import *

pygame.init()

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

PLAYER = game.objects.Player(32, 16, Vector2(WIDTH / 2, HEIGHT - 32), 10)

all_sprites = pygame.sprite.Group()

ENEMIES = []

ENEMIES_X = 11
ENEMIES_Y = 5

for y in range(ENEMIES_Y):
    for x in range(ENEMIES_X):
        size = Vector2(32, 16)
        ENEMIES.append(game.objects.Enemy(32, 16, Vector2((x * size.x) + (WIDTH / 2) - (ENEMIES_X * size.x / 2), (y * size.y) + 20), 10))

def start():
    all_sprites.add(PLAYER)

    for enemy in ENEMIES:
        all_sprites.add(enemy)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
        PLAYER.checkInput()

        for enemy in ENEMIES:
            enemy.update()
        
        displaysurface.fill((0, 0, 0))
    
        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
    
        pygame.display.update()
        FramePerSec.tick(FPS)
