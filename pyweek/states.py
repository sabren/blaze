
"""
here we define some states for our console.
"""
import eventnet.driver
import pygame, display, sys
from pygame.locals import *

GameState = 'PLAY'
MenuState = 'MENU'
HighScoreState = 'SCORE'
CreditsState = 'CREDITS'
HelpState = 'HELP'
# this is the base state. it's the superclass.

class State(eventnet.driver.Handler):

    def __init__(self):
        super(State, self).__init__()
        self.done = False
        self.next = None
        self.capture() # listen for events

    def kick(self):
        """
        you kick it to make it start. :)
        
        This is so we can pause the execution
        of a state and com back to it later.
        (eg, when a confirmation dialog pops
        up or whatever)
        """
        self.done = False
    
    def tick(self):
        """
        then it starts ticking...
        """
        raise NotImplementedError("you need to override tick()")
    

## concrete states #########################################

#from game import Game


# move these to separate files if they get big...

class MenuState(State):

    def EVT_KeyDown(self, event):
        if not self.done:
            self.done = True
            if event.key == K_p:
                eventnet.driver.post('PLAY')
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

