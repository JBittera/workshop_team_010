from menu_screen import MenuScreen
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, YELLOW
class MainMenuScreen(MenuScreen):

    def __init__(self, game):
        super().__init__(game)
        self.menu_items = [
            ("Hrát", lambda: self.game.change_screen("game")),
            ("Výběr mapy", lambda: self.game.change_screen("map_menu")),
            ("Konec hry", lambda: self.game.exit()),
        ]
        self.player1_controls_text = "Player 1: WASD - Move, E - Shoot"
        self.player2_controls_text = "Player 2: Arrows - Move, Shift - Shoot"
        self.controls_font = pygame.font.Font("fonts/PressStart2P.ttf", 18)

    def draw(self, surface):
        super().draw(surface)

        player1_controls_render = self.controls_font.render(self.player1_controls_text, True, WHITE)
        player2_controls_render = self.controls_font.render(self.player2_controls_text, True, WHITE)

        player1_controls_rect = player1_controls_render.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        player2_controls_rect = player2_controls_render.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))

        surface.blit(player1_controls_render, player1_controls_rect)
        surface.blit(player2_controls_render, player2_controls_rect)
