from events import MENU
from states import State, EXIT
from game import Game
import images
import eventnet.driver
from pygame.locals import *

class Scores(State):

    def kick(self):
        super(Scores, self).kick()
        self.display.showImage(0,0, images.SCORES)

    def EVT_KeyDown(self, event):
        if not self.done:
            self.done = True

