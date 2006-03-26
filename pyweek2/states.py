import pygame, eventnet.driver
'''
Store states here.
'''
pygame.font.init()

class State(eventnet.driver.Subscriber):
    '''
    State superclass.
    '''
    def __init__(self):
        self.next = None

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

class menu_state(State):
    '''
    A superclass for menus
    '''

    def __init__(self, screen, title, options=(), background=None,
                 reg_font=pygame.font.SysFont('Arial', 12),
                 head_font=pygame.font.SysFont('Arial', 20)):
        State.__init__(self)
        if background == None:
            self.background = pygame.Surface((screen.get_width(),
                                              screen.get_height()))
            self.background.fill((0,0,0))
        else: self.background = background
        self.screen = screen
        self.options = options

        self.reg_font = reg_font
        self.reg_height = reg_font.get_ascent()+font.get_descent()+5

        head_font.set_underline(True)
        self.title_pos = (
            (screen.get_width()/2)-(head_font.size(title)[0]/2),
            (screen.get_height()/2)-(head_font.size(title)[1]/2))
        self.title = self.head_font.render(title, True, (255,255,255))
        
    def tick(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.title, self.title_pos)
        #for option in options:
            
            
