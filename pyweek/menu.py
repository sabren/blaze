from events import MENU
from states import State, EXIT, Scores, Credits, Help, TextInput
from game import Game
from constants import IMAGE
import eventnet.driver
from pygame.locals import *
from levellist import LevelList

class Menu(State):

    def kick(self):
        super(Menu, self).kick()
        self.display.showImage(0,0, IMAGE.MENU)

    def EVT_KeyDown(self, event):
        if not self.done:
            if event.key == K_p:
                eventnet.driver.post(MENU.PLAY)
            elif event.key == K_h:
                #eventnet.driver.post('SCORE')
                pass
            elif event.key == K_e:
                eventnet.driver.post('HELP')
            elif event.key == K_c:
                eventnet.driver.post('CREDITS')
            elif event.key == K_1:
                #eventnet.driver.post('HIGHSCORE')
                pass
            elif event.key == K_x:
                eventnet.driver.post(MENU.EXIT)

    def EVT_HIGHSCORE(self, event):
        self.done = True
        self.next = TextInput(self.display)
            
    def EVT_MENU_PLAY(self, event):
        # we need done = true in *here* because
        # of the tests...
        self.done = True
        #self.next = Game(self.display)
	self.next = LevelList(self.display)
        
    def EVT_MENU_EXIT(self, event):
        self.done = True
        self.next = EXIT

    def EVT_SCORE(self, event):
        self.done = True
        self.next = Scores(self.display)

    def EVT_CREDITS(self, event):
        self.done = True
        self.next = Credits(self.display)

    def EVT_HELP(self, event):
        self.done = True
        self.next = Help(self.display)

