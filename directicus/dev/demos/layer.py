from directicus.layer import *
import pygame,directicus
directicus.event.debugging = False

if __name__=='__main__':
    class Gun(directicus.sprite.Sprite):
        image = pygame.image.load('media/howitzer.png')
        
        def __init__(self,pos=(0,0)):
            directicus.sprite.Sprite.__init__(self)
            self.rect.center = pos
        
    class LayerDemo(directicus.engine.State):
        def start(self):
            directicus.engine.State.start(self)
            pygame.display.set_caption('Directicus Layering Demo')
            
            bg1 = pygame.display.get_surface().copy()
            bg2 = pygame.Surface((300,200))
            bg2.fill((100,100,100))
            sprites = [
                Gun((150,100)),
                Gun((145,90)),
                Gun((155,110)),
            ]
            self.layer1 = IsometricLayer(background=bg1,sprites=sprites)
            disp = pygame.display.get_surface()
            self.layer1.start(disp)
            
        def onTick(self,event):
            directicus.engine.State.onTick(self,event)
            disp = pygame.display.get_surface()
            disp.fill((0,0,0))
            self.layer1.render(disp)
            pygame.display.flip()
            
    e = directicus.engine.Engine()
    e.size = (300,200)
    e.DEFAULT = LayerDemo
    e.run()