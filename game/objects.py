import time

import pygame
from pygame.math import Vector2

import game.start
from game.input import get_key_right, get_key_left, get_key_fire
from game.util import get_texture


class MoveableSprite(pygame.sprite.Sprite):
    def __init__(self, sizeX: int, sizeY: int, position: Vector2, velocity: Vector2):
        super().__init__()
        self.size = Vector2(sizeX, sizeY)
        self.surf = pygame.transform.scale(self.get_texture(), self.size)
        self.rect = self.surf.get_rect(center=(sizeX // 2, sizeY // 2))
        self.rect.x += position.x
        self.rect.y += position.y
        self.velocity = velocity
        self.deltaTime = 0
        self.currentTime = time.time()
        game.start.add_entity(self)

    def update(self):
        self.update_position()
        self.deltaTime = time.time() - self.currentTime
        self.currentTime = time.time()

    def update_position(self):
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
        game.start.remove_entity(self)
        del self

    def get_texture(self) -> pygame.Surface:
        surface = pygame.Surface((1, 1))
        surface.fill((128, 255, 40))
        return surface


class LivingSprite(MoveableSprite):
    def __init__(self, size_x: int, size_y: int, position: Vector2, velocity: Vector2, health: int):
        super().__init__(size_x, size_y, position, velocity)
        self._health = health
        self.value = 0

        self.kills = 0

    def update(self):
        super().update()

        if self.get_health() <= 0:
            self.kill()

    def get_health(self) -> int:
        return self._health

    def set_health(self, health: int):
        self._health = health

    def add_health(self, health: int):
        self.set_health(self.get_health() + health)

    def kill(self):
        self.remove()

    def on_kill_enemy(self, enemy: "LivingSprite"):
        self.kills += 1


class Projectile(MoveableSprite):
    def __init__(self, width: int, height: int, position: Vector2, velocity: Vector2, origin: "Player"):
        super().__init__(width, height, position, velocity)
        self.origin = origin

    def update(self):
        super().update()

        for enemy in game.start.enemies:
            if enemy.rect.collidepoint(self.rect.center):
                self.on_collision(enemy)

    def on_collision(self, other: LivingSprite):
        other.kill()
        self.origin.on_kill_enemy(other)
        self.kill()

    def kill(self):
        self.origin.projectiles.remove(self)
        super().remove()


class Player(LivingSprite):
    def __init__(self, size_x: int, size_y: int, position: Vector2, health: int):
        super().__init__(size_x, size_y, position, Vector2(0, 0), health)

        self.projectiles = []
        self.fireCooldown = 0

        # Movement
        self.moveX = 0
        self.moveY = 0
        self.frame = 0

        self.score = 0

    def update(self):
        super().update()

        if self.fireCooldown > 0:
            self.fireCooldown = max((0, self.fireCooldown - self.deltaTime))

        # Update projectiles
        for projectile in self.projectiles:
            projectile.update()

    def check_input(self, keys, mouse):
        """
        Handles the player's input
        """

        # Movement
        direction = Vector2(0, 0)
        direction.x += get_key_right(keys) - get_key_left(keys)
        self.velocity = direction
        self.update()

        # Projectile
        if self.fireCooldown <= 0 and get_key_fire(keys, mouse):
            projectile = Projectile(2, 8, Vector2(self.rect.x + (self.size.x / 2) - 2.5,
                                                  self.rect.y + (self.size.y / 2) - 2.5), Vector2(0, 1), self)
            self.projectiles.append(projectile)
            self.fireCooldown = 0.5

        # Debug
        if keys[pygame.K_LCTRL] and keys[pygame.K_LSHIFT] and get_key_fire(keys, mouse):
            self.fireCooldown = 0

    def on_collide(self, projectile: Projectile):
        if projectile.origin is not self:
            self.kill()

    def get_texture(self) -> pygame.Surface:
        return get_texture("player", game.start.GREEN)

    def on_kill_enemy(self, enemy: LivingSprite):
        super().on_kill_enemy(enemy)
        self.score += enemy.value


class Enemy(LivingSprite):
    def __init__(self, size_x: int, size_y: int, position: Vector2, health, value: int, enemy_type: int):
        self.enemy_type = enemy_type
        super().__init__(size_x, size_y, position, Vector2(0, 0), health)

        self.move_timer = 0
        self.moves = 15
        self.direction = 1
        self.rows = 1
        self.value = value

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

        self.update_position()

    def kill(self):
        game.start.enemies.remove(self)
        super().kill()

    def get_texture(self) -> pygame.Surface:
        if self.enemy_type == 1:
            return get_texture("enemy_1")
        elif self.enemy_type == 2:
            return get_texture("enemy_2")
        else:
            return get_texture("enemy_3")


class Text:
    def __init__(self, font: pygame.font.Font, text: str, color: tuple[int, int, int], position: Vector2):
        self.color = color
        self.font = font
        self.surf = self.font.render(text, False, self.color)
        self.rect = self.surf.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y

        game.start.texts.append(self)
        game.start.add_entity(self)

    def set_text(self, text: str):
        self.surf = self.font.render(text, False, self.color)

    @staticmethod
    def get_multicolored_text(font: pygame.font.Font, texts: list[dict], position: Vector2) -> list["Text"]:
        final_texts = []
        offset = 0

        for section in texts:
            text = section["text"]
            color = section["color"]
            new_position = position
            new_position.x += offset
            text_obj = Text(font, text, color, new_position)
            offset += text_obj.rect.bottomright[0]
            final_texts.append(text_obj)

        return final_texts
