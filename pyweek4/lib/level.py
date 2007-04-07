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

import pygame,player,data,cPickle,sprites,os
from campaign import Campaign

class Level(object):
    def __init__(self,tileset=data.Basement,size=(800,600)):
        object.__init__(self)
        self.tileset = tileset
        self.filename = ''
        self.size = size
        self.all = pygame.sprite.Group()
        self.player = player.Player()
        self.floors = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.cameras = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.stairs = pygame.sprite.Group()
        self.exit = sprites.Exit(level=self)
        self.all.add(self.player,self.exit)
        self.s = pygame.sprite.Sprite()
        self.s.image = data.texture(img=self.tileset.background,size=size)
        self.s.rect = self.s.image.get_rect()
        self.background = self.s.image.copy()

        # Draw platforms around the border
        for x in range(size[0]/self.tileset.floor.get_width()+1):
            x *= self.tileset.floor.get_width()
            floor = sprites.Floor((x,-self.tileset.floor.get_height()),self)
            floor = sprites.Floor((x,size[1]+self.tileset.floor.get_height()/2),self)
        for y in range(size[1]/self.tileset.wall.get_height()+1):
            y *= self.tileset.wall.get_height()
            wall = sprites.Wall((-self.tileset.wall.get_width(),y),self)
            wall = sprites.Wall((size[0]+self.tileset.wall.get_width(),y),self)

    def intro(self):
        surf = pygame.Surface((800,600))
        surf.fill((0,0,0))
        surf.set_colorkey((0,0,0))
        try:
            intro_file = os.path.join(
                os.path.dirname(self.filename),
                os.path.splitext(os.path.basename(self.filename))[0]+'.txt')
            f = open(intro_file)
            intro = [line.strip() for line in f.readlines()]
            f.close()
            fnt = Font('data/verdanai.ttf',20)
            y = 5
            for line in intro:
                line = fnt.render(line,True,(0,255,0))
                bg = line.copy()
                bg.fill((100,100,100,255))
                bg.blit(line,(0,0))
                line = bg
                surf.blit(bg,(400-(line.get_width()/2),y))
                y += line.get_height()+5
        except:
            pass
        return surf

    def clear(self):
        self.all.clear(self.s.image,self.background)

    def update(self):
        self.player.update(self)
        self.exit.update(self)
        self.cameras.update(self)
        self.enemies.update(self)

    def draw(self):
        self.all.draw(self.s.image)

def save(level,filename):
    size = level.size
    player = level.player.rect.center
    walls = [wall.rect.center for wall in level.walls]
    floors = [floor.rect.center for floor in level.floors]
    cameras = [camera.rect.center for camera in level.cameras]
    enemies = [enemy.rect.center for enemy in level.enemies]
    stairs = [stair.rect.center for stair in level.stairs]

    f = open(filename,'w')
    cPickle.dump(level.tileset._name,f)
    cPickle.dump(size,f)
    cPickle.dump(player,f)
    cPickle.dump(walls,f)
    cPickle.dump(floors,f)
    cPickle.dump(cameras,f)
    cPickle.dump(enemies,f)
    cPickle.dump(stairs,f)
    cPickle.dump(level.exit.rect.center,f)
    cPickle.dump(level.filename,f)
    f.close()

def load(filename):
    f = open(filename,'r')
    tileset = cPickle.load(f)
    size = cPickle.load(f)
    player = cPickle.load(f)
    walls = cPickle.load(f)
    floors = cPickle.load(f)
    cameras = cPickle.load(f)
    enemies = cPickle.load(f)
    stairs = cPickle.load(f)
    exit = cPickle.load(f)
    filename = cPickle.load(f)
    f.close()

    tileset = getattr(data,tileset)
    lvl = Level(tileset,size)
    lvl.player.rect.center = player
    for wall in walls:
        wall = sprites.Wall(wall,lvl)
    for floor in floors:
        floor = sprites.Floor(floor,lvl)
    for camera in cameras:
        camera = sprites.Camera(camera,lvl)
    for enemy in enemies:
        enemy = sprites.Enemy(enemy,lvl)
    for stair in stairs:
        stair = sprites.Stair(stair,lvl)
    lvl.exit.rect.center = exit
    lvl.filename = filename

    return lvl
