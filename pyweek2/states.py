import pygame, eventnet.driver
'''
Store states here.
'''
pygame.font.init()

class State(eventnet.driver.Subscriber):
    '''
    State superclass.
    '''
    def __init__(self, screen):
        self.next = None
        self.screen = screen

    def start(self):
        '''
        Start the state running. (put initialization here)
        '''
        self.done = False
        self.capture() #start listening for events

    def tick(self):
        '''
        Called every frame, put updates here.
        '''
        pass

    def quit(self, next=None):
        '''
        Exit state and specify next state.
        '''
        self.done = True
        self.release() # stop listening
