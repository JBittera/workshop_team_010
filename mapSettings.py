from settings import (SCREEN_WIDTH, SCREEN_HEIGHT)

MAP_SETTINGS = {
    "map_desert": {
        "background_image_path": "images/background.png",
        "stone_positions": [
            (200, 200),
            (500, 400),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        ]
    },
    "map_forest": {
        "background_image_path": "images/forest_background.png", # Example for a different background
        "stone_positions": [
            (100, 100),
            (700, 150),
            (300, 500),
            (600, 100)
        ]
    },
    # Add more map settings here as needed
    "map_city": {
        "background_image_path": "images/city_background.png",
        "stone_positions": [
            (150, 300),
            (400, 100),
            (650, 500),
            (250, 550)
        ]
    }
}