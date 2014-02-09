import pyglet

import resources, cursor

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
        
        # units
        self.party_size = 3
        self.magic_team = []
        self.boxes = []

    def move_map(self, add_x, add_y):
        self.x += add_x
        self.y += add_y

    def redraw_map(self):
        self.board = []
        for r in range(self.map_height):
            self.board.append([])
        for r in self.board:
            row = self.board.index(r)
            for c in range(self.map_width):
                tile_identity = self.foot_map[row][c]
                if tile_identity == 0:
                    r.append(pyglet.sprite.Sprite(
                        img = self.dirt,
                        x = c * self.dirt.width + self.x,
                        y = (self.board.index(r) + 1) * self.dirt.height + self.y,
                        batch = self.batch,
                        group = self.level.background)
                        )
                if tile_identity == 1:
                    r.append(pyglet.sprite.Sprite(
                        img = self.wall,
                        x = c * self.wall.width + self.x,
                        y = (self.board.index(r) + 1) * self.wall.height + self.y,
                        batch = self.batch,
                        group = self.level.background)
                        )
                if tile_identity == 2:
                    r.append(pyglet.sprite.Sprite(
                        img = self.water,
                        x = c * self.water.width + self.x,
                        y = (self.board.index(r) + 1) * self.water.height + self.y,
                        batch = self.batch,
                        group = self.level.background)
                        )
        for unit in self.boxes:
            unit.selector.batch = self.level.batch

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