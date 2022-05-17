import pygame


def get_key_fire(keys, mouse) -> bool:
    return mouse[0] or keys[pygame.K_SPACE]


def get_key_left(keys) -> bool:
    return keys[pygame.K_LEFT] or keys[pygame.K_a]


def get_key_right(keys) -> bool:
    return keys[pygame.K_RIGHT] or keys[pygame.K_d]
