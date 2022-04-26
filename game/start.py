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

PLAYER = game.objects.Player(10, 10, Vector2(WIDTH / 2, HEIGHT - 32), 10)

all_sprites = pygame.sprite.Group()

ENEMIES = []

for y in range(5):
    for x in range(20):
        ENEMIES.append(game.objects.Enemy(10, 10, Vector2(x * 20, y * 20), 10))

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
        
        displaysurface.fill((0, 0, 0))
    
        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
    
        pygame.display.update()
        FramePerSec.tick(FPS)
