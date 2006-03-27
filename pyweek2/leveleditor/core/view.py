import pygame, eventnet.driver, os
from states import State,Menu
from grid import Grid

class LEView(eventnet.driver.Handler):
    def __init__(self,leveleditor):
        eventnet.driver.Handler.__init__(self) 
        pygame.init()
        self.capture()
        self.leveleditor = leveleditor
        self.done = False
        self.object = None
        self.screen = pygame.display.set_mode((800, 600)) #windowed for now
        self.evt_prefix = 'LE_'
        self.load_default_state()
    def tick(self):
        if not self.state.done:
            self.state.tick()
            if self.state.toolbar.selected:
                self.state.window.object = self.state.toolbar.selected
        elif self.state.next <> None:
            self.state = self.state.next
        else: self.load_default_state()
    def load_default_state(self):
        try: self.state.quit()
        except: pass
        self.state = LEState(self.screen,self.leveleditor.config,self.leveleditor.objects)
        self.state.start()
    def EVT_Quit(self,event):
        self.release()
        self.done = True
    def EVT_MouseButtonDown(self, event):
        pos = pygame.mouse.get_pos()
        if self.state.toolbar.is_in_save_pos(pos):
            self.state.window.grid.save_level()
        else:
            self.state.window.grid.add_object_in_pos(self.state.window.object,pos)
    def EVT_MouseButtonUp(self, event):
        pass

class LEWindow(State):
    def __init__(self,screen,config):
        State.__init__(self,screen)
        self.config = config
        self.object = None
        self.rect = pygame.Rect(100,0,700,600)
        width,height = map(int,self.config['screen_size'].split('x'))
        tile_size = int(config['tile_size'])
        self.screen.fill((255,255,255),self.rect)
        self.grid = Grid(width,height,tile_size,(700,600),screen)
        
    def tick(self):
        self.grid.render()
        pygame.display.flip()

class LEToolbar(Menu):
    def __init__(self,screen,config,objects):
        State.__init__(self,screen)
        self.config = config
        self.objects = objects
        self.object_positions = []
        self.selected = None
        self.rect = pygame.Rect(0,0,100,600)
        self.title_font = pygame.font.SysFont('Arial', 15)
        self.save_location = []
        self.draw_items()

    def is_in_save_pos(self,pos):
        if len(self.save_location) == 4:
            if pos[0] >= self.save_location[0] and pos[0] <= self.save_location[2] and pos[1] >= self.save_location[1] and pos[1] <= self.save_location[3]:
                return True
        return False
        
    def draw_items(self):
        self.screen.fill((255,255,255),self.rect)
        img = self.title_font.render("SAVE LEVEL",True,(0,0,0))
        x = 2
        y = 550
        self.screen.blit(img, (x,y))
        self.screen.fill((0,0,0),pygame.Rect(100,0,1,600))
        self.save_location = [x,y,x+img.get_width(),y+img.get_height()]
        x = 0
        y = 0
        for group,objects_in_group in self.objects.iteritems():
            img = self.title_font.render(group, True, (0,0,0))
            x = (self.rect.width/2)-(img.get_width()/2)
            self.screen.blit(img, (x,y))
            y += img.get_height()+5
            for object in objects_in_group:
                x,y = object.render(self.screen,self.rect,x,y,os.path.join(self.config['sprites_path'],object.sprite))
        pygame.display.flip()

    def highlight_object(self,object):
        object.highlight(self.screen)
        pygame.display.flip()
        
    def unhighlight_object(self,object):
        if object is None: return
        object.unhighlight(self.screen)
        pygame.display.flip()

    def tick(self):
        selected = None
        for group,objects_in_group in self.objects.iteritems():
            for object in objects_in_group:
                width = object.get_width()
                height = object.get_height()
                top_left = object.get_top_left()
                if self.over_coordinates(width,height,top_left):
                    selected = object
                    if selected == self.selected: return
                    else: 
                        self.unhighlight_object(self.selected)
                        self.selected = object
        if not self.selected is None: self.highlight_object(self.selected)
        else: self.draw_items()

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
