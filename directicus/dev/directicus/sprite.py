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
Easy sprites with support for animations and pixel-perfect collision detection.
'''

import pygame, event

class Sprite(pygame.sprite.Sprite,event.Listener):
    '''
    When subclassing be sure to specify a Sprite.image before __init__().
    '''

    #pixel-perfect collisions
    usePP = False

    def __init__(self,**groups):
        '''
        Sprite.__init__(**groups) - load sprite inside "groups" sprite groups
        '''

        pygame.sprite.Sprite.__init__(self, groups)
        event.Listener.__init__(self)
        self.rect = self.image.get_rect()
        self.points = [] #for collisions
        self.calcMap()

    def start(self):
        '''
        Sprite.start() - called right before first update()s
        '''

        pass

    def collidePoint(self,point):
        '''
        Sprite.collidePoint(point) - see if "point" is part of the sprite
        '''

        self.calcMap()
        return point in self.points

    def calcMap(self):
        '''
        Sprite.calcMap() - list coords elegible for collisions on the surface
        '''

        self.points = []
        if self.usePP:
            for y in range(self.image.get_height()):
                for x in range(self.image.get_width()):
                    if self.image.get_at((x,y))[3] > 0:
                        point = (self.rect.x+x, self.rect.y+y)
                        self.points.append(point)
        else:
            #just add all pixels
            for y in range(self.image.get_height()):
                for x in range(self.image.get_width()):
                    point = (self.rect.left+x, self.rect.top+y)
                    self.points.append(point)

    def collideSprite(self,sprite):
        '''
        Sprite.collideSprite(sprite - check for a collision with another sprite
        '''

        if self.usePP or sprite.usePP:
            for point in sprite.points:
                if point in self.points:
                    return True
            return False
        else:
            return self.rect.colliderect(sprite.rect)

    def collideGroup(self,group):
        '''
        collideGroup(group) - returns a list of touching sprites in "group"
        '''

        collisions = []
        for sprite in group.sprites():
            if self.collideSprite(sprite):
                collisions.append(sprite)
        return collisions

    def kill(self):
        '''
        Sprite.kill() - leave all groups and disconnect events
        '''

        self.unRegister()
        pygame.sprite.Sprite.kill(self)

    def update(self):
        '''
        Sprite.update() - per-frame updates
        '''

        pass

class AnimatedSprite(Sprite):
    '''
    Takes AnimatedSprite.anim instead of Sprite.image.
    '''

    def __init__(self,**groups):
        '''
        AnimatedSprite.__init__(**groups) - load anim and __init__() superclass
        '''

        self.image = self.anim.surf
        Sprite.__init__(self)

    def update(self):
        '''
        AnimatedSprite.update() - update AnimatedSprite.anim
        '''

        self.anim.tick()
        if self.anim.surf == self.anim.seq[0]:
            self.onStart()
        if self.anim.surf == self.anim.seq[-1]:
            self.onEnd()
        self.image = self.anim.surf
        
    def onStart(self):
        pass

    def onEnd(self):
        '''
        AnimatedSprite.onEnd - called when the animation ends
        '''

        pass
