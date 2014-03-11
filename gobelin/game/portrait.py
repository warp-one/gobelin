import pyglet

import resources

class Portrait(pyglet.sprite.Sprite):
    def __init__(self, unit, *args, **kwargs):
        super(Portrait, self).__init__(*args, **kwargs)
        self.unit = unit
        self.def_x, self.def_y = unit.wx, unit.wy
        
    def die(self):
        self.batch = None 

    def _show(self):
        self.x, self.y = self.def_x, self.def_y
        self.visible = True

    def _hide(self):
        self.x, self.y = -200, -200
        self.visible = False