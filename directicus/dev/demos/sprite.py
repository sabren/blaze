import pygame,directicus
directicus.event.debugging = False

if __name__=='__main__':
    class MySprite(directicus.sprite.Sprite):
        image = pygame.image.load('media/howitzer.png')
        usePP = True
    
    sprite = MySprite()
    sprite.rect.center = (150,100)
    
    class MyState(directicus.engine.State):
        def start(self):
            directicus.engine.State.start(self)
            pygame.display.set_caption('Directicus Sprite Collision Demo')
            disp = pygame.display.get_surface()
            disp.blit(sprite.image,sprite.rect)
            pygame.display.flip()
            
        def onTick(self,event):
            sprite.update()
            
        def onMouseMotion(self,event):
            if sprite.collidePoint(event.pos):
                print 'Collision!'
                
    e = directicus.engine.Engine()
    e.size = (300,200)
    e.DEFAULT = MyState
    e.run()