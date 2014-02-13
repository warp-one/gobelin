from math import sqrt

import pyglet
from pyglet.window import key

import cursor

class MobileUnit(cursor.MapMover):
    def __init__(self, *args, **kwargs):
        super(MobileUnit, self).__init__(*args, **kwargs)
        
        self.moments = 7
        
    def on_key_press(self, symbol, modifiers):
        if True:
            super(MobileUnit, self).on_key_press(symbol, modifiers)
            self.moments -= 1
        
class GoblinUnit(MobileUnit):
    def __init__(self, *args, **kwargs):
        super(GoblinUnit, self).__init__(*args, **kwargs)
        self.strong = False
        
    def take_turn(self):
        victim = self.find_nearest_foe()
        while self.moments:
            self.move_toward_foe(victim)
        
    def find_nearest_foe(self):
        foes = []
        range = 10000
        target = None
        for unit in self.map.magic_team:
            distance = sqrt(
                        (self.map_c - unit.map_c) ** 2 +
                        (self.map_r - unit.map_r) ** 2
                        )
            foes.append((unit, int(distance)))
        for pair in foes:
            if pair[1] < range:
                range = pair[1]
                target = pair[0]
        return target
        
    def move_toward_foe(self, target):
        c_diff = self.map_c - target.map_c
        r_diff = self.map_r - target.map_r
        if abs(c_diff) >= abs(r_diff):
            if c_diff > 0:
                self.on_key_press(key.LEFT, None)
            else:
                self.on_key_press(key.RIGHT, None)
        else:
            if r_diff > 0:
                self.on_key_press(key.DOWN, None)
            else:
                self.on_key_press(key.UP, None)