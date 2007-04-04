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

import pygame,player,data,cPickle,sprites

class Level(object):

    def __init__(self,size=(800,600)):
        self.size = size
        self.all = pygame.sprite.Group()
        self.player = player.Player()
        self.floors = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.cameras = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.stairs = pygame.sprite.Group()
        self.all.add(self.player)
        self.s = pygame.sprite.Sprite()
        self.s.image = data.texture('data/textures/brick.png',size).convert()
        self.s.rect = self.s.image.get_rect()
        self.background = self.s.image.copy()
        for x in range(size[0]/data.floor.get_width()+1):
            x *= data.floor.get_width()
            floor = sprites.Floor((x,-data.floor.get_height()),self)
            floor = sprites.Floor((x,size[1]+data.floor.get_height()/2),self)
        for y in range(size[1]/data.wall.get_height()+1):
            y *= data.wall.get_height()
            wall = sprites.Wall((-data.wall.get_width(),y),self)
            wall = sprites.Wall((size[0]+data.wall.get_width(),y),self)

    def clear(self):
        self.all.clear(self.s.image,self.background)

    def update(self):
        self.player.update(self)
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
    cPickle.dump(size,f)
    cPickle.dump(player,f)
    cPickle.dump(walls,f)
    cPickle.dump(floors,f)
    cPickle.dump(cameras,f)
    cPickle.dump(enemies,f)
    cPickle.dump(stairs,f)
    f.close()

def load(filename):
    f = open(filename,'r')
    size = cPickle.load(f)
    player = cPickle.load(f)
    walls = cPickle.load(f)
    floors = cPickle.load(f)
    cameras = cPickle.load(f)
    enemies = cPickle.load(f)
    stairs = cPickle.load(f)
    f.close()

    lvl = Level(size)
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
    return lvl
