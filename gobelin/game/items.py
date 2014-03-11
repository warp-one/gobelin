class BaseItem(object):
    def __init__(self):
        self.name = "the wazu-la"
        self.description = "a featureless cube of vague weight"
        self.bearer = None
        self.image = resources.default
        self.image.width = 80
        self.image.height = 80
        # the map associations that units have is only needed if an
        # item is not in a unit inventory
        self.game_map = None
        self.map_x, self.map_y = 0, 0
        
    def use(self):
        print "This item doesn't have a use."

    def _attach(self, bearer):
        self.bearer = bearer
        self.map_x, self.map_y = 0, 0
        
    def _detach(self):
        self.map_x, self.map_y = self.bearer.map_x, self.bearer.map_y
        self.bearer = None
        
    def pick_up(self, bearer):
        self._attach(bearer)
        print "You picked up {0}.".format(self.name)
        
    def discard(self):
        self._detach()
        self.image.visible = False
        print "You dropped {0}.".format(self.name)
        
class Venlafaxine(BaseItem):
    pass
    
class BarkKnife(BaseItem):
    pass
    
class Clavicle(BaseItem):
    pass