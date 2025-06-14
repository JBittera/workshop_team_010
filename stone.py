import pygame
from settings import STONE_SIZE

class Stone(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        if not self.image:
            self.rect = pygame.Rect(x, y, STONE_SIZE[0], STONE_SIZE[1])