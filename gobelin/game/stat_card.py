import pyglet

class StatLabel(pyglet.text.Label):
    def __init__(self, *args, **kwargs):
        super(StatLabel, self).__init__(*args, **kwargs)
        self.unit = None
        self.def_x, self.def_y = 700, 300
        
    def die(self):
        self.batch = None 
        