import pyglet

import resources, cursor, map

class TestMap(object):
    def __init__(self, level, batch):
        self.board = []
        self.level = level
        self.batch = batch
        self.foot_map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        self.x = 300
        self.y = 300

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
        
        self.sight_range = 5

    def move_map(self, add_x, add_y):
        self.x += add_x
        self.y += add_y

    def redraw_map(self):
        self.board = []
        row = 0
        try:
            light_sources = self.magic_team
        except IndexError:
            light_source = None
            print "index error"
        for r in range(self.map_height):
            self.board.append([])
        for r in self.board:
            for c in range(self.map_width):
                tile_identity = self.foot_map[row][c]
                x_pos = c * self.step + self.x
                y_pos = (row + 1) * self.step + self.y
                tile_batch = self.batch
                tile_group = self.level.background
                if map.distance((row, c), light_sources) < self.sight_range:
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
        for unit in self.boxes:
            if map.distance((unit.map_r, unit.map_c), light_sources) < self.sight_range:
                unit.selector.batch = self.level.batch
            else:
                unit.selector.batch = None
        for unit in self.goblin_team:
            if map.distance((unit.map_r, unit.map_c), light_sources) < self.sight_range:
                unit.selector.batch = self.level.batch
            else:
                unit.selector.batch = None

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
        for b in self.boxes:
            if self.foot_map[b.map_r][b.map_c] == 2:
                b.die()
                self.foot_map[b.map_r][b.map_c] = 0
        self.redraw_map()