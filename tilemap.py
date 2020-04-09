from pytmx.util_pygame import load_pygame

from settings import *

def tile_from_coords(i, tilesize):
    return int(round((i - tilesize / 2) / tilesize))

def tile_from_xcoords(i, tilesize):
    return int(round(i / tilesize))

def round_to_tilesize(i, tilesize):
    return tilesize * round((i - tilesize / 2) / tilesize)

def round_to_mtilesize(i, tilesize):
    return tilesize * (round((i) / tilesize) + 1 / 2)

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

def clamp(x, s, b):
    return max(min(x, b), s)

class TiledMap:
    def __init__(self, filename):
        tm = load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tilesize = tm.tilewidth
        self.tmxdata = tm
        self.map = [[0 for row in range(tm.height)] for col in range(tm.width)]

    def render(self, surface, layers):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in layers:
            for x, y, gid in self.tmxdata.get_layer_by_name(layer):
                tile = ti(gid)
                if tile:
                    surface.blit(tile, (x * self.tmxdata.tilewidth,
                                        y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height), pg.SRCALPHA, 32).convert_alpha()
        self.render(temp_surface, ["background"])
        return temp_surface

    def make_objects(self):
        temp_surface = pg.Surface((self.width, self.height), pg.SRCALPHA, 32).convert_alpha()
        self.render(temp_surface, ["foreground"])
        return temp_surface

    def change_node(self, x, y, state):
        if (x < 0 or x > self.width or y < 0 or y > self.height):
            return False
        self.map[x][y] = state

    def get_map(self):
        return self.map


class Camera:
    def __init__(self, map, width, height):
        self.width = width
        self.height = height
        self.map_width = map.width
        self.map_height = map.height
        self.tilesize = map.tilesize
        self.current_zoom = min(width / map.width, height / map.height)
        if (width / map.width > height / map.height):
            self.short_width = True
        else:
            self.short_width = False
        self.minzoom = self.current_zoom
        self.critical_ratio = max(width / map.width, height / map.height) + 0.1
        self.camera = pg.Rect((self.width - self.map_width * (self.current_zoom + 0.05)) / 2, (self.height- self.map_height * self.current_zoom) / 2, width, height)

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_tuple(self, tuple):
        return ([x * self.current_zoom + self.camera.topleft[i] for i, x in enumerate(tuple)])

    def apply_rect(self, rect):
        x = rect.x * self.current_zoom + self.camera.topleft[0]
        y = rect.y * self.current_zoom + self.camera.topleft[1]
        w = rect.w * self.current_zoom
        h = rect.h * self.current_zoom
        return pg.Rect(x, y, w, h)

    # # For testing purposes only
    # def apply_template(self, rect):

    def apply_image(self, image):
        size = image.get_rect().size
        return pg.transform.scale(image, ([round(self.current_zoom * x) for x in size]))

    def correct_mouse(self, pos):
        return ([round((x - self.camera.topleft[i]) / self.current_zoom) for i, x in enumerate(pos)])

    def update(self, x, y, amount):
        self.current_zoom += amount

        newx = x - self.width / 2
        newy = y - self.height / 2

        self.camera = self.camera.move(amount * (self.map_width - self.width - newx) / 2,
                                       amount * (self.map_height - self.height - newy))

        minx = self.width - self.map_width * self.current_zoom
        miny = self.height - self.map_height * self.current_zoom
        self.camera.x = clamp(self.camera.x, minx, 0)
        self.camera.y = clamp(self.camera.y, miny, 0)

        if (self.current_zoom < self.critical_ratio):
            if self.short_width:
                self.camera.x = (self.width - self.map_width * self.current_zoom) / 2

            else:
                self.camera.y = (self.height - self.map_height * self.current_zoom) / 2


    def zoom(self, amount, pos):
        if (amount > 0 and self.current_zoom >= self.minzoom + 1 or amount < 0 and self.current_zoom <= self.minzoom):
            return


        self.update(pos[0], pos[1], amount)
