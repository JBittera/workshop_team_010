from menu_screen import MenuScreen

class MainMenuScreen(MenuScreen):

    def __init__(self, game):
        super().__init__(game)
        self.menu_items = [
            ("Hrát", lambda: self.game.change_screen("game")),
            ("Výběr mapy", lambda: self.game.change_screen("map_menu")),
            ("Konec hry", lambda: self.game.exit()),
        ]
