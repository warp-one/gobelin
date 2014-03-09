from math import sqrt
from random import choice, randint

import pyglet
from pyglet.window import key

import map_mover, cursor, resources, terrain, stat_card, guts, grid

class MobileUnit(map_mover.MapMover):
    def __init__(self, *args, **kwargs):
        super(MobileUnit, self).__init__(*args, **kwargs)
        
        self.name = ""
        self.body = guts.Body()
        self.speed = self.body.aptitudes['speed']
        self.moments = self.speed
        self.wx = 0
        self.wy = 0
        self.stats = [self.name].extend([self.body.get_status(), self.moments])
        self.stat_card = []
        self.health_card = []
        self.selector.visible = True
        
    def on_key_press(self, symbol, modifiers):
        if self.moments > 0:
            if super(MobileUnit, self).on_key_press(symbol, modifiers):
                self.moments -= 15
                if self.stats:
                    self.stats[2] -= 15
                return True
            else:
                return False

    def set_name(self):
        self.name = choice(['not a goblin'])
                
    def display_stats(self):
        a_number = 0
        self.stats = [self.name, self.body.get_status(), self.moments]
        self.stats.extend(self.body.body.values())
        for stat in self.stats:
            new_stat_x = self.wx
            new_stat_y = self.wy - (a_number * 20)
            new_stat_label = stat_card.StatLabel(
                                    "{0}".format(stat),
                                    x = new_stat_x,
                                    y = new_stat_y,
                                    batch = self.game_map.level.batch
                                    )
            new_stat_label.def_x, new_stat_label.def_y = new_stat_x, new_stat_y
            new_stat_label.unit = self
            self.stat_card.append(new_stat_label)
            a_number += 1

    def update_stats(self):
        current_stat = 0
        self.stats = [self.name, self.body.get_status(), self.moments]
        self.stats.extend(self.body.body.values())
        for stat in self.stat_card:
            try:
                stat.text = "{0}".format(self.stats[current_stat])
            except IndexError:
                print "You tried to use an index of {0}, which was out of range".format(current_stat)
            current_stat += 1
            
    def clear_stats(self):
        pass
        
    def die(self):
        pass
        
class GoblinUnit(MobileUnit):
    def __init__(self, *args, **kwargs):
        super(GoblinUnit, self).__init__(*args, **kwargs)
        self.strong = False
        self.very_strong = False
        self.speed = 30
        self.moments = self.speed
        self.fog.image = resources.shadow
        
    def take_turn(self):
        victim = self.find_nearest_foe()
        while self.moments > 0:
            for coordinate in grid.target_cross(self):
                if (coordinate[0], coordinate[1]) == (victim.map_x, victim.map_y):
                    self.attack(victim)
            self.move_toward_foe(victim)
            
        
    def find_nearest_foe(self):
        foes = []
        enemy_range = 10000
        target = None
        for unit in self.game_map.magic_team:
            distance = sqrt(
                        (self.map_x - unit.map_x) ** 2 +
                        (self.map_y - unit.map_y) ** 2
                        )
            foes.append((unit, int(distance)))
        for pair in foes:
            if pair[1] < enemy_range:
                enemy_range = pair[1]
                target = pair[0]
        return target
        
    def move_toward_foe(self, target):
        c_diff = self.map_x - target.map_x
        r_diff = self.map_y - target.map_y
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
        does_hit = target.body.receive_light_melee(self.body)
        if does_hit and isinstance(does_hit, (int, long)):
            pass
        elif does_hit:
            print "I hit your {0}!".format(does_hit)
        else:
            print "I missed."
        self.moments -= 20
        
                
class MagicWoman(MobileUnit):
    def __init__(self, *args, **kwargs):
        super(MagicWoman, self).__init__(*args, **kwargs)
        self.strong = False
        self.very_strong = False
        self.ready = False
        self.speed = 100000
        self.name = choice(['Llynze', 'Mah Lissa', 'E-Fay'])
        
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
        for coordinate in grid.target_cross(self):
            self.targets.append((coordinate, pyglet.sprite.Sprite(
                       img = resources.target,
                       x = coordinate[1] * self.game_map.step + self.game_map.x,
                       y = (coordinate[0] + 1) * self.game_map.step + self.game_map.y,
                       batch = self.game_map.batch
                       ) ))
        self.ready = True

    def cast_spell(self):
        self.targets = []
        self.ready = False
        
class MyHim(MobileUnit):
    def __init__(self, *args, **kwargs):
        super(MyHim, self).__init__(*args, **kwargs)
        self.strong = True
        self.very_strong = False
        self.speed = 75000
        self.name = 'him'
        
    def on_key_press(self, symbol, modifiers):
        super(MyHim, self).on_key_press(symbol, modifiers)