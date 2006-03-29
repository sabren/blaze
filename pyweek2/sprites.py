import pygame, eventnet.driver, os

def check_collisions(sprite, groups):
    for group in groups:
        collidelist = pygame.sprite.spritecollide(sprite, group, False)
        if collidelist <> []:
            eventnet.driver.post('Collide', collidelist=collidelist+[sprite])

class Group(pygame.sprite.Group, eventnet.driver.Handler):
    '''
    Our base sprite group object.
    '''

    def __init__(self, sprites=[]):
        pygame.sprite.Group.__init__(self, sprites)
        eventnet.driver.Handler.__init__(self)
        self.capture()

    def tick(self):
        self.update()

    def kill(self):
        '''
        Kill all sprites and self-destruct.
        '''

        for sprite in self.sprites():
            sprite.kill()
        self.empty()
        self.release()

class Sprite(pygame.sprite.Sprite, eventnet.driver.Handler):
    '''
    Our sprite base class.
    '''

    def __init__(self, img, groups=[], pos=(0,0)):
        pygame.sprite.Sprite.__init__(self, groups)
        eventnet.driver.Handler.__init__(self)
        self.capture()
        self.image = img
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect = self.rect.move(self.pos)

    def update(self):
        '''
        This is called instead of tick() .
        '''
        self.rect = self.rect.move(self.pos)

    def kill(self):
        '''
        Replaces quit() .
        '''
        self.release()
        pygame.sprite.Sprite.kill(self)

class hero(Sprite):
    '''
    Class to manage the hero.
    INCOMPLETE
    '''

    HULL_IMAGE = pygame.image.load(os.path.join('data', 'hero', 'hull.bmp'))
    TURRET_IMAGE = pygame.image.load(os.path.join('data', 'hero', 'turret.bmp'))
    TURRET_POS = (HULL_IMAGE.get_width()/2, HULL_IMAGE.get_height()/3)

    def __init__(self, pos, groups=[]):
        Sprite.__init__(self, self.HULL_IMAGE, groups, pos)
        self.turret = Sprite(self.TURRET_IMAGE)
        self.hull = Sprite(self.HULL_IMAGE)

enemies = []
