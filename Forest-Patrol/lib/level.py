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

import pygame,cPickle,resources,random
from sprites import Tree,Ranger,ActiveRanger,Castle,Army,Enemy,Player

resources = resources.ResourceManager()
grass = resources.Grass.still

class Level(object):

    size = (800,600) #in pixels
    trees = pygame.sprite.Group()
    rangers = pygame.sprite.Group()
    enemies = list()
    sprites = pygame.sprite.Group()
    castles = pygame.sprite.Group()
    collideRects = list()
    armies = list()
    player = None
    rangersPerArmy = 5
    filename = ''

    def game(self):
        '''
        Convert rangers to active rangers for a game.
        '''

        #g = pygame.sprite.Group()
        #for old in self.rangers.sprites():
        #    new = ActiveRanger()
        #    g.add(new)
        #    self.sprites.add(g)
        #    new.rect.center = old.rect.center
        #    old.kill()
        #self.rangers = g
        pass

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

def create(size=(3000,3000),trees=30,enemies=1,rangers=10):
    level = Level()
    level.size = size
    if size == (3000,3000):
        trees = 50
    elif size == (5000,5000):
        trees = 70
    elif size == (7000,7000):
        trees = 100
    level.rangersPerArmy = rangers
    for enemy in range(enemies):
        pos = [random.randint(0,size[0]-353),
               random.randint(0,size[1]-315)]
        castle = Castle()
        castle.rect.topleft = pos
        army = Army(castle,level)
        level.armies.append(army)
        enemy = Enemy([army])
        level.enemies.append(enemy)
    pos = [random.randint(0,size[0]-353),
           random.randint(0,size[1]-315)]
    castle = Castle()
    castle.rect.topleft = pos
    level.player = Player([Army(castle,level)])
    castles = [army.castle for army in level.armies]+[castle]
    for castle in castles:
        level.sprites.add(castle)
        level.castles.add(castle)
    for tree in range(trees):
        tree = Tree()
        pos = [random.randint(0,size[0]),
               random.randint(0,size[1])]
        tree.rect.center = pos
        while tree.rect.collidelist(level.sprites.sprites()) != -1:
            pos = [random.randint(0,size[0]),
                   random.randint(0,size[1])]
            tree.rect.center = pos
        level.sprites.add(tree)
        level.trees.add(tree)
    return level
