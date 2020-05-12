from data.settings import *
import random
from data.tilemap import tile_from_coords

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y, name):
        self.groups = game.enemies
        super().__init__(self.groups)
        
        self.clock = game.clock
        self.game = game
        self.name = name
        
        data = ENEMY_DATA[name]
        self.name = name
        self.hp = data["hp"]
        self.speed = data["speed"]
        self.dropped_protein = data["protein"]
        self.original_image = data["image"]
        self.raw_image = self.original_image
        self.sound = pg.mixer.Sound(data["death_sound_path"])
        self.flying = data["flying"]
        if data["shield"]:
            self.shield = True
            self.shield_max_hp = data["shield_hp"]
            self.shield_hp = data["shield_hp"]
            self.shield_max_recharge_delay = data["shield_recharge_delay"]
            self.shield_recharge_rate = data["shield_recharge_rate"]
        else:
            self.shield = False
        if data["explode_on_death"]:
            self.explode_on_death = True
            self.explode_radius = data["explode_radius"]
        else:
            self.explode_on_death = False
        
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
        self.shield_end = 0
        
        self.recreate_path()

    def update(self):
        passed_time = self.clock.get_time() / 1000
        self.slow_end -= passed_time

        if self.shield and self.shield_hp != self.shield_max_hp:
            if self.shield_recharge_delay <= 0:
                self.shield_hp += 1
                self.shield_recharge_delay = self.shield_recharge_rate

            else:
                self.shield_recharge_delay -= passed_time

        if self.slowed and self.slow_end <= 0:
            self.reset_speed()

        if (self.maximising != 0 and self.image.get_size()[0] + self.maximising > 0 and self.image.get_size()[0] + self.maximising <= self.rect.w):
            self.image_size += self.maximising
            self.image = pg.transform.scale(self.raw_image, (self.image_size, self.image_size))

        if self.image_size + self.maximising == 0 or self.image_size + self.maximising == self.rect.w:
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

    def damage(self, amount):
        if self.shield and self.shield_hp > 0:
            self.shield_recharge_delay = self.shield_max_recharge_delay
            if amount > self.shield_hp:
                self.shield_hp = 0
                self.hp -= amount - self.shield_hp
            else:
                self.shield_hp -= amount

        else:
            self.hp -= amount

        if (self.hp <= 0):
            self.sound.play()
            self.game.protein += self.dropped_protein
            if self.explode_on_death:
                Explosion(self.game, self.rect.center[0] - self.explode_radius / 2, self.rect.center[1] - self.explode_radius / 2, self.explode_radius)
            self.kill()

    def get_hp_surf(self):
        hp_surf = pg.Surface((self.hp * 2, 5))
        if self.is_slowed():
            hp_surf.fill(RED)
        else:
            hp_surf.fill(GREEN)

        if not self.shield:
            return hp_surf

        shield_surf = pg.Surface((self.shield_hp * 2, 5))
        shield_surf.fill(CYAN)
        combo_surf = pg.Surface((max(self.shield_hp, self.hp) * 2, 10)).convert_alpha()
        combo_surf.fill((0, 0, 0, 0))
        combo_surf.blit(hp_surf, hp_surf.get_rect(center=(combo_surf.get_rect().center[0], 7)))
        combo_surf.blit(shield_surf, shield_surf.get_rect(center=(combo_surf.get_rect().center[0], 2)))
        return combo_surf

    def recreate_path(self):
        self.path = self.game.pathfinder.astar((self.new_node[0], self.new_node[1]), self.game.goals, self.flying)
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
        self.raw_image = self.original_image
        self.image = pg.transform.scale(self.raw_image, (self.image_size, self.image_size))
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
        image_surf.blit(self.original_image.convert_alpha(), (0, 0))
        image_surf.fill(HALF_GREEN, None, pg.BLEND_RGBA_MULT)
        self.raw_image = image_surf
        self.image = pg.transform.scale(self.raw_image, (self.image_size, self.image_size))

class Explosion(pg.sprite.Sprite):
    def __init__(self, game, x, y, rad):
        for tile_x in range(tile_from_coords(x, game.map.tilesize), tile_from_coords(x + rad, game.map.tilesize) + 1):
            for tile_y in range(tile_from_coords(y, game.map.tilesize), tile_from_coords(y + rad, game.map.tilesize) + 1):
                game.map.remove_tower(tile_x, tile_y)
        game.pathfinder.clear_nodes(game.map.get_map())
        game.draw_tower_bases_wrapper()
        game.make_stripped_path_wrapper()
        for enemy in game.enemies:
            enemy.recreate_path()
        super().__init__(game.explosions)
        self.clock = game.clock
        self.x = x
        self.y = y
        self.rad = rad
        self.state = 0
        self.surf = pg.Surface((rad, rad)).convert_alpha()

    def update(self):
        passed_time = self.clock.get_time() / 1000
        self.state += passed_time / EXPLOSION_TIME
        if self.state >= 1:
            self.kill()
        else:
            self.surf.fill((255, 0, 0, 127 * self.state))

    def get_surf(self):
        return self.surf
