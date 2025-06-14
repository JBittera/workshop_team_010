import pygame
import math
import settings

from settings import (
    BUSH_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, YELLOW,
    PLAYER_SIZE, BULLET_IMAGE_PATH, GAME_ICON_PATH,
    player_animation_paths,
    STONE_SIZE_SMALL,
    STONE_SIZE_BIG,
    CURRENT_MAP_SETTING_NAME
)
from utils import load_image, no_collision, random_player1_start_position, random_player2_start_position
from player import Player
from bullet import Bullet
from stone import Stone
from bush import Bush
from mapSettings import MAP_SETTINGS

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Top-Down Shooter (2 Players)")

background_image = None
bullet_image = load_image(BULLET_IMAGE_PATH, (10, 10)) # Bullet image is not map-specific
stone_small_image = None
stone_big_image = None
bush_image = None

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

all_sprites = pygame.sprite.Group()
stone_group = pygame.sprite.Group()
bush_group = pygame.sprite.Group()
obstacles = pygame.sprite.Group()


def _switch_map_assets(map_name):
    global background_image, stone_small_image, stone_big_image, bush_image, obstacles

    settings.CURRENT_MAP_SETTING_NAME = map_name
    chosen_map = MAP_SETTINGS[settings.CURRENT_MAP_SETTING_NAME]

    background_image = load_image(chosen_map["background_image_path"], (SCREEN_WIDTH, SCREEN_HEIGHT))
    stone_small_image = load_image(chosen_map["small_stone_image_path"], STONE_SIZE_SMALL)
    stone_big_image = load_image(chosen_map["big_stone_image_path"], STONE_SIZE_BIG)
    bush_image = load_image(chosen_map["bush_image_path"], BUSH_SIZE)

    stone_group.empty()
    bush_group.empty()

    for pos_x, pos_y, stone_type in chosen_map["stone_positions"]:
        if stone_type == "small":
            stone_group.add(Stone(pos_x, pos_y, stone_small_image))
        elif stone_type == "big":
            stone_group.add(Stone(pos_x, pos_y, stone_big_image))

    for pos_x, pos_y in chosen_map["bush_positions"]:
        bush_group.add(Bush(pos_x, pos_y, bush_image))

    obstacles = pygame.sprite.Group(stone_group, bush_group)

    all_sprites.empty()
    all_sprites.add(stone_group, bush_group)
    if 'player1' in globals() and 'player2' in globals():
        all_sprites.add(player1, player2)


player1_start_x, player1_start_y = no_collision(random_player1_start_position, obstacles)
player2_start_x, player2_start_y = no_collision(random_player2_start_position, obstacles)

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

_switch_map_assets(settings.CURRENT_MAP_SETTING_NAME)

bullets = pygame.sprite.Group()

font = pygame.font.Font(None, 36)

running = True
game_start = True
game_menu = False
game_over = False
maps_menu = False
winner_text = ""
selected_index = 0  # aktuálně vybraná položka v menu

start_time = pygame.time.get_ticks()


while running:
    current_time = pygame.time.get_ticks()

    # ÚVODNÍ SCREEN
    #**********************
    if game_start:
        screen.blit(background_image, (0, 0))
        title_font = pygame.font.Font("fonts/PressStart2P.ttf", 45)  # menší velikost = víc "pixelově"
        title_text = title_font.render("BULÁNCI 010", False, WHITE)  # False = bez vyhlazování
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_text, title_rect)

        if current_time - start_time >= 3000:
            game_start = False
            game_menu = True

        pygame.display.flip()
        clock.tick(FPS)
        continue

    #**********************
    # GAME MENU SCREEN
    #**********************
    if game_menu:
        screen.blit(background_image, (0, 0))
        menu_font = pygame.font.Font("fonts/PressStart2P.ttf", 24)
        menu_items = ["Hrát", "Výběr mapy", "Konec hry"]
        menu_rects = []

        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if selected_index == 0: # Hrát
                        game_menu = False
                        player1.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
                        player2.rect.center = (SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT // 2)
                        for bullet in bullets:
                            bullet.kill()
                        bullets.empty()
                        _switch_map_assets(settings.CURRENT_MAP_SETTING_NAME)

                    elif selected_index == 1: # Výběr mapy
                        game_menu = False
                        maps_menu = True
                    elif selected_index == 2: # Konec hry
                        running = False
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(menu_items)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        for i, item in enumerate(menu_items):
            menu_text = menu_font.render(item, True, YELLOW if i == selected_index else WHITE)
            menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, 100 + i * 60))
            menu_rects.append(menu_rect)

            if menu_rect.collidepoint(mouse_pos):
                selected_index = i
                if mouse_clicked:
                    if i == 0: # Hrát
                        game_menu = False
                        player1.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
                        player2.rect.center = (SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT // 2)
                        for bullet in bullets:
                            bullet.kill()
                        bullets.empty()
                        _switch_map_assets(settings.CURRENT_MAP_SETTING_NAME)
                    elif i == 1: # Výběr mapy
                        game_menu = False
                        maps_menu = True
                    elif i == 2: # Konec hry
                        running = False

            screen.blit(menu_text, menu_rect)

        pygame.display.flip()
        clock.tick(FPS)
        continue

    #**********************
    #VÝBĚR MAPY SCREEN
    #**********************
    if maps_menu:
        screen.blit(background_image, (0, 0))

        map_font = pygame.font.Font("fonts/PressStart2P.ttf", 20)
        map_names = list(MAP_SETTINGS.keys()) + ["Back"]

        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    maps_menu = False
                    game_menu = True
                elif event.key == pygame.K_RETURN:
                    if map_names[selected_index] == "Back":
                        maps_menu = False
                        game_menu = True
                    else:
                        _switch_map_assets(map_names[selected_index])
                        maps_menu = False
                        game_menu = True
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(map_names)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(map_names)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
        
        # načtení obsahu menu map
        for index, name in enumerate(map_names):
            color = YELLOW if index == selected_index else WHITE
            map_text = map_font.render(name, True, color)
            map_rect = map_text.get_rect(center=(SCREEN_WIDTH // 2, 100 + index * 50))

            if map_rect.collidepoint(mouse_pos):
                selected_index = index
                if mouse_clicked:
                    if name == "Back":
                        maps_menu = False
                        game_menu = True
                    else:
                        _switch_map_assets(name)
                        maps_menu = False
                        game_menu = True

            screen.blit(map_text, map_rect)

        pygame.display.flip()
        clock.tick(FPS)
        continue

    # GAME ITSELF:
    else:

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
        player1.update(keys, current_time, stone_group)
        player2.update(keys, current_time, stone_group)
        bullets.update()

        pygame.sprite.groupcollide(bullets, stone_group, True, False)

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

    bush_group.draw(screen)

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


            player1.rect.center = no_collision(random_player1_start_position, obstacles)
            player2.rect.center = no_collision(random_player2_start_position, obstacles)

            for bullet in bullets:
                bullet.kill()
            bullets.empty()

            _switch_map_assets(settings.CURRENT_MAP_SETTING_NAME)


        if player1.animation_frames[player1.direction]:
            player1.current_frame_index = 0
            player1.image = player1.animation_frames[player1.direction][player1.current_frame_index]

        if player2.animation_frames[player2.direction]:
            player2.current_frame_index = 0
            player2.image = player2.animation_frames[player2.direction][player2.current_frame_index]

    pygame.display.flip()

    clock.tick(FPS)
pygame.quit()