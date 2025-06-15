from menu_screen import MenuScreen

class PauseMenuScreen(MenuScreen):

    def __init__(self, game):
        super().__init__(game)
        self.menu_items = [
            ("Resume", lambda: self.game.change_screen("game", reset=False)),
            ("Quit the game", lambda: self.game.change_screen("menu")),
        ]
