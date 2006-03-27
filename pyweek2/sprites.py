import pygame, eventnet.driver

class Group(pygame.sprite.Group, eventnet.driver.Subscriber):
    '''
    Our base sprite group object.
    '''

    def __init__(self):
        self.capture()
        pygame.sprite.Group.__init__(self)

    def tick(self):
        self.update()
        self.draw()

    def add_sprite(self, sprite):
        self.sprites.append(sprite)

    def kill(self):
        '''
        Kill all sprites and self-destruct.
        '''

        for sprite in self.sprites:
            sprite.kill()
        self.empty()
        self.release()

class Sprite(pygame.sprite.Sprite, eventnet.driver.Subscriber):
    '''
    Our sprite base class.
    '''

    def __init__(self, img, groups=[], pos=(0,0)):
        self.capture()
        pygame.sprite.Sprite.__init__(self, groups)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.move(self.pos)
        self.pos = pos

    def update(self):
        '''
        This is called instead of tick() .
        '''
        self.rect = self.image.get_rect()
        self.rect.move(self.pos)
        pass

    def kill(self):
        '''
        Replaces quit() .
        '''
        self.release()
        pygame.sprite.Sprite.kill(self)

class hero(eventnet.driver.Handler):
    '''
    Class to manage the hero.
    INCOMPLETE
    '''

    HULL_IMAGE = pygame.image.load(os.path.join('data', 'hero', 'hull.bmp'))
    TURRET_IMAGE = pygame.image.load(os.path.join('data', 'hero', 'turret.bmp'))
    TURRET_POS = (HULL_IMAGE.get_width()/2, HULL_IMAGE.get_height()/3)

    def __init__(self, pos):
        Sprite.__init__(self)
        self.turret = Sprite(TURRET_IMAGE)
        self.hull = Sprite(HULL_IMAGE)

