
from events import MENU
from states import State, EXIT
from game import Game
import images
import eventnet.driver
from pygame.locals import *

class Menu(State):

    def kick(self):
        print "kick the menu!"
        super(Menu, self).kick()
        self.display.showImage(0,0, images.MENU)

    def EVT_KeyDown(self, event):
        if event.key == K_p:
            eventnet.driver.post(MENU.PLAY)
        elif event.key == K_h:
            eventnet.driver.post('SCORE')
        elif event.key == K_e:
            eventnet.driver.post('HELP')
        elif event.key == K_c:
            eventnet.driver.post('CREDITS')
        elif event.key == K_x:
            eventnet.driver.post(MENU.EXIT)
            
    def EVT_MENU_PLAY(self, event):
        # we need done = true in *here* because
        # of the tests...
        self.done = True
        self.next = Game(self.display)
        
    def EVT_MENU_EXIT(self, event):
        self.done = True
        self.next = EXIT

    def EVT_SCORE(self, event):
        # high_scores.png is supposed to come on screen
        print 'SCORE'
        self.startState(HighScoresState(), 'high_scores.png')

    def EVT_CREDITS(self, event):
        pass
