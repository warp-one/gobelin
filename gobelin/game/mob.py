from math import sqrt
from random import choice, randint

import pyglet
from pyglet.window import key

import map_mover, cursor, resources, terrain, stat_card, guts, grid, portrait

goblin_faces = [resources.unitp11,
                resources.unitp10]

class MobileUnit(map_mover.MapMover):
    def __init__(self, *args, **kwargs):
        super(MobileUnit, self).__init__(*args, **kwargs)
        
        self.name = ("", "")
        self.body = guts.Body()
        self.speed = self.body.aptitudes['speed']
        self.moments = self.speed
        self.wx = 0
        self.wy = 0
        self.stats = []
        self.stat_card = []
        self.health_card = []
        self.selector.visible = True
        
    def on_key_press(self, symbol, modifiers):
        if self.lose_time(15):
            if super(MobileUnit, self).on_key_press(symbol, modifiers):
                if self.stats:
                    self.update_stats()
                return True
            else:
                if self in self.game_map.magic_team:
                    self.gain_time(15)
                return False

    def gain_time(self, duration):
        if duration + self.moments <= self.speed:
            self.moments += duration
        else:
            self.moments = self.speed
        return True

    def lose_time(self, duration):
        if duration <= self.moments:
            self.moments -= duration
            return True
        else:
            return False

    def set_name(self):
        self.name = choice(['not a goblin'])

    def display_stats(self):
        n = 1
        self.stats = [("", self.name), self.body.get_status(), ("time", self.moments)]
        self.stats.extend(self.body.body.items())
        for stat in self.stats:
            new_stat_x = self.wx
            new_stat_y = self.wy - (n * 20)
            label_text = "{0}: {1}".format(stat[0], stat[1])
            new_stat_label = stat_card.StatLabel(
                                    text = label_text,
                                    x = new_stat_x,
                                    y = new_stat_y,
                                    batch = self.game_map.level.batch
                                    )
            new_stat_label.def_x, new_stat_label.def_y = new_stat_x, new_stat_y
            new_stat_label.unit = self
            self.stat_card.append(new_stat_label)
            n += 1

    def update_stats(self):
        current_stat = 0
        self.stats = [("", self.name), ("", self.body.get_status()), ("time", self.moments)]
        self.stats.extend(self.body.body.items())
        for card in self.stat_card:
            stat0, stat1 = self.stats[current_stat][0], self.stats[current_stat][1]
            try:
                if stat0:
                    card.text = "{0}: {1}".format(stat0, stat1)
                else:
                    card.text = "{0}".format(stat1)
            except IndexError:
                print "You tried to use an index of {0}, which was out of range".format(current_stat)
            current_stat += 1
    
    def clear_stats(self):
        pass

    def show_info(self):
        self.show_portrait()
        self.show_stats()
        
    def hide_info(self):
        self.hide_portrait()
        self.hide_stats()

    def hide_portrait(self):
        self.portrait._hide()
        
    def show_portrait(self):
        self.portrait._show()
        
    def hide_stats(self):
        for s in self.stat_card:
            s._hide()
        
    def show_stats(self):
        for s in self.stat_card:
            s._show()

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
        self.portrait = portrait.Portrait(self,
                         img = goblin_faces.pop(randint(0,len(goblin_faces) - 1)),
                         x = self.wx,
                         y = self.wy,
                         batch = self.game_map.batch)
        self.portrait.visible = False
        
    def take_turn(self):
        adjacent_to_foe = False
        victim = self.find_nearest_foe()
        while self.moments > 0:
            for coordinate in grid.target_cross(self):
                if (coordinate[0], coordinate[1]) == (victim.map_x, victim.map_y):
                    adjacent_to_foe = True
            if adjacent_to_foe and self.lose_time(20):
                self.attack(victim)
            elif not adjacent_to_foe and self.lose_time(15):
                self.move_toward_foe(victim)
            else:
                return True
        return False

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
                self.on_key_press(key.LEFT, None):
            else:
                self.on_key_press(key.RIGHT, None):
        else:
            if r_diff > 0:
                self.on_key_press(key.DOWN, None):
            else:
                self.on_key_press(key.UP, None):
                
        
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
        self.name = choice(["Llynze", "Mah Lissa", "E-Fay"])
        self.portrait = portrait.Portrait(self,
                                    img = resources.unitp00,
                                    x = self.wx,
                                    y = self.wy,
                                    batch = self.game_map.batch)
        self.portrait.visible = False
        
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
        self.name = "hemry"
        self.portrait = portrait.Portrait(self,
                                    img = resources.unitp01,
                                    x = self.wx,
                                    y = self.wy,
                                    batch = self.game_map.batch)
        self.portrait.visible = False
        
    def on_key_press(self, symbol, modifiers):
        super(MyHim, self).on_key_press(symbol, modifiers)