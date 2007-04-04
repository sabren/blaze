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

from directicus.sprite import AnimatedSprite
from directicus.gfx import Animation
from eventnet.driver import Handler
import pygame, data

class Person(AnimatedSprite,Handler):
    speed = 3
    animation_set = None

    def __init__(self):
        for name in ['walk_left',
                     'walk_right',
                     'die_back_left',
                     'die_back_right',
                     'die_forward_left',
                     'die_forward_right']:
            anim = getattr(self.animation_set,name)
            setattr(self.animation_set,name,Animation(anim,True))
        self.anim = self.animation_set.walk_right
        AnimatedSprite.__init__(self)
        self.level = None
        self.vy = 3
        self.vx = 0
        self.capture()
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.punching = False
        self.kicking = False
        self.dying = False
        self.direction = 'right'

    def die(self,direction):
        self.dying = True
        if direction == 1:
            # We're attacked from the right
            if self.direction == 'left':
                self.anim = self.animation_set.die_forward_left
            else:
                self.anim = self.animation_set.die_back_right
        else:
            # We're attacked from the left
            if self.direction == 'left':
                self.anim = self.animation_set.die_back_left
            else:
                self.anim = self.animation_set.die_forward_right

    def kill(self):
        self.release()
        AnimatedSprite.kill(self)

    def update(self,level):
        if self.anim in [self.animation_set.walk_left,
                         self.animation_set.punch_left,
                         self.animation_set.die_forward_left,
                         self.animation_set.die_back_left]:
            self.direction = 'left'
        else:
            self.direction = 'right'
        self.level = level
        self.image = self.anim.seq[0]
        old = self.rect.center
        self.rect.centery += self.vy
        if self.vy:
            self.vy += 0.1

        if pygame.sprite.spritecollideany(self,self.level.floors) or \
           pygame.sprite.spritecollideany(self,self.level.walls):
            self.rect.center = old
            self.vy = 0.1
            self.grounded = True

        old = self.rect.center
        self.rect.centerx += self.vx
        if pygame.sprite.spritecollideany(self,self.level.floors) or \
           pygame.sprite.spritecollideany(self,self.level.walls):
            self.rect.center = old

        if self.punching or self.kicking:
            if self.anim.index == len(self.anim.seq)-1:
                self.recover()
            else:
                AnimatedSprite.update(self)
        elif self.dying:
            if self.anim.index < len(self.anim.seq)-1:
                AnimatedSprite.update(self)
                self.rect.centery += 2
                if self.anim in [self.animation_set.die_back_left,
                                 self.animation_set.die_back_right]:
                    if self.direction == 'right':
                        self.rect.centerx -= 2
                    else:
                        self.rect.centerx += 2
                else:
                    if self.direction == 'right':
                        self.rect.centerx += 2
                    else:
                        self.rect.centerx -= 2
            else:
                self.kill()
        elif self.vx > 0:
            i = self.anim.index
            self.anim = self.animation_set.walk_right
            self.anim.index = i
            AnimatedSprite.update(self)
        elif self.vx < 0:
            i = self.anim.index
            self.anim = self.animation_set.walk_left
            self.anim.index = i
            AnimatedSprite.update(self)
        self.image.set_colorkey(self.image.get_at((0,0)))

    def kick(self):
        self.kicking = True
        if self.anim == self.animation_set.walk_left:
            self.anim = Animation(self.animation_set.kick_left,False)
        elif self.anim == self.animation_set.walk_right:
            self.anim = Animation(self.animation_set.kick_right,False)

    def punch(self):
        self.punching = True
        if self.anim == self.animation_set.walk_left:
            self.anim = Animation(self.animation_set.punch_left,False)
        elif self.anim == self.animation_set.walk_right:
            self.anim = Animation(self.animation_set.punch_right,False)

    def recover(self):
        self.kicking = False
        self.punching = False
        if self.anim.seq in [self.animation_set.kick_left,self.animation_set.punch_left]:
            self.anim = self.animation_set.walk_left
        elif self.anim.seq in [self.animation_set.kick_right,self.animation_set.punch_right]:
            self.anim = self.animation_set.walk_right
