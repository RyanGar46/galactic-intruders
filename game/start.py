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
all_sprites.add(PLAYER)

def start():
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