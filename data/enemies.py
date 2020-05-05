from data.settings import *
import random
from data.tilemap import tile_from_coords

class Enemy(pg.sprite.Sprite):
    def __init__(self, clock, game, x, y, name):
        self.groups = game.enemies
        super().__init__(self.groups)
        
        self.clock = clock
        self.game = game
        self.name = name
        
        data = ENEMY_DATA[name]
        self.name = name
        self.hp = data["hp"]
        self.speed = data["speed"]
        self.dropped_protein = data["protein"]
        self.raw_image = data["image"]
        self.sound = pg.mixer.Sound(data["death_sound_path"])
        
        self.image = data["image"].copy()
        self.image_size = self.image.get_size()[0]
        image_size = self.image.get_size()
        self.rect = pg.Rect(x, y, image_size[0], image_size[1])
        
        self.direction = [1 if random.random() < 0.5 else -1, 1 if random.random() < 0.5 else -1]
        self.carry_x = 0
        self.carry_y = 0
        self.new_node = ((tile_from_coords(x, self.game.map.tilesize), tile_from_coords(y, self.game.map.tilesize)), 0)
        self.maximising = 0
        self.damagable = True

        self.slowed = False
        self.slow_end = 0
        
        self.recreate_path()

    def update(self):
        if (self.hp <= 0):
            self.sound.play()
            self.game.protein += self.dropped_protein
            self.kill()
            return

        passed_time = self.clock.get_time() / 1000

        if passed_time >= self.slow_end:
            self.reset_speed()

        if (self.maximising != 0 and self.image.get_size()[0] + self.maximising > 0 and self.image.get_size()[0] + self.maximising <= self.rect.w):
            self.image_size += self.maximising
            self.image = pg.transform.scale(self.raw_image, (self.image_size, self.image_size))

        if self.image.get_size()[0] + self.maximising == 0 or self.image.get_size()[0] + self.maximising == self.rect.w:
            self.maximising = 0

        if (self.rect.left <= self.new_node_rect.left):
            self.direction[0] = abs(self.direction[0])

        elif (self.rect.right >= self.new_node_rect.right):
            self.direction[0] = -abs(self.direction[0])

        if (self.rect.top <= self.new_node_rect.top):
            self.direction[1] = abs(self.direction[1])

        elif (self.rect.bottom >= self.new_node_rect.bottom):
            self.direction[1] = -abs(self.direction[1])

        self.carry_x += round(self.speed * passed_time * self.direction[0])
        self.carry_y += round(self.speed * passed_time * self.direction[1])

        if (abs(self.carry_x) >= 1):
            self.rect.x += self.carry_x
            self.carry_x = 0
        if (abs(self.carry_y) >= 1):
            self.rect.y += self.carry_y
            self.carry_y = 0

        if (self.new_node_rect.collidepoint(self.rect.topleft) and self.new_node_rect.collidepoint(self.rect.bottomright)):
            self.load_next_node()

    def get_hp_rect(self):
        h = 5
        w = self.hp * 2
        x = self.rect.x + (self.game.map.tilesize - w) / 2
        y = self.rect.y - 12
        return pg.Rect(x, y, w, h)

    def recreate_path(self):
        self.path = self.game.pathfinder.astar((self.new_node[0], self.new_node[1]), self.game.goals)
        self.load_next_node()

    def load_next_node(self):
        if self.path == False:
            print("PATHFINDING ERROR") # This should never happen
            self.kill()
            return

        if (len(self.path) == 0):
            self.game.lives = max(self.game.lives - 1, 0)
            
            if self.game.lives <= 0:
                self.game.cause_of_death = " ".join(self.name.split("_")).title() # removes underscores, capitalizes it properly

            self.kill()
            return
        
        self.end_dist = len(self.path)
        prevlayer = self.new_node[1]
        self.new_node = self.path.pop(0)
        
        if abs(prevlayer) == 1 and abs(self.new_node[1]) == 2:
            self.maximising = -1
            self.damagable = False
        elif abs(prevlayer) == 2 and abs(self.new_node[1]) == 1:
            self.maximising = 1
            self.damagable = False
        elif prevlayer == 0:
            self.damagable = True

        self.new_node_rect = pg.Rect(self.new_node[0][0] * self.game.map.tilesize, self.new_node[0][1] * self.game.map.tilesize, self.game.map.tilesize, self.game.map.tilesize)
        
    def reset_speed(self):
        self.speed = ENEMY_DATA[self.name]["speed"]
        self.image = ENEMY_DATA[self.name]["image"].copy()
        self.slowed = False

    def is_slowed(self):
        return self.slowed

    def slow(self, slow_speed, slow_duration):
        self.speed = ENEMY_DATA[self.name]["speed"]
        self.slowed = True
        self.slow_end = self.clock.get_time() / 1000 + slow_duration
        self.speed *= slow_speed

        image_surf = pg.Surface(self.image.get_size()).convert_alpha()
        image_surf.fill((0, 0, 0, 0))
        image_surf.blit(self.image.convert_alpha(), (0, 0))
        image_surf.fill(HALF_GREEN, None, pg.BLEND_RGBA_MULT)
        self.image = image_surf
