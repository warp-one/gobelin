import pyglet
from pyglet.window import key

import resources

class MapMover(object):
    def __init__(self, map, map_x=0, map_y=0):
        self.map = map
        self.map_x = map_x
        self.map_y = map_y
        
        self.selector = pyglet.sprite.Sprite(
                                  img = resources.magic_w,
                                  batch = None,
                                  x = self.map.x + 10*self.map_x,
                                  y = self.map.y + 10*(self.map_y+1)
                                  )
        self.step = self.selector.width

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            if self.is_legal_move(self.map_x + 1, self.map_y):
                self.selector.y += self.step
                self.map_x += 1
        if symbol == key.DOWN:
            if self.is_legal_move(self.map_x - 1, self.map_y):
                self.selector.y -= self.step
                self.map_x -= 1
        if symbol == key.RIGHT:
            if self.is_legal_move(self.map_x, self.map_y + 1):
                self.selector.x += self.step
                self.map_y += 1
        if symbol == key.LEFT:
            if self.is_legal_move(self.map_x, self.map_y - 1):
                self.selector.x -= self.step
                self.map_y -= 1

    def is_on_board(self, row, col):
        is_on_row, is_on_col = False, False
        if row <= self.map.map_height - 1 and row >= 0:
            is_on_row = True
        if col <= self.map.map_width - 1 and col >= 0:
            is_on_col = True

        return is_on_row & is_on_col
        
    def is_not_blocked(self, row, col):
        try:
            if self.map.foot_map[row][col]:
                return False
        except IndexError:
            print "Stop trying to walk off the edge!"
            return False
        return True
        
    def is_legal_move(self, row, col):
        return self.is_on_board(row, col) & self.is_not_blocked(row, col)
