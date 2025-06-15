import pygame

from mapSettings import MAP_SETTINGS
from splash_screen import SplashScreen
from main_menu_screen import MainMenuScreen
from map_menu_screen import MapMenuScreen
from game_screen import GameScreen
from pause_menu_screen import PauseMenuScreen
from settings import FPS, GAME_ICON_PATH, INITIAL_MAP_SETTING_NAME, SCREEN_HEIGHT, SCREEN_WIDTH
from utils import load_image

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Top-Down Shooter (2 Players)")
        game_icon = load_image(GAME_ICON_PATH)
        if game_icon:
            pygame.display.set_icon(game_icon)
        pygame.mixer.music.load("music/main_menu.ogg")
        self.change_map(INITIAL_MAP_SETTING_NAME)

        self.running = True
        self.clock = pygame.time.Clock()

        self.screens = {
            "splash": SplashScreen(self),
            "menu": MainMenuScreen(self),
            "map_menu": MapMenuScreen(self),
            "game": GameScreen(self),
            "pause": PauseMenuScreen(self),
        }
        self.change_screen("splash")

    def change_screen(self, name, reset=True):
        self.current_screen = self.screens[name]
        if reset:
            self.current_screen.reset()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.current_screen.handle_event(event)

            self.current_screen.update()
            self.current_screen.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

    def exit(self):
        self.running = False

    def change_map(self, map_name):
        self.map_name = map_name
        self.chosen_map = MAP_SETTINGS[self.map_name]

        click_sound = pygame.mixer.Sound("music/click.mp3")
        click_sound.set_volume(0.5)

        self.assets = {
            'background': load_image(self.chosen_map["background_image_path"], (SCREEN_WIDTH, SCREEN_HEIGHT)),
            "click_sound": click_sound,
        }
