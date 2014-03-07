from pyglet.window import key
import pyglet

import screen, test_map, cursor, resources, mob

class LevelAdministrator(screen.Screen):
    def __init__(self, game):
        self.game = game
        self.foreground = pyglet.graphics.OrderedGroup(2)
        self.midground = pyglet.graphics.OrderedGroup(1)
        self.background = pyglet.graphics.OrderedGroup(0)
        self.selected_unit = 0
        self.selected_enemy = 0
        self.selectors = []
        
    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.selected_unit += 1
            if self.selected_unit < len(self.current_map.magic_team):
                pass
            else:
                self.selected_unit = 0
            self.friend_selector.select(self.selected_unit)
            self.game.window.pop_handlers()
            self.game.window.push_handlers(self.current_map.magic_team[self.selected_unit].on_key_press)
        if symbol == key.TAB:
            self.selected_enemy += 1
            if self.selected_enemy < len(self.current_map.goblin_team):
                pass
            else:
                self.selected_enemy = 0
            self.foe_selector.select(self.selected_enemy)
        if symbol == key.ENTER:
            self.enemy_turn()
            for unit in self.current_map.goblin_team:
                unit.moments = unit.speed
                unit.update_stats()
            for unit in self.current_map.magic_team:
                unit.moments = unit.speed
                unit.update_stats()
        if symbol == key.F1:
            self.game.window.pop_handlers()
            self.game.window.push_handlers(self.current_map.map_editor[0])
        if symbol == key.F2:
            self.game.window.pop_handlers()
            self.game.window.push_handlers(self.friend_selector.selected_unit)
        self.current_map.update_map()
        for cursor in self.selectors:
            cursor.update()
            
    def start(self):
        self.batch = pyglet.graphics.Batch()
        self.current_map = test_map.TestMap(self, self.batch)

        self.spawn_magic_team()
        self.spawn_goblin_team()
        
        self.current_map.place_objects()
        for b in self.current_map.boxes:
            b.selector.batch = self.batch
        self.spawn_map_editor()
        self.create_cursors()
        
        self.current_map.redraw()

    def spawn_magic_team(self):
        self.test_mover_1 = mob.MyHim(self.current_map, 2, 8, group = self.foreground)
        self.test_mover_1.selector.batch = self.batch
        self.test_mover_1.fog.batch = self.batch
        self.current_map.magic_team.append(self.test_mover_1)
        self.game.window.push_handlers(self.test_mover_1.on_key_press)

        self.test_mover_2 = mob.MagicWoman(self.current_map, 5, 5, resources.magic_w, self.foreground)
        self.test_mover_2.selector.batch = self.batch
        self.test_mover_2.fog.batch = self.batch
        self.current_map.magic_team.append(self.test_mover_2)
        
        for unit in self.current_map.magic_team:
            unit.wx, unit.wy = 700, 500
            unit.display_stats()
            self.current_map.light_sources.append(unit)
            unit.fog.visible = False
            for stat in unit.stat_card:
                stat.def_x, stat.def_y = 700, 300
            
    def spawn_goblin_team(self):
        self.test_enemy_1 = mob.GoblinUnit(self.current_map, 10, 10, resources.goblin, self.foreground)
        self.test_enemy_1.selector.batch = self.batch
        self.test_enemy_1.fog.batch = self.batch
        self.current_map.goblin_team.append(self.test_enemy_1)
        
        self.test_enemy_2 = mob.GoblinUnit(self.current_map, 6, 1, resources.goblin, self.foreground)
        self.test_enemy_2.selector.batch = self.batch
        self.test_enemy_2.fog.batch = self.batch
        self.test_enemy_2.speed = 45
        self.current_map.goblin_team.append(self.test_enemy_2)
        
        for unit in self.current_map.goblin_team:
            unit.wx, unit.wy = 700, 300
            unit.display_stats()
            for stat in unit.stat_card:
                stat.def_x, stat.def_y = 700, 200

    def enemy_turn(self):
        for unit in self.current_map.goblin_team:
            unit.take_turn()
            
    def spawn_map_editor(self):
        self.map_editor = cursor.MapEditor(self.current_map, 1, 4, resources.cursor)
        self.map_editor.selector.batch = self.batch
        self.current_map.map_editor.append(self.map_editor)
            
    def create_cursors(self):
        self.friend_selector = cursor.Selector(img = resources.select, 
                                        x = 0, 
                                        y = 0,
                                        batch = self.batch,
                                        group = self.midground)
        self.friend_selector.map = self.current_map
        self.friend_selector.units = self.current_map.magic_team
        self.friend_selector.select(self.selected_unit)
#        self.friend_selector.selected_unit.display_stats()

        self.foe_selector = cursor.Selector(img = resources.rslect, 
                                        x = 0, 
                                        y = 0,
                                        batch = self.batch,
                                        group = self.midground)
        self.foe_selector.map = self.current_map
        self.foe_selector.units = self.current_map.goblin_team
        self.foe_selector.select(self.selected_enemy)
        
        self.selectors.extend([self.friend_selector, self.foe_selector])

    def on_draw(self):
        self.game.window.clear()
        self.batch.draw()

    def clear(self):
        pass
        