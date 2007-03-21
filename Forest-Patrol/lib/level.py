# Forest Patrol
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

import pygame,cPickle,resources
from sprites import Tree,Ranger,ActiveRanger,Castle

resources = resources.ResourceManager()
grass = resources.Grass.still #pygame.image.load('data/grass.png')

class Level(object):

    size = (800,600) #in pixels
    trees = pygame.sprite.Group()
    rangers = pygame.sprite.Group()
    sprites = pygame.sprite.Group()
    castles = pygame.sprite.Group()
    collideRects = list()
    filename = ''

    def game(self):
        '''
        Convert rangers to active rangers for a game.
        '''

        g = pygame.sprite.Group()
        for old in self.rangers.sprites():
            new = ActiveRanger()
            g.add(new)
            self.sprites.add(g)
            new.rect.center = old.rect.center
            old.kill()
        self.rangers = g
        for sprite in self.sprites:
            if hasattr(sprite,'baseRect'):
                sprite.baseRect.midbottom = sprite.rect.midbottom

    def render(self):
        #draw background
        self.background = pygame.Surface(self.size)
        for y in range((self.size[1]/grass.get_height())+1):
            for x in range((self.size[0]/grass.get_width())+1):
                self.background.blit(grass,(x*grass.get_width(),y*grass.get_height()))
                x += grass.get_width()
            y += grass.get_height()
        self.surface = self.background.copy()

    def clear(self):
        self.sprites.clear(self.surface,self.background)

    def draw(self,sprites=None):
        ### THIS SHOULD ALLOW FOR REDRAWING ONLY A FEW SPRITES ###
        if sprites == None:
            sprites = self.sprites.sprites()
        yList = [sprite.rect.bottom for sprite in sprites]
        yList.sort()
        group = pygame.sprite.OrderedUpdates()
        for sprite in yList:
            sprite = [s for s in sprites if s.rect.bottom == sprite][0]
            del(sprites[sprites.index(sprite)])
            group.add(sprite)
        group.draw(self.surface)
        self.sprites = group

def save(level,filename):
    size = level.size
    trees = [tree.rect.center for tree in level.trees.sprites()]
    rangers = [ranger.rect.center for ranger in level.rangers.sprites()]
    castles = [castle.rect.center for castle in level.castles.sprites()]

    f = open(filename,'w')
    cPickle.dump(size,f)
    cPickle.dump(trees,f)
    cPickle.dump(rangers,f)
    cPickle.dump(castles,f)
    f.close()

def load(filename):
    f = open(filename,'r')
    size = cPickle.load(f)
    trees = cPickle.load(f)
    rangers = cPickle.load(f)
    castles = cPickle.load(f)
    f.close()
    lvl = Level()
    lvl.size = size
    for tree in trees:
        s = Tree()
        s.rect.center = tree
        lvl.trees.add(s)
        lvl.sprites.add(s)
    for ranger in rangers:
        s = Ranger()
        s.rect.center = ranger
        lvl.rangers.add(s)
        lvl.sprites.add(s)
    for castle in castles:
        s = Castle()
        s.rect.center = castle
        lvl.castles.add(s)
        lvl.sprites.add(s)
    lvl.filename = filename
    return lvl

if __name__=='__main__':
    Level.trees = [(100,100),(150,100),(200,200)]
    Level.rangers = [(400,300)]
    
    pygame.init()
    lvl = Level()
    disp = pygame.display.set_mode((800,600),pygame.NOFRAME)
    disp.blit(lvl.background,(0,0))
    lvl.sprites.draw(disp)
    pygame.display.flip()
    raw_input()
