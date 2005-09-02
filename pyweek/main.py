"""
script to tie all components together and run game,
please feel free to send me feedack!
Micah
"""

# not sure if we need all of these but they're here just in case
import pygame, unittest
import cPickle, os, sys, string, loader, eventnet.driver, eventnet._pygame, events, string
from pygame.locals import *
from menu import Menu
from game import Game
from states import Ticker, EXIT
from display import Display, ImageManager, MockDisplay
from events import MENU, GAME


#function to load all 3 level elements
def load(name):    
    suffixes = ['back.png', 'geom.svg', 'fore.png']
    return ["-".join([name, suf]) for suf in suffixes]

class TestLoad(unittest.TestCase):

    def test(self):
        goal = ["xyz-back.png","xyz-geom.svg","xyz-fore.png"]
        self.assertEquals(goal, load("xyz"))



"""
The Console is the main state machine for our game
system.
"""

class ConsoleTest(unittest.TestCase):
    def test(self):
        con = Console(MockDisplay())
        
        # on start, we go to the menu state
        assert isinstance(con.state, Menu)
        assert not con.done
        assert not con.state.done
        
        # so now we're sitting here looking at
        # the console and it's showing us a menu
        
        # really we're going to hit some buttons
        # so... we're firing off an event.
        
        # so.. let's say we pick "play!"
        eventnet.driver.post(MENU.PLAY)
        con.tick()


        #@TODO: test pause here..
        
        # now we should be in the game mode
        assert isinstance(con.state, Game),\
               "the game should start when we pick play"


        # but let's quit back to the menu:
        eventnet.driver.post(GAME.QUIT)
        eventnet.driver.post(GAME.YES)
        con.tick()

        assert isinstance(con.state, Menu),\
               "quit should take you back to the menu..."

        

        eventnet.driver.post(MENU.EXIT)
        con.tick()
        assert con.done

      

# The game Console (our master object)
from states import Ticker

class Console(Ticker):
    def __init__(self, display):
        super(Console, self).__init__(display)
        self.loadDefaultState()
        self.state.kick()

    def loadDefaultState(self):
        self.state = Menu(self.display)

    def tick(self):
        self.state.tick()
        if self.state.done:
            next = self.state.next
            if next is EXIT:
                self.done = True
            elif next is None:
                self.loadDefaultState()
            else:
                self.state = self.state.next
                self.state.kick()
                


"""
The Game is just one state in the console,
but it's the main one.

Let's start with the end in mind here. The
game is one room at a time, so in terms of
the master state machine (main.Console)
each room can just be its own state. So
there are three ways to exit the game
state:

   - quit -> back to menu -> states.Menu
   - die -> replay room -> states.Game(self.room)
   - beat the room -> go to next room -> NextRoom(self.room)

So NextRoom is responsible for loading the next
room, and if necessary, showing the ending screen. 

So run() should return one of those states.

--

So now that we know what the end is, we need
to figure out how to get there.

HOW TO QUIT
-----------
The user clicks the Quit button.
There's probably a confirmation screen
"""








"""

HOW TO DIE
----------


HOW TO BEAT THE ROOM
--------------------




"""

        
def pygame_events():
    for event in pygame.event.get():
        eventnet.driver.post(pygame.event.event_name(event.type),
                             **event.dict)


if __name__=="__main__":

    disp = Display(t='Kiwi Run')
    con = Console(disp)

    # load all levels and parse into list
    lvl_list = []
    for lvl in os.listdir('rooms'):

        # adds name of level to list
        if string.find(lvl, '-') == -1:
            lvl_list += [os.path.splitext(lvl)[0]]

    #loop to keep checking for mode changes
    while not con.done:
        pygame_events()
        con.tick()
        
    pygame.quit()        
