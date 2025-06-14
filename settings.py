SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BUSH_SIZE = (140, 140)
BOX_SIZE = (70, 70)
GRAY = (100, 100, 100)
FPS = 60

PLAYER_SIZE = (40, 40)
BULLET_SIZE = (10, 10)

BULLET_IMAGE_PATH = "images/bullet.png"
GAME_ICON_PATH = "images/ico_game.png"

STONE_SIZE = (60, 60)
STONE_SIZE_SMALL = (50, 50)
STONE_SIZE_BIG = (100, 100)

PLAYER_FRAME_WIDTH = 59
PLAYER_FRAME_HEIGHT = 82

PLAYER1_SPRITESHEET_PATH = "images/player_sprites/player1_spritesheet.png"
PLAYER2_SPRITESHEET_PATH = "images/player_sprites/player2_spritesheet.png"

player_animation_data = {
    'player1': {
        'row': 0,
        'left_start_frame': 3,
        'right_start_frame': 9,
        'num_frames': 3
    },
    'player2': {
        'row': 0,
        'left_start_frame': 3,
        'right_start_frame': 9,
        'num_frames': 3
    }
}

BORDER_PADDING = 40

PLAYER_SPEED = 4
PLAYER_HEALTH = 100
PLAYER_SHOOT_COOLDOWN = 200
PLAYER_INITIAL_BULLETS_COUNT = 10
BOX_BULLETS_COUNT = 5
BOX_SPAWN_DELAY = 3000

BULLET_SPEED = 10

CURRENT_MAP_SETTING_NAME = "University"
