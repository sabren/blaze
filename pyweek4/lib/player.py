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
from data import Hero
from eventnet.driver import Handler
import pygame

class Player(AnimatedSprite,Handler):
    '''
    Our hero.
    '''

    anim = Hero.walk_right
    level = None
    speed = 3
    vy = 3
    vx = 0

    def __init__(self):
        AnimatedSprite.__init__(self)
        self.capture()
        self.rect.topleft = (0,0)
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.attacking = False

    def kill(self):
        self.release()
        AnimatedSprite.kill(self)

    def update(self,level):
        self.level = level
        self.image = self.anim.seq[0]
        old = self.rect.center
        self.rect.centery += self.vy
        clampRect = pygame.Rect(self.level.s)
        clampRect.topleft = (0,0)
        if self.vy:
            self.vy += 0.1

        if pygame.sprite.spritecollideany(self,self.level.floors) or \
           pygame.sprite.spritecollideany(self,self.level.walls):
            self.rect.center = old

        old = self.rect.center
        self.rect.centerx += self.vx
        if pygame.sprite.spritecollideany(self,self.level.floors) or \
           pygame.sprite.spritecollideany(self,self.level.walls):
            self.rect.center = old

        if self.attacking:
            if self.anim.index == len(self.anim.seq)-1:
                self.recover()
            else:
                AnimatedSprite.update(self)
        elif self.vx > 0:
            i = self.anim.index
            self.anim = Hero.walk_right
            self.anim.index = i
            AnimatedSprite.update(self)
        elif self.vx < 0:
            i = self.anim.index
            self.anim = Hero.walk_left
            self.anim.index = i
            AnimatedSprite.update(self)
        self.image.set_colorkey(self.image.get_at((0,0)))

    def kick(self):
        self.attacking = True
        if self.anim == Hero.walk_left:
            self.anim = Animation(Hero.kick_left,False)
        elif self.anim == Hero.walk_right:
            self.anim = Animation(Hero.kick_right,False)

    def punch(self):
        self.attacking = True
        if self.anim == Hero.walk_left:
            self.anim = Animation(Hero.punch_left,False)
        elif self.anim == Hero.walk_right:
            self.anim = Animation(Hero.punch_right,False)

    def recover(self):
        self.attacking = False
        if self.anim.seq in [Hero.kick_left,Hero.punch_left]:
            self.anim = Hero.walk_left
        elif self.anim.seq in [Hero.kick_right,Hero.punch_right]:
            self.anim = Hero.walk_right

    def EVT_KeyDown(self,event):
        if event.key == pygame.K_RIGHT:
            self.vx = self.speed
        elif event.key == pygame.K_LEFT:
            self.vx = -self.speed
        elif event.key == pygame.K_SPACE:
            self.vy = -3
        elif event.key == pygame.K_LCTRL:
            self.kick()
        elif event.key == pygame.K_LALT:
            self.punch()
        elif event.key == pygame.K_LSHIFT:
            self.vx *= 3

    def EVT_KeyUp(self,event):
        if event.key in (pygame.K_RIGHT,pygame.K_LEFT):
            self.vx = 0
        elif event.key in (pygame.K_LSHIFT,pygame.K_RSHIFT):
            self.vx /= 3
