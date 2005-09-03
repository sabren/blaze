"""
here we define some states for our console.
"""
import pygame, display, sys, eventnet.driver, images
from pygame.locals import *

# Menu moved to menu.py
# Game moved to game.py

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


# other states should do this:
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

class Scores(State):

    def kick(self):
        super(Scores, self).kick()
        self.display.showImage(0,0, images.SCORES)

    def EVT_KeyDown(self, event):
        if not self.done:
            self.done = True

class Credits(State):

    def kick(self):
        super(Credits, self).kick()
        self.display.showImage(0,0, images.CREDITS)

    def EVT_KeyDown(self, event):
        if not self.done:
            self.done = True

class Help(State):

    def kick(self):
        super(Help, self).kick()
        self.display.showImage(0,0, images.HELP)

    def EVT_KeyDown(self, event):
        if not self.done:
            self.done = True

class Exit(State):
    """
    this state represents quitting the system.
    we should check for it explicitly.
    """
    def __init__(self):
        pass
    def kick(self):
        raise TypeError("never kick EXIT!")
    def tick(self):
        raise TypeError("never tick EXIT!")


# and only use the constant. It's a singleton:
EXIT = Exit()
del Exit
