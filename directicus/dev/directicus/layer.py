# Directicus
# Copyright (C) 2006-2007 Team Trailblazer

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

'''
Level object
'''

import pygame,cPickle,sprite,gui

class Layer(gui.Element):
    def start(self,dest=None):
        self.update()
        if dest:
            dest.blit(self.image,(0,0))
    
    def update(self):
        gui.Element.update(self)
        self._children.update()
        self._children.draw(self.image)

def makeIsometric(group):
    if not isinstance(group,pygame.sprite.OrderedUpdates):
        group = pygame.sprite.OrderedUpdates(group.sprites())
    group._spritelist.sort(lambda a,b:-1+(int(a.rect.bottom > b.rect.bottom)*2))

class IsometricLayer(Layer):
    '''
    Renders sprites from back to front.
    '''

    def start(self,dest=None):
        Layer.start(self,dest)
        self._children = pygame.sprite.OrderedUpdates(self._children.sprites())

    def update(self):
        if not isinstance(self._children,pygame.sprite.OrderedUpdates):
            self.start()
        self._children._spritelist.sort(lambda a,b:-1+(int(a.rect.bottom > b.rect.bottom)*2))
        self.children = self._children.sprites()
        Layer.update(self)