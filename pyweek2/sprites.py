import pygame, eventnet.driver, os, math

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

    HULL_IMAGE = pygame.image.load(os.path.join('data', 'hero', 'hull.png'))
    center = (HULL_IMAGE.get_width()/2, HULL_IMAGE.get_height()/2)
    if HULL_IMAGE.get_width() > HULL_IMAGE.get_height():
        img = pygame.Surface((HULL_IMAGE.get_width(),
                              HULL_IMAGE.get_height()+10))
    else:
        img = pygame.Surface((HULL_IMAGE.get_height(),
                              HULL_IMAGE.get_height()))
    img.set_colorkey((0,0,0))
    img.fill((0,0,0))
    img.blit(HULL_IMAGE, ((img.get_width()/2)-center[0],
                          (img.get_height()/2)-center[1]))
    HULL_IMAGE = img

    TURRET_IMAGE = pygame.image.load(os.path.join('data', 'hero',
                                                  'turret.png'))
    center = (TURRET_IMAGE.get_width()/2, TURRET_IMAGE.get_height()/2)
    if TURRET_IMAGE.get_width() > TURRET_IMAGE.get_height():
        img = pygame.Surface((TURRET_IMAGE.get_width(),
                              TURRET_IMAGE.get_height()+10))
    else:
        img = pygame.Surface((TURRET_IMAGE.get_height(),
                              TURRET_IMAGE.get_height()))
    img.set_colorkey((255,255,255))
    img.fill((255,255,255))
    img.blit(TURRET_IMAGE, ((img.get_width()/2)-center[0],
                            (img.get_height()/2)-center[1])
             )
    TURRET_IMAGE = img
    TURRET_POS = (
            (HULL_IMAGE.get_width()/2)-(TURRET_IMAGE.get_width()/2),
            (HULL_IMAGE.get_height()/2)-(TURRET_IMAGE.get_width()/2))

    def __init__(self, pos, groups=[]):
        self.turret = self.TURRET_IMAGE
        self.turret_angle = 0
        self.hull = self.HULL_IMAGE
        self.hull_angle = 0
        self.image = self.hull.copy()
        self.image.blit(self.turret, self.TURRET_POS)
        Sprite.__init__(self, self.image, groups,
                        pos=self.image.get_rect().topleft)
        self.rect = self.rect.move(pos)
        self.rect = self.hull.get_rect()

    def update(self):
        pass

    def move(self, x, y):# x,y are from top left.
        self.rect.move_ip(x,y)
        self._position_parts()

    def rotate_turret(self):
        y = pygame.mouse.get_pos()[0] - pygame.display.get_surface().get_width()/2
        x = pygame.mouse.get_pos()[1] - pygame.display.get_surface().get_height()/2
        if x == 0:
            x = 1
        if y == 0:
            y = 1
        angle = math.atan(float(y)/float(x)) * 57.295779513082323
        if x < 0:
            angle += 179
        if angle < 0:
            angle += 360
        angle += 180
        self.turret = pygame.transform.rotate(self.TURRET_IMAGE, angle)

        self.image = self.hull.copy()
        self.image.blit(self.turret, (
            (self.hull.get_width()/2)-(self.turret.get_width()/2),
            (self.hull.get_height()/2)-(self.turret.get_width()/2)))

    def rotate_hull(self, angle):
        self.hull.image = pygame.transform.rotate(self.HULL_IMAGE, angle)
        self.image = self.hull.copy()
        self.image.blit(self.turret, (
            (self.hull.get_width()/2)-(self.turret.get_width()/2),
            (self.hull.get_height()/2)-(self.turret.get_width()/2)))
        self.rect = self.hull.get_rect()

    def _position_parts(self):
        """Position turret and hull relative to hero.rect"""
        self.turret.rect.midtop = self.rect.midtop
        self.hull.rect.midbottom = self.rect.midbottom

enemies = [Sprite(
    pygame.image.load(os.path.join('data', 'enemies', 'dummy.bmp')))]
