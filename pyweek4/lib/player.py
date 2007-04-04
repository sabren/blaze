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
from data import Hero,Enemy
from eventnet.driver import Handler
from person import Person
import pygame

class Player(Person):
    '''
    Our hero.
    '''

    def __init__(self):
        self.animation_set = Hero()
        Person.__init__(self)
        self.rect.topleft = (0,0)

    def EVT_KeyDown(self,event):
        if event.key == pygame.K_RIGHT:
            self.vx = self.speed
        elif event.key == pygame.K_LEFT:
            self.vx = -self.speed
        elif event.key == pygame.K_SPACE:
            self.interact()
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
