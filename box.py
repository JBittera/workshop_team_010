import random
import pygame
from settings import BORDER_PADDING, SCREEN_WIDTH, SCREEN_HEIGHT

class Box(pygame.sprite.Sprite):
    def __init__(self, image, obstacles):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = self._new_box_position(obstacles)

    def _new_box_position(self, obstacles):
        while True:
            x = random.randint(BORDER_PADDING, SCREEN_WIDTH - self.rect.width - BORDER_PADDING)
            y = random.randint(BORDER_PADDING, SCREEN_HEIGHT - self.rect.height - BORDER_PADDING)
            self.rect.topleft = (x, y)
            if not pygame.sprite.spritecollideany(self, obstacles):
                return x, y

    def draw(self, screen):
        screen.blit(self.image, self.rect)
