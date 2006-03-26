'''
"core" of the game
'''

#add your imports here
import pygame, eventnet.driver

class dummyState:
    '''
    This is an empty state.
    '''
    
    def __init__(self):
        self.next = None

    def start(self):
        '''
        Start the state running. (put initialization here)
        '''
        self.done = False

    def tick(self):
        '''
        Called every frame, put updates here.
        '''
        pass

class game:
    '''
    Game object. Will prob'ly make others (LAN_Game, Net_Game, etc)
    '''

    def __init__(self):
        self.done = False
        self.state = dummyState()
        self.state.start()

    def tick(self):
        if not self.state.done:
            self.state.tick()
        elif self.state.next <> None:
            self.state = self.state.next
        else: self.load_default_state()

    def load_default_state(self):
        self.state.done = True
        self.state = dummyState()
        self.state.start()

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600)) #windowed for now
    game = game()

    while 1: #mainloop

        #post pygame events to eventnet
        for event in pygame.event.get():
            driver.post(pygame.event.event_name(event.type),
                        **event.dict)

        game.tick()
        
