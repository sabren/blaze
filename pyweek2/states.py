import pygame, eventnet.driver
'''
Store states here.
'''
pygame.font.init()

class State(eventnet.driver.Subscriber):
    '''
    State superclass. Doubles as a dummy state.
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

class Menu(State):
    def __init__(self, screen, options=['New Game', 'Load Game', 'Highscores',
                                        'Help', 'Quit'], title='Main Menu'):
        State.__init__(self, screen)
        self.selected = None
        title_font = pygame.font.SysFont('Arial', 50, bold=True)
        title_font.set_underline(True)
        self.title = title_font.render(title, True, (115,115,115))
        self.title_pos = ((screen.get_width()/2)-(self.title.get_width()/2),
                          100)
        self.reg_font = pygame.font.SysFont('Arial', 40)
        self.screen = screen
        self.options = options

    def over_image(self, image, top_left):
        '''
        Method to check if the mouse is over an image
        '''
        ms_pos = pygame.mouse.get_pos()
        bottom_right = (top_left[0]+image.get_width(),
                        top_left[1]+image.get_height())
        if ms_pos[0] > top_left[0] and ms_pos[0] < bottom_right[0]:
            x = True
        else:
            x = False
        if ms_pos[1] > top_left[1] and ms_pos[1] < bottom_right[1]:
            y = True
        else:
            y = False
        if x and y:
            return True
        else:
            return False

    def tick(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.title, self.title_pos)
        y = self.title_pos[1]+self.title.get_height()+10
        for option in self.options:
            if self.selected == option:
                img = self.reg_font.render(option, True, (255,255,255))
            else:
                img = self.reg_font.render(option, True, (115,115,115))
            x = (self.screen.get_width()/2)-(img.get_width()/2)
            self.screen.blit(img, (x,y))
            if self.over_image(img, (x,y)):
                self.selected = option
            elif self.selected == option:
                self.selected = None
            y += img.get_height()+5
        pygame.display.flip()
