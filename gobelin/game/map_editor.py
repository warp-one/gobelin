import pyglet
from pyglet.window import key

from map_mover import MapMover

class MapEditor(MapMover):
    def __init__(self, *args, **kwargs):
        super(MapEditor, self).__init__(*args, **kwargs)
        self.moments = 0
        self.confirm = False
        
    def on_key_press(self, symbol, modifiers):
        super(MapEditor, self).on_key_press(symbol, modifiers)
        whole_map = self.game_map.all_tile_cds
        current_plot = whole_map[(self.map_x, self.map_y)]
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
        if symbol == key.D:
            if current_plot.identity == 'dirt':
                current_plot.become('pit')
            else:
                current_plot.become('dirt')
        if symbol == key.X:
            for unit in self.game_map.boxes:
                if (self.map_y, self.map_x) == (unit.map_y, unit.map_x):
                    unit.die()
                    return
            self.game_map.place_boxes([(self.map_x, self.map_y)])
        if symbol == key.S:
            for unit in self.game_map.torches:
                if (self.map_y, self.map_x) == (unit.map_y, unit.map_x):
                    unit.die()
                    return
            self.game_map.place_torches([(self.map_x, self.map_y)])
        if symbol == key.Q:
            for unit in self.game_map.magic_team:
                unit.moments += 7
        if symbol == key.V:
            if not self.game_map.all_visible:
                self.game_map.all_visible = True
            else:
                self.game_map.all_visible = False
        if symbol == key.DELETE and self.last_key == key.C:
            for tile in whole_map:
                whole_map[tile].become('dirt')
                
        self.last_key = symbol

    def is_legal_move(self, col, row):
        return True