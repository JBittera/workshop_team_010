import pygame

from screen import Screen
from settings import SCREEN_WIDTH, WHITE

SPLASH_SCREEN_DURATION = 3000

class SplashScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.start_time = pygame.time.get_ticks()
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def draw(self, surface):
        current_time = pygame.time.get_ticks()
        surface.blit(self.game.assets['background'], (0, 0))

        title_font = pygame.font.Font("fonts/PressStart2P.ttf", 45)  # menší velikost = víc "pixelově"
        title_text = title_font.render("BULÁNCI 010", False, WHITE)  # False = bez vyhlazování
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        surface.blit(title_text, title_rect)

        if current_time - self.start_time >= SPLASH_SCREEN_DURATION:
            self.game.change_screen("menu")
