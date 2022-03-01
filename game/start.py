import pygame
import sys
import game.objects
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2
 
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
 
PT1 = game.objects.Platform(WIDTH, 100)
PLAYER = game.objects.Player(10, 10)

def start():
    all_sprites = pygame.sprite.Group()
    all_sprites.add(PT1)
    all_sprites.add(PLAYER)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
        PLAYER.checkMovement()
        
        displaysurface.fill((0, 0, 0))
    
        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
    
        pygame.display.update()
        FramePerSec.tick(FPS)