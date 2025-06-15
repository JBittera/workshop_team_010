import pygame
from box import Box
from bush import Bush
from player import Player
from screen import Screen
from settings import BOX_BULLETS_COUNT, BOX_SIZE, BOX_SPAWN_DELAY, BULLET_SIZE, BUSH_SIZE, PLAYER_FRAME_HEIGHT, PLAYER_FRAME_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, SPRITESHEET_PATH, STONE_SIZE_BIG, STONE_SIZE_SMALL, WHITE, YELLOW, player_animation_data
from stone import Stone
from utils import load_frames_from_spritesheet, load_image, no_collision, random_player1_start_position, random_player2_start_position

NEW_BOX_EVENT = pygame.USEREVENT + 1

player1_controls = {
    'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d, 'shoot': pygame.K_e
}

player2_controls = {
    'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'shoot': pygame.K_RSHIFT
}

class GameScreen(Screen):
    def __init__(self, game):
        super().__init__(game)

        player_hit_sound = pygame.mixer.Sound("music/hitted.mp3")
        player_hit_sound.set_volume(0.8)
        reload_sound = pygame.mixer.Sound("music/reload.mp3")
        reload_sound.set_volume(0.6)
        victory_sound = pygame.mixer.Sound("music/victory.mp3")
        victory_sound.set_volume(0.6)

        self.assets = {
            "player_hit_sound": player_hit_sound,
            "reload_sound": reload_sound,
            "victory_sound": victory_sound
        }

        self.assets.update({
            f'{player}_animation_frames': {
                direction: load_frames_from_spritesheet(
                    SPRITESHEET_PATH[player],
                    PLAYER_FRAME_WIDTH,
                    PLAYER_FRAME_HEIGHT,
                    player_animation_data[player]['row'],
                    player_animation_data[player][f'{direction}_start_frame'],
                    player_animation_data[player]['num_frames']
                ) for direction in ['down', 'left', 'up', 'right']
            } for player in ['player1', 'player2']
        })

        self.player1 = Player(0, 0, player1_controls, "Player 1", self.assets['player1_animation_frames'])
        self.player2 = Player(0, 0, player2_controls, "Player 2", self.assets['player2_animation_frames'])


        self.all_sprites = pygame.sprite.Group()
        self.stone_group = pygame.sprite.Group()
        self.bush_group = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.font = pygame.font.Font(None, 36)

        self.map_name = None
        self.reset()

    def reset(self):
        self.game_over = False
        self.winner_text = ""

        if self.map_name != self.game.map_name:
            self.map_name = self.game.map_name
            self.switch_map_assets()

        self.player1.health = 100
        self.player2.health = 100
        self.player1.rect.center = no_collision(random_player1_start_position, self.objects)
        self.player2.rect.center = no_collision(random_player2_start_position, self.objects)

        for bullet in self.bullets:
            bullet.kill()
        self.bullets.empty()

        if self.player1.animation_frames[self.player1.direction]:
            self.player1.current_frame_index = 0
            self.player1.direction = 'down'
            self.player1.image = self.player1.animation_frames[self.player1.direction][self.player1.current_frame_index]

        if self.player2.animation_frames[self.player2.direction]:
            self.player2.current_frame_index = 0
            self.player2.direction = 'down'
            self.player2.image = self.player2.animation_frames[self.player2.direction][self.player2.current_frame_index]


        self.box = Box(self.assets['box'], self.all_sprites)

        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.assets['map_music'])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def switch_map_assets(self):
        chosen_map = self.game.chosen_map

        bullet_image = load_image(chosen_map["bullet_image_path"], BULLET_SIZE)
        shoot_sound = pygame.mixer.Sound(chosen_map["shoot_sound_path"])
        shoot_sound.set_volume(0.5)
        rock_hit_sound = pygame.mixer.Sound(chosen_map["rock_hit_sound_path"])
        rock_hit_sound.set_volume(0.5)

        self.assets.update({
            'bullet': {
                'up': pygame.transform.rotate(bullet_image, 90),
                'down': pygame.transform.rotate(bullet_image, -90),
                'left': pygame.transform.rotate(bullet_image, 180),
                'right': bullet_image,
            },
            'box': load_image(chosen_map["box_image_path"], BOX_SIZE),
            'map_music': chosen_map["map_music_path"],
            'shoot_sound': shoot_sound,
            'rock_hit_sound': rock_hit_sound,
        })

        stone_small_image = load_image(chosen_map["small_stone_image_path"], STONE_SIZE_SMALL)
        stone_big_image = load_image(chosen_map["big_stone_image_path"], STONE_SIZE_BIG)
        bush_image = load_image(chosen_map["bush_image_path"], BUSH_SIZE)

        self.stone_group.empty()
        self.bush_group.empty()

        for pos_x, pos_y, stone_type in chosen_map["stone_positions"]:
            if stone_type == "small":
                self.stone_group.add(Stone(pos_x, pos_y, stone_small_image))
            elif stone_type == "big":
                self.stone_group.add(Stone(pos_x, pos_y, stone_big_image))

        for pos_x, pos_y in chosen_map["bush_positions"]:
            self.bush_group.add(Bush(pos_x, pos_y, bush_image))

        self.obstacles.empty()
        self.obstacles.add(self.stone_group)

        self.objects.empty()
        self.objects.add(self.stone_group, self.bush_group)

        self.all_sprites.empty()
        self.all_sprites.add(self.player1, self.player2, self.stone_group, self.bush_group)

    def handle_event(self, event):
        current_time = pygame.time.get_ticks()
        if event.type == pygame.KEYDOWN:
            if not self.game_over:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_screen("pause", reset=False)
                else:
                    if event.key == player1_controls['shoot']:
                        bullet = self.player1.shoot(current_time, self.assets['bullet'])
                        if bullet:
                            self.assets['shoot_sound'].play()
                            self.all_sprites.add(bullet)
                            self.bullets.add(bullet)
                    if event.key == player2_controls['shoot']:
                        bullet = self.player2.shoot(current_time, self.assets['bullet'])
                        if bullet:
                            self.assets['shoot_sound'].play()
                            self.all_sprites.add(bullet)
                            self.bullets.add(bullet)
        elif event.type == NEW_BOX_EVENT:
            self.box = Box(self.assets['box'], self.all_sprites)

    def update(self):
        if self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.reset()
            return

        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        self.player1.update(keys, current_time, self.obstacles)
        self.player2.update(keys, current_time, self.obstacles)
        self.bullets.update()

        pygame.sprite.groupcollide(self.bullets, self.stone_group, True, False)


        if self.box:
            if pygame.sprite.collide_rect(self.player1, self.box):
                self.assets['reload_sound'].play()
                self.player1.bullets_count += BOX_BULLETS_COUNT
                self.box.kill()
                self.box = None
            elif pygame.sprite.collide_rect(self.player2, self.box):
                self.assets['reload_sound'].play()
                self.player2.bullets_count += BOX_BULLETS_COUNT
                self.box.kill()
                self.box = None
            if not self.box:
                pygame.time.set_timer(NEW_BOX_EVENT, BOX_SPAWN_DELAY, 1)

        hits_player1 = pygame.sprite.spritecollide(self.player1, self.bullets, True)
        for hit in hits_player1:
            self.player1.health -= 10
            self.assets['rock_hit_sound'].play()
            if self.player1.health <= 0:
                self.assets['victory_sound'].play()
                self.assets['player_hit_sound'].play()
                self.player1.health = 0
                self.game_over = True
                self.winner_text = "Player 2 Wins!"

        hits_player2 = pygame.sprite.spritecollide(self.player2, self.bullets, True)
        for hit in hits_player2:
            self.player2.health -= 10
            self.assets['rock_hit_sound'].play()
            if self.player2.health <= 0:
                self.assets['victory_sound'].play()
                self.assets['player_hit_sound'].play()
                self.player2.health = 0
                self.game_over = True
                self.winner_text = "Player 1 Wins!"


    def draw(self, surface):

        surface.blit(self.game.assets['background'], (0, 0))

        self.player1.draw_health_bar(surface)
        self.player2.draw_health_bar(surface)

        self.all_sprites.draw(surface)

        if self.box: self.box.draw(surface)


        player1_text = self.font.render(f"{self.player1.name}: {self.player1.bullets_count}", True, WHITE)
        surface.blit(player1_text, (10, 10))
        player2_text = self.font.render(f"{self.player2.name}: {self.player2.bullets_count}", True, WHITE)
        surface.blit(player2_text, (SCREEN_WIDTH - player2_text.get_width() - 10, 10))

        if self.game_over:
            game_over_font = pygame.font.Font(None, 74)
            winner_display = game_over_font.render(self.winner_text, True, YELLOW)
            winner_rect = winner_display.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            surface.blit(winner_display, winner_rect)

            restart_font = pygame.font.Font(None, 48)
            restart_text = restart_font.render("Press R to Restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            surface.blit(restart_text, restart_rect)

            if self.player1.animation_frames[self.player1.direction]:
                self.player1.current_frame_index = 0
                self.player1.image = self.player1.animation_frames[self.player1.direction][self.player1.current_frame_index]

            if self.player2.animation_frames[self.player2.direction]:
                self.player2.current_frame_index = 0
                self.player2.image = self.player2.animation_frames[self.player2.direction][self.player2.current_frame_index]
