from pyglet.window import key
import pyglet

import screen, test_map, cursor, resources, mob

class LevelAdministrator(screen.Screen):
    def __init__(self, game):
        self.game = game
        self.foreground = pyglet.graphics.OrderedGroup(1)
        self.background = pyglet.graphics.OrderedGroup(0)
        
    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.selected_unit += 1
            if self.selected_unit < len(self.current_map.magic_team):
                pass
            else:
                self.selected_unit = 0
            self.game.window.pop_handlers()
            self.game.window.push_handlers(self.current_map.magic_team[self.selected_unit].on_key_press)
        if symbol == key.ENTER:
            for unit in self.current_map.goblin_team:
                unit.moments = 7
            self.enemy_turn()
            for unit in self.current_map.magic_team:
                unit.moments = 7
        self.current_map.update_map()
            
    def start(self):
        self.batch = pyglet.graphics.Batch()
        self.current_map = test_map.TestMap(self, self.batch)
        self.current_map.redraw_map()

        self.test_mover_1 = mob.MobileUnit(self.current_map)
        self.test_mover_1.selector.batch = self.batch
        self.current_map.magic_team.append(self.test_mover_1)
        self.game.window.push_handlers(self.test_mover_1.on_key_press)

        self.test_mover_2 = mob.MobileUnit(self.current_map, 5, 5, resources.magic_w)
        self.test_mover_2.selector.batch = self.batch
        self.current_map.magic_team.append(self.test_mover_2)
        
        self.test_enemy_1 = mob.GoblinUnit(self.current_map, 10, 10)
        self.test_enemy_1.selector.batch = self.batch
        self.current_map.goblin_team.append(self.test_enemy_1)
        
        self.current_map.place_objects()
        for b in self.current_map.boxes:
            b.selector.batch = self.batch
        
        self.map_editor = cursor.MapEditor(self.current_map, 1, 4, resources.cursor)
        self.map_editor.selector.batch = self.batch
        self.current_map.magic_team.append(self.map_editor)

        self.selected_unit = 0
        
    def enemy_turn(self):
        for unit in self.current_map.goblin_team:
            unit.take_turn()

    def on_draw(self):
        self.game.window.clear()
        self.batch.draw()

    def clear(self):
        pass
        