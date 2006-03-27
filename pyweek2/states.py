import pygame, eventnet.driver, os, sys, sprites
from leveleditor.data.config import get_config
from leveleditor.data.objects import get_grouped_objects
'''
Store states here.
'''

pygame.font.init()

class State(eventnet.driver.Handler):
    '''
    State superclass. Doubles as a dummy state.
    '''
    def __init__(self, screen):
        eventnet.driver.Handler.__init__(self)
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
    def __init__(self, screen, options=['New Game', 'Load Game', 'Level Editor',
                                        'Highscores', 'Help', 'Quit'],
                 title='Main Menu'):
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
        self.evt_prefix = 'MENU_'

    def over_coordinates(self, width, height, top_left):
        '''
        Method to check if the mouse is in a certain position
        '''
        ms_pos = pygame.mouse.get_pos()
        bottom_right = (top_left[0]+width,
                        top_left[1]+height)
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

    def over_image(self, image, top_left):
        '''
        Method to check if the mouse is over an image
        '''
        return self.over_coordinates(image.get_width(),image.get_height(),
                                     top_left)

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

    def EVT_MouseButtonDown(self, event):
        if self.selected <> None: eventnet.driver.post(
            self.evt_prefix+''.join(self.selected.split()))

    def EVT_MENU_Quit(self, event):
        eventnet.driver.post('Quit')
        self.quit()

class GameState(State):

    def __init__(self, screen):
        State.__init__(screen)
        self.sprites = sprites.Group()

    def join_sprite_group(self, sprite):
        self.sprites.add_sprite(sprite)

    def tick(self):
        self.sprites.tick()
