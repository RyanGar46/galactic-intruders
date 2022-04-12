from shutil import move
import pygame
import time
from pygame import Vector2
import game.start


class MoveableSprite(pygame.sprite.Sprite):
    def __init__(self, sizeX: int, sizeY: int, position: Vector2, velocity: Vector2):
        super().__init__()
        self.size = Vector2(sizeX, sizeY)
        self.surf = pygame.Surface((sizeX, sizeY))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect(center = (sizeX / 2, sizeY / 2))
        self.rect.x += position.x
        self.rect.y += position.y
        self.velocity = velocity
        self.deltaTime = 0
        self.currentTime = time.time()

    def update(self):
        self.updatePosition()
        self.deltaTime = time.time() - self.currentTime
        self.currentTime = time.time()

    def updatePosition(self):
        """
        Update sprite position
        """
        self.rect.x += self.velocity.x
        self.rect.y -= self.velocity.y

    def onCollide(self):
        pass

    def remove(self):
        game.start.all_sprites.remove(self)


class LivingSprite(MoveableSprite):
    def __init__(self, sizeX: int, sizeY: int, position: Vector2, velocity: Vector2, health: int):
        super().__init__(sizeX, sizeY, position, velocity)
        self.set_health(health)

    def update(self):
        super().update()
        
        if (self.get_health() <= 0):
            self.kill()

    def get_health(self) -> int:
        return self._health

    def set_health(self, health: int):
        self._health = health

    def add_health(self, health: int):
        self.set_health(self.get_health() + health)

    def kill(self):
        self.remove


class Projectile(MoveableSprite):
    def __init__(self, width: int, height: int, position: Vector2, velocity: Vector2, origin: LivingSprite):
        super().__init__(width, height, position, velocity)
        self.origin = origin


class Player(LivingSprite):
    def __init__(self, sizeX: int, sizeY: int, position: Vector2, health: int):
        super().__init__(sizeX, sizeY, position, Vector2(0, 0), health)

        self.projectiles = []
        self.fireCooldown = 0

        # Movement
        self.moveX = 0
        self.moveY = 0
        self.frame = 0

    def update(self):
        super().update()

        if self.fireCooldown > 0:
            self.fireCooldown = max((0, self.fireCooldown - self.deltaTime))
        
        # Update projectiles
        for projectile in self.projectiles:
            projectile.update()

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
        self.velocity = direction
        self.update()

        # Projectile
        if self.fireCooldown <= 0 and mouse[0]:
            projectile = Projectile(5, 5, Vector2(self.rect.x + (self.size.x / 2) - 2.5, self.rect.y + (self.size.y / 2) - 2.5), Vector2(0, 1), self)
            game.start.all_sprites.add(projectile)
            self.projectiles.append(projectile)
            self.fireCooldown = 0.5

    def onCollide(self, projectile: Projectile):
        if (projectile.origin is not self):
            self.kill()


class Enemy(LivingSprite):
    def __init__(self, sizeX: int, sizeY: int, position: Vector2, velocity: Vector2, health):
        super().__init__(sizeX, sizeY, position, velocity, health)
