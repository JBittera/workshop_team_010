import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, RED, GREEN, PLAYER_SPEED, PLAYER_HEALTH, PLAYER_SHOOT_COOLDOWN, \
    PLAYER_SIZE


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, controls, name, animation_frames_set):
        super().__init__()
        self.animation_frames = animation_frames_set
        self.direction = 'right'
        self.current_frame_index = 0

        if self.animation_frames[self.direction]:
            self.image = self.animation_frames[self.direction][self.current_frame_index]
        else:
            self.image = None

        if self.image:
            self.rect = self.image.get_rect(center=(x, y))
        else:
            self.rect = pygame.Rect(0, 0, PLAYER_SIZE[0], PLAYER_SIZE[1])
            self.rect.center = (x, y)

        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH
        self.controls = controls
        self.name = name
        self.last_shot_time = 0
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        self.last_frame_update = pygame.time.get_ticks()
        self.animation_speed = 100

    def update(self, keys, current_time):
        moving = False

        if keys[self.controls['left']]:
            self.rect.x -= self.speed
            self.direction = 'left'
            moving = True
        elif keys[self.controls['right']]:
            self.rect.x += self.speed
            self.direction = 'right'
            moving = True

        if keys[self.controls['up']]:
            self.rect.y -= self.speed
            moving = True
        if keys[self.controls['down']]:
            self.rect.y += self.speed
            moving = True

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(SCREEN_WIDTH, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(SCREEN_HEIGHT, self.rect.bottom)

        if self.animation_frames[self.direction]:
            if moving and current_time - self.last_frame_update > self.animation_speed:
                self.current_frame_index = (self.current_frame_index + 1) % len(self.animation_frames[self.direction])
                self.image = self.animation_frames[self.direction][self.current_frame_index]
                self.last_frame_update = current_time
            elif not moving:
                self.current_frame_index = 0
                self.image = self.animation_frames[self.direction][self.current_frame_index]
        else:
            self.image = None

    def shoot(self, current_time, bullet_img):
        from bullet import Bullet

        if current_time - self.last_shot_time > self.shoot_cooldown:
            self.last_shot_time = current_time

            bullet_spawn_offset_x = self.rect.width / 2 + 5
            bullet_start_x = self.rect.centerx

            angle = 0
            if self.direction == 'left':
                bullet_start_x -= bullet_spawn_offset_x
                angle = math.pi
            elif self.direction == 'right':
                bullet_start_x += bullet_spawn_offset_x
                angle = 0

            bullet_start_y = self.rect.centery

            if bullet_img:
                return Bullet(bullet_start_x, bullet_start_y, angle, bullet_img)
        return None

    def draw_health_bar(self, surface):
        health_bar_width = self.rect.width
        health_bar_height = 5
        health_ratio = self.health / 100.0

        bar_x = self.rect.x
        bar_y = self.rect.y - 10

        pygame.draw.rect(surface, RED, (bar_x, bar_y, health_bar_width, health_bar_height))
        pygame.draw.rect(surface, GREEN, (bar_x, bar_y, health_bar_width * health_ratio, health_bar_height))
