import pygame, os
import time
from pygame import Vector2

import game.start
from game.util import get_texture_path


class MoveableSprite(pygame.sprite.Sprite):
    def __init__(self, sizeX: int, sizeY: int, position: Vector2, velocity: Vector2):
        super().__init__()
        self.size = Vector2(sizeX, sizeY)
        self.surf = pygame.transform.scale(self.get_texture(), self.size)
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


    def set_position(self, x: float, y: float):
        self.rect.x = x
        self.rect.y = y


    def add_position(self, x: float, y: float):
        self.set_position(self.rect.x + x, self.rect.y + y)

    def remove(self):
        game.start.all_sprites.remove(self)
        del self

    def get_texture(self) -> pygame.Surface:
        surface = pygame.Surface((1, 1))
        surface.fill((128, 255, 40))
        return surface


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
        self.remove()


class Projectile(MoveableSprite):
    def __init__(self, width: int, height: int, position: Vector2, velocity: Vector2, origin: "Player"):
        super().__init__(width, height, position, velocity)
        self.origin = origin

    def update(self):
        super().update()

        for enemy in game.start.ENEMIES:
            if enemy.rect.collidepoint(self.rect.center):
                self.onCollision(enemy)

    def onCollision(self, other: LivingSprite):
        self.kill()
        other.kill()

    def kill(self):
        self.origin.projectiles.remove(self)
        super().kill()


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
        if projectile.origin is not self:
            self.kill()

    def get_texture(self) -> pygame.Surface:
        return get_texture_path("player")


class Enemy(LivingSprite):
    def __init__(self, sizeX: int, sizeY: int, position: Vector2, health):
        super().__init__(sizeX, sizeY, position, Vector2(0, 0), health)

        self.move_timer = 0
        self.moves = 15
        self.direction = 1
        self.rows = 1

    def update(self):
        super().update()

        if self.move_timer <= 0:
            self.add_position(2 * self.direction, 0)

            # Flip direction
            if self.moves % 25 == 0:
                self.add_position(0, 10)
                self.direction *= -1
                self.rows += 1

            self.moves += 1
            self.move_timer = (self.rows * 10) ** -0.5
        else:
            self.move_timer -= self.deltaTime
      
        self.updatePosition()

    def kill(self):
        game.start.ENEMIES.remove(self)
        super().kill()

    def get_texture(self) -> pygame.Surface:
        return get_texture_path("enemy_1")
