#Directicus
#Copyright (C) 2006 Team Trailblazer
#
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

'''
Storage of multiple images in a single file and animations.
'''

import pygame

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

if __name__=='__main__':
    import glob,engine,sprite
    seq = glob.glob('exploBig/*.bmp')
    seq = [[pygame.image.load(img) for img in seq[:7]],
           [pygame.image.load(img) for img in seq[8:]]]
    saveGrid(seq,'temp.bmp')
    seq = loadGrid('temp.bmp',(40,40),(0,0,0))
    ani = seq [0]
    ani.extend(seq[1])
    ani = Animation(ani,loop=True)

    sprite.AnimatedSprite.anim = ani
    sprite = sprite.AnimatedSprite()

    s = engine.State()
    def tick(event):
        sprite.update()
        pygame.display.get_surface().fill((0,0,0))
        pygame.display.get_surface().blit(sprite.image,sprite.rect)
        pygame.display.flip()
    s.EVT_tick = tick
    e = engine.Engine(20)
    e.DEFAULT = s
    e.size = (300,200)
    e.run()
