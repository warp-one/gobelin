from math import sqrt

import pyglet

import resources

def _distance(c1, c2):
    return sqrt((c1[0] - c2[0])**2 +
                (c1[1] - c2[1])**2
               )

def closest_distance(coordinate, units):
    lowest_distance = 1000
    if units:
        for unit in units:
            a_distance = _distance(coordinate, (unit.map_x, unit.map_y))
            if a_distance < lowest_distance:
                lowest_distance = a_distance
        return lowest_distance
    else:
        return 0
        
def _target_cross(unit):
    cross =  {'east': (unit.map_x + 1, unit.map_y),
              'west': (unit.map_x - 1, unit.map_y),
              'north': (unit.map_x, unit.map_y + 1),
              'south': (unit.map_x, unit.map_y - 1)}
    result = {}
    for key in cross:
        if cross[key] in unit.game_map.all_tile_cds:
            result[key] = cross[key]
    return result
    
def target_cross(unit):
    return _target_cross(unit).values()

def adj_tile_type(cross, type, all_tiles):
    num = 0
    for c in cross:
        if all_tiles[c].identity == type:
            num += 1
    return num

def _circle_point(y_term, origin, radius):
    if y_term:
        if y_term > 0:
            sign = 1
        else:
            sign = -1
    else:
        sign = 1
    x_1 = sqrt(radius**2 - (y_term - sign*origin[1])**2) - origin[0]
    x_2 = sqrt(radius**2 - (y_term - sign*origin[1])**2) + origin[0]
    return (x_1, x_2)
    
def nearby_coordinates(origin, radius):
    nearby_c = []
    for y in range((origin[1] - radius), (origin[1] + radius + 1)):
        xs = _circle_point(y, origin, radius)
        x_beg, x_end = int(xs[0]), int(xs[1])
        nearby_c.extend([(x_beg, y), (x_end, y)])
        for x in range(x_beg + 1, x_end):
            nearby_c.append((x, y))
    return nearby_c

class Quad(object):
    def __init__(self, game_map, c2pl):
        self.selector = pyglet.sprite.Sprite(
                             img = resources.default,
                             x = 0,
                             y = 0,
                             batch = game_map.batch,
                             group = game_map.level.background)
        self.fog = pyglet.sprite.Sprite(
                             img = resources.mist,
                             x = 0,
                             y = 0,
                             batch = game_map.batch,
                             group = game_map.level.background)
        self.dark = pyglet.sprite.Sprite(
                             img = resources.dark,
                             x = 0,
                             y = 0,
                             batch = game_map.batch,
                             group = game_map.level.background)
        
        self.game_map = game_map
        self.map_x, self.map_y = c2pl[0], c2pl[1]

        image_x = self.game_map.x + self.selector.width * self.map_x
        image_y = self.game_map.y + self.selector.height * (self.map_y + 1)
        self.images = [self.selector, self.fog, self.dark]
        for i in self.images:
            i.x, i.y = image_x, image_y
            i.visible = False
        self.identity = 0

    def fully_lit(self):
        self.selector.visible = True
        self.fog.visible = False
        self.dark.visible = False
        
    def in_shadow(self):
        self.selector.visible = False
        self.fog.visible = True
        self.dark.visible = False
    
    def in_darkness(self):
        self.selector.visible = False
        self.fog.visible = False
        self.dark.visible = True
        
    def hide(self):
        self.selector.visible = False
        self.fog.visible = False
        self.dark.visible = False