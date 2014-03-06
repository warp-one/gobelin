from random import randint

import pyglet

import resources, cursor, map

class TestMap(object):
    def __init__(self, level, batch):
        self.board = []
        self.level = level
        self.batch = batch
        self.foot_map = []
        self.new_map = [] #N
        self.x = 100
        self.y = 100
        self.all_tile_cds = {}
        for i in range(40):
            self.foot_map.append([])
        for i in range(40):
            for j in range(40):
                self.foot_map[i].append(0)
                tile_group = self.level.background                 #N
                self.new_map.append(map.Terrain(self,
                                                (i, j),
                                                'dirt'))
                if not randint(0, 5):
                    current_plot = self.new_map[-1]
                    current_plot.become('wall')
                self.all_tile_cds[(i, j)] = self.new_map[-1]
                                                
        self.map_width = len(self.foot_map[0])
        self.map_height = len(self.foot_map)

        # textures
        self.dirt = resources.dirt
        self.wall = resources.block
        self.water = resources.water
        self.step = self.dirt.width
        
        # units
        self.party_size = 3
        self.magic_team = []
        self.goblin_team = []
        self.map_editor = []
        self.boxes = []
        self.light_sources = []
        
        # smaller sight range for darker caves
        self.sight_range = 5
        self.all_visible = False

    def move_map(self, add_x, add_y):
        self.x += add_x
        self.y += add_y

    def redraw(self):
        entities = []
        if self.new_map:
            entities.extend(self.new_map)
        if self.boxes:
            entities.extend(self.boxes)
        if self.goblin_team:
            entities.extend(self.goblin_team)
        if self.level.selectors:
            entities.extend(self.level.selectors)
        for thing in entities:
            x, y = thing.map_x, thing.map_y
            sight_distance = map.closest_distance((x, y), self.light_sources)
            if sight_distance < self.sight_range or self.all_visible:
                try:
                    thing.selector.visible = True
                    thing.fog.visible = False
                    thing.dark.visible = False
                except AttributeError:
                    thing.visible = True
            elif sight_distance < 10:
                try:
                    thing.selector.visible = False
                    thing.fog.visible = True
                    thing.dark.visible = False
                except AttributeError:
                    thing.visible = False
            elif sight_distance < 18:
                try:
                    thing.selector.visible = False
                    thing.fog.visible = False
                    thing.dark.visible = True
                except AttributeError:
                    thing.visible = False
            else:
                try: 
                    thing.selector.visible = False
                    thing.fog.visible = False
                except AttributeError:
                    thing.visible = False
        for tile in self.all_tile_cds:
            self.all_tile_cds[tile].repaint()
        
    def place_objects(self):
        crates = [(1, 1),
                  (2, 2),
                  (3, 3)]
        for b in crates:
            self.boxes.append(cursor.PushableBox(self, 
                            b[0],
                            b[1],
                            resources.box)
                            )

    def update_map(self):
        # turn boxes-in-water into land
        for b in self.boxes:
            current_plot = self.all_tile_cds[(b.map_x, b.map_y)]
            if current_plot.identity == "water":
                b.die()
                current_plot.become("dirt")
        self.redraw()