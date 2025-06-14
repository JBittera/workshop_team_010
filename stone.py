import pygame
from settings import STONE_SIZE, GRAY

class Stone(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        if image:
            self.image = image
        else:
            self.image = pygame.Surface(STONE_SIZE)
            self.image.fill(GRAY)

        self.rect = self.image.get_rect(topleft=(x, y))