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

'''
Centralized data source
'''

from directicus.gfx import Animation,loadGrid
import pygame

class Hero:
    walk_left = Animation(loadGrid('data/animations/walk-left.png',(35,48))[0],True)
    walk_right = Animation(loadGrid('data/animations/walk-right.png',(35,48))[0],True)
    kick_left = loadGrid('data/animations/kick-left.png',(35,48))[0]
    kick_right = loadGrid('data/animations/kick-right.png',(35,48))[0]
    punch_left = loadGrid('data/animations/punch-left.png',(35,48))[0]
    punch_right = loadGrid('data/animations/punch-right.png',(35,48))[0]
    button = loadGrid('data/animations/walk-left.png',(35,48))[0][0]

class Camera:
    anim = loadGrid('data/animations/camera.png',(35,30))[0]
    still = loadGrid('data/animations/camera.png',(35,30))[0][0]

wall = pygame.image.load('data/wall.png').convert()
floor = pygame.image.load('data/floor.png').convert()

def texture(filename,size=(20,20)):
    surf = pygame.Surface(size)
    img = pygame.image.load(filename)
    for y in range(size[1]/img.get_height()+1):
        y = y*img.get_height()
        for x in range(size[0]/img.get_width()+1):
            x = x*img.get_width()
            surf.blit(img,(x,y))
    return surf

icon = pygame.image.load('data/icon.png').convert()
icon.set_colorkey(icon.get_at((0,0)))
