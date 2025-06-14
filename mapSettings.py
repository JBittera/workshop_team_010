from settings import (SCREEN_WIDTH, SCREEN_HEIGHT)

MAP_SETTINGS = {
    "map_university": {
        "background_image_path": "images/maps/map_1/map/background.png",
        "stone_positions": [
            (200, 200, "small"),
            (500, 400, "big"),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, "small")
        ],
        "bush_positions": [
            (100, 300),
            (400, 50),
        ]
    },
    "map_forest": {
        "background_image_path": "images/maps/map_2/map/background.png", # Example for a different background
        "stone_positions": [
            (100, 100, "big"),
            (700, 150, "small"),
            (300, 500, "big"),
            (600, 100, "small")
        ],
        "bush_positions": [
            (100, 300),
            (400, 300),
        ]
    },
    # Add more map settings here as needed
    "map_city": {
        "background_image_path": "images/city_background.png",
        "stone_positions": [
            (150, 300, "small"),
            (400, 100, "big"),
            (650, 500, "small"),
            (250, 550, "big")
        ],
        "bush_positions": [
            (100, 300),
            (400, 300),
        ]
    }
}
