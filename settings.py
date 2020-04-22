from os import path, listdir


import json
import pygame as pg

LIVES = 5
PROTEIN = 50
              
ZOOM_AMOUNT = 0.05

# define some colors (R, G, B)
WHITE = pg.Color(255, 255, 255)
BLACK = pg.Color(0, 0, 0)
DARKGREY = pg.Color(40, 40, 40)
LIGHTGREY = pg.Color(100, 100, 100)
GREEN = pg.Color(0, 255, 0)
DARK_GREEN = pg.Color(0, 60, 0)
RED = pg.Color(255, 0, 0)
DARK_RED = pg.Color(60, 0, 0)
YELLOW = pg.Color(255, 255, 0)
ORANGE = pg.Color(255, 127, 0)
MAROON = pg.Color(127, 0, 0)
HALF_WHITE = pg.Color(255, 255, 255, 127)
HALF_RED = pg.Color(255, 0, 0, 127)

# game settings
FPS = 60
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SPAWN_RATE = 1

# looks for img_folder and map_folder in the same folder as the code
GAME_FOLDER = path.dirname(path.abspath(__file__))
IMG_FOLDER = path.join(GAME_FOLDER, "img")
MAP_FOLDER = path.join(GAME_FOLDER, 'maps')
LEVELS_FOLDER = path.join(GAME_FOLDER, "levels")
FONTS_FOLDER = path.join(GAME_FOLDER, "fonts")
AUDIO_FOLDER = path.join(GAME_FOLDER, "audio")

PATH_IMG_FOLDER = path.join(IMG_FOLDER, "path")
UI_IMG_FOLDER = path.join(IMG_FOLDER, "ui")
ENEMIES_IMG_FOLDER = path.join(IMG_FOLDER, "enemies")
TOWERS_IMG_FOLDER = path.join(IMG_FOLDER, "towers")
GAME_OVER_IMG_FOLDER = path.join(IMG_FOLDER, "game_over")

ENEMIES_AUD_FOLDER = path.join(AUDIO_FOLDER, "enemies")
TOWERS_AUD_FOLDER = path.join(AUDIO_FOLDER, "towers")
GAME_OVER_AUD_FOLDER = path.join(AUDIO_FOLDER, "game_over")

MENU_OFFSET = 10
MENU_TEXT_SIZE = 25

# load ui images
HEART_IMG = pg.image.load(path.join(UI_IMG_FOLDER, "heart.png"))
PROTEIN_IMG = pg.image.load(path.join(UI_IMG_FOLDER, "protein.png"))
LEFT_ARROW_IMG = pg.image.load(path.join(UI_IMG_FOLDER, "left.png"))
RIGHT_ARROW_IMG = pg.transform.rotate(pg.image.load(path.join(UI_IMG_FOLDER, "left.png")).copy(), 180)

 # Initializing the mixer in the settings file lol but rn i don't see a better way.
# Audio
AUDIO_HEART_BEEP_PATH = path.join(GAME_OVER_AUD_FOLDER, "heart_beep.wav")
AUDIO_FLATLINE_PATH = path.join(GAME_OVER_AUD_FOLDER, "flatline.wav")

LEVEL_DATA = []
for file in listdir(LEVELS_FOLDER):
    with open(path.join(LEVELS_FOLDER, file)) as data_file:
        level = json.load(data_file)
        enemies = []
        for wave in level["waves"]:
            for enemy in wave["enemy_type"]:
                if enemy not in enemies:
                    enemies.append(enemy)
        level["enemies"] = enemies
        LEVEL_DATA.append(level)

# load enemy data
with open(path.join(GAME_FOLDER, "enemies.json"), "r") as data_file:
    ENEMY_DATA = json.load(data_file)
    for enemy in ENEMY_DATA:
        ENEMY_DATA[enemy]["image"] = pg.image.load(path.join(ENEMIES_IMG_FOLDER, "{}.png".format(enemy)))
        ENEMY_DATA[enemy]["death_sound_path"] = path.join(ENEMIES_AUD_FOLDER, "{}.wav".format(enemy))

# load tower data
with open(path.join(GAME_FOLDER, "towers.json"), "r") as data_file:
    TOWER_DATA = json.load(data_file)
    for tower in TOWER_DATA:
        for level in range(3):
            TOWER_DATA[tower][level]["gun_image"] = pg.image.load(path.join(TOWERS_IMG_FOLDER, tower + "_gun" + str(level) + ".png"))
            TOWER_DATA[tower][level]["base_image"] = pg.image.load(path.join(TOWERS_IMG_FOLDER, tower + "_base" + str(level) + ".png"))
            TOWER_DATA[tower][level]["bullet_image"] = pg.image.load(path.join(TOWERS_IMG_FOLDER, tower + "_bullet" + str(level) + ".png"))
            TOWER_DATA[tower][level]["shoot_sound_path"] = path.join(TOWERS_AUD_FOLDER, "{}.wav".format(tower))

# load path images
PATH_VERTICAL_IMG = pg.image.load(path.join(PATH_IMG_FOLDER, "vertical.png"))
PATH_HORIZONTAL_IMG = pg.image.load(path.join(PATH_IMG_FOLDER, "horizontal.png"))
PATH_CORNER1_IMG = pg.image.load(path.join(PATH_IMG_FOLDER, "corner1.png"))
PATH_CORNER2_IMG = pg.image.load(path.join(PATH_IMG_FOLDER, "corner2.png"))
PATH_CORNER3_IMG = pg.image.load(path.join(PATH_IMG_FOLDER, "corner3.png"))
PATH_CORNER4_IMG = pg.image.load(path.join(PATH_IMG_FOLDER, "corner4.png"))

# load other images
START_SCREEN_IMG = pg.image.load(path.join(IMG_FOLDER, "start_screen.png"))
LEVEL_BUTTON_IMG = pg.image.load(path.join(IMG_FOLDER, "level_button.png"))

# load game over images
RESTART_BTN_IMGS = [[None, None], [None, None]]
BACK_BTN_IMGS = [[None, None], [None, None]]

for i, to_concat_1 in enumerate(["", "_lost"]):
    for j, to_concat_2 in enumerate(["", "_hover"]):
        RESTART_BTN_IMGS[i][j] = pg.image.load(path.join(GAME_OVER_IMG_FOLDER, "restart_btn{}{}.png".format(to_concat_1, to_concat_2)))
        BACK_BTN_IMGS[i][j] = pg.image.load(path.join(GAME_OVER_IMG_FOLDER, "back_btn{}{}.png".format(to_concat_1, to_concat_2)))
        
HEART_MONITOR_NORMAL_IMG = pg.image.load(path.join(GAME_OVER_IMG_FOLDER, "heart_monitor_normal.png"))
HEART_MONITOR_FLATLINE_IMG = pg.image.load(path.join(GAME_OVER_IMG_FOLDER, "heart_monitor_flatline.png"))

# load fonts path
GAME_OVER_FONT = path.join(FONTS_FOLDER, "mini_pixel-7.ttf")
