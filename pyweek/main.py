"""
script to tie all components together and run game,
please feel free to send me feedack!
Micah
"""

# not sure if we need all of these but they're here just in case
import pygame, unittest
import cPickle, os, sys, string, loader, eventnet.driver, eventnet._pygame, events, string
from pygame.locals import *
from states import *
from display import Display, ImageManager
from events import MENU, INPUT


#function to load all 3 level elements
def load(name):    
    suffixes = ['back.png', 'geom.svg', 'fore.png']
    return ["-".join([name, suf]) for suf in suffixes]

class TestLoad(unittest.TestCase):

    def test(self):
        goal = ["xyz-back.png","xyz-geom.svg","xyz-fore.png"]
        self.assertEquals(goal, load("xyz"))

# The game Console (our master object)
class Console(eventnet.driver.Handler):
    def __init__(self):
        super(Console, self).__init__()
        self.state = MenuState()
        self.capture()
        self.state.kick()
        self.state.run()

    def startState(state):
        self.state = state
        self.state.kick()
        self.state.run()

    def EVT_PLAY(self, event):
        startState(GameState())

    def EVT_MENU(self, event):
        startState(MenuState())

    def EVT_SCORE(self, event):
        startState(HighScoresState())

    def EVT_CREDITS(self, event):
        startState(CreditsState())

    def EVT_Quit(self, event):
        pygame.quit()

    # this proves that the event dictionary is there and functional
    def EVT_KeyDown(self, event):
        if event.key == K_x:
            pygame.quit()
        else:
            print event.key




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



class QuitGameTest(unittest.TestCase):
    def test(self):
        con = Console()
        assert isinstance(con.state,MenuState)
        assert not con.state.done
        eventnet.driver.post(INPUT.QUIT)
        eventnet.driver.post(INPUT.YES)
        assert con.state.done





"""

HOW TO DIE
----------


HOW TO BEAT THE ROOM
--------------------


"""

     
        
class ConsoleTest(unittest.TestCase):
    def test(self):
        con = Console()
        
        # on start, we go to the menu state
        assert isinstance(con.state, MenuState)
        
        # so now we're sitting here looking at
        # the console and it's showing us a menu
        
        # really we're going to hit some buttons
        # so... we're firing off an event.
        
        # so.. let's say we pick "play!"
        eventnet.driver.post(MENU.PLAY)
        
        # now we should be in the game mode
        assert isinstance(con.state, GameState),\
               "the game should start when we pick play"


if __name__=="__main__":

    con = Console()

    disp = Display(t='Kiwi Run')
    imanager = ImageManager (disp.buffer)
    imanager.load ("menu.png")
    imanager.blit ("menu.png")
    disp.flip()

    # load all levels and parse into list
    lvl_list = []
    for lvl in os.listdir('rooms'):

        # adds name of level to list
        if string.find(lvl, '-') == -1:
            lvl_list += [os.path.splitext(lvl)[0]]

    #loop to keep checking for mode changes
    while True:
        for event in pygame.event.get():
            eventnet.driver.post(pygame.event.event_name(event.type),
                                 **event.dict)
        
