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
    Our little steamboat.
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
        self.size = self.rect.size
        self.rudder = 0
        self.angle = 0
        self.engine = 0
        self.steam_vent = self.rect.center

    def update(self):
        old_pos = self.image.get_rect().center
        self.course = (math.degrees(-math.sin(math.radians(self.angle))),
                       math.degrees(-math.cos(math.radians(self.angle))))
        if self.engine != 0:
            self.old_pos = self.rect.center
            if self.engine == 1:
                self.angle += self.rudder
                self.rect = self.rect.move((self.course[0]/15,
                                            self.course[1]/15))
            else:
                self.angle -= self.rudder
                self.rect = self.rect.move((-self.course[0]/15,
                                            -self.course[1]/15))

            if self.rudder != 0:
                old_rect = self.rect
                self.hull = pygame.transform.rotate(self.HULL_IMAGE, self.angle)
                self.image = self.hull.copy()
                self.image.blit(self.turret, (
                    (self.hull.get_width()/2)-(self.turret.get_width()/2),
                    (self.hull.get_height()/2)-(self.turret.get_width()/2)))
                self.rect = self.hull.get_rect()
                self.rect.center = old_rect.center
        self.steam_vent = (self.rect.left+(old_pos[0]-self.course[0]/3),
                           self.rect.top+(old_pos[1]-self.course[1]/3))

    def EVT_MouseMotion(self, event):
        y = event.pos[0] - pygame.display.get_surface().get_width()/2
        x = event.pos[1] - pygame.display.get_surface().get_height()/2
        if x == 0:
            x = 1
        if y == 0:
            y = 1
        angle = math.degrees(math.atan(float(y)/float(x)))
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

    def EVT_KeyDown(self, event):
        if event.key in [pygame.K_w, pygame.K_a, pygame.K_d,
                         pygame.K_s]:
            if event.key == pygame.K_d:
                self.rudder = -1
            elif event.key == pygame.K_a:
                self.rudder = 1
            elif event.key == pygame.K_w:
                self.engine = 1
            elif event.key == pygame.K_s:
                self.engine = -1

    def EVT_KeyUp(self, event):
        if event.key in [pygame.K_w, pygame.K_a, pygame.K_d,
                         pygame.K_s]:
            if event.key == pygame.K_d and self.rudder == -1:
                self.rudder = 0
            elif event.key == pygame.K_a and self.rudder == 1:
                self.rudder = 0
            elif event.key == pygame.K_w and self.engine == 1:
                self.engine = 0
            elif event.key == pygame.K_s and self.engine == -1:
                self.engine = 0

enemies = [Sprite(
    pygame.image.load(os.path.join('data', 'enemies', 'howitzer.png')))]
