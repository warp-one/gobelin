import pyglet
from pyglet.window import key

import resources, terrain, grid, map_mover

class Selector(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(Selector, self).__init__(*args, **kwargs)
        self.game_map = None
        self.units = []
        self.selected_unit = None
        self.identity = 0
        
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
                unit.hide_portrait()
            else:
                for stat in unit.stat_card:
                    stat.x = stat.def_x
                    stat.y = stat.def_y
                unit.show_portrait()
        
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
            
    def fully_lit(self):
        self.visible = True
            
    def in_shadow(self):
        self.visible = True

    def in_darkness(self):
        self.visible = False
        
    def hide(self):
        self.visible = False

class PushableBox(map_mover.MapMover):
    def __init__(self, *args, **kwargs):
        super(PushableBox, self).__init__(*args, **kwargs)
        self.selector.image = resources.random_box()
        self.strong = True
        self.very_strong = False
        self.fog.image = resources.empty
        self.dark.image = resources.empty
        
    def on_key_press(self):
        pass
        
    def _blocked_special(self, col, row):
        if self.game_map.all_tile_cds[(col, row)].boxable:
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
        self.game_map.boxes.remove(self)
        
class Torch(PushableBox):
    def __init__(self, *args, **kwargs):
        super(Torch, self).__init__(*args, **kwargs)
        self.selector.image = resources.torch
        self.fog.image = resources.sshadw
        self.dark.image = resources.flame
        self.brightness = 3
    
    def get_pushed(self, pusher_r, pusher_c, pusher):
        delta_x = self.map_x - pusher_c
        delta_y = self.map_y - pusher_r
        if pusher.very_strong:
            if self.is_legal_move(self.map_x + delta_x, self.map_y + delta_y):
                self.selector.x += self.step * (delta_x)
                self.selector.y += self.step * (delta_y)
                self.map_x += delta_x
                self.map_y += delta_y
                return True
        return False        

    def die(self):
        self.selector.batch = None
        self.game_map.torches.remove(self)
