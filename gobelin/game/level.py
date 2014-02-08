from pyglet.window import key
import pyglet

import screen, test_map, cursor

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

    def start(self):
        self.batch = pyglet.graphics.Batch()
        self.current_map = test_map.TestMap(self, self.batch)
        self.current_map.show_map()

        self.test_mover_1 = cursor.MapMover(self.current_map)
        self.test_mover_1.selector.batch = self.batch
        self.current_map.magic_team.append(self.test_mover_1)
        self.game.window.push_handlers(self.test_mover_1.on_key_press)

        self.test_mover_2 = cursor.MapMover(self.current_map, 3, 3)
        self.test_mover_2.selector.batch = self.batch
        self.current_map.magic_team.append(self.test_mover_2)

        self.selected_unit = 0

    def on_draw(self):
        self.game.window.clear()
        self.batch.draw()

    def clear(self):
        pass