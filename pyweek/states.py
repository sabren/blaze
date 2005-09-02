
"""
here we define some states for our console.
"""
import eventnet.driver
import images
import pygame, display, sys
from pygame.locals import *

# this is the base state. it's the superclass.


class Ticker(eventnet.driver.Handler):
    def __init__(self, display):
        super(Ticker, self).__init__()
        self.display = display
        self.done = False
        self.capture() # listen for events

    def tick(self):
        """
        then it starts ticking...
        by default, each tick does nothing.
        """
        pass


class State(Ticker):

    def __init__(self, display):
        super(State, self).__init__(display)
        self.next = None

    def kick(self):
        """
        you kick it to make it start. :)
        
        This is so we can pause the execution
        of a state and com back to it later.
        (eg, when a confirmation dialog pops
        up or whatever)
        """
        self.done = False
    
    

## concrete states #########################################

#from game import Game


# move these to separate files if they get big...

from events import MENU

class MenuState(State):

    def kick(self):
        self.display.showImage(0,0, images.MENU)

    def EVT_KeyDown(self, event):
        if not self.done:
            
            # picking anything ends the state
            self.done = True
            
            if event.key == K_p:
                eventnet.driver.post(MENU.PLAY)
            elif event.key == K_h:
                eventnet.driver.post('SCORE')
            elif event.key == K_e:
                eventnet.driver.post('HELP')
            elif event.key == K_c:
                eventnet.driver.post('CREDITS')
            elif event.key == K_x:
                sys.exit(0)
            else:
                self.done = False

    def EVT_MENU_PLAY(self, event):
        self.next = GameState(self.display)

    def quit(self, modes):
        self.done = True



class GameState(State):
    pass


class HighScoreState(State):

    def EVT_KeyDown(self, event):
        if not self.done:
            eventnet.driver.post('Quit')
            self.done = True

class CreditsState(State):
    pass
    
class ExitState(State):
    pass

class StateManager(object):
    pass

