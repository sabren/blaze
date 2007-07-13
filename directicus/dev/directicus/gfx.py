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
Storage of multiple images in a single file and animations.
'''

import pygame

class SpriteSheet(object):
    def __init__(self,filename=None,surf=None):
        object.__init__(self)
        self.filename = filename
        if surf:
            self.surf = surf
        else:
            self.surf = pygame.image.load(filename)
            
    def get(self,rect=None,x=0,y=0,width=0,height=0,size=None,pos=None):
        if rect:
            x,y,width,height = rect.x,rect.y,rect.width,rect.height
        elif size:
            width,height = size
            if pos:
                x,y = pos
        elif not (width and height):
            raise ValueError, 'You must use either a pygame rect "rect", tuples for "size" and "pos", or "x", "y", "width", and "height" arguments.'
        clipRect = pygame.Rect(x,y,width,height)
        clipSurf = pygame.Surface(clipRect.size)
        clipSurf.blit(self.surf,(-x,-y))
        return clipSurf
    
    def set(self,surf,x=0,y=0,pos=None):
        if pos:
            x,y = pos
        self.surf.blit(surf,(x,y))
        
    def save(self,filename=None):
        if not filename:
            filename = self.filename
        pygame.image.save(self.surf,filename)
        
class GridSheet(SpriteSheet):
    '''
    A gridded variation of our spritesheet.
    '''
    
    def __init__(self,filename=None,surf=None,size=None,x=0,y=0,spacing=0):
        SpriteSheet.__init__(self,filename,surf)
        if size:
            x,y = size
        elif not x and not y:
            raise ValueError, 'You must specify the size via "size" or x and y args.'
        self.size = size
        self.spacing = spacing
        
    def get(self,row=0,col=0):
        pos = ((col*self.size[0])+(self.spacing*col),
               (row*self.size[1])+(self.spacing*row))
        return SpriteSheet.get(self,pos=pos,size=self.size)
    
    def set(self,surf,row=0,col=0):
        pos = ((col*self.size[0])+(self.spacing*col),
               (row*self.size[1])+(self.spacing*row))
        SpriteSheet.set(self,surf,pos=pos)
        
    def getMatrix(self):
        matrix = []
        for y in range(self.surf.get_height()/self.size[1]):
            row = []
            for x in range(self.surf.get_width()/self.size[0]):
                row.append(self.get(y,x))
            matrix.append(row)
        return matrix
    
    def setMatrix(self,matrix):
        for row in matrix:
            for col in row:
                self.set(col,matrix.index(row),row.index(col))

def saveGrid(map,filename):
    '''
    saveGrid(map,filename) - save a 2d map of images into a single file

    Useful for frames in an animation.
    '''

    height = map[0][0].get_height()
    width = map[0][0].get_width()
    new = pygame.Surface((width*len(map[0]),(height*len(map))))
    alpha = map[0][0].get_colorkey()
    if alpha:
        new.fill(alpha)
        new.set_colorkey(alpha)
    y = 0
    for row in map:
        x = 0
        for image in row:
            new.blit(image, (x,y))
            x += width
        y += height
    pygame.image.save(new,filename)

def loadGrid(image,size=(20,20),colorkey=None):
    '''
    loadGrid(image,size=(20,20),colorkey=None) - inverse of saveGrid
    '''

    if type(image) == type('<string>'):
        image = pygame.image.load(image)

    map = []
    y = 0
    for row in range(image.get_height()/size[1]):
        row = []
        x = 0
        for img in range(image.get_width()/size[0]):
            img = pygame.Surface(size)
            if colorkey:
                img.set_colorkey((0,0,0))
            img.blit(image,(-x,-y))
            row.append(img)
            x += size[0]
        map.append(row)
        y += size[1]
    return map

class Animation(object):
    '''
    A sequence of images playing at the FPS rate of the game to simulate
    an animation.
    '''

    def __init__(self, seq=[], loop=False):
        '''
        Animation.__init__(seq=[],loop=False) - prep images and standby
        '''

        for image in seq:
            if type(image) == type('<string>'):
                seq[seq.index(image)] = pygame.image.load(image)

        self.index = 0
        self.loop = loop
        self.seq = seq
        self.surf = seq[0]

    def tick(self):
        '''
        Animation.tick() - called to update Animation.seq every frame
        '''

        if self.index == (len(self.seq)-1):
            if self.loop:
                self.index = 0
                self.surf = self.seq[0]
        else:
            self.index += 1
            self.surf = self.seq[self.index]