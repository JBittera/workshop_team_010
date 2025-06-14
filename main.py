import pygame
import math


from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, YELLOW,
    PLAYER_SIZE, BULLET_IMAGE_PATH, GAME_ICON_PATH,
    BACKGROUND_IMAGE_PATH, player_animation_paths
)
from utils import load_image
from player import Player
from bullet import Bullet

pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Top-Down Shooter (2 Players)")

background_image = load_image(BACKGROUND_IMAGE_PATH, (SCREEN_WIDTH, SCREEN_HEIGHT))
bullet_image = load_image(BULLET_IMAGE_PATH, (10, 10))

game_icon = load_image(GAME_ICON_PATH)
if game_icon:
    pygame.display.set_icon(game_icon)

player_animation_frames = {
    'left': [],
    'right': []
}

for i in range(1, 5):
    left_path = player_animation_paths['left'].format(i=i)
    right_path = player_animation_paths['right'].format(i=i)

    frame_left = load_image(left_path, PLAYER_SIZE)
    frame_right = load_image(right_path, PLAYER_SIZE)

    if frame_left:
        player_animation_frames['left'].append(frame_left)
    if frame_right:
        player_animation_frames['right'].append(frame_right)

clock = pygame.time.Clock()

player1_start_x = SCREEN_WIDTH // 4
player1_start_y = SCREEN_HEIGHT // 2
player2_start_x = SCREEN_WIDTH * 3 // 4
player2_start_y = SCREEN_HEIGHT // 2

player1_controls = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d,
    'shoot': pygame.K_e
}
player1 = Player(player1_start_x, player1_start_y, player1_controls, "Player 1", player_animation_frames)

player2_controls = {
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'shoot': pygame.K_RSHIFT
}
player2 = Player(player2_start_x, player2_start_y, player2_controls, "Player 2", player_animation_frames)

all_sprites = pygame.sprite.Group()
all_sprites.add(player1, player2)

bullets = pygame.sprite.Group()

font = pygame.font.Font(None, 36)

running = True
game_over = False
winner_text = ""

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == player1_controls['shoot']:
                    bullet = player1.shoot(current_time, bullet_image)
                    if bullet:
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                if event.key == player2_controls['shoot']:
                    bullet = player2.shoot(current_time, bullet_image)
                    if bullet:
                        all_sprites.add(bullet)
                        bullets.add(bullet)

    if not game_over:
        keys = pygame.key.get_pressed()
        player1.update(keys, current_time)
        player2.update(keys, current_time)
        bullets.update()

        hits_player1 = pygame.sprite.spritecollide(player1, bullets, True)
        for hit in hits_player1:
            player1.health -= 10
            if player1.health <= 0:
                player1.health = 0
                game_over = True
                winner_text = "Player 2 Wins!"

        hits_player2 = pygame.sprite.spritecollide(player2, bullets, True)
        for hit in hits_player2:
            player2.health -= 10
            if player2.health <= 0:
                player2.health = 0
                game_over = True
                winner_text = "Player 1 Wins!"


    screen.blit(background_image, (0, 0))


    all_sprites.draw(screen)

    player1.draw_health_bar(screen)
    player2.draw_health_bar(screen)

    player1_health_text = font.render(f"{player1.name}: {player1.health}", True, WHITE)
    screen.blit(player1_health_text, (10, 10))
    player2_health_text = font.render(f"{player2.name}: {player2.health}", True, WHITE)
    screen.blit(player2_health_text, (SCREEN_WIDTH - player2_health_text.get_width() - 10, 10))


    if game_over:
        game_over_font = pygame.font.Font(None, 74)
        winner_display = game_over_font.render(winner_text, True, YELLOW)
        winner_rect = winner_display.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        screen.blit(winner_display, winner_rect)

        restart_font = pygame.font.Font(None, 48)
        restart_text = restart_font.render("Press R to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(restart_text, restart_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_over = False
            player1.health = 100
            player2.health = 100


            player1.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
            player2.rect.center = (SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT // 2)

            for bullet in bullets:
                bullet.kill()
            bullets.empty()

            if player1.animation_frames[player1.direction]:
                player1.current_frame_index = 0
                player1.image = player1.animation_frames[player1.direction][player1.current_frame_index]

            if player2.animation_frames[player2.direction]:
                player2.current_frame_index = 0
                player2.image = player2.animation_frames[player2.direction][player2.current_frame_index]

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
