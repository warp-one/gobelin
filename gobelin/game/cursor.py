

import pyglet
from pyglet.window import key

import resources

class MapMover(object):
    def __init__(self, map, map_c=0, map_r=0, img=resources.default):
        self.map = map
        self.map_c = map_c
        self.map_r = map_r
        self.img = img
        
        self.selector = pyglet.sprite.Sprite(
                                  img = self.img,
                                  batch = None,
                                  x = self.map.x + 10*self.map_c,
                                  y = self.map.y + 10*(self.map_r+1)
                                  )
        self.step = self.selector.width

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            if self.is_legal_move(self.map_c, self.map_r + 1):
                self.selector.y += self.step
                self.map_r += 1
        if symbol == key.DOWN:
            if self.is_legal_move(self.map_c, self.map_r - 1):
                self.selector.y -= self.step
                self.map_r -= 1
        if symbol == key.RIGHT:
            if self.is_legal_move(self.map_c + 1, self.map_r):
                self.selector.x += self.step
                self.map_c += 1
        if symbol == key.LEFT:
            if self.is_legal_move(self.map_c - 1, self.map_r):
                self.selector.x -= self.step
                self.map_c -= 1

    def is_on_board(self, col, row):
        is_on_row, is_on_col = False, False
        if row <= self.map.map_height - 1 and row >= 0:
            is_on_row = True
        if col <= self.map.map_width - 1 and col >= 0:
            is_on_col = True

        return is_on_row & is_on_col
        
    def is_not_blocked(self, col, row):
        not_blocked = False
        try:
            if not self.map.foot_map[row][col]:
                not_blocked = True
            for unit in self.map.magic_team:
                if (unit.map_r, unit.map_c) == (row, col):
                    not_blocked = False
            for unit in self.map.boxes:
                if (unit.map_r, unit.map_c) == (row, col):
                    if unit.get_pushed(self.map_r, self.map_c):
                        not_blocked = True
                    else:
                        not_blocked = False
        except IndexError:
            print "Stop trying to walk off the edge!"
        return not_blocked
        
    def is_legal_move(self, col, row):
        return self.is_on_board(col, row) & self.is_not_blocked(col, row)
        
class PushableBox(MapMover):
    def on_key_press(self):
        pass

    # tries to get pushed from some direction and lets you know if it succeeds
    def get_pushed(self, pusher_r, pusher_c):
        delta_c = self.map_c - pusher_c
        delta_r = self.map_r - pusher_r
        if delta_c and self.is_legal_move(self.map_c + delta_c, self.map_r):
            self.selector.x += self.step * (delta_c)
            self.map_c += delta_c
            return True
        if delta_r and self.is_legal_move(self.map_c, self.map_r + delta_r):
            self.selector.y += self.step * (delta_r)
            self.map_r += delta_r
            return True
        return False
        
class MapEditor(MapMover):
    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            self.selector.y += self.step
            self.map_r += 1
        if symbol == key.DOWN:
            self.selector.y -= self.step
            self.map_r -= 1
        if symbol == key.RIGHT:
            self.selector.x += self.step
            self.map_c += 1
        if symbol == key.LEFT:
            self.selector.x -= self.step
            self.map_c -= 1
        if symbol == key.Z:
            if self.map.foot_map[self.map_r][self.map_c] == 1:
                changed_tile = 0
            else:
                changed_tile = 1
            self.map.foot_map[self.map_r][self.map_c] = changed_tile    
            self.map.redraw_map()
        if symbol == key.X:
            for unit in self.map.boxes:
                if (self.map_r, self.map_c) == (unit.map_r, unit.map_c):
                    unit.selector.batch = None
                    self.map.boxes.remove(unit)
                    return
            self.map.boxes.append(PushableBox(
                                    self.map,
                                    self.map_c,
                                    self.map_r,
                                    resources.box)
                                    )
            self.map.boxes[-1].batch = pyglet.graphics.Batch()
