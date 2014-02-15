import pyglet

import resources, cursor, map

class TestMap(object):
    def __init__(self, level, batch):
        self.board = []
        self.level = level
        self.batch = batch
        self.foot_map = []
        for i in range(20):
            self.foot_map.append([])
        for i in range(20):
            for j in range(20):
                self.foot_map[i].append(0)
        self.map_width = len(self.foot_map[0])
        self.map_height = len(self.foot_map)
        self.x = 300
        self.y = 300

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
        
        # smaller sight range for darker caves
        self.sight_range = 5
        self.all_visible = False

    def move_map(self, add_x, add_y):
        self.x += add_x
        self.y += add_y

    def redraw(self):
        row = 0
        self.board = []
        for r in range(self.map_height):
            self.board.append([])
        # establish who is doing the looking
        try:
            light_sources = self.magic_team
        except IndexError:
            light_source = None
            print "index error"
        # find out what all is near the magic team
        for r in self.board:
            for c in range(self.map_width):
                tile_identity = self.foot_map[row][c]
                x_pos = c * self.step + self.x
                y_pos = (row + 1) * self.step + self.y
                tile_batch = self.batch
                tile_group = self.level.background
                sight_distance = map.closest_distance((row, c), light_sources)
                if sight_distance < self.sight_range or self.all_visible:
                    if tile_identity == 0:
                        r.append(pyglet.sprite.Sprite(
                            img = self.dirt,
                            x = x_pos,
                            y = y_pos,
                            batch = tile_batch,
                            group = tile_group)
                            )
                    elif tile_identity == 1:
                        r.append(pyglet.sprite.Sprite(
                            img = self.wall,
                            x = x_pos,
                            y = y_pos,
                            batch = tile_batch,
                            group = tile_group)
                            )
                    elif tile_identity == 2:
                        r.append(pyglet.sprite.Sprite(
                            img = self.water,
                            x = x_pos,
                            y = y_pos,
                            batch = tile_batch,
                            group = tile_group)
                            )
            row += 1
        # collect all the things we might see in the cave
        entities = []
        if self.boxes:
            entities.extend(self.boxes)
        if self.goblin_team:
            entities.extend(self.goblin_team)
        # decide if they're close enough to see
        for unit in entities:
            row, col = unit.map_r, unit.map_c
            sight_distance = map.closest_distance((row, col), light_sources)
            if sight_distance < self.sight_range or self.all_visible:
                unit.selector.batch = self.level.batch
            else:
                unit.selector.batch = None
        if self.level.foe_selector.selected_unit:
            if not self.level.foe_selector.selected_unit.selector.batch:
                self.level.foe_selector.batch = None
            else:
                self.level.foe_selector.batch = self.level.batch

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
            if self.foot_map[b.map_r][b.map_c] == 2:
                b.die()
                self.foot_map[b.map_r][b.map_c] = 0
        self.redraw()