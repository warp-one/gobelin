import pyglet
from pyglet.window import key

from map_mover import MapMover
import resources

class MapEditor(MapMover):
    def __init__(self, *args, **kwargs):
        super(MapEditor, self).__init__(*args, **kwargs)
        self.moments = 0
        self.confirm = False
        self.selector.visible = True
        
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
        if symbol == key._1 and self.last_key == key.C:
            grid_index = 0
            for row in range(8):
                for col in range(8):
                    tile_location = (col + self.map_x, row + self.map_y)
                    changed_tile = whole_map[tile_location]
                    changed_tile.become_doodad('supermarket')
                    changed_tile.selector.image = resources.spmkt_tiles[grid_index]
                    changed_tile.fog.image = resources.smfog_tiles[grid_index]
                    changed_tile.verticals.image = resources.smsign_tiles[grid_index]
                    changed_tile.verticals.x = changed_tile.selector.x
                    changed_tile.verticals.y = changed_tile.selector.y
                    changed_tile.verticals.batch = changed_tile.selector.batch
                    changed_tile.verticals.group = self.game_map.level.frontground
                    for pt in changed_tile.pathable_tiles:
                        if tile_location == (pt[0] + self.map_x, pt[1] + self.map_y):
                            changed_tile.pathable = True
                    grid_index += 1
                
        self.last_key = symbol

    def is_legal_move(self, col, row):
        return True