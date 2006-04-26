#Clad in Iron 0.5
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

import pygame, eventnet.driver, sprites, cPickle, os, glob, random

try:
    tmpfile = os.path.join(os.environ['TMP'], 'temp.bmp')
except KeyError, e:
    tmpfile = 'temp.bmp' #defaulting to CWD doesn't seem nice, but...

class tile(sprites.Sprite):
    def __init__(self, image, solid=False):
        sprites.Sprite.__init__(self, image)
        self.image = image
        self.rect = self.image.get_rect()
        self.solid = solid

default_tile = tile(pygame.image.load(os.path.join(
    'data', 'tiles', 'Grs2Watr22.bmp')))
reg_tiles = [tile(pygame.image.load(x)) for x in glob.glob(
    os.path.join('data', 'tiles', '*.bmp'))]
solid_tiles = [tile(pygame.image.load(x), True) for x in glob.glob(
    os.path.join('data', 'tiles', 'solid', '*.bmp'))]
tiles = solid_tiles + reg_tiles
test_tiles = [tiles, tiles, tiles, tiles]
empty_level={'enemies': [], 'hero': (0,0), 'tiles': test_tiles}

def load(name):
    '''
    This and save() convert pygame surfaces to strings through a tempfile so
    that the surfaces can be pickled.
    '''

    f = open(os.path.join('data', 'levels', name+'.lvl'))
    lvl = cPickle.load(f)
    f.close()
    for i in range(len(lvl['enemies'])):
        enemy = lvl['enemies'][i]
        del(lvl['enemies'][i])
        #f = open(tmpfile, 'wb')
        #f.write(enemy[0])
        #f.close()
        #img = pygame.image.load(tmpfile)
        img = pygame.image.fromstring(enemy[0], enemy[2], 'RGB')
        img.set_colorkey((0,0,0,255))
        enemy = sprites.Sprite(img, pos=enemy[1])
        lvl['enemies'].insert(i, enemy)
    for index in range(len(lvl['tiles'])):
        row = lvl['tiles'][index]
        del(lvl['tiles'][index])
        for i in range(len(row)):
            t = row[i]
            del(row[i])
            #f = open(tmpfile, 'wb')
            #f.write(t[0])
            #f.close()
            img = pygame.image.fromstring(t[0], t[2], 'RGB')
            t = tile(img, t[1])
            row.insert(i, t)
        lvl['tiles'].insert(index, row)

    return lvl

def save(name, lvl):
    '''
    The ugliest code in the program as of today :p see load()
    '''

    for i in range(len(lvl['enemies'])):
        print range(len(lvl['enemies']))
        enemy = lvl['enemies'][i]
        try:
            rect = enemy.rect
            del(lvl['enemies'][i])
            enemy = sprites.Sprite(enemy.image, pos=enemy.rect.topleft)
            enemy.rect = rect
            #pygame.image.save(enemy.image, tmpfile)
            #enemy.image = open(tmpfile, 'rb').read()
            enemy.image = pygame.image.tostring(enemy.image, 'RGB')
            enemy = (enemy.image, enemy.rect.topleft, enemy.rect.size)
            lvl['enemies'].insert(i, enemy)
        except Exception, e:
            print e

    for index in range(len(lvl['tiles'])):
        row = lvl['tiles'][index]
        del(lvl['tiles'][index])
        for i in range(len(row)):
            try:
                t = row[i]
                rect = t.rect
                del(row[i])
                t = tile(t.image, t.solid)
                t.rect = rect
                #pygame.image.save(t.image, tmpfile)
                #t.image = open(tmpfile, 'rb').read()
                t.image = pygame.image.tostring(t.image, 'RGB')
                t = (t.image, t.solid, t.rect.size)
                row.insert(i, t)
            except:
                pass
        lvl['tiles'].insert(index, row)

    cPickle.dump(lvl, open(os.path.join('data', 'levels', name+'.lvl'), 'w'))

def new(width, height):
    tiles = []
    for row in range(height):
        y = row
        row = []
        for Tile in range(width):
            x = Tile
            Tile = tile(default_tile.image, False)
            Tile.rect = Tile.rect.move((x,y))
            row += [Tile]
        tiles += [row]
    return {'enemies': [], 'hero': (-100,0), 'tiles': tiles}
