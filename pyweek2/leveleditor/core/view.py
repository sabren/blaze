import pygame, eventnet.driver, os
from states import State,Menu

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
        
class LEToolbar(Menu):
    def __init__(self,screen,config,objects):
        State.__init__(self,screen)
        self.config = config
        self.objects = objects
        self.object_positions = []
        self.objects_rendered = False
        self.rect = pygame.Rect(0,0,100,600)
        self.title_font = pygame.font.SysFont('Arial', 15)
        self.draw_items()
        
    def draw_items(self):
        self.screen.fill((255,0,0),self.rect)
        x = 0
        y = 0
        for group,objects_in_group in self.objects.iteritems():
            img = self.title_font.render(group, True, (0,0,0))
            x = (self.rect.width/2)-(img.get_width()/2)
            self.screen.blit(img, (x,y))
            y += img.get_height()+5
            w = img.get_width()
            h = img.get_height()
            self.object_positions.append(((x,y),w,h))
            for object in objects_in_group:
                x,y,w,h = object.render(self.screen,self.rect,x,y,os.path.join(self.config['sprites_path'],object.sprite))
                self.object_positions.append(((x,y),w,h))
        pygame.display.flip()

    def tick(self):
        dirty = False
        for top_left,width,height in self.object_positions:
            if self.over_coordinates(width,height,top_left):
                self.screen.fill((0,0,0),self.rect)
                dirty = True
        if dirty: self.draw_items()

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
    
    
