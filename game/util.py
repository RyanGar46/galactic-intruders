import os
import pygame


def get_texture(texture: str) -> pygame.Surface:
    return pygame.image.load(os.path.abspath(os.path.join("assets", "textures", f"{texture}.png")))


def get_font(name: str, size: int) -> pygame.font.Font:
    return pygame.font.Font(os.path.abspath(os.path.join("assets", "fonts", f"{name}.ttf")), size)
