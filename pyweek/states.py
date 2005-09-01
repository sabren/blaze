
"""
here we define some states for our console.
"""
import eventnet.driver
import pygame

# this is the base state. it's the superclass.

GameState = 'MENU_PLAY'
MenuState = 'MenuState'
HighScoreState = 'HighScoreState'
CreditsState = 'CreditsState'
ExitState = 'ExitState'

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
    
    def run(self):
        """
        here's the thing that makes it run.

        """
        while not self.done:
            yield self.tick()


## concrete states #########################################

#from game import Game


# move these to separate files if they get big...

class MenuState(State):

    def run(self):
        eventnet.driver.post(self.pick([GameState, HighScoreState,
                                       CreditsState, ExitState]))

    def EVT_MENU_EXIT(self, event):
        pygame.quit()
        
    def pick(self, modes):
        # show a menu and let user pick
        return modes[0]

class GameState(State):
    def run(self):
        pass

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
    
class ExitState(State):
    def run(self):
        pass

class StateManager(object):
    pass



