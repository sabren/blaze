
import pygame, eventnet.driver

class Sprite(pygame.sprite.Sprite,eventnet.driver.Handler):
    '''
    When subclassing be sure to specify a Sprite.image before __init__().
    '''

    def __init__(self,**groups):
        pygame.sprite.Sprite.__init__(self, groups)
        eventnet.driver.Handler.__init__(self)
        self.rect = self.image.get_rect()

        self.pointMap = []
        for y in self.image.get_height():
            row = []
            for x in self.image.get_width():
                if self.image.get_at((x,y)):
                    row.append(True)
                else:
                    row.append(False)
            self.pontMap.append(row)

    def ppCollidePoint(self,point):
        '''
        Pixel perfect collision detection.
        '''

        for row in self.pointMap:
            for pixel in row:
                if point == pixel:
                    return True

        return False

    def update(self):
        '''
        Put your per-frame updates here.
        '''

        pass

class AnimatedSprite(Sprite):
    '''
    Takes AnimatedSprite.animation instead of Sprite.image.
    '''

    def __init__(self,**groups):
        Sprite.__init__(self)
        self.image = self.anim.surf

    def update(self):
        self.anim.tick()
