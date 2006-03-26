'''
"core" of the game
'''

#add your imports here
import pygame, eventnet.driver, sys, states

class game(eventnet.driver.Subscriber):
    '''
    Game object. Will prob'ly make others (LAN_Game, Net_Game, etc)
    '''

    def __init__(self):
        pygame.init()
        self.capture()
        self.done = False
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
        self.state = states.Menu(self.screen)
        self.state.start()

    def EVT_Quit(self):
        self.release()
        self.done = True

def main():
    g = game()
    while not g.done: #mainloop
        #post pygame events to eventnet
        for event in pygame.event.get():
            eventnet.driver.post(pygame.event.event_name(event.type),
                                 **event.dict)
        g.tick()
    pygame.quit()
        
if __name__=='__main__':
    main()
