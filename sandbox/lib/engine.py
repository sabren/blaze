'''
Main module. Use this to run your game.
'''

import pygame, state, eventnet.driver

class Engine(eventnet.driver.Handler):
    '''
    Toplevel control object.
    '''

    DEFAULT = state.State()

    def __init__(self,fps=40):
        eventnet.driver.Handler.__init__(self)
        self.state = None
        self.size = (800,600)
        self.fullscreen = False
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.capture()

    def loadDefaultState(self):
        self.state = self.DEFAULT
        self.state.start()

    def run(self):
        pygame.init()
        if self.fullscreen:
            pygame.display.set_mode(self.size,pygame.FULLSCREEN)
        else:
            pygame.display.set_mode(self.size)
        self.loadDefaultState()

        #mainloop
        while 1:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                eventnet.driver.post(pygame.event.event_name(event.type),
                                     **event.dict)
            if self.state.done and self.state.next:
                self.state = self.state.next
                self.state.start()
            elif self.state.done and not self.state.next:
                self.loadDefaultState()
            else:
                self.state.tick()

    def EVT_Quit(self,event):
        import sys
        sys.exit(0)

if __name__=='__main__':
    e = Engine()
    e.run()
