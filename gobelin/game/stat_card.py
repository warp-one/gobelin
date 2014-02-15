import pyglet

class StatLabel(pyglet.text.Label):
    def __init__(self, *args, **kwargs):
        super(StatLabel, self).__init__(*args, **kwargs)
        self.unit = None
        
    def die(self):
        self.batch = None
        self.unit.stat_card.remove(self)