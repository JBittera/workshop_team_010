from mapSettings import MAP_SETTINGS
from menu_screen import MenuScreen


class MapMenuScreen(MenuScreen):

    def __init__(self, game):
        super().__init__(game, prev_screen='menu')

        def get_action(map_name):
            def action():
                self.game.change_map(map_name)
                self.game.change_screen("menu")

            return action

        self.menu_items = [
            *((map_name, get_action(map_name)) for map_name in MAP_SETTINGS.keys()),
            ("Back", lambda: self.game.change_screen('menu')),
        ]
