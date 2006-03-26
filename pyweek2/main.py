'''
"core" of the game
'''

#add your imports here
import pygame, eventnet.driver, sys
from states import State

class game:
    '''
    Game object. Will prob'ly make others (LAN_Game, Net_Game, etc)
    '''

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600)) #windowed for now
        self.load_default_state()

    def tick(self):
        if not self.state.done:
            self.state.tick()
        elif self.state.next <> None:
            self.state = self.state.next
        else: self.load_default_state()

    def load_default_state(self):
        try: self.state.quit()
        except: pass
        self.state = State(self.screen)
        self.state.start()

def main():
    g = game()

    while 1: #mainloop

        #post pygame events to eventnet
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            eventnet.driver.post(pygame.event.event_name(event.type),
                                 **event.dict)

        g.tick()
        
if __name__=='__main__':
    main()
