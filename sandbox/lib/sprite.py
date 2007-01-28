
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

        if self.usePP:
            if self.image.get_colorkey():
                for y in range(self.image.get_height()):
                    for x in range(self.image.get_width()):
                        if self.image.get_at((x,y)) != self.image.get_colorkey():
                            point = (self.rect.left+x, self.rect.top+y)
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
    s = State()
    def tick():
        pygame.display.get_surface().fill((0,0,0))
    Sprite.image = pygame.image.load('howitzer.png')
