import os
import pygame

def get_texture_path(texture: str) -> pygame.Surface:
    return pygame.image.load(os.path.abspath(os.path.join("assets", "textures", f"{texture}.png")))
