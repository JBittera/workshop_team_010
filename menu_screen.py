import pygame
from screen import Screen
from settings import SCREEN_WIDTH, WHITE, YELLOW

class MenuScreen(Screen):
    def __init__(self, game, prev_screen=None):
        super().__init__(game)
        self.menu_items = []
        self.prev_screen = prev_screen
        self.menu_font = pygame.font.Font("fonts/PressStart2P.ttf", 24)
        self.reset()

    def reset(self):
        self.mouse_clicked = False
        self.selected_index = 0

    def handle_event(self, event):
        # FUNKCE menu pomocí kláves
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.prev_screen:
                    self.game.change_screen(self.prev_screen)
                    self.game.assets['click_sound'].play()
            elif event.key == pygame.K_RETURN:
                _, action = self.menu_items[self.selected_index]
                action()
                self.game.assets['click_sound'].play()
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.menu_items)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.mouse_clicked = True

    def draw(self, surface):
        surface.blit(self.game.assets['background'], (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        for i, (text, action) in enumerate(self.menu_items):
            menu_text = self.menu_font.render(text, True, YELLOW if i == self.selected_index else WHITE)
            menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, 100 + i * 60))

            if menu_rect.collidepoint(mouse_pos):
                self.selected_index = i
                if self.mouse_clicked:
                    self.game.assets['click_sound'].play()
                    action()

            surface.blit(menu_text, menu_rect)
        self.mouse_clicked = False
