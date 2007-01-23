
import pygame, eventnet.driver

class State(eventnet.driver.Handler):
    '''
    Master state object.
    '''

    def __init__(self):
        '''
        Setup to run.
        '''
        
        eventnet.driver.Handler.__init__(self)
        self.done = True
        self.next = None

    def start(self):
        '''
        Set the state running.
        '''

        self.capture() #start eventnet
        self.done = False

    def tick(self):
        '''
        Called once every frame.
        '''

        pass

    def quit(self, next=None):
        '''
        Call when finished. If next is none default state will load.
        '''
        
        self.release()
        self.next = next
        self.done = True
