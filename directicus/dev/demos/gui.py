import pygame,directicus
from directicus.gui import *
directicus.event.debugging = False

if __name__=='__main__':
    global dragging
    dragging = False
    
    root = Element(
        Element(
            pos=(400,50),
            color=(255,255,255),
            text='GUI Demo',
            font_size=40,
            align=CENTER,
            font_style=(UNDERLINE,ITALIC),
        ),
        Element(
            Element(
                text='Simple Dialog',
                size=(300,15),
                background_color=(0,0,100),
                background_image=pygame.image.load('media/bar.png'),
                background_style=REPEAT_X,
                font_style=(BOLD,ITALIC),
            ),
            Element(
                text='Hello World!',
                color=(255,255,255),
                pos=(5,25),
                size=(100,30),
                font_size=12,
                font_style=NORMAL,
            ),
    
            text='',
            border_left=((150,150,150),1),
            border_right=((50,50,50),1),
            border_bottom=((50,50,50),1),
            background_color=(0,0,0),
            pos=(400,300),
            size=(300,200),
            align=CENTER,
            valign=CENTER,
        ),
    
        background_color=(0,0,0),
        background_image=pygame.image.load('media/lightning.png'),
        size=(800,600),
    )
    
    @directicus.event.eventListener(root.children[1].children[0])
    def onMouseDown(self,event):
        Element.onMouseDown(self,event)
        global dragging
        dragging = True
        
    @directicus.event.eventListener(root)
    def onMouseUp(self,event):
        global dragging
        dragging = False
        
    @directicus.event.eventListener(root.children[1])
    def onMouseMotion(self,event):
        Element.onMouseMotion(self,event)
        self.pos = list(self.pos)
        if dragging:
            self.pos[0] += event.rel[0]
            self.pos[1] += event.rel[1]
            
    class GUIDemo(directicus.engine.State):        
        def start(self):
            directicus.engine.State.start(self)
            pygame.display.set_caption('Directicus Graphical User Interface Demo')
            self.root = pygame.sprite.Group(root)
            self.onTick(None)
            pygame.display.flip()
    
        def onTick(self,event):
            disp = pygame.display.get_surface()
            self.root.update()
            self.root.draw(disp)
            pygame.display.flip()
            
    e = directicus.engine.Engine()
    e.DEFAULT = GUIDemo
    e.size = (800,600)
    e.run()