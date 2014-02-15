from math import sqrt

import pyglet
from pyglet.window import key

import cursor, resources, map, stat_card

class MobileUnit(cursor.MapMover):
    def __init__(self, *args, **kwargs):
        super(MobileUnit, self).__init__(*args, **kwargs)
        
        self.speed = 75
        self.moments = self.speed
        self.l_leg = 1.0
        self.r_leg = 1.0
        self.wx = 0
        self.wy = 0
        self.stat_card = []
        
    def on_key_press(self, symbol, modifiers):
        if self.moments > 0:
            if super(MobileUnit, self).on_key_press(symbol, modifiers):
                self.moments -= 15
            
    def display_stats(self):
        self.stats = [self.moments]
        self.stat_card = []
        for stat in self.stats:
            self.stat_card.append(stat_card.StatLabel(
                                    "{0}".format(stat),
                                    x = self.wx,
                                    y = self.wy,
                                    batch = self.map.level.batch
                                    ))
            self.stat_card[-1].unit = self
                                    
    def clear_stats(self):
        for stat in self.stat_card:
            stat.die()
            stat.delete()
        self.stat_card = []
        self.stats = []
        
class GoblinUnit(MobileUnit):
    def __init__(self, *args, **kwargs):
        super(GoblinUnit, self).__init__(*args, **kwargs)
        self.strong = False
        self.speed = 30
        
    def take_turn(self):
        victim = self.find_nearest_foe()
        while self.moments > 0:
            self.move_toward_foe(victim)
        
    def find_nearest_foe(self):
        foes = []
        enemy_range = 10000
        target = None
        for unit in self.map.magic_team:
            distance = sqrt(
                        (self.map_c - unit.map_c) ** 2 +
                        (self.map_r - unit.map_r) ** 2
                        )
            foes.append((unit, int(distance)))
        for pair in foes:
            if pair[1] < enemy_range:
                enemy_range = pair[1]
                target = pair[0]
        return target
        
    def move_toward_foe(self, target):
        c_diff = self.map_c - target.map_c
        r_diff = self.map_r - target.map_r
        if abs(c_diff) >= abs(r_diff):
            if c_diff > 0:
                if not self.on_key_press(key.LEFT, None):
                    self.lose_time(15)
            else:
                if not self.on_key_press(key.RIGHT, None):
                    self.lose_time(15)
        else:
            if r_diff > 0:
                if not self.on_key_press(key.DOWN, None):
                    self.lose_time(15)
            else:
                if not self.on_key_press(key.UP, None):
                    self.lose_time(15)
                
    def lose_time(self, duration):
        self.moments -= duration
                
class MagicWoman(MobileUnit):
    def __init__(self, *args, **kwargs):
        super(MagicWoman, self).__init__(*args, **kwargs)
        self.strong = False
        self.ready = False
        self.speed = 100
        
    def on_key_press(self, symbol, modifiers):
        if not self.ready:
            super(MagicWoman, self).on_key_press(symbol, modifiers)
        if symbol == key.R:
            if not self.ready:
                self.prepare_spell()
            else:
                self.cast_spell()
            
    def prepare_spell(self):
        self.targets = [] 
        for coordinate in map.target_cross(self):
            self.targets.append((coordinate, pyglet.sprite.Sprite(
                                          img = resources.target,
                                          x = coordinate[1] * self.map.step + self.map.x,
                                          y = (coordinate[0] + 1) * self.map.step + self.map.y,
                                          batch = self.map.batch
                                          )))
        self.ready = True

    def cast_spell(self):
        self.targets = []
        self.ready = False 