'''
"core" of the game
'''

#add your imports here
import pygame, eventnet.driver, sys, states, os
from jukebox import Jukebox

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
        self.next = next
        self.release() # stop listening

class Menu(State):
    def __init__(self, screen, options=['Single Player', 'Level Editor',
                                        'Options', 'Quit'],
                 title='Clad in Iron'):
        State.__init__(self, screen)
        self.selected = None
        title_font = pygame.font.SysFont('Arial', 50, bold=True)
        title_font.set_underline(True)
        self.title = title_font.render(title, True, (0,0,0))
        self.title_pos = ((screen.get_width()/2)-(self.title.get_width()/2),
                          100)
        self.reg_font = pygame.font.SysFont('Arial', 40)
        self.screen = screen
        self.options = options
        self.evt_prefix = 'MENU_'

        self.background = pygame.image.load(
            os.path.join('data', 'background.bmp'))
        frame = pygame.Surface((800,600))
        frame.fill((255,255,255))
        frame.set_alpha(100)
        self.background.blit(frame, (0,0))

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
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.title, self.title_pos)
        y = self.title_pos[1]+self.title.get_height()+10
        for option in self.options:
            if self.selected == option:
                img = self.reg_font.render(option, True, (255,255,255))
            else:
                img = self.reg_font.render(option, True, (0,0,0))
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

    def EVT_MENU_SinglePlayer(self, event):
        self.quit(states.SinglePlayerMenu(self.screen))

    def EVT_MENU_LevelEditor(self, event):
        self.quit(states.EditChoice(self.screen))

class game(eventnet.driver.Handler):
    '''
    Game object. Will prob'ly make others (LAN_Game, Net_Game, etc)
    '''

    def __init__(self):
        eventnet.driver.Handler.__init__(self)
        pygame.init()
        pygame.display.set_caption('Clad in Iron')
        pygame.display.set_icon(pygame.image.load(
            os.path.join('data', 'flag.jpg')))
        self.capture()
        self.done = False
        self.screen = pygame.display.set_mode((800, 600)) #windowed for now
        self.volume = 0.2
        self.jkbx = Jukebox()
        self.jkbx.load_song('confedmarch')
        self.jkbx.play_song('confedmarch')
        self.load_default_state()

    def tick(self):
        self.jkbx.set_song_volume(self.volume)
        for sound in self.jkbx.get_sounds():
            sound.set_volume(self.volume)
        if not self.jkbx.is_song_playing(): self.jkbx.play_random_song()
        if not self.state.done:
            self.state.tick()
        elif self.state.next <> None:
            self.state = self.state.next
            self.state.start()
        else: self.load_default_state()

    def load_default_state(self):
        #try:catch is because the first time this is called there is
        #no self.state
        try: self.state.quit()
        except: pass
        self.state = Menu(self.screen)
        self.state.start()

    def EVT_Quit(self, event):
        self.release()
        self.done = True

    def EVT_KeyDown(self, event):
        if event.key == pygame.K_F9:
            fn = 'screenshot.bmp'
            num = 0
            while 1:
                try:
                    open(fn).close()
                except:
                    break
                fn = 'screenshot%s.bmp' % str(num)
                num += 1
            pygame.image.save(self.screen, fn)
        elif event.key == pygame.K_KP_PLUS and self.volume < 1.0:
            self.volume += 0.1
        elif event.key == pygame.K_KP_MINUS and self.volume > 0.0:
            self.volume -= 0.1
        

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
