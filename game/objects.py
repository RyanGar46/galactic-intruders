import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int):
        super().__init__() 
        self.surf = pygame.Surface((width, height))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect(center = (width / 2, height / 2))
 
class Platform(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center = (width / 2, height / 2))