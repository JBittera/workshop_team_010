import pygame
from settings import PLAYER_SIZE, PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, BORDER_PADDING
import random

def load_image(path, scale=None):

    try:
        image = pygame.image.load(path).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        return None

def load_frames_from_spritesheet(sheet_path, frame_width, frame_height, row_index, start_frame_column, num_frames):
    sheet = load_image(sheet_path)
    frames = []
    if sheet:
        for i in range(num_frames):
            # Calculate the x-coordinate for the current frame
            x_offset = (start_frame_column + i) * frame_width
            y_offset = row_index * frame_height

            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (x_offset, y_offset, frame_width, frame_height))
            frames.append(frame)
    return frames

def random_player1_start_position():
    x = random.randint(
        PLAYER_SIZE[0]//2 + BORDER_PADDING,
        SCREEN_WIDTH//2 - PLAYER_SIZE[0]//2 - BORDER_PADDING
    )
    y = random.randint(
        PLAYER_SIZE[1]//2 + BORDER_PADDING,
        SCREEN_HEIGHT - PLAYER_SIZE[1]//2 - BORDER_PADDING
    )
    return x, y

def random_player2_start_position():
    x = random.randint(
        SCREEN_WIDTH//2 + PLAYER_SIZE[0]//2 + BORDER_PADDING,
        SCREEN_WIDTH - PLAYER_SIZE[0]//2 - BORDER_PADDING
    )
    y = random.randint(
        PLAYER_SIZE[1]//2 + BORDER_PADDING,
        SCREEN_HEIGHT - PLAYER_SIZE[1]//2 - BORDER_PADDING
    )
    return x, y

def no_collision(player_pos_func, sprite_group):
    while True:
        rect = pygame.Rect(0, 0, PLAYER_SIZE[0] + 2*PLAYER_SPEED, PLAYER_SIZE[1] + 2*PLAYER_SPEED)
        rect.center = player_pos_func()
        sprite = pygame.sprite.Sprite()
        sprite.rect = rect
        if not pygame.sprite.spritecollideany(sprite, sprite_group):
            return rect.center
