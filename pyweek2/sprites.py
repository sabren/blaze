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
        self.rect = pygame.Rect(self.pos, self.rect.size)

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
    #TURRET_POS = (HULL_IMAGE.get_width()/2, HULL_IMAGE.get_height()/3)

    def __init__(self, pos, groups=[]):
        Sprite.__init__(self, self.HULL_IMAGE, groups, pos)
        self.turret = Sprite(self.TURRET_IMAGE)
        self.turret.angle = 0
        self.hull = Sprite(self.HULL_IMAGE)
        self.hull.angle = 0
        self.rect = pygame.Rect(0,0,800,600)
        self._position_parts()
        self.rect = pygame.Rect.union(self.hull.rect, self.turret.rect)
        self.rect.move_ip(*pos)
        self._position_parts()

    def update(self):
        self.hull.update()
        self.turret.update()

    def move(self, x, y):# x,y are from top left.
        self.rect.move_ip(x,y)
        self._position_parts()

    def rotate_turret(self, angle):
        self.turret.angle += angle
        old_center = self.turret.rect.center
        self.turret.image = pygame.transform.rotate(
            self.TURRET_IMAGE, self.turret.angle)
        self.turret.rect = self.turret.image.get_rect()
        self.turret.rect.center = old_center

    def rotate_hull(self, angle):
        self.hull.angle += angle
        old_center = self.hull.rect.center
        self.hull.image = pygame.transform.rotate(
            self.HULL_IMAGE, self.hull.angle)
        self.hull.rect = self.hull.image.get_rect()
        self.hull.rect.center = old_center

    def _position_parts(self):
        """Position turret and hull relative to hero.rect"""
        self.turret.rect.midtop = self.rect.midtop
        self.hull.rect.midbottom = self.rect.midbottom

enemies = [Sprite(
    pygame.image.load(os.path.join('data', 'enemies', 'dummy.bmp')))]
