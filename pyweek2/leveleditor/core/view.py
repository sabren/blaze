import pygame, eventnet.driver
from states import State

class LEView(eventnet.driver.Subscriber):
    def __init__(self,leveleditor):
        pygame.init()
        self.capture()
        self.leveleditor = leveleditor
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
        self.state = LEState(self.screen,self.leveleditor.config,self.leveleditor.objects)
        self.state.start()
    def EVT_Quit(self):
        self.release()
        self.done = True

class LEWindow(State):
    def __init__(self,screen,config):
        State.__init__(self,screen)
        self.config = config
    def tick(self):
        r = pygame.Rect(100,0,800,600)
        self.screen.fill((0,255,0),r)
        pygame.display.flip()
        
class LEToolbar(State):
    def __init__(self,screen,config,objects):
        State.__init__(self,screen)
        self.config = config
        self.objects = objects
        self.objects_rendered = False
    def tick(self):
        if not self.objects_rendered:
            r = pygame.Rect(0,0,100,600)
            self.screen.fill((255,0,0),r)
            x = 0
            y = 0
            for object in self.objects:
                x,y = object.render(self.screen,r,x,y)
            pygame.display.flip()
            self.objects_rendered = True
        
class LEState(State):
    def __init__(self,screen,config,objects): 
        State.__init__(self,screen)
        self.config = config
        self.objects = objects
        self.window = LEWindow(screen,config)
        self.toolbar = LEToolbar(screen,config,objects)
    def tick(self):
        #self.screen.fill((0,0,0))
        #pygame.display.flip()
        self.window.tick()
        self.toolbar.tick()
    
    
