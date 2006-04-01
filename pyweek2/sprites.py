#Clad in Iron 0.5
#Copyright (C) 2006 Team Trailblazer
#
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

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
        self.collide_rect = self.rect
        self.health = 100
        self.armor = 100
        self.right_delay = 0
        self.left_delay = 0

    def update(self):
        if self.health < 0:
            eventnet.driver.post('HeroDied')
        if self.left_delay > 0:
            self.left_delay -= 1
        if self.right_delay > 0:
            self.right_delay -= 1
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

    def distance(self, pos):
        a = self.rect.center
        b = pos

        if a[0] > b[0]:
            x = a[0] - b[0]
        else:
            x = b[0] - a[0]
        if a[1] > b[1]:
            y = a[1] - b[1]
        else:
            y = b[1] - a[1]
        return x+y

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

    def EVT_Explosion(self, event):
        if self.rect.collidepoint(event.pos[0], event.pos[1]):
            self.health -= 10
            if self.armor > 0:
                self.armor -= 10
                self.health += (self.armor/10)

class Howitzer(Sprite):
    '''
    An enemy to shoot and be shot at.
    '''

    IMAGE = pygame.image.load(os.path.join('data', 'enemies', 'howitzer.png'))
    def __init__(self, groups=[]):
        Sprite.__init__(self, self.IMAGE, groups,
                        pos=self.IMAGE.get_rect().topleft)
        self.image = self.IMAGE
        self.rect = self.image.get_rect()
        self.target = None
        self.angle = 0
        self.delay = 0

    def distance(self, pos):
        a = self.rect.center
        b = pos

        if a[0] > b[0]:
            x = a[0] - b[0]
        else:
            x = b[0] - a[0]
        if a[1] > b[1]:
            y = a[1] - b[1]
        else:
            y = b[1] - a[1]
        return x+y

    def update(self):
        if self.target != None and self.distance(self.target.center) < 500:
            y = self.rect.centerx - self.target.rect.centerx
            x = self.rect.centery - self.target.rect.centery
            if x == 0:
                x = 1
            if y == 0:
                y = 1
            angle = math.degrees(math.atan(float(y)/float(x)))
            if x < 0:
                angle += 179
            if angle < 0:
                angle += 360

            if self.angle > angle:
                diff = self.angle - angle
            else:
                diff = angle - self.angle
            if diff < 3:
                if self.delay == 0:
                    eventnet.driver.post('Shot', start_pos=self.rect.center,
                                         end_pos=self.target.rect.center)
                    self.delay = 50
                else:
                    self.delay -= 1
            else:
                if self.angle > angle:
                    self.angle -= 5
                else:
                    self.angle += 5
                pos = self.rect.center
                self.image = pygame.transform.rotate(self.IMAGE, self.angle)
                self.rect.center = pos

    def EVT_Explosion(self, event):
        if self.distance(event.pos) < 50:
            self.kill()

enemies = [Sprite(pygame.image.load(os.path.join('data', 'enemies',
                                                 'howitzer.png')))]
