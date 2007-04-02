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

import pygame,player,data

class Level(object):

    def __init__(self,size=(800,600)):
        self.all = pygame.sprite.Group()
        self.player = player.Player()
        self.all.add(self.player)
        self.s = pygame.sprite.Sprite()
        self.s.image = data.texture('data/textures/brick.jpg',size).convert()
        self.s.rect = self.s.image.get_rect()
        self.background = self.s.image.copy()

    def clear(self):
        self.all.clear(self.s.image,self.background)

    def update(self):
        self.player.update(self)

    def draw(self):
        self.all.draw(self.s.image)
