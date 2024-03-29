'''
Main module. Use this to run your game.
'''

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

    def EVT_tick(self,event):
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

if not pygame.font.get_init():
    pygame.font.init()

class Menu(State):
    '''
    A class to display a very simple menu.
    '''

    headerFont = pygame.font.SysFont('Verdana',50)
    headerFont.set_underline(True)
    regularFont = pygame.font.SysFont('Verdana',30)
    color = (255,255,255)
    hover = (100,100,100)
    title = 'Menu Demo'
    options = ['Nothing','Quit']
    background = None
    prefix = 'Menu_'

    def start(self):
        State.start(self)
        if self.background == None:
            self.background = pygame.display.get_surface().copy()
        title = self.headerFont.render(self.title, True, self.color)
        self.background.blit(title,
                             ((self.background.get_width()/2)-(title.get_width()/2),
                              20))
        opts = []
        y = 100
        for option in self.options:
            img = self.regularFont.render(option,True,self.color)
            rect = img.get_rect()
            rect.midtop = (self.background.get_width()/2,y)
            opts.append([option,img,rect])
            y += 50
        self.options = opts
        self.selected = None

    def EVT_tick(self,event):
        pygame.display.get_surface().blit(self.background,(0,0))
        self.selected = None
        for option in self.options:
            old = option
            if option[2].collidepoint(pygame.mouse.get_pos()):
                option[1] = self.regularFont.render(option[0],True,self.hover)
                self.selected = ''.join(option[0].split())
            else:
                option[1] = self.regularFont.render(option[0],True,self.color)
            self.options[self.options.index(old)] = option
            pygame.display.get_surface().blit(option[1],option[2])
        pygame.display.flip()

    def EVT_MouseButtonDown(self,event):
        if self.selected != None:
            eventnet.driver.post(self.prefix + self.selected)

    def EVT_Menu_Quit(self,event):
        eventnet.driver.post('Quit')


class Engine(eventnet.driver.Handler):
    '''
    Toplevel control object.
    '''

    DEFAULT = Menu()

    def __init__(self,fps=20):
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
            for event in pygame.event.get():
                eventnet.driver.post(pygame.event.event_name(event.type),
                                     **event.dict)
            if self.state.done and self.state.next:
                self.state = self.state.next
                self.state.start()
            elif self.state.done and not self.state.next:
                self.loadDefaultState()
            else:
                self.clock.tick(self.fps)
                eventnet.driver.post('tick')

    def EVT_Quit(self,event):
        import sys
        sys.exit(0)

if __name__=='__main__':
    e = Engine()
    e.run()
