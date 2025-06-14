import pygame
from settings import BUSH_SIZE

class Bush(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        if not self.image:
            self.rect = pygame.Rect(x, y, BUSH_SIZE[0], BUSH_SIZE[1])
