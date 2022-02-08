from shutil import move
import pygame
from pygame import Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int):
        super().__init__() 
        self.surf = pygame.Surface((width, height))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect(center = (width / 2, height / 2))

        # Movement
        self.moveX = 0
        self.moveY = 0
        self.frame = 0

    def move(self, vec: Vector2):
        """
        control player movement
        """
        self.moveX += vec.x
        self.moveY += vec.y

    def update(self):
        """
        Update sprite position
        """
        self.rect.x = self.rect.x + self.moveX
        self.rect.y = self.rect.y + self.moveY

    def checkMovement(self, event: pygame.event):
        """
        Determains if and where the player should move
        """
        if event.type == pygame.KEYDOWN:
            direction = Vector2(0, 0)
            if event.key == pygame.K_RIGHT:
                direction.x += 1
            if event.key == pygame.K_LEFT:
                direction.x -= 1
            if event.key == pygame.K_UP:
                direction.y += 1
            if event.key == pygame.K_DOWN:
                direction.y -= 1

            self.move(direction)
            self.update()
 
class Platform(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center = (width / 2, height / 2))
