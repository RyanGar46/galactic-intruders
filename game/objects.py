from shutil import move
import pygame
from pygame import Vector2
import game.start


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
        self.moveX = vec.x
        self.moveY = -vec.y

    def updatePosition(self):
        """
        Update sprite position
        """
        self.rect.x += self.moveX
        self.rect.y += self.moveY

    def checkInput(self):
        """
        Handles the player's input
        """
        keys = pygame.key.get_pressed()

        # leftclick, middleclick, rightclick
        mouse = pygame.mouse.get_pressed()

        # Movement
        direction = Vector2(0, 0)
        direction.x += keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        direction.y += keys[pygame.K_UP] - keys[pygame.K_DOWN]
        self.move(direction)
        self.updatePosition()

        # Projectile
        if mouse[0]:
            projectile = Projectile(5, 5)
            game.start.all_sprites.add(projectile)

 
class Projectile(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center = (width / 2, height / 2))

        self.velocity = Vector2(0, 0)

    def updatePosition(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
