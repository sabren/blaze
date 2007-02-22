
if __name__=='__main__':
    from directicus import engine
    from directicus.sprite import *
    import pygame

    Sprite.image = pygame.image.load('howitzer.png')
    Sprite.image.set_colorkey((255,255,255))
    Sprite.usePP = True
    sprite = Sprite()
    sprite.rect.topleft = (50,50)

    s = engine.State

    def tick(self,event):
        disp = pygame.display.get_surface()
        disp.fill((0,0,0))
        disp.blit(sprite.image,sprite.rect)
        pygame.display.flip()

    def motion(self,event):
        if sprite.collidePoint(event.pos):
            print 'COLLISION!!!!'

    s.EVT_MouseMotion = motion

    s.EVT_tick = tick
    e = engine.Engine()
    e.DEFAULT = s
    e.size = (300,200)
    e.run()
