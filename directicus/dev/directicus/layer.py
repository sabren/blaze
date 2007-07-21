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

import pygame,cPickle,sprite

class Layer(object):
    
    def __init__(self,background=None,foreground=None,sprites=[]):
        object.__init__(self)
        if background:
            self.background = background
        self.foreground = foreground
        self._sprites = sprites
        if isinstance(sprites,pygame.sprite.Group):
            self.sprites = sprites
        else:
            self.sprites = pygame.sprite.Group(sprites)
        self.surf = None
    
    def update(self,*args,**kwargs):
        if not self.surf:
            self.surf = self.background.copy()
        self.sprites.clear(self.surf,self.background)
        self.sprites.update(*args,**kwargs)
        self.sprites.draw(self.surf)
        
    def start(self,dest):
        dest.blit(self.background,(0,0))
    
    def render(self,dest=None):
        if not dest:
            dest = self.background.copy()
        self.sprites.clear(dest,self.background)
        self.sprites.update()
        self.sprites.draw(dest)
        if self.foreground:
            dest.blit(self.foreground,(0,0),self.foreground.get_rect())
        return dest

class IsometricLayer(Layer):
    '''
    Renders sprites from back to front.
    '''

    def start(self,dest=None):
        Layer.start(self,dest)
        self.sprites = pygame.sprite.OrderedUpdates(self.sprites.sprites())

    def render(self,*args,**kwargs):
        self.sprites._spritelist.sort(lambda a,b:-1+(int(a.rect.bottom > b.rect.bottom)*2))
        Layer.render(self,*args,**kwargs)