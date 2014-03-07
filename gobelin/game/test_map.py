from random import randint

import pyglet

import resources, cursor, map

class TestMap(object):
    def __init__(self, level, batch):
        self.level = level
        self.batch = batch
        self.new_map = []
        self.x = 100
        self.y = 100
        self.all_tile_cds = {}
        
        self.generate()
        
        # units
        self.party_size = 3
        self.magic_team = []
        self.goblin_team = []
        self.map_editor = []
        self.boxes = []
        self.light_sources = []
        
        # smaller sight range for darker caves
        self.all_visible = False

    def generate(self):
        for i in range(40):
            for j in range(40):
                tile_group = self.level.background
                self.new_map.append(map.Terrain(self,
                                                (i, j),
                                                'dirt'))
                if not randint(0, 7):
                    current_plot = self.new_map[-1]
                    current_plot.become('wall')
                elif not randint(0, 4):
                    current_plot = self.new_map[-1]
                    current_plot.become('pit')
                self.all_tile_cds[(i, j)] = self.new_map[-1]
        for tile in self.all_tile_cds:
            current_plot = self.all_tile_cds[tile]
            adj_pit = map.adj_tile_type(map.target_cross(current_plot), 'pit', self.all_tile_cds)
            if adj_pit >= 2:
                if not randint(0, 1):
                    current_plot.become('pit')
            elif self.all_tile_cds[tile].identity == 'pit':
                if not randint(0, 0):
                    current_plot.become('dirt')
            adj_wall = map.adj_tile_type(map.target_cross(current_plot), 'wall', self.all_tile_cds)
            if adj_wall and adj_wall < 3:
                if not randint(0, 4):
                    current_plot.become('wall')
            elif self.all_tile_cds[tile].identity == 'wall':
                if not randint(0, 0):
                    current_plot.become('dirt')

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
            if sight_distance < 6 or self.all_visible:
                try:
                    thing.selector.visible = True
                    thing.fog.visible = False
                    thing.dark.visible = False
                except AttributeError:
                    thing.visible = True
            elif sight_distance < 11:
                try:
                    thing.selector.visible = False
                    thing.fog.visible = True
                    thing.dark.visible = False
                except AttributeError:
                    thing.visible = False
            elif sight_distance < 16:
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
                    thing.dark.visible = False
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