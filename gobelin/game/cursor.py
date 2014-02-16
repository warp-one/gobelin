import pyglet
from pyglet.window import key

import resources, map

class Selector(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(Selector, self).__init__(*args, **kwargs)
        self.map = None
        self.units = []
        self.selected_unit = None
        
    def select(self, unit_index):
        if self.selected_unit:
            self.selected_unit.clear_stats()
        self.visible_units = 0
        for unit in self.units:
            if unit.selector.batch:
                self.visible_units += 1
        if self.visible_units:
            self.selected_unit = self.units[unit_index]
            while not self.selected_unit.selector.batch:
                unit_index += 1
                if unit_index == len(self.units):
                    unit_index = 0
                self.selected_unit = self.units[unit_index]
        else:
            self.selected_unit = None
        self.update()
        
    def update(self):
        if self.selected_unit:
            self.x = self.selected_unit.selector.x
            self.y = self.selected_unit.selector.y
            self.selected_unit.clear_stats()
            self.selected_unit.display_stats()
            return True
        else:
            return False

class MapMover(object):
    def __init__(self, map, map_c=0, map_r=0, img=resources.default, group=None):
        self.map = map
        self.map_c = map_c
        self.map_r = map_r
        self.img = img
        self.group = group
        
        self.strong = True
        
        self.selector = pyglet.sprite.Sprite(
                                  img = self.img,
                                  batch = None,
                                  x = self.map.x + 10*self.map_c,
                                  y = self.map.y + 10*(self.map_r+1),
                                  group = self.group
                                  )
        self.step = self.selector.width

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            if self.is_legal_move(self.map_c, self.map_r + 1):
                self.selector.y += self.step
                self.map_r += 1
                return True
        if symbol == key.DOWN:
            if self.is_legal_move(self.map_c, self.map_r - 1):
                self.selector.y -= self.step
                self.map_r -= 1
                return True
        if symbol == key.RIGHT:
            if self.is_legal_move(self.map_c + 1, self.map_r):
                self.selector.x += self.step
                self.map_c += 1
                return True
        if symbol == key.LEFT:
            if self.is_legal_move(self.map_c - 1, self.map_r):
                self.selector.x -= self.step
                self.map_c -= 1
                return True
        return False

    def is_on_board(self, col, row):
        is_on_row, is_on_col = False, False
        if row <= self.map.map_height - 1 and row >= 0:
            is_on_row = True
        if col <= self.map.map_width - 1 and col >= 0:
            is_on_col = True

        return is_on_row & is_on_col
        
    def is_not_blocked(self, col, row):
        pathable = False
        unoccupied = True
        try:
            if self.map.foot_map[row][col] == 0:
                pathable = True
            if self._blocked_special(col, row):
                pathable = True
            for unit in self.map.magic_team:
                if (unit.map_r, unit.map_c) == (row, col):
                    unoccupied = False
            for unit in self.map.goblin_team:
                if (unit.map_r, unit.map_c) == (row, col):
                    unoccupied = False
            for unit in self.map.boxes:
                if (unit.map_r, unit.map_c) == (row, col):
                    if unit.get_pushed(self.map_r, self.map_c, self):
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
        
class PushableBox(MapMover):
    def on_key_press(self):
        pass
        
    def _blocked_special(self, col, row):
        if self.map.foot_map[row][col] == 2:
            return True

    # tries to get pushed from some direction and lets you know if it succeeds
    def get_pushed(self, pusher_r, pusher_c, pusher):
        delta_c = self.map_c - pusher_c
        delta_r = self.map_r - pusher_r
        if pusher.strong:
            if delta_c and self.is_legal_move(self.map_c + delta_c, self.map_r):
                self.selector.x += self.step * (delta_c)
                self.map_c += delta_c
                return True
            if delta_r and self.is_legal_move(self.map_c, self.map_r + delta_r):
                self.selector.y += self.step * (delta_r)
                self.map_r += delta_r
                return True
        return False
        
    def die(self):
        self.selector.batch = None
        self.map.boxes.remove(self)
        
class MapEditor(MapMover):
    def __init__(self, *args, **kwargs):
        super(MapEditor, self).__init__(*args, **kwargs)
        self.moments = 0
        
    def on_key_press(self, symbol, modifiers):
        super(MapEditor, self).on_key_press(symbol, modifiers)
        if symbol == key.Z:
            if self.map.foot_map[self.map_r][self.map_c] == 1:
                changed_tile = 0
            else:
                changed_tile = 1
            self.map.foot_map[self.map_r][self.map_c] = changed_tile    
        if symbol == key.A:
            if self.map.foot_map[self.map_r][self.map_c] == 2:
                changed_tile = 0
            else:
                changed_tile = 2
            self.map.foot_map[self.map_r][self.map_c] = changed_tile    
        if symbol == key.X:
            for unit in self.map.boxes:
                if (self.map_r, self.map_c) == (unit.map_r, unit.map_c):
                    unit.die()
                    return
            self.map.boxes.append(PushableBox(
                                    self.map,
                                    self.map_c,
                                    self.map_r,
                                    resources.box)
                                    )
        if symbol == key.Q:
            for unit in self.map.magic_team:
                unit.moments += 7
        if symbol == key.V:
            if not self.map.all_visible:
                self.map.all_visible = True
            else:
                self.map.all_visible = False
                
    def is_legal_move(self, col, row):
        return True