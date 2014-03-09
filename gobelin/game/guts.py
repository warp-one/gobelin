from random import choice, randint

class Body(object):
    def __init__(self):
        self.body = {'head':  30,
                     'torso': 34,
                     'l_arm': 7,
                     'r_arm': 7,
                     'l_leg': 10,
                     'r_leg': 10}
        self.aptitudes = {
                     'speed': 70,
                     'wit':   15,
                     'heft':  1
                     }
        self._health = self.get_health()
        self._status = self.get_status()
        self.bio = [self._status, self.aptitudes['speed']]
        
    def get_health(self):
        total_HP = 0
        for limb in self.body:
            total_HP += self.body[limb]
        return total_HP
        
    def get_status(self):
        self._health = self.get_health()
        if self._health < 30:
            return "I feel very sick."
        elif self._health < 60:
            return "I am tired and in pain."
        elif self._health < 90:
            return "I am fatigued."
        else:
            return "I feel fine."
            
    def receive_light_melee(self, assailant):
        for limb in self.body:
            this_limb = self.body[limb]
            miss = randint(0, len(self.body))
            if not miss:
                print "HITTT"
                self.body[limb] -= assailant.aptitudes['heft'] + randint(1, 2)
                if this_limb <= 0:
                    print "You lost a {0}.".format(limb)
                    this_limb = 0
                    return self.body.pop(limb)
                return limb
        return False
        