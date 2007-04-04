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
import data, eventnet.driver

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

        if self._dist(self.level.player.rect.centery,self.rect.centery) < 100 \
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
