
from constants import REPEAT
from states import Gear
import pygame.locals as pg
from events import GAME
import eventnet.driver
from events import LEVELLIST

class Controller(Gear):
    """
    like a gamepad with repeating events...
    """
    def __init__(self):
        super(Controller, self).__init__(None)
        self.buttonsDown = []
        self.ticks = 0
        self.keymap = {
            pg.K_x : GAME.QUIT,
            pg.K_RIGHT : GAME.RIGHT,
            pg.K_LEFT : GAME.LEFT,
            pg.K_UP : LEVELLIST.UP,
            pg.K_DOWN : LEVELLIST.DOWN,
            pg.K_SPACE : GAME.JUMP,
        }

    """def EVT_KeyDown(self, event):
        if event.key in self.keymap:
            eventnet.driver.post(self.keymap[event.key])
            self.buttonsDown.append(self.keymap[event.key])

    def EVT_KeyUp(self, event):
        if event.key in self.keymap:
            self.buttonsDown.remove(self.keymap[event.key])"""

    def tick(self):
        self.ticks += 1
        if self.ticks < REPEAT.TICKS:
            pass
        else:
            self.ticks = 0
            for button in self.buttonsDown:
                eventnet.driver.post(button)            

