import os
import pygame
from typing import Optional


def get_texture(texture: str, color: Optional[tuple[int, int, int]] = None) -> pygame.Surface:
    sprite = pygame.image.load(os.path.abspath(os.path.join("assets", "textures", f"{texture}.png")))

    if color is not None:
        color_sprite = pygame.Surface(sprite.get_size()).convert_alpha()
        color_sprite.fill(color)
        sprite.blit(color_sprite, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    return sprite


def get_font(name: str, size: int) -> pygame.font.Font:
    return pygame.font.Font(os.path.abspath(os.path.join("assets", "fonts", f"{name}.ttf")), size)
