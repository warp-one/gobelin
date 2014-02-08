import pyglet

import menu, level

class Game(object):
    def __init__(self):
        self.current_screen = menu.MainMenu(self)
        self.bounds = (800, 600)
        
    def clearCurrentScreen(self):
        self.current_screen.clear()
        self.window.remove_handlers()
        
    def startCurrentScreen(self):
        self.window.set_handler("on_key_press", self.current_screen.on_key_press)
        self.window.set_handler("on_draw", self.current_screen.on_draw)
        self.current_screen.start()
        
    def startPlaying(self):
        self.clearCurrentScreen()
        self.current_screen = level.LevelAdministrator(self)
        self.startCurrentScreen()
        
    def execute(self):
        self.window = pyglet.window.Window(self.bounds[0], self.bounds[1])
        self.startCurrentScreen()
        pyglet.app.run()
