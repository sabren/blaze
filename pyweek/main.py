"""
will eventually become script to tie all components together and run game,
please feel free to send me feedack!
Micah
"""

# not sure if we need all of these but they're here just in case
import pygame, unittest
import cPickle, os, sys, string, loader, eventnet.driver, eventnet._pygame, events, string
from pygame.locals import *

# load all levels and parse into list
lvl_list = []
for lvl in os.listdir('rooms'):

    # adds name of level to list
    if string.find(lvl, '-') == -1:
        lvl_list += [os.path.splitext(lvl)[0]]

MENU_PLAY="MENU_PLAY"

#function to load all 3 level elements
def load(file):
    list = []
    lst = ['back.png', 'geom.svg', 'fore.png']
    for x in range(3):
        list += [string.join([file, lst[x]], '-')]
    return list


def allThreeFilenames(base):
    suffixes = ['back.png', 'geom.svg', 'fore.png']
    return ["-".join([base, suf]) for suf in suffixes]


class TestAllThreeFilenames(unittest.TestCase):

    def test(self):
        goal = ["xyz-back.png","xyz-geom.svg","xyz-fore.png"]
        self.assertEquals(goal, load("xyz"))
        self.assertEquals(goal, allThreeFilenames("xyz"))

# superclass for game modes
class State(object):
    def run(self):
        raise NotImplementedError("Abstract Class")


class ExitState(State):
    pass

class MenuState(State):

    def run(self):
        return self.pick(GameState, HighScoreState, CreditsState, ExitState)

    def pick(self, modes):
        # really show a menu and let user pick
        return modes[0]
    
class GameState(State):

    def run(self):
        while True:
            if pause: pass
            if quit: break
            eventStuff()

class HighScoreState(State):
    def run(self):
        #showScoresOnScreen()
        while True:        
            if escape:
                break
            # maybe blit some background animation or whatever..
            
class CreditsState(State):
    def run(self):
        pass
    

class StateManager(object):
    pass

# The game Console (our master object)
class Console(eventnet.driver.Handler):
    def __init__(self):
        super(Console, self).__init__()
        self.state = MenuState()
        self.capture()

    def EVT_MENU_PLAY(self, event):
        self.state = GameState()

con = Console()

# on start, we go to the menu state

# so now we're sitting here looking at
# the console and it's showing us a menu

# really we're going to hit some buttons
# so... we're firing off an event.

# so.. let's say we pick "play!"
eventnet.driver.post(MENU_PLAY)

# now we should be in the game mode

#initialize pygame
pygame.init() 


# set screen size and put it up 
window = pygame.display.set_mode((640, 480)) 
pygame.display.set_caption('Test') 
screen = pygame.display.get_surface()

# activate the event_handler
handle = events.event_handler()
handle.capture()

#loop to keep checking for mode changes
while 1:
    for event in pygame.event.get():
        eventnet.driver.post(event.type, **event.dict)
