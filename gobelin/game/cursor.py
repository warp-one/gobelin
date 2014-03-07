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
            if unit.selector.visible:
                self.visible_units += 1
        if self.visible_units:
            self.selected_unit = self.units[unit_index]
            while not self.selected_unit.selector.visible:
                unit_index += 1
                if unit_index == len(self.units):
                    unit_index = 0
                self.selected_unit = self.units[unit_index]
                self.selected_unit.update_stats()
            self.visible = True
        else:
            self.selected_unit = None
        self.update()
        for unit in self.units:
            if unit != self.selected_unit:
                for stat in unit.stat_card:
                    stat.x = 0
                    stat.y = 0
            else:
                for stat in unit.stat_card:
                    stat.x = stat.def_x
                    stat.y = stat.def_y
        
    def update(self):
        if self.visible:
            if self.selected_unit:
                self.x = self.selected_unit.selector.x
                self.y = self.selected_unit.selector.y
                self.map_x = self.selected_unit.map_x
                self.map_y = self.selected_unit.map_y
                self.selected_unit.update_stats()
                return True
            else:
                self.visible = False
                return False
        else:
            self.selected_unit = None
            self.visible = False
            
class MapMover(object):
    def __init__(self, map, map_x=0, map_y=0, img=resources.default, group=None):
        self.map = map
        self.map_x = map_x
        self.map_y = map_y
        self.img = img
        self.group = group
        
        self.strong = True
        
        self.selector = pyglet.sprite.Sprite(
                                  img = self.img,
                                  batch = None,
                                  x = self.map.x + 10*self.map_x,
                                  y = self.map.y + 10*(self.map_y+1),
                                  group = self.group
                                  )
        self.fog = pyglet.sprite.Sprite(
                                  img = resources.shadow,
                                  batch = None,
                                  x = self.map.x + 10*self.map_x,
                                  y = self.map.y + 10*(self.map_y+1),
                                  group = self.group
                                  )
        self.dark = pyglet.sprite.Sprite(img=resources.dark)
        self.images = [self.selector, self.fog, self.dark]

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
        if (col, row) in self.map.all_tile_cds:
            return True
        else:
            return False
        
    def is_not_blocked(self, col, row):
        current_plot = self.map.all_tile_cds[(col, row)]
        pathable = False
        unoccupied = True
        try:
            if current_plot.pathable:
                pathable = True
            if self._blocked_special(col, row):
                pathable = True
            for unit in self.map.magic_team:
                if (unit.map_y, unit.map_x) == (row, col):
                    unoccupied = False
            for unit in self.map.goblin_team:
                if (unit.map_y, unit.map_x) == (row, col):
                    unoccupied = False
            for unit in self.map.boxes:
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
        
class PushableBox(MapMover):
    def on_key_press(self):
        pass
        
    def _blocked_special(self, col, row):
        if self.map.all_tile_cds[(col, row)].boxable:
            return True

    # tries to get pushed from some direction and lets you know if it succeeds
    def get_pushed(self, pusher_r, pusher_c, pusher):
        delta_x = self.map_x - pusher_c
        delta_y = self.map_y - pusher_r
        if pusher.strong:
            if self.is_legal_move(self.map_x + delta_x, self.map_y + delta_y):
                self.selector.x += self.step * (delta_x)
                self.selector.y += self.step * (delta_y)
                self.map_x += delta_x
                self.map_y += delta_y
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
        current_plot = self.map.all_tile_cds[(self.map_x, self.map_y)]
        if symbol == key.Z:
            if current_plot.identity == 'dirt':
                current_plot.become('wall')
            else:
                current_plot.become('dirt')
        if symbol == key.A:
            if current_plot.identity == 'water':
                current_plot.become('dirt')
            else:
                current_plot.become('water')
        if symbol == key.X:
            for unit in self.map.boxes:
                if (self.map_y, self.map_x) == (unit.map_y, unit.map_x):
                    unit.die()
                    return
            self.map.boxes.append(PushableBox(
                                    self.map,
                                    self.map_x,
                                    self.map_y,
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