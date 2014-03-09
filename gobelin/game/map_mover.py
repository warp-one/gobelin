import pyglet
from pyglet.window import key

import grid, resources

class MapMover(grid.Quad):
    def __init__(self, game_map, map_x=0, map_y=0, img=resources.default, group=None):
        super(MapMover, self).__init__(game_map, (map_x, map_y))
        self.img = img
        self.group = group
        for image in self.images:
            image.group = self.group
        
        self.strong = False
        
        self.selector.image = img
        self.step = self.selector.width

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            if self.is_legal_move(self.map_x, self.map_y + 1):
                for s in self.images:
                    s.y += self.step
                self.map_y += 1
                return True
        if symbol == key.DOWN:
            if self.is_legal_move(self.map_x, self.map_y - 1):
                for s in self.images:
                    s.y -= self.step
                self.map_y -= 1
                return True
        if symbol == key.RIGHT:
            if self.is_legal_move(self.map_x + 1, self.map_y):
                for s in self.images:
                    s.x += self.step
                self.map_x += 1
                return True
        if symbol == key.LEFT:
            if self.is_legal_move(self.map_x - 1, self.map_y):
                for s in self.images:
                    s.x -= self.step
                self.map_x -= 1
                return True
        return False

    def is_on_board(self, col, row):
        if (col, row) in self.game_map.all_tile_cds:
            return True
        else:
            return False
        
    def is_not_blocked(self, col, row):
        current_plot = self.game_map.all_tile_cds[(col, row)]
        pathable = False
        unoccupied = True
        try:
            if current_plot.pathable:
                pathable = True
            if self._blocked_special(col, row):
                pathable = True
            for unit in self.game_map.magic_team:
                if (unit.map_y, unit.map_x) == (row, col):
                    unoccupied = False
            for unit in self.game_map.goblin_team:
                if (unit.map_y, unit.map_x) == (row, col):
                    unoccupied = False
            solid_objects = self.game_map.boxes + self.game_map.torches
            for unit in solid_objects:
                if (unit.map_y, unit.map_x) == (row, col):
                    if unit.get_pushed(self.map_y, self.map_x, self):
                        unoccupied = True
                    else:
                        unoccupied = False
        except IndexError:
            print "Stop trying to walk off the edge!"
        return pathable & unoccupied

    def _blocked_special(self, col, row):
        return False
        
    def is_legal_move(self, col, row):
        return self.is_on_board(col, row) & self.is_not_blocked(col, row)
