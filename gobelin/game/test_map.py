import pyglet

import resources

class TestMap(object):
    def __init__(self, level, batch):
        self.board = []
        self.level = level
        self.batch = batch
        self.foot_map = [
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 0, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 1],
            [0, 1, 1, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 1, 1]
            ]
        self.x = 300
        self.y = 300

        self.map_width = len(self.foot_map[0])
        self.map_height = len(self.foot_map)

        # textures
        self.dirt = resources.dirt
        self.wall = resources.block
        
        # units
        self.magic_team = []

    def move_map(self, add_x, add_y):
        self.x += add_x
        self.y += add_y

    def show_map(self):
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