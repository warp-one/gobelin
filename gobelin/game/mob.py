from math import sqrt
from random import choice, randint

import pyglet
from pyglet.window import key

import cursor, resources, map, stat_card

class MobileUnit(cursor.MapMover):
    def __init__(self, *args, **kwargs):
        super(MobileUnit, self).__init__(*args, **kwargs)
        
        self.speed = 75
        self.moments = self.speed
        self.body = 100
        self.wx = 0
        self.wy = 0
        self.stat_card = []
        
    def on_key_press(self, symbol, modifiers):
        if self.moments > 0:
            if super(MobileUnit, self).on_key_press(symbol, modifiers):
                self.moments -= 15
                return True
            else:
                return False
            
    def display_stats(self):
        self.stats = [self.moments]
        self.stats.append(self.body)
        self.stat_card = []
        a_number = 0
        for stat in self.stats:
            self.stat_card.append(stat_card.StatLabel(
                                    "{0}".format(stat),
                                    x = self.wx,
                                    y = self.wy - a_number * 20,
                                    batch = self.map.level.batch
                                    ))
            self.stat_card[-1].unit = self
            a_number += 1
                                    
    def clear_stats(self):
        for stat in self.stat_card:
            self.stat_card.remove(stat)
            stat.delete()
            stat.die()
        self.stat_card = []
        self.stats = []
        
    def die(self):
        print "WE DIED!"
        
class GoblinUnit(MobileUnit):
    def __init__(self, *args, **kwargs):
        super(GoblinUnit, self).__init__(*args, **kwargs)
        self.strong = False
        self.speed = 30
        self.moments = self.speed
        
    def take_turn(self):
        victim = self.find_nearest_foe()
        while self.moments > 0:
            for coordinate in map.target_cross(self):
                if (coordinate[0], coordinate[1]) == (victim.map_c, victim.map_r):
                    self.attack(victim)
                    print "got 'im, boss"
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
        
    def attack(self, target):
        target.body -= 13 + randint(1,3)
        if target.body <= 0.0:
            target.die()
        self.moments -= 20
        
                
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
        
class MyHim(MobileUnit):
    def __init__(self, *args, **kwargs):
        super(MyHim, self).__init__(*args, **kwargs)
        self.strong = True
        self.speed = 75
        
    def on_key_press(self, symbol, modifiers):
        super(MyHim, self).on_key_press(symbol, modifiers)