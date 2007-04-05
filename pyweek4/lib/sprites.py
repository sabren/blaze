# Ascent of Justice
# Copyright (C) 2007 Team Trailblazer

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from directicus.sprite import Sprite, AnimatedSprite
from directicus.gfx import Animation
from person import Person
import data, eventnet.driver, pygame, random

class Wall(Sprite):

    def __init__(self,pos=(0,0),lvl=None):
        self.image = data.wall
        Sprite.__init__(self)
        self.rect.center = pos
        if lvl:
            lvl.all.add(self)
            lvl.walls.add(self)

class Floor(Sprite):

    def __init__(self,pos=(0,0),lvl=None):
        self.image = data.floor
        Sprite.__init__(self)
        self.rect.center = pos
        if lvl:
            lvl.all.add(self)
            lvl.floors.add(self)

class Camera(AnimatedSprite):

    def __init__(self,pos,lvl):
        self.anim = Animation(data.Camera.anim,True)
        AnimatedSprite.__init__(self)
        self.rect.center = pos
        if lvl:
            lvl.all.add(self)
            lvl.cameras.add(self)
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.direction = 'right'
        self.level = None

    def update(self,level=None):
        self.level = level
        AnimatedSprite.update(self)
        if self.anim.index < 35 or self.anim.index > 205:
            self.direction = 'right'
        elif 138 > self.anim.index > 103:
            self.direction = 'left'
        else:
            self.direction = 'center'
        self.image.set_colorkey(self.image.get_at((0,0)))

        if self.level.player.rect.centery > self.rect.bottom \
           and self._dist(self.level.player.rect) < 500:

            if self.direction == 'left' and \
               self.level.player.rect.right < self.rect.left and \
               200 > self._dist(self.level.player.rect.right,self.rect.left) > 20:
                eventnet.driver.post('alarm',pos=self.rect.center)
            elif self.direction == 'right' and \
                 self.level.player.rect.left > self.rect.right and \
                 200 > self._dist(self.level.player.rect.left,self.rect.right) > 20:
                eventnet.driver.post('alarm',pos=self.rect.center)

    def _dist(self,a,b=None):
        if b == None:
            b = self.rect.center
        if type(a) == type(1):
            return max(a,b)-min(a,b)
        else:
            return (max(a[0],b[0])-min(a[0],b[0]))+(max(a[1],b[1])-min(a[1],b[1]))

class Stair(Sprite):

    def __init__(self,pos,level):
        self.image = data.stairs.copy()
        Sprite.__init__(self)
        self.rect.center = pos
        self.level = level
        self.level.all.add(self)
        self.level.stairs.add(self)
        self.image.set_colorkey(self.image.get_at((10,0)))

class Enemy(Person,eventnet.driver.Handler):
    speed = 2

    def __init__(self,pos,level):
        self.animation_set = data.Enemy()
        eventnet.driver.Handler.__init__(self)
        Person.__init__(self,level)
        self.capture()
        self.rect.center = pos
        self.level = level
        self.level.enemies.add(self)
        self.level.all.add(self)
        self.flying = False
        self.lastpos = self.rect.center
        self.alarm = 0

    def kill(self):
        Person.kill(self)
        self.release()

    def update(self,level):
        Person.update(self,level)
        if self in self.enemies:
            self.enemies.remove(self)
        for ally in pygame.sprite.spritecollide(self,self.level.enemies,False):
            if self.flying:
                if ally.rect.centerx > self.rect.centerx:
                    ally.die(1)
                else:
                    ally.die(-1)
        if pygame.sprite.spritecollideany(self,self.enemies):
            self.rect.center = old
            if self.flying:
                self.audio.play(random.choice(data.punch))
        if self.level.player.rect.colliderect(self.rect):
            enemy = self.level.player
            if enemy.rect.centerx > self.rect.centerx:
                # Enemy is to our right
                if enemy.punching or enemy.kicking:
                    self.die(1)
                    if enemy.kicking:
                        self.flying = True
                        self.vy = -3
                        self.vx = -10
            elif enemy.rect.centerx < self.rect.centerx:
                # Enemy is to our left
                if enemy.punching or enemy.kicking:
                    self.die(-1)
                    if enemy.kicking:
                        self.flying = True
                        self.vy = -3
                        self.vx = 10
        if self.direction == 'left':
            self.vx = -self.speed
        else:
            self.vx = self.speed
        if abs(self.vx) > 3:
            self.vx /= 3
        if (self._dist(self.level.player.rect.bottom,self.rect.bottom) < 20 and \
           (self.direction == 'left' and self.level.player.rect.centerx < self.rect.centerx) or \
           (self.direction == 'right' and self.level.player.rect.centerx > self.rect.centerx) and \
           self._dist(self.level.player.rect.center,self.rect.center) < 500) or \
           self._dist(self.level.player.rect.center,self.rect.center) < 10 or \
           self.alarm:
            self.vx *= 3
            if self._dist(self.rect.center,self.level.player.rect.center) < 7:
                self.vx = 0
                self.punch()
        if self.alarm:
            self.alarm -= 1
        if self._dist(self.lastpos, self.rect.center) < 2:
            if self.direction == 'left':
                self.direction = 'right'
                self.vx = self.speed
            else:
                self.direction = 'left'
                self.vx = -self.speed
            self.rect.centerx += self.vx*2
            Person.update(self,level)
        self.lastpos = self.rect.center

    def EVT_alarm(self,event):
        self.alarm = 480

class Exit(Sprite):

    def __init__(self,pos=(50,0),level=None):
        self.image = data.exitDoor
        Sprite.__init__(self)
        self.rect.center = pos
        self.level = level
        self.level.exit = self
        self.level.all.add(self)

    def update(self,level):
        self.level = level
        if self.rect.colliderect(self.level.player.rect):
            eventnet.driver.post('win')
