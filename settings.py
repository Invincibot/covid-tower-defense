from os import path

import json
import pygame as pg

LIVES = 5
PROTEIN = 40
BUY_COST = 10 # should be kept outside of the class so that the buy_cost can be
              # checked against the protein without needing to instantiate the tower
MAX_STAGE = 2
              
ZOOM_AMOUNT = 0.05

# define some colors (R, G, B)
WHITE = pg.Color(255, 255, 255)
BLACK = pg.Color(0, 0, 0)
DARKGREY = pg.Color(40, 40, 40)
LIGHTGREY = pg.Color(100, 100, 100)
GREEN = pg.Color(0, 255, 0)
RED = pg.Color(255, 0, 0)
YELLOW = pg.Color(255, 255, 0)
HALF_WHITE = pg.Color(255, 255, 255, 127)
HALF_RED = pg.Color(255, 0, 0, 127)

# game settings
FPS = 10
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SPAWN_RATE = 1

# looks for img_folder and map_folder in the same folder as the code
GAME_FOLDER = path.dirname(path.abspath(__file__))
IMG_FOLDER = path.join(GAME_FOLDER, "img")
MAP_FOLDER = path.join(GAME_FOLDER, 'maps')
LEVELS_FOLDER = path.join(GAME_FOLDER, "levels")

HEART_IMG = pg.image.load(path.join(IMG_FOLDER, "heart.png"))
PROTEIN_IMG = pg.image.load(path.join(IMG_FOLDER, "protein.png"))
LEFT_ARROW_IMG = pg.image.load(path.join(IMG_FOLDER, "left.png"))
RIGHT_ARROW_IMG = pg.transform.rotate(pg.image.load(path.join(IMG_FOLDER, "left.png")).copy(), 180)

SAMPLE_LEVEL_DATA = path.join(LEVELS_FOLDER, "sample.json")

with open(path.join(GAME_FOLDER, "enemies.json"), "r") as data_file:
    ENEMY_DATA = json.load(data_file)
    for enemy in ENEMY_DATA:
        ENEMY_DATA[enemy]["image"] = pg.image.load(path.join(IMG_FOLDER, ENEMY_DATA[enemy]["image"]))

LEVEL_BUTTON_IMG = pg.image.load(path.join(IMG_FOLDER, "level_button.png"))
ANTIBODY_GUN_IMGS = []
ANTIBODY_BASE_IMGS = []
for i in range(MAX_STAGE + 1):
    ANTIBODY_GUN_IMGS.append(pg.image.load(path.join(IMG_FOLDER, "naive_t_cell_gun{}.png".format(i))))
    ANTIBODY_BASE_IMGS.append(pg.image.load(path.join(IMG_FOLDER, "naive_t_cell_base{}.png".format(i))))

PATH_VERTICAL_IMG = pg.image.load(path.join(IMG_FOLDER, "path/vertical.png"))
PATH_HORIZONTAL_IMG = pg.image.load(path.join(IMG_FOLDER, "path/horizontal.png"))
PATH_CORNER1_IMG = pg.image.load(path.join(IMG_FOLDER, "path/corner1.png"))
PATH_CORNER2_IMG = pg.image.load(path.join(IMG_FOLDER, "path/corner2.png"))
PATH_CORNER3_IMG = pg.image.load(path.join(IMG_FOLDER, "path/corner3.png"))
PATH_CORNER4_IMG = pg.image.load(path.join(IMG_FOLDER, "path/corner4.png"))

START_SCREEN_IMG = pg.image.load(path.join(IMG_FOLDER, "start_screen.png"))
