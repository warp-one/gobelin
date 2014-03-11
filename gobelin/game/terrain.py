from math import sqrt
import pyglet
import resources, grid

terrain_types = {}

class TerrainType(object):
    def __init__(self):
        self.pathable_tiles = []

    def _retile(self, arg1, arg2):
        return arg1, arg2

class Dirt(TerrainType):
    def __init__(self, terrain_dict):
        super(Dirt, self).__init__()
        self.image = resources.dirt
        self.f_image = resources.mist
        self.d_image = resources.dark
        self.pathable = True
        self.boxable = True
        self.destructible = False
        terrain_dict['dirt'] = self

class Wall(TerrainType):
    def __init__(self, terrain_dict):
        super(Wall, self).__init__()
        self.image = resources.brick
        self.f_image = resources.block
        self.d_image = resources.block
        self.pathable = False
        self.boxable = False
        self.destructible = True
        terrain_dict['wall'] = self
        
    def _retile(self, game_map, tile):
        tiles = game_map.all_tile_cds
        wall_under, wall2under = None, None
        try:
            wall_under = tiles[(tile.map_x, tile.map_y - 1)].identity
        except:
            wall_under = None
        try:
            wall2under = tiles[(tile.map_x, tile.map_y - 2)].identity
        except:
            wall2under = None
        tile.selector.image = resources.pillar
        for i in grid.target_cross(tile):
            if game_map.all_tile_cds[i].identity == "wall":
                tile.selector.image = resources.brick
        if wall_under == "wall" and wall2under == "wall":
            tile.selector.image = resources.brk_t
        elif wall_under == "wall":
            tile.selector.image = resources.brk_c
        else:
            pass

class Pit(TerrainType):
    def __init__(self, terrain_dict):
        super(Pit, self).__init__()
        self.image = resources.bmpt_lookup[0b0000]
        self.f_image = resources.mist
        self.d_image = resources.dark
        self.pathable = False
        self.boxable = True
        self.destructible = False
        terrain_dict['pit'] = self

    def _retile(self, game_map, tile):
        pit_img = 0b0000
        adj_tiles = grid._target_cross(tile)
        for match in adj_tiles:
            if game_map.all_tile_cds[adj_tiles[match]].identity == "pit":
                if match == 'north':
                    pit_img = pit_img | 0b1000
                if match == 'east':
                    pit_img = pit_img | 0b0100
                if match == 'south':
                    pit_img = pit_img | 0b0010
                if match == 'west':
                    pit_img = pit_img | 0b0001
        tile.selector.image = resources.bmpt_lookup[pit_img]
        
class Water(TerrainType):
    def __init__(self, terrain_dict):
        super(Water, self).__init__()
        self.image = resources.water
        self.f_image = resources.mist
        self.d_image = resources.dark
        self.pathable = False
        self.boxable = True
        self.destructible = False
        terrain_dict['water'] = self
        
class Doodad(TerrainType):
    def __init__(self, terrain_dict):
        super(Doodad, self).__init__()
        self.image = resources.default
        self.f_image = resources.default
        self.d_image = resources.block
        self.pathable = False
        self.boxable = False
        self.destructible = False
        terrain_dict['doodad'] = self
        
class Supermarket(Doodad):
    def __init__(self, terrain_dict):
        super(Supermarket, self).__init__({})
        self.pathable_tiles = [(2,0), (3,0), (4,0), (5,0),
                               (5,1), (5,2), (5,3), (5,4), 
                               (5,5), (5,6), (5,7), (6,1), 
                               (6,2), (6,5), (6,6), (6,7),
                               (7,0), (7,1), (7,2), (7,3),
                               (7,4), (7,5), (7,6), (7,7)]
        terrain_dict['supermarket'] = self

all_terrain = [Dirt, Wall, Pit, Water, Supermarket]        
for _ in all_terrain:
    _(terrain_types)
       
class Terrain(grid.Quad):
    def __init__(self, game_map, c2pl, tile):
        super(Terrain, self).__init__(game_map, c2pl)
        self.become(tile)
        
    def become(self, tile):
        self.identity = tile
        self.attributes = terrain_types[tile]
        self.selector.image = self.attributes.image
        self.fog.image = self.attributes.f_image
        self.dark.image = self.attributes.d_image
        self.pathable = self.attributes.pathable
        self.boxable = self.attributes.boxable
        self.destructible = self.attributes.destructible
        self.pathable_tiles = self.attributes.pathable_tiles
        self.repaint()
        
    def become_doodad(self, tile):
        self.become(tile)
        self.verticals = pyglet.sprite.Sprite(
                                        img = resources.default,
                                        x = 0,
                                        y = 0,
                                        batch = None,
                                        group = None
                                        )

    def repaint(self):
        terrain_types[self.identity]._retile(self.game_map, self)
