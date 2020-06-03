import textwrap

from data.display import *
from data.tilemap import Camera, TiledMap
from data.settings import *
from data.dev_tools import TowerEditMenu, EnemyEditMenu

class StartMenu(Display):        
    def draw(self):
        self.fill(BLACK)
        self.blit(START_SCREEN_IMG, ((SCREEN_WIDTH - START_SCREEN_IMG.get_width()) / 2, 0))
        
        return self
    
    def event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                return "menu"
                
        return -1
    
class Menu(Display):
    def __init__(self):
        super().__init__()
        self.camera = Camera(SCREEN_WIDTH * 0.8, SCREEN_HEIGHT * 0.8, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        self.base_zoom = self.camera.get_zoom()
        self.zoom_step = -1
        self.body_images = []
        self.body_image = self.camera.apply_image(BODY_IMG)
        
        self.body_coords = (-250, 150)
        
        self.level_button_rect = LEVEL_BUTTON_IMG.get_rect()
        self.level_button_rect_2 = LEVEL_BUTTON_IMG_2.get_rect()
        self.level_buttons = []
        self.init_levels()

        self.tower_preview_button = pg.Rect((800, 200), self.level_button_rect.size)
        self.enemy_preview_button = pg.Rect((800, 600), self.level_button_rect.size)
        self.upgrades_menu_button = pg.Rect((800, 1000), self.level_button_rect.size)
        self.tower_edit_button = pg.Rect((1200, 200), self.level_button_rect.size)
        self.enemy_edit_button = pg.Rect((1200, 600), self.level_button_rect.size)
        self.level_edit_button = pg.Rect((1200, 1000), self.level_button_rect.size)
        self.options_button = pg.Rect((850, -100), OPTIONS_IMGS[0].get_size())
        
        self.init_body_1()

        self.over_level = -1
        
    def init_levels(self):
        for i, level in enumerate(LEVEL_DATA):
            temp_coords = BODY_PARTS[list(BODY_PARTS)[level["body_part"]]]
            true_coords = (temp_coords[0] + self.body_coords[0] - self.level_button_rect_2.w // 2,
                           temp_coords[1] + self.body_coords[1] - self.level_button_rect_2.h // 2)
            self.level_buttons.append(pg.Rect(true_coords, self.level_button_rect_2.size))
        
    def init_body_1(self): #inits half the body_images on game startup
        for i in range(5):
            self.camera.zoom(ZOOM_AMT_MENU)
            self.body_images.append(self.camera.apply_image(BODY_IMG))
        
    def new(self, args): #inits the other half
        self.level_infos = [None for i in range(len(LEVEL_DATA))]
        if len(self.body_images) < 6: # so this will only run when first switching to menu
            while self.camera.zoom(ZOOM_AMT_MENU) != False:
                self.body_images.append(self.camera.apply_image(BODY_IMG))
            self.camera.zoom(self.base_zoom - self.camera.get_zoom())

    def update(self):
        self.update_level()

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.camera.move(25, 0)

        elif keys[pg.K_RIGHT]:
            self.camera.move(-25, 0)

        elif keys[pg.K_UP]:
            self.camera.move(0, 25)

        elif keys[pg.K_DOWN]:
            self.camera.move(0, -25)

    def draw(self):
        self.fill((0, 0, 0))
        
        self.blit(self.body_image, self.camera.apply_tuple(self.body_coords))

        big_font = pg.font.Font(FONT, LEVEL_BUTTON_IMG.get_rect().w * 4)
        lives_font = pg.font.Font(FONT, LEVEL_BUTTON_IMG.get_rect().w)
        level_text = big_font.render("Levels", 1, WHITE)
        self.blit(self.camera.apply_image(level_text), self.camera.apply_tuple((START_SCREEN_IMG.get_rect().w / 2 - level_text.get_rect().center[0], -50 - level_text.get_rect().center[1])))
        
        hover_options = self.options_button.collidepoint(self.camera.correct_mouse(pg.mouse.get_pos()))
        self.blit(self.camera.apply_image(OPTIONS_IMGS[hover_options]), self.camera.apply_rect(self.options_button))

        for i, button in enumerate(self.level_buttons):
            if len(SAVE_DATA["levels"]) - 1 >= i:
                self.blit(self.camera.apply_image(LEVEL_BUTTON_IMG_2), self.camera.apply_rect(button))
                #lives_text = lives_font.render(str(i + 1), 1, WHITE)
                #self.blit(self.camera.apply_image(lives_text), self.camera.apply_rect(lives_text.get_rect(center=button.center)))
            else:
                grey_image = LEVEL_BUTTON_IMG_2.copy()
                grey_image.fill(DARK_GREY, special_flags=pg.BLEND_RGB_MIN)
                self.blit(self.camera.apply_image(grey_image), self.camera.apply_rect(button))
                #self.blit(self.camera.apply_image(LOCK_IMG), self.camera.apply_rect(LOCK_IMG.get_rect(center=button.center)))

        self.blit(self.camera.apply_image(LEVEL_BUTTON_IMG), self.camera.apply_rect(self.tower_preview_button))
        lives_text = lives_font.render("Tower", 1, WHITE)
        self.blit(self.camera.apply_image(lives_text), self.camera.apply_tuple(
            (self.tower_preview_button.center[0] - lives_text.get_rect().center[0],
             self.tower_preview_button.center[1] - lives_text.get_rect().center[
                 1] - lives_text.get_rect().height + MENU_OFFSET)))
        lives_text = lives_font.render("Preview", 1, WHITE)
        self.blit(self.camera.apply_image(lives_text), self.camera.apply_tuple(
            (self.tower_preview_button.center[0] - lives_text.get_rect().center[0],
             self.tower_preview_button.center[1] - lives_text.get_rect().center[
                 1] + lives_text.get_rect().height - MENU_OFFSET)))

        self.blit(self.camera.apply_image(LEVEL_BUTTON_IMG), self.camera.apply_rect(self.enemy_preview_button))
        lives_text = lives_font.render("Enemy", 1, WHITE)
        self.blit(self.camera.apply_image(lives_text), self.camera.apply_tuple(
            (self.enemy_preview_button.center[0] - lives_text.get_rect().center[0],
             self.enemy_preview_button.center[1] - lives_text.get_rect().center[
                 1] - lives_text.get_rect().height + MENU_OFFSET)))
        lives_text = lives_font.render("Preview", 1, WHITE)
        self.blit(self.camera.apply_image(lives_text), self.camera.apply_tuple(
            (self.enemy_preview_button.center[0] - lives_text.get_rect().center[0],
             self.enemy_preview_button.center[1] - lives_text.get_rect().center[
                 1] + lives_text.get_rect().height - MENU_OFFSET)))

        self.blit(self.camera.apply_image(LEVEL_BUTTON_IMG), self.camera.apply_rect(self.upgrades_menu_button))
        lives_text = lives_font.render("Upgrades", 1, WHITE)
        self.blit(self.camera.apply_image(lives_text), self.camera.apply_tuple(
            (self.upgrades_menu_button.center[0] - lives_text.get_rect().center[0],
             self.upgrades_menu_button.center[1] - lives_text.get_rect().center[
                 1] - lives_text.get_rect().height + MENU_OFFSET)))
        lives_text = lives_font.render("Menu", 1, WHITE)
        self.blit(self.camera.apply_image(lives_text), self.camera.apply_tuple(
            (self.upgrades_menu_button.center[0] - lives_text.get_rect().center[0],
             self.upgrades_menu_button.center[1] - lives_text.get_rect().center[
                 1] + lives_text.get_rect().height - MENU_OFFSET)))

        self.blit(self.camera.apply_image(LEVEL_BUTTON_IMG), self.camera.apply_rect(self.tower_edit_button))
        lives_text = lives_font.render("Tower", 1, WHITE)
        self.blit(self.camera.apply_image(lives_text), self.camera.apply_tuple(
            (self.tower_edit_button.center[0] - lives_text.get_rect().center[0], self.tower_edit_button.center[1] - lives_text.get_rect().center[1] - lives_text.get_rect().height + MENU_OFFSET)))
        lives_text = lives_font.render("Edit", 1, WHITE)
        self.blit(self.camera.apply_image(lives_text), self.camera.apply_tuple(
            (self.tower_edit_button.center[0] - lives_text.get_rect().center[0], self.tower_edit_button.center[1] - lives_text.get_rect().center[1] + lives_text.get_rect().height - MENU_OFFSET)))

        self.blit(self.camera.apply_image(LEVEL_BUTTON_IMG), self.camera.apply_rect(self.enemy_edit_button))
        lives_text = lives_font.render("Enemy", 1, WHITE)
        self.blit(self.camera.apply_image(lives_text), self.camera.apply_tuple(
            (self.enemy_edit_button.center[0] - lives_text.get_rect().center[0],
             self.enemy_edit_button.center[1] - lives_text.get_rect().center[
                 1] - lives_text.get_rect().height + MENU_OFFSET)))
        lives_text = lives_font.render("Edit", 1, WHITE)
        self.blit(self.camera.apply_image(lives_text), self.camera.apply_tuple(
            (self.enemy_edit_button.center[0] - lives_text.get_rect().center[0],
             self.enemy_edit_button.center[1] - lives_text.get_rect().center[
                 1] + lives_text.get_rect().height - MENU_OFFSET)))

        self.blit(self.camera.apply_image(LEVEL_BUTTON_IMG), self.camera.apply_rect(self.level_edit_button))
        lives_text = lives_font.render("Level", 1, WHITE)
        self.blit(self.camera.apply_image(lives_text), self.camera.apply_tuple(
            (self.level_edit_button.center[0] - lives_text.get_rect().center[0],
             self.level_edit_button.center[1] - lives_text.get_rect().center[
                 1] - lives_text.get_rect().height + MENU_OFFSET)))
        lives_text = lives_font.render("Edit", 1, WHITE)
        self.blit(self.camera.apply_image(lives_text), self.camera.apply_tuple(
            (self.level_edit_button.center[0] - lives_text.get_rect().center[0],
             self.level_edit_button.center[1] - lives_text.get_rect().center[
                 1] + lives_text.get_rect().height - MENU_OFFSET)))

        if self.over_level != -1:
            if self.level_infos[self.over_level] == None:
                new_level_info = LevelInfo(self.over_level)
                self.level_infos[self.over_level] = new_level_info.draw()

            if self.level_buttons[self.over_level].centerx < self.get_width() / 2:
                self.blit(self.camera.apply_image(self.level_infos[self.over_level]), self.camera.apply_tuple(self.level_buttons[self.over_level].topright))
            else:
                self.blit(self.camera.apply_image(self.level_infos[self.over_level]), self.camera.apply_rect(self.level_infos[self.over_level].get_rect(topright = self.level_buttons[self.over_level].topleft)))
                
        return self

    def update_level(self):
        mouse_pos = self.camera.correct_mouse(pg.mouse.get_pos())
        for i, button in enumerate(self.level_buttons):
            if button.collidepoint(mouse_pos):
                self.over_level = i
                return
            
        self.over_level = -1

    def get_over_level(self):
        return self.over_level
    
    def update_body_img(self):
        if self.zoom_step >= 0:
            self.body_image = self.body_images[self.zoom_step]
        else:
            self.body_image = self.camera.apply_image(BODY_IMG)

    def event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = self.camera.correct_mouse(pg.mouse.get_pos())
                if self.tower_preview_button.collidepoint(mouse_pos):
                    return "tower_preview"
                elif self.enemy_preview_button.collidepoint(mouse_pos):
                    return "enemy_preview"
                elif self.upgrades_menu_button.collidepoint((mouse_pos)):
                    return "upgrades_menu"
                elif self.tower_edit_button.collidepoint(mouse_pos):
                    return "tower_edit"
                elif self.enemy_edit_button.collidepoint(mouse_pos):
                    return "enemy_edit"
                elif self.level_edit_button.collidepoint(mouse_pos):
                    return "level_edit"
                elif self.options_button.collidepoint(mouse_pos):
                    return "options"
                
                if self.over_level != -1 and self.over_level <= len(SAVE_DATA["levels"]) - 1:
                    return "tower_select"

            elif event.button == 4:
                if self.camera.zoom(ZOOM_AMT_MENU) != False:
                    self.zoom_step += 1
                    self.update_body_img()

            elif event.button == 5:
                if self.camera.zoom(-ZOOM_AMT_MENU) != False:
                    self.zoom_step -= 1
                    self.update_body_img()

        return -1

class TowerMenu(Display):
    def __init__(self):
        super().__init__()

    def get_dims(self):
        return (GRID_CELL_SIZE, GRID_CELL_SIZE)

    def get_locs(self, row, col):
        x = GRID_MARGIN_X + col * (GRID_CELL_SIZE + GRID_SEPARATION)
        y = GRID_MARGIN_Y + row * (GRID_CELL_SIZE + GRID_SEPARATION)

        return (x, y)

    def make_btn(self, string):
        font = pg.font.Font(FONT, 70)
        text = font.render(string, 1, WHITE)
        btn = pg.transform.scale(LEVEL_BUTTON_IMG,
                                 (text.get_width() + BTN_PADDING * 2, text.get_height())).copy().convert_alpha()
        btn.blit(text, text.get_rect(center=btn.get_rect().center))
        return btn

class TowerSelectMenu(TowerMenu):
    def __init__(self):
        super().__init__()
        self.start_btn = self.make_btn("Start")
        self.back_btn = self.make_btn("Back")
        self.start_btn_rect = pg.Rect(SCREEN_WIDTH - BTN_X_MARGIN - self.start_btn.get_width(),
                                      BTN_Y, self.start_btn.get_width(), self.start_btn.get_height())
        self.back_btn_rect = pg.Rect(BTN_X_MARGIN, BTN_Y, self.back_btn.get_width(), self.back_btn.get_height())
        
        self.start_btn_disabled = self.make_btn("Start")
        self.start_btn_disabled.fill(LIGHT_GREY, None, pg.BLEND_RGB_MULT)
        
        self.left_btn_rect = None
        self.right_btn_rect = None
        
    def new(self, args):
        # args[0] = level
        self.level_data = LEVEL_DATA[args[0]]
        map = TiledMap(path.join(MAP_FOLDER, "{}.tmx".format(list(BODY_PARTS)[LEVEL_DATA[args[0]]["body_part"]])))
        self.map_img = None
        self.draw_map(map)

        self.difficulty = 0
        self.max_difficulty = 0
        while self.max_difficulty < 3 and SAVE_DATA["levels"][args[0]][self.max_difficulty]:
            self.max_difficulty += 1

        self.max_difficulty -= 1
        self.towers = []
        self.tower_rects = []
        self.tower_selected = []

        self.over_tower = [-1, -1]
        self.num_selected = 0

        tower_names = SAVE_DATA["owned_towers"]

        row = -1
        for i in range(len(tower_names)):
            if i % GRID_ROW_SIZE == 0:
                row += 1
                self.towers.append([])
                self.tower_rects.append([])
                self.tower_selected.append([])

            self.towers[row].append(tower_names[i])
            self.tower_rects[row].append(pg.Rect(self.get_locs(row, i % GRID_ROW_SIZE), self.get_dims()))
            self.tower_selected[row].append(False)

        self.tower_infos = [None for i in range(len(tower_names))]
        self.enemy_infos = {}

        self.load_level_data()

    def load_level_data(self):
        self.max_wave = len(self.level_data["waves"][self.difficulty])
        self.curr_wave = 0
        self.wave_info = None
        self.over_enemy = None
        self.wave_data = {}
        
    def draw(self):
        self.fill(BLACK)
        
        title_font = pg.font.Font(FONT, 120)
        text_font = pg.font.Font(FONT, 70)
        
        # Draws upper left text
        title_1 = title_font.render("Select Towers", 1, WHITE)
        selected_text = text_font.render("Selected: {}/{}".format(self.num_selected, SAVE_DATA["game_attrs"]["max_towers"]["value"]), 1, WHITE)
        
        self.blit(title_1, (SCREEN_WIDTH / 4 - title_1.get_width() / 2, 0)) # puts these on the x center of the screnn's left half
        self.blit(selected_text, (SCREEN_WIDTH / 4 - selected_text.get_width() / 2, title_1.get_height() - 20))
        
        # Draws upper right text + buttons
        title_2 = title_font.render("Wave {}/{}".format(self.curr_wave + 1, self.max_wave), 1, WHITE)
        left_btn = self.make_btn("<")
        right_btn = self.make_btn(">")
        
        title_2_x = SCREEN_WIDTH * 3 / 4 - title_2.get_width() / 2 # puts title_2 on the x center of the screen's right half
        left_right_y = (title_2.get_height() - left_btn.get_height()) / 2 # puts btns on the y center of title_2
        
        left_x = title_2_x - left_btn.get_width() - 20
        right_x = title_2_x + title_2.get_width() + 20
        
        self.blit(title_2, (title_2_x, 0))
        self.blit(left_btn, (left_x, left_right_y))
        self.blit(right_btn, (right_x, left_right_y))
        
        self.left_btn_rect = left_btn.get_rect(x = left_x, y = left_right_y)
        self.right_btn_rect = right_btn.get_rect(x = right_x, y = left_right_y)
        
        # Draws towers
        for row, grid_row in enumerate(self.towers):
            for col, tower in enumerate(grid_row):
                
                tower_img = pg.transform.scale(TOWER_DATA[tower]["stages"][0]["image"].convert_alpha(), self.get_dims())

                if not self.tower_selected[row][col]:
                    if self.num_selected == SAVE_DATA["game_attrs"]["max_towers"]["value"]:
                        tower_img.fill(HALF_RED, None, pg.BLEND_RGBA_MULT)
                    else:
                        tower_img.fill(HALF_WHITE, None, pg.BLEND_RGBA_MULT)

                self.blit(tower_img, self.get_locs(row, col))
                
        # Draws waves info
        wave_coords = (SCREEN_WIDTH / 2, GRID_MARGIN_Y - selected_text.get_height())
        self.draw_wave_info(wave_coords)
        self.blit(self.wave_info, wave_coords)
        
        # Draws map
        self.blit(self.map_img, (SCREEN_WIDTH * 3 / 4 - self.map_img.get_width() / 2, SCREEN_HEIGHT / 2 - 80))
                
        # Draws stuff at the bottom

        if self.difficulty == 0:
            difficulty = "Mild"
        elif self.difficulty == 1:
            difficulty = "Acute"
        else:
            difficulty = "Severe"
        difficulty_text = text_font.render("Difficulty: {}".format(difficulty), 1, WHITE)
        self.blit(difficulty_text, ((SCREEN_WIDTH - difficulty_text.get_width()) / 2, BTN_Y))

        if self.difficulty > 0:
            minus_btn = self.make_btn("<")
            minus_x = SCREEN_WIDTH / 2 - difficulty_text.get_width() / 2 - minus_btn.get_width() - 20
            self.blit(minus_btn, (minus_x, BTN_Y))
            self.minus_btn_rect = minus_btn.get_rect(x=minus_x, y=BTN_Y)

        if self.difficulty < self.max_difficulty:
            plus_btn = self.make_btn(">")
            plus_x = SCREEN_WIDTH / 2 + difficulty_text.get_width() / 2 + 20
            self.blit(plus_btn, (plus_x, BTN_Y))
            self.plus_btn_rect = plus_btn.get_rect(x=plus_x, y=BTN_Y)

        start_btn = self.start_btn
        if self.num_selected == 0:
            start_btn = self.start_btn_disabled

        self.blit(start_btn, (self.start_btn_rect.x, BTN_Y))
        self.blit(self.back_btn, (BTN_X_MARGIN, BTN_Y))
        
        # Draws tower infos
        if self.over_tower[0] != -1:
            row, col = self.over_tower
            ind = row * GRID_ROW_SIZE + col
            
            if self.tower_infos[ind] == None:
                new_tower_info = TowerInfo(self.towers[row][col])
                self.tower_infos[ind] = new_tower_info.draw()
                
            self.blit(self.tower_infos[ind], self.tower_rects[row][col].topright)
                
        # Draws enemy infos
        if self.over_enemy != None:
            if self.enemy_infos.get(self.over_enemy) == None:
                enemy_name = clean_title(self.over_enemy)
                new_enemy_info = HoverInfo(enemy_name, ENEMY_DATA[self.over_enemy]["description"])
                self.enemy_infos[self.over_enemy] = new_enemy_info.draw()
            
            self.blit(self.enemy_infos[self.over_enemy],
                      self.enemy_infos[self.over_enemy].get_rect(topright = self.wave_data[self.over_enemy]["rect"].topleft))
                
        return self

    def get_difficulty(self):
        return self.difficulty

    def draw_map(self, map):
        img = map.make_map()
        img.blit(map.make_objects(), (0, 0))
        
        # scales map down so that it is no bigger than a rectangle with dimensions (SCREEN_WIDTH / 2, SCREEN_WIDTH / 4)
        scale_factor = min((SCREEN_WIDTH / 2 - GRID_MARGIN_X) / img.get_width(), (SCREEN_HEIGHT / 2 - 40) / img.get_height())
        self.map_img = pg.transform.scale(img, (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor)))
    
    def draw_wave_info(self, wave_coords):
        wave_font = pg.font.Font(FONT, 50)
        enemy_surfs = []
        self.wave_data = {}
        
        for sub_wave in self.level_data["waves"][self.difficulty][self.curr_wave]:
            if self.wave_data.get(sub_wave["enemy_type"]):
                self.wave_data[sub_wave["enemy_type"]]["count"] += sub_wave["enemy_count"]
            else:
                self.wave_data[sub_wave["enemy_type"]] = {"count": sub_wave["enemy_count"]}
        
        wave_data_keys = list(self.wave_data)
        
        for enemy_type in wave_data_keys:
            text = wave_font.render("{}x".format(self.wave_data[enemy_type]["count"]), 1, WHITE)
            enemy_img = pg.transform.scale(ENEMY_DATA[enemy_type]["image"], (GRID_2_CELL_SIZE, GRID_2_CELL_SIZE))
            enemy_surf = pg.Surface((text.get_width() + enemy_img.get_width(), max(text.get_height(), enemy_img.get_height())))
            
            enemy_surf.blit(text, (0, 0))
            enemy_surf.blit(enemy_img, (text.get_width(), 0))
            
            self.wave_data[enemy_type]["rect"] = pg.Rect(text.get_width(), 0, GRID_2_CELL_SIZE, GRID_2_CELL_SIZE)
            
            enemy_surfs.append(enemy_surf)
        
        self.wave_info = pg.Surface((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
        x = 0
        y = 0
        for i, surf in enumerate(enemy_surfs):
            if x + surf.get_width() >= SCREEN_WIDTH / 2 - GRID_2_MARGIN_X:
                x = 0
                y += GRID_2_CELL_SIZE + GRID_SEPARATION
                
            self.wave_info.blit(surf, (x, y))
            
            self.wave_data[wave_data_keys[i]]["rect"].x += x + wave_coords[0]
            self.wave_data[wave_data_keys[i]]["rect"].y += y + wave_coords[1]
            
            x += surf.get_width() + GRID_2_SEPARATION
    
    def get_selected_towers(self):
        selected_towers = []
        for row, grid_row in enumerate(self.towers):
            for col, tower in enumerate(grid_row):
                if self.tower_selected[row][col]:
                    selected_towers.append(tower)
        return selected_towers
    
    def event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                
                if self.back_btn_rect.collidepoint(mouse_pos):
                    return "menu"
                elif self.start_btn_rect.collidepoint(mouse_pos) and self.num_selected > 0:
                    return "game"
                elif self.left_btn_rect.collidepoint(mouse_pos):
                    og_wave = self.curr_wave
                    self.curr_wave = max(self.curr_wave - 1, self.min_wave)
                    while isinstance(self.level_data["waves"][self.difficulty][self.curr_wave][0], str):
                        if self.curr_wave == self.min_wave:
                            self.curr_wave = og_wave
                            break
                        self.curr_wave -= 1
                elif self.right_btn_rect.collidepoint(mouse_pos):
                    og_wave = self.curr_wave
                    self.curr_wave = min(self.curr_wave + 1, self.max_wave - 1)
                    while isinstance(self.level_data["waves"][self.difficulty][self.curr_wave][0], str):
                        if self.curr_wave == self.max_wave - 1:
                            self.curr_wave = og_wave
                            break
                        self.curr_wave += 1
                elif self.difficulty > 0 and self.minus_btn_rect.collidepoint(mouse_pos):
                    self.difficulty -= 1
                    self.load_level_data()
                elif self.difficulty < self.max_difficulty and self.plus_btn_rect.collidepoint(mouse_pos):
                    self.difficulty += 1
                    self.load_level_data()
                elif self.over_tower[0] != -1:
                    row, col = self.over_tower
                    if self.tower_selected[row][col]:
                        self.num_selected -= 1
                        self.tower_selected[row][col] = False
                    elif self.num_selected < SAVE_DATA["game_attrs"]["max_towers"]["value"]:
                        self.num_selected += 1
                        self.tower_selected[row][col] = True
                            
        if event.type == pg.MOUSEMOTION:
            mouse_pos = pg.mouse.get_pos()
            for row, grid_row in enumerate(self.tower_rects):
                for col, rect in enumerate(grid_row):
                    if rect.collidepoint(mouse_pos):
                        self.over_tower = [row, col]
                        return -1
                    
            for enemy_type in self.wave_data:
                if self.wave_data[enemy_type]["rect"].collidepoint(mouse_pos):
                    self.over_enemy = enemy_type
                    return -1
                    
            self.over_tower = [-1, -1]
            self.over_enemy = None
                        
        return -1

class HoverInfo(pg.Surface):
    def __init__(self, title, description):
        self.info_font = pg.font.Font(FONT, MENU_TEXT_SIZE)
        
        self.title = title
        self.description = description
        
        self.texts = []
        self.height = MENU_OFFSET
        self.width = MENU_OFFSET
        
    def make_title(self):
        title_font = pg.font.Font(FONT, MENU_TEXT_SIZE * 2)
        title_text = title_font.render(self.title, 1, WHITE)
        self.add_text(title_text)
    
    def make_description(self):
        text = textwrap.fill(self.description, 30 - round(MENU_TEXT_SIZE / 30)) # No idea how to really calculate this.
        text = text.split("\n")
        
        for i, part in enumerate(text):
            rendered_text = self.info_font.render(part, 1, WHITE)
            if i == len(text) - 1:
                self.add_text(rendered_text)
            else:
                self.add_text_custom(rendered_text, MENU_OFFSET // 5)
            
    def make_other_info(self):
        pass # to be overrided
    
    def add_text(self, text):
        self.add_text_custom(text, MENU_OFFSET)
        
    def add_text_custom(self, text, line_spacing): # only used when the line spacing is changed
        self.texts.append([text, line_spacing])
        self.height += text.get_height() + line_spacing
        self.width = max(self.width, text.get_width() + MENU_OFFSET * 2)
            
    def draw(self):
        self.make_title()
        self.make_description()
        self.make_other_info()
        
        super().__init__((self.width, self.height))
        self.fill(DARK_GREY)
        
        temp_height = MENU_OFFSET
        for text in self.texts:
            self.blit(text[0], (MENU_OFFSET, temp_height))
            temp_height += text[0].get_height() + text[1] # text[1] = line_spacing of the text
            
        return self
    
class LevelInfo(HoverInfo):
    def __init__(self, level):
        self.unlocked = level <= len(SAVE_DATA["levels"]) - 1
        self.level = level
        if self.unlocked:
            self.level_data = LEVEL_DATA[level]
            super().__init__(list(BODY_PARTS)[self.level_data["body_part"]].capitalize(), self.level_data["description"])
        else:
            super().__init__("{}. ???".format(self.level + 1), "An unknown level. Complete the previous levels to unlock this one!")
        
    def make_other_info(self):
        if self.unlocked:
            if self.level_data["difficulty"] == 0:
                difficulty_text = self.info_font.render("Easy", 1, GREEN)
            elif self.level_data["difficulty"] == 1:
                difficulty_text = self.info_font.render("Medium", 1, YELLOW)
            elif self.level_data["difficulty"] == 2:
                difficulty_text = self.info_font.render("Hard", 1, ORANGE)
            elif self.level_data["difficulty"] == 3:
                difficulty_text = self.info_font.render("Very Hard", 1, RED)
            elif self.level_data["difficulty"] == 4:
                difficulty_text = self.info_font.render("Extreme", 1, MAROON)
            self.add_text(difficulty_text)

            waves_text = self.info_font.render("{} Waves".format(len(self.level_data["waves"])), 1, WHITE)
            self.add_text(waves_text)

            enemy_surf = pg.Surface((self.texts[0][0].get_width() + MENU_OFFSET * 2, MENU_TEXT_SIZE))
            enemy_surf.fill(DARK_GREY)
            for i, enemy in enumerate(self.level_data["enemies"]):
                enemy_image = pg.transform.scale(ENEMY_DATA[enemy]["image"], (MENU_TEXT_SIZE, MENU_TEXT_SIZE))
                enemy_surf.blit(enemy_image, (i * (MENU_TEXT_SIZE + MENU_OFFSET), 0))

            self.add_text(enemy_surf)
            
            high_score_text = self.info_font.render("High Score: {}".format(SAVE_DATA["highscores"][self.level]), 1, WHITE)
            self.add_text(high_score_text)

            max_diff = 0
            while max_diff < len(SAVE_DATA["levels"][self.level]) and SAVE_DATA["levels"][self.level][max_diff]:
                max_diff += 1
            max_diff -= 1

            if max_diff == 0:
                max_diff_text = "Mild"
            elif max_diff == 1:
                max_diff_text = "Acute"
            else:
                max_diff_text = "Severe"

            text = self.info_font.render("Maximum Difficulty Unlocked: {}".format(max_diff_text), 1, WHITE)
            self.add_text(text)
        
class TowerInfo(HoverInfo):
    def __init__(self, tower):
        self.tower_data = TOWER_DATA[tower]
        self.stages_data = self.tower_data["stages"]
        
        tower_name = clean_title(tower)
        super().__init__(tower_name, self.tower_data["description"])
        
    def make_other_info(self):
        stages_text = self.info_font.render("Stages: {}".format(len(self.stages_data)), 1, WHITE)
        self.add_text(stages_text)
        
        costs = []
        for i in range(len(self.stages_data)):
            costs.append(str(self.stages_data[i]["upgrade_cost"]))
        
        cost_text = self.info_font.render("Cost: {}".format("/".join(costs)), 1, WHITE)
        self.add_text(cost_text)

class UpgradesMenu(TowerMenu):
    def __init__(self):
        super().__init__()
        self.done_btn = self.make_btn("Done")
        self.done_btn_rect = pg.Rect(BTN_X_MARGIN, BTN_Y, self.done_btn.get_width(), self.done_btn.get_height())
        self.confirm_tower_menu = ActionMenu("Are you sure you want to buy this tower?", "Yes", "No")
        self.confirm_upgrade_menu = ActionMenu("Are you sure you want to buy this upgrade?", "Yes", "No")
        self.confirming = False

    def new(self, args):
        self.towers = []
        self.tower_rects = []
        self.tower_owned = []
        self.over_tower = [-1, -1]

        tower_names = list(TOWER_DATA)
        row = -1
        for i in range(len(TOWER_DATA)):
            if i % GRID_ROW_SIZE == 0:
                row += 1
                self.towers.append([])
                self.tower_rects.append([])
                self.tower_owned.append([])

            self.towers[row].append(tower_names[i])
            self.tower_rects[row].append(pg.Rect(self.get_locs(row, i % GRID_ROW_SIZE), self.get_dims()))
            self.tower_owned[row].append(tower_names[i] in SAVE_DATA["owned_towers"])

        self.tower_infos = [None for i in range(len(tower_names))]

        self.upgrade_names = list(SAVE_DATA["game_attrs"])
        self.upgrades = []
        self.upgrade_rects = []
        self.upgrade_button_rects = []
        self.over_upgrade = -1
        height = GRID_MARGIN_Y
        for attr in SAVE_DATA["game_attrs"]:
            surf, rect = self.make_upgrade(attr, SAVE_DATA["game_attrs"][attr]["value"])
            self.upgrades.append(surf)
            self.upgrade_rects.append(surf.get_rect(topright=(SCREEN_WIDTH - GRID_MARGIN_X, height)))
            rect.topright = self.upgrade_rects[-1].topright
            self.upgrade_button_rects.append(rect)
            height += self.upgrade_button_rects[-1].height + MENU_OFFSET

        self.upgrade_infos = [None for i in range(len(self.upgrade_names))]

        font = pg.font.Font(FONT, 70)
        self.dna_text = font.render("DNA: " + str(SAVE_DATA["max_dna"] - SAVE_DATA["used_dna"]), 1, WHITE)

    def draw(self):
        self.fill(BLACK)

        title_font = pg.font.Font(FONT, 120)
        text_font = pg.font.Font(FONT, 70)

        title_1 = title_font.render("Buy Towers", 1, WHITE)
        self.blit(title_1, (SCREEN_WIDTH / 4 - title_1.get_width() / 2, 0)) # puts these on the x center of the screnn's left half

        for row, grid_row in enumerate(self.towers):
            for col, tower in enumerate(grid_row):
                tower_img = pg.transform.scale(TOWER_DATA[tower]["stages"][0]["image"].convert_alpha(), self.get_dims())

                if not self.tower_owned[row][col]:
                    if self.is_tower_buyable(self.towers[row][col]):
                        tower_img.fill(HALF_WHITE, None, pg.BLEND_RGBA_MULT)
                    else:
                        tower_img.fill(HALF_RED, None, pg.BLEND_RGBA_MULT)

                self.blit(tower_img, self.get_locs(row, col))

        title_2 = title_font.render("Upgrades", 1, WHITE)
        self.blit(title_2, (SCREEN_WIDTH * 3 / 4 - title_1.get_width() / 2, 0))

        for i, attr in enumerate(self.upgrades):
            self.blit(attr, self.upgrade_rects[i])
            
        self.blit(self.done_btn, self.done_btn_rect)
        self.blit(self.dna_text, self.dna_text.get_rect(topright=(SCREEN_WIDTH - BTN_X_MARGIN, BTN_Y)))

        if not self.confirming:
            if self.over_tower[0] != -1:
                row, col = self.over_tower
                ind = row * GRID_ROW_SIZE + col

                if self.tower_infos[ind] == None:
                    new_tower_info = BuyTowerInfo(self.towers[row][col], -1 if self.tower_owned[row][col] else 1 if self.is_tower_buyable(self.towers[row][col]) else 0)
                    self.tower_infos[ind] = new_tower_info.draw()

                self.blit(self.tower_infos[ind], self.tower_rects[row][col].topright)
            elif self.over_upgrade != -1:
                if self.upgrade_infos[self.over_upgrade] == None:
                    new_upgrade_info = UpgradeInfo(self.upgrade_names[self.over_upgrade], 1 if self.is_upgrade_buyable(self.over_upgrade) else 0)
                    self.upgrade_infos[self.over_upgrade] = new_upgrade_info.draw()
                self.blit(self.upgrade_infos[self.over_upgrade], self.upgrade_infos[self.over_upgrade].get_rect(top=self.upgrade_button_rects[self.over_upgrade].topleft[1], right = self.upgrade_button_rects[self.over_upgrade].topleft[0] - MENU_OFFSET))

        if self.confirming:
            self.blit(self.confirm_menu_surf, self.confirm_menu_rect)

        return self

    def make_upgrade(self, string, value):
        font = pg.font.Font(FONT, 70)
        text = font.render(clean_title(string) + ": " + str(value), 1, WHITE)
        plus_text = font.render("+", 1, WHITE)
        btn = pg.transform.scale(LEVEL_BUTTON_IMG, (plus_text.get_height(), plus_text.get_height())).copy().convert_alpha()
        btn.blit(plus_text, plus_text.get_rect(center=btn.get_rect().center))
        btn_rect = btn.get_rect(topleft=(text.get_width() + MENU_OFFSET, 0))
        surf = pg.Surface((text.get_width() + MENU_OFFSET + btn.get_width(), btn_rect.height))
        surf.blit(text, (0, 0))
        surf.blit(btn, btn_rect)
        return surf, btn_rect

    def is_tower_buyable(self, tower):
        return SAVE_DATA["max_dna"] - SAVE_DATA["used_dna"] >= TOWER_DATA[tower]["unlock_cost"]

    def is_upgrade_buyable(self, upgrade):
        return SAVE_DATA["max_dna"] - SAVE_DATA["used_dna"] >= SAVE_DATA["game_attrs"][self.upgrade_names[upgrade]]["upgrade_cost"]

    def event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                if self.confirming:
                    if self.confirm_menu_rect.collidepoint(mouse_pos):
                        result = self.confirm_menu.event((mouse_pos[0] - self.confirm_menu_rect.x, mouse_pos[1] - self.confirm_menu_rect.y))
                        if result == 1:
                            if self.over_tower[0] != -1:
                                row, col = self.over_tower
                                SAVE_DATA["owned_towers"].append(self.towers[row][col])
                                SAVE_DATA["used_dna"] += TOWER_DATA[self.towers[row][col]]["unlock_cost"]
                                self.tower_owned[row][col] = True
                                self.tower_infos = [None for i in range(len(TOWER_DATA))] # Force a reload of all tower infos when buying a new tower
                            else:
                                upgrade_name = self.upgrade_names[self.over_upgrade]
                                SAVE_DATA["game_attrs"][upgrade_name]["value"] += SAVE_DATA["game_attrs"][upgrade_name]["increment"]
                                SAVE_DATA["used_dna"] += SAVE_DATA["game_attrs"][upgrade_name]["upgrade_cost"]
                                SAVE_DATA["game_attrs"][upgrade_name]["upgrade_cost"] += SAVE_DATA["game_attrs"][upgrade_name]["cost_increment"]
                                surf, rect = self.make_upgrade(upgrade_name, SAVE_DATA["game_attrs"][upgrade_name]["value"])
                                self.upgrades[self.over_upgrade] = surf
                                self.upgrade_rects[self.over_upgrade] = surf.get_rect(topright=(SCREEN_WIDTH - GRID_MARGIN_X, self.upgrade_rects[self.over_upgrade].top))
                                rect.topright = self.upgrade_rects[self.over_upgrade].topright
                                self.upgrade_button_rects[self.over_upgrade] = rect
                                self.upgrade_infos = [None for i in self.upgrade_names]
                            font = pg.font.Font(FONT, 70)
                            self.dna_text = font.render("DNA: " + str(SAVE_DATA["max_dna"] - SAVE_DATA["used_dna"]), 1,
                                                        WHITE)
                        elif result == -1:
                            return -1
                    self.confirming = False
                    self.over_tower = [-1, -1]

                else:
                    if self.done_btn_rect.collidepoint(mouse_pos):
                        return "menu"
                    elif self.over_tower[0] != -1:
                        row, col = self.over_tower
                        if not self.tower_owned[row][col] and self.is_tower_buyable(self.towers[row][col]):
                            self.confirm_menu = self.confirm_tower_menu
                            self.confirm_menu_surf = self.confirm_menu.draw()
                            self.confirm_menu_rect = self.confirm_menu_surf.get_rect(
                                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                            self.confirming = True
                    else:
                        if self.over_upgrade != -1:
                            if self.is_upgrade_buyable(self.over_upgrade):
                                self.confirm_menu = self.confirm_upgrade_menu
                                self.confirm_menu_surf = self.confirm_menu.draw()
                                self.confirm_menu_rect = self.confirm_menu_surf.get_rect(
                                    center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                                self.over_upgrade = self.over_upgrade
                                self.confirming = True

        if event.type == pg.MOUSEMOTION and not self.confirming:
            mouse_pos = pg.mouse.get_pos()
            for row, grid_row in enumerate(self.tower_rects):
                for col, rect in enumerate(grid_row):
                    if rect.collidepoint(mouse_pos):
                        self.over_tower = [row, col]
                        self.over_upgrade = -1
                        return -1

            self.over_tower = [-1, -1]
            for i, rect in enumerate(self.upgrade_button_rects):
                if rect.collidepoint(mouse_pos):
                    self.over_upgrade = i
                    return -1

            self.over_upgrade = -1

        return -1

class BuyTowerInfo(TowerInfo):
    def __init__(self, tower, buyable):
        self.buyable = buyable
        super().__init__(tower)

    def make_other_info(self):
        if self.buyable == 0:
            unlock_text = self.info_font.render("Unlock Cost: " + str(self.tower_data["unlock_cost"]), 1, RED)
            self.add_text(unlock_text)
            error_text = self.info_font.render("Insufficient DNA to buy this tower!", 1, RED)
            self.add_text(error_text)
        elif self.buyable == 1:
            unlock_text = self.info_font.render("Unlock Cost: " + str(self.tower_data["unlock_cost"]), 1, YELLOW)
            self.add_text(unlock_text)
        else:
            unlock_text = self.info_font.render("You own this tower!", 1, GREEN)
            self.add_text(unlock_text)

        super().make_other_info()

class UpgradeInfo(HoverInfo):
    def __init__(self, upgrade, buyable):
        self.buyable = buyable
        self.upgrade_data = SAVE_DATA["game_attrs"][upgrade]
        upgrade_name = (" ".join(upgrade.split("_"))).title()  # removes underscores, capitalizes it properly
        super().__init__(upgrade_name, self.upgrade_data["description"])

    def make_other_info(self):
        if self.buyable == 0:
            unlock_text = self.info_font.render("Upgrade Cost: " + str(self.upgrade_data["upgrade_cost"]), 1, RED)
            self.add_text(unlock_text)
            error_text = self.info_font.render("Insufficient DNA to buy this upgrade!", 1, RED)
            self.add_text(error_text)
        else:
            unlock_text = self.info_font.render("Upgrade Cost: " + str(self.upgrade_data["upgrade_cost"]), 1, YELLOW)
            self.add_text(unlock_text)

        new_value_text = self.info_font.render("Current Value: " + str(self.upgrade_data["value"]), 1, WHITE)
        self.add_text(new_value_text)

        if self.buyable == 1:
            new_value_text = self.info_font.render("Upgraded Value: " + str(self.upgrade_data["value"] + self.upgrade_data["increment"]), 1, GREEN)
            self.add_text(new_value_text)

        super().make_other_info()

# In the future we can use this for other menus that only take up half the screen e.g. in tutorials, and such.

class ActionMenu(pg.Surface):
    def __init__(self, message, btn1txt, btn2txt):
        large_font = pg.font.Font(FONT, 70)
        self.texts = []
        self.height = MENU_OFFSET * 2
        self.width = SCREEN_WIDTH / 2
        text = textwrap.fill(message, 30)  # Hardcoding lmao

        for part in text.split('\n'):
            rendered_text = large_font.render(part, 1, WHITE)
            self.texts.append(rendered_text)
            self.height += rendered_text.get_height() + round(MENU_OFFSET / 2)
            self.width = max(self.width, rendered_text.get_width() + MENU_OFFSET * 4)

        self.button1 = self.make_btn(btn1txt)
        self.button2 = self.make_btn(btn2txt)
        self.height += self.button1.get_height() + round(MENU_OFFSET / 2)
        self.button1_rect = self.button1.get_rect(bottomleft=(MENU_OFFSET, self.height - MENU_OFFSET))
        self.button2_rect = self.button2.get_rect(bottomright=(self.width - MENU_OFFSET, self.height - MENU_OFFSET))

    def draw(self):
        super().__init__((self.width, self.height))

        self.fill(DARK_GREY)
        t_height = MENU_OFFSET
        for text in self.texts:
            self.blit(text, text.get_rect(centerx=self.width / 2, y=t_height))
            t_height += text.get_height() + round(MENU_OFFSET / 2)

        self.blit(self.button1, self.button1_rect)
        self.blit(self.button2, self.button2_rect)

        return self

    def make_btn(self, string):
        font = pg.font.Font(FONT, 70)
        text = font.render(string, 1, WHITE)
        btn = pg.transform.scale(LEVEL_BUTTON_IMG,
                                 (text.get_width() + BTN_PADDING * 2, text.get_height())).copy().convert_alpha()
        btn.blit(text, text.get_rect(center=btn.get_rect().center))
        return btn

    def event(self, mouse_pos):
        if self.button1_rect.collidepoint(mouse_pos):
            return 1
        elif self.button2_rect.collidepoint(mouse_pos):
            return 2
        else:
            return -1
