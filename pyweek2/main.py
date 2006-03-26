'''
"core" of the game
'''

#add your imports here
import pygame, eventnet.driver
from states import state

class game:
    '''
    Game object. Will prob'ly make others (LAN_Game, Net_Game, etc)
    '''

    def __init__(self):
        self.done = False
        self.state = state()
        self.state.start()

    def tick(self):
        if not self.state.done:
            self.state.tick()
        elif self.state.next <> None:
            self.state = self.state.next
        else: self.load_default_state()

    def load_default_state(self):
        self.state.quit()
        self.state = state()
        self.state.start()

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600)) #windowed for now
    g = game()

    while 1: #mainloop

        #post pygame events to eventnet
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit(0)

            eventnet.driver.post(pygame.event.event_name(event.type),
                                 **event.dict)

        g.tick()
        
if __name__=='__main__':
    main()
