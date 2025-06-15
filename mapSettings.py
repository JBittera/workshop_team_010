from settings import (SCREEN_WIDTH, SCREEN_HEIGHT)

MAP_SETTINGS = {
    "University": {
        "background_image_path": "images/maps/map_1/map/background.png",
        "stone_positions": [
            (200, 200, "small"),
            (550, 400, "big"),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, "small")
        ],
        "bush_positions": [
            (100, 300),
            (400, 50),
        ],
        "small_stone_image_path": "images/maps/map_1/objects/small_rock.png",
        "big_stone_image_path": "images/maps/map_1/objects/big_rock.png",
        "bush_image_path": "images/maps/map_1/objects/bush.png",
        "box_image_path": "images/maps/map_1/objects/box.png",
        "bullet_image_path": "images/maps/map_1/bullet/bullet.png",
        "map_music_path": "images/maps/map_1/music/University.mp3",
        "shoot_sound_path": "images/maps/map_1/music/shoot_map1.mp3",
        "rock_hit_sound_path": "images/maps/map_1/music/rockshoot_map1.mp3",
        "map_tiles_path": "images/maps/map_1/objects/map_tiles.png"
    },
    "Deadwood": {
        "background_image_path": "images/maps/map_2/map/background.png",
        "stone_positions": [
            (100, 100, "big"),
            (700, 150, "small"),
            (300, 500, "big"),
            (600, 100, "small")
        ],
        "bush_positions": [
            (100, 300),
            (400, 300),
        ],
        "small_stone_image_path": "images/maps/map_2/objects/small_rock.png",
        "big_stone_image_path": "images/maps/map_2/objects/big_rock.png",
        "bush_image_path": "images/maps/map_2/objects/bush.png",
        "box_image_path": "images/maps/map_2/objects/box.png",
        "bullet_image_path": "images/maps/map_2/bullet/bullet.png",
        "map_music_path": "images/maps/map_2/music/Deadwood.mp3",
        "shoot_sound_path": "images/maps/map_2/music/shoot_map2.mp3",
        "rock_hit_sound_path": "images/maps/map_2/music/rockshoot_map2.mp3",
        "map_tiles_path": "images/maps/map_2/objects/map_tiles.png"
    },
    "Cyberpark": {
        "background_image_path": "images/maps/map_3/map/background.png",
        "stone_positions": [
            (150, 300, "small"),
            (400, 100, "big"),
            (650, 500, "small"),
            (250, 550, "big")
        ],
        "bush_positions": [
            (100, 300),
            (400, 300),
        ],
        "small_stone_image_path": "images/maps/map_3/objects/small_rock.png",
        "big_stone_image_path": "images/maps/map_3/objects/big_rock.png",
        "bush_image_path": "images/maps/map_3/objects/bush.png",
        "box_image_path": "images/maps/map_3/objects/box.png",
        "bullet_image_path": "images/maps/map_3/bullet/bullet.png",
        "map_music_path": "images/maps/map_3/music/Cyberpark.mp3",
        "shoot_sound_path": "images/maps/map_3/music/shoot_map3.mp3",
        "rock_hit_sound_path": "images/maps/map_3/music/rockshoot_map3.mp3",
        "map_tiles_path": "images/maps/map_3/objects/map_tiles.png"
    }
}
