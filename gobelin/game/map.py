from math import sqrt
import pyglet
import resources

def closest_distance(coordinate, units):
    lowest_distance = 1000
    if units:
        for unit in units:
            a_distance = sqrt(
                 (coordinate[0] - unit.map_x)**2 +
                 (coordinate[1] - unit.map_y)**2
                 )
            if a_distance < lowest_distance:
                lowest_distance = a_distance
        return lowest_distance
    else:
        return 0
        
def target_cross(unit):
    cross =  [(unit.map_x + 1, unit.map_y),
              (unit.map_x - 1, unit.map_y),
              (unit.map_x, unit.map_y + 1),
              (unit.map_x, unit.map_y - 1)]
    return [x for x in cross if x in unit.map.all_tile_cds]
    
class Terrain(object):
    def __init__(self, map, c2pl, tile):
        self.selector = pyglet.sprite.Sprite(
                             img = resources.dirt,
                             x = 0,
                             y = 0,
                             batch = map.batch,
                             group = map.level.background)
        self.fog = pyglet.sprite.Sprite(
                             img = resources.block,
                             x = 0,
                             y = 0,
                             batch = map.batch,
                             group = map.level.background)
        self.fog.visible = False
        self.dark = pyglet.sprite.Sprite(
                             img = resources.dark,
                             x = 0,
                             y = 0,
                             batch = map.batch,
                             group = map.level.background)
        self.dark.visible = False
        
        self.tiles = {
                 'dirt': {'image':resources.dirt,
                          'f_image':resources.mist,
                          'd_image':resources.dark,
                          'pathable':True, 
                          'boxable':True, 
                          'destructible':False},
                 'wall': {'image':resources.brick,
                          'f_image':resources.block,
                          'd_image':resources.block,
                          'pathable':False,
                          'boxable':False,
                          'destructible':True},
                 'water':{'image':resources.water,
                          'f_image':resources.mist,
                          'd_image':resources.dark,
                          'pathable':False,
                          'boxable':True,
                          'destructible':False}
                 }
        self.map = map
        self.map_x, self.map_y = c2pl[0], c2pl[1]
        image_x = self.map.x + self.selector.width * self.map_x
        image_y = self.map.y + self.selector.height * (self.map_y + 1)
        
        images = [self.selector, self.fog, self.dark]
        for i in images:
            i.x, i.y = image_x, image_y
        
        self.become(tile)
        
    def become(self, tile):
        self.identity = tile
        tile_features = self.tiles[tile]
        self.selector.image = tile_features['image']
        self.fog.image = tile_features['f_image']
        self.dark.image = tile_features['d_image']
        self.pathable = tile_features['pathable']
        self.boxable = tile_features['boxable']
        self.destructible = tile_features['destructible']
        self.repaint()
        
    def repaint(self):
        tiles = self.map.all_tile_cds
        wall_under, wall2under = None, None
        try:
            wall_under = tiles[(self.map_x, self.map_y - 1)].identity
        except:
            wall_under = None
        try:
            wall2under = tiles[(self.map_x, self.map_y - 2)].identity
        except:
            wall2under = None
        if self.identity == "wall":
            self.selector.image = resources.pillar
            adj_tiles = target_cross(self)
            for i in adj_tiles:
                if self.map.all_tile_cds[i].identity == "wall":
                    self.selector.image = resources.brick
            if wall_under == "wall" and wall2under == "wall":
                self.selector.image = resources.brk_t
            elif wall_under == "wall":
                self.selector.image = resources.brk_c
            else:
                pass                
        