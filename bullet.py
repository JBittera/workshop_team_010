import pygame
import math
from settings import BULLET_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, BULLET_SIZE


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, image):

        super().__init__()
        self.image = image

        if self.image:
            self.rect = self.image.get_rect(center=(x, y))
        else:
            self.rect = pygame.Rect(0, 0, BULLET_SIZE[0], BULLET_SIZE[1])
            self.rect.center = (x, y)

        self.speed = BULLET_SPEED
        self.velocity_x = self.speed * math.cos(angle)
        self.velocity_y = self.speed * math.sin(angle)

    def update(self):

        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        if (self.rect.left > SCREEN_WIDTH or
                self.rect.right < 0 or
                self.rect.top > SCREEN_HEIGHT or
                self.rect.bottom < 0):
            self.kill()
