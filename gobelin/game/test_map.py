from random import randint, choice

import pyglet

import resources, cursor, terrain, grid

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
        self.torches = []
        
        # smaller sight range for darker caves
        self.all_visible = False

    def generate(self):
        for i in range(40):
            for j in range(40):
                tile_group = self.level.background
                self.new_map.append(terrain.Terrain(self,
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
            adj_pit = grid.adj_tile_type(grid.target_cross(current_plot), 'pit', self.all_tile_cds)
            if adj_pit >= 2:
                if not randint(0, 1):
                    current_plot.become('pit')
            elif self.all_tile_cds[tile].identity == 'pit':
                if not randint(0, 0):
                    current_plot.become('dirt')
            adj_wall = grid.adj_tile_type(grid.target_cross(current_plot), 'wall', self.all_tile_cds)
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
#        nearby_coordinates = [] 
#        for l in self.light_sources:
#            nearby_coordinates.extend(grid.nearby_coordinates((l.map_x, l.map_y), 17))
#        nearby_coordinates = list(set(nearby_coordinates))
        if self.new_map:
            entities.extend(self.new_map)
#            for a in self.all_tile_cds:
#                entities[a] = self.all_tile_cds[a]
        if self.boxes:
            entities.extend(self.boxes)
        if self.torches:
            entities.extend(self.torches)
        if self.goblin_team:
            entities.extend(self.goblin_team)
#        if self.level.selectors:
#            entities.extend(self.level.selectors)
#        for c in nearby_coordinates:
#            if c in entities:
#                thing = entities[c]
#                sight_distance = grid.closest_distance(c, self.light_sources) 
#                torch_distance = grid.closest_distance(c, self.torches)
#                if sight_distance < 6 or self.all_visible:
#                    thing.fully_lit()
#                elif sight_distance < 11:
#                    if torch_distance < self.torches[0].brightness:
#                        thing.fully_lit()
#                    else:
#                        thing.in_shadow()
#                elif sight_distance < 16:
#                    thing.in_darkness()
#                else:
#                    thing.hide()
#                if entities[c].identity:
#                    entities[c].repaint()
        for thing in entities:
            x, y = thing.map_x, thing.map_y
            sight_distance = grid.closest_distance((x, y), self.light_sources)
            torch_distance = grid.closest_distance((x, y), self.torches)
            if sight_distance < 6 or self.all_visible:
                thing.fully_lit()
            elif sight_distance < 11:
                if torch_distance < self.torches[0].brightness:
                    thing.fully_lit()
                else:
                    thing.in_shadow()
            elif sight_distance < 16:
                thing.in_darkness()
            else:
                thing.hide()
        for tile in self.all_tile_cds:
            self.all_tile_cds[tile].repaint()
        
    def place_boxes(self, box_cds):
        for bc in box_cds:
            self.boxes.append(cursor.PushableBox(
                            self, 
                            bc[0],
                            bc[1],
                            resources.random_box())
                            )
            for img in self.boxes[-1].images:
                img.batch = self.batch
            
    def place_torches(self, torch_cds):
        for tc in torch_cds:
            self.torches.append(cursor.Torch(
                            self, 
                            tc[0],
                            tc[1],
                            resources.torch)
                            )
            for img in self.torches[-1].images:
                img.batch = self.batch

    def update_map(self):
        # turn boxes-in-water into land
        for b in self.boxes:
            current_plot = self.all_tile_cds[(b.map_x, b.map_y)]
            if current_plot.identity == "water" or current_plot.identity == "pit":
                b.die()
                if current_plot.identity == "water":
                    current_plot.become("dirt")
        self.redraw()