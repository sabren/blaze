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

import pygame,directicus.sprite
from eventnet.driver import Handler
from directicus.gfx import Animation,loadGrid
import resources

class Army(object):
    level = None
    castle = None

    def __init__(self,castle,level):
        object.__init__(self)
        self.level = level
        self.rangers = pygame.sprite.Group()
        self.castle = castle
        self.deployTroops(level.rangersPerArmy)

    def deployTroops(self,count):
        pos = [self.castle.rect.left,
               self.castle.rect.bottom+5]
        for ranger in range(count):
            ranger = ActiveRanger()
            ranger.rect.midtop = pos
            self.level.rangers.add(ranger)
            self.level.sprites.add(ranger)
            self.rangers.add(ranger)
            pos[0] += ranger.rect.width+1

class Enemy(Army):
    pass

class Castle(directicus.sprite.Sprite):
    image = resources.Castle.still
    image.set_colorkey((24,102,14))
    usePP = True
    baseRect = image.get_rect()

    def __init__(self):
        directicus.sprite.Sprite.__init__(self)
        self.rect.clamp(pygame.display.get_surface().get_rect())

class Tree(directicus.sprite.Sprite):
    image = resources.Tree.still
    image.set_colorkey((20,102,14))
    usePP = True

class Ranger(directicus.sprite.Sprite):
    image = resources.Ranger.still
    usePP = True
    old = image.get_rect()
    baseRect = pygame.Rect(old)
    baseRect.width = old.width/2
    baseRect.height = old.height/3
    baseRect.midbottom = old.midbottom
    del(old)

class ActiveRanger(directicus.sprite.AnimatedSprite,Ranger):
    dest = None
    path = []
    level = None
    speed = 5
    anims = resources.Ranger.walk
    anim = anims['180']

    def __init__(self):
        directicus.sprite.AnimatedSprite.__init__(self)
        self.baseRect.midbottom = self.rect.midbottom

    def target(self,what):
        self.dest = what
        self.path = self._plot(self.dest)

    def update(self,level=None):
        if self.path:
            old = self.rect.center
            self.path.reverse()
            new = self.path.pop()
            i = self.anim.index
            if new[0] == self.rect.centerx and new[1] < self.rect.centery:
                self.anim = self.anims['0']
            elif new[0] > self.rect.centerx and new[1] < self.rect.centery:
                self.anim = self.anims['45']
            elif new[0] > self.rect.centerx and new[1] == self.rect.centery:
                self.anim = self.anims['90']
            elif new[0] > self.rect.centerx and new[1] > self.rect.centery:
                self.anim = self.anims['135']
            elif new[0] == self.rect.centerx and new[1] > self.rect.centery:
                self.anim = self.anims['180']
            elif new[0] < self.rect.centerx and new[1] > self.rect.centery:
                self.anim = self.anims['225']
            elif new[0] < self.rect.centerx and new[1] == self.rect.centery:
                self.anim = self.anims['270']
            elif new[0] < self.rect.centerx and new[1] < self.rect.centery:
                self.anim = self.anims['335']
            self.anim.index = i
            self.path.reverse()
            self.rect.center = new
            if self.collide(level.rangers):
                self.path.insert(0,new)
                self.rect.center = old
                self.path = self._plot(self.dest)
            else:
                directicus.sprite.AnimatedSprite.update(self)
        else:
            self.anim.index = 0
            directicus.sprite.AnimatedSprite.update(self)
        self.baseRect.midbottom = self.rect.midbottom
        self.image.set_colorkey(self.image.get_at((0,0)))

    def collide(self,group):
        collisions = list()
        for sprite in group:
            if sprite == self:
                continue
            if self._diff(self.rect.center,sprite.rect.center) < self.rect.width:
                return True
        return False

    def _plot(self,dest):
        '''
        Plot a set of waypoints from current position to "dest".
        '''

        dest = list(dest)
        cur = list(self.rect.center)
        path = []
        while self._diff(cur,dest) > self.speed:
            if max(dest[0],cur[0])-min(dest[0],cur[0]) > self.speed-1:
                if dest[0] > cur[0]:
                    cur[0] += self.speed
                elif dest[0] < cur[0]:
                    cur[0] -= self.speed
            if max(dest[1],cur[1])-min(dest[1],cur[1]) > self.speed-1:
                if dest[1] > cur[1]:
                    cur[1] += self.speed
                elif dest[1] < cur[1]:
                    cur[1] -= self.speed
            if list(cur) in path:
                return path
            path.append(list(cur))
        return path

    def _diff(self,a,b):
        return (max(a[0],b[0])-min(a[0],b[0])) + (max(a[1],b[1])-min(a[1],b[1]))

class MiniMap(directicus.sprite.Sprite):

    level = None
    image = pygame.Surface((1,1))
    enemy = pygame.Surface((2,2))
    enemy.fill((255,0,0))
    ally = enemy.copy()
    ally.fill((0,255,0))
    tree = pygame.Surface((5,5))
    tree.fill((0,50,0))
    castle = pygame.Surface((10,10))
    castle.fill((100,100,100))
    pos = None

    def tick(self):
        if self.level:
            self.image = pygame.Surface(self.shrink(self.level.size))
            self.image.set_alpha(150)
            self.image.fill((0,175,0))
            for tree in self.level.trees.sprites():
                self.image.blit(self.tree,self.shrink(tree.rect.center))
            for castle in self.level.castles.sprites():
                self.image.blit(self.castle,self.shrink(castle.rect.center))
            enemies = list()
            for army in self.level.enemies:
                enemies.extend(army.rangers.sprites())
            for ranger in enemies:
                self.image.blit(self.enemy,self.shrink(ranger.rect.center))
            for ranger in self.level.player.rangers.sprites():
                self.image.blit(self.ally,self.shrink(ranger.rect.center))
            if self.pos:
                img = pygame.Surface(self.shrink(pygame.display.get_surface().get_size()))
                img.fill((255,0,0))
                img.set_colorkey((255,0,0))
                pygame.draw.rect(img,(255,255,255),img.get_rect(),3)
                r = img.get_rect()
                r.topleft = self.shrink(self.pos)
                self.image.blit(img,r)

    def shrink(self,what):
        new = [0,0]
        if what[0] != 0:
            new[0] = what[0]/50
        if what[1] != 0:
            new[1] = what[1]/50
        return new

    def grow(self,what):
        return (what[0]*50,what[1]*50)

    def draw(self):
        self.rect = self.image.get_rect()
        self.rect.right = pygame.display.get_surface().get_width()-5
        self.rect.bottom = pygame.display.get_surface().get_height()-5
        pygame.sprite.Group(self).draw(pygame.display.get_surface())
