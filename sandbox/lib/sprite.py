
import pygame, eventnet.driver

class Sprite(pygame.sprite.Sprite,eventnet.driver.Handler):
    '''
    When subclassing be sure to specify a Sprite.image before __init__().
    '''

    #pixel-perfect collisions
    usePP = False

    def __init__(self,**groups):
        pygame.sprite.Sprite.__init__(self, groups)
        eventnet.driver.Handler.__init__(self)
        self.rect = self.image.get_rect()
        self.points = [] #for collisions

    def collidePoint(self,point):
        self.calcMap()
        return point in self.points

    def calcMap(self):
        '''
        If using pixel perfect (usePP) you need to have a colorkey set.
        '''

        self.points = []
        if self.usePP:
            if self.image.get_colorkey():
                for y in range(self.image.get_height()):
                    for x in range(self.image.get_width()):
                        if self.image.get_at((x,y))[3] > 0:
                            point = (self.rect.x+x, self.rect.y+y)
                            self.points.append(point)
            else:
                raise AttributeError, 'Sprite.image needs a colorkey for this operation!'
        else:
            #just add all pixels
            for y in range(self.image.get_height()):
                for x in range(self.image.get_width()):
                    point = (self.rect.left+x, self.rect.top+y)
                    self.points.append(point)

    def collideSprite(self,sprite):
        sprite.calcMap()
        for point in sprite.points:
            if point in self.points:
                return True

        return False

    def collideGroup(self,group):
        collisions = []
        for sprite in group.sprites():
            if self.collideSprite(sprite):
                collisions.append(sprite)
        return collisions

    def update(self):
        '''
        Put your per-frame updates here.
        '''

        pass

class AnimatedSprite(Sprite):
    '''
    Takes AnimatedSprite.anim instead of Sprite.image.
    '''

    def __init__(self,**groups):
        self.image = self.anim.surf
        Sprite.__init__(self)

    def update(self):
        self.anim.tick()

if __name__=='__main__':
    import engine,state

    Sprite.image = pygame.image.load('howitzer.png')
    Sprite.image.set_colorkey((255,255,255))
    Sprite.usePP = True
    sprite = Sprite()
    sprite.rect.topleft = (50,50)

    s = state.State()
    def tick():
        disp = pygame.display.get_surface()
        disp.fill((0,0,0))
        disp.blit(sprite.image,sprite.rect)
        pygame.display.flip()

    def motion(event):
        if sprite.collidePoint(event.pos):
            print 'COLLISION!!!!'

    s.EVT_MouseMotion = motion

    s.tick = tick
    e = engine.Engine()
    e.DEFAULT = s
    e.size = (300,200)
    e.run()
