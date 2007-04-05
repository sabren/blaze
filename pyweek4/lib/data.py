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
    walk_left = loadGrid('data/animations/walk-left.png',(35,48))[0]
    walk_right = loadGrid('data/animations/walk-right.png',(35,48))[0]
    kick_left = loadGrid('data/animations/kick-left.png',(35,48))[0]
    kick_right = loadGrid('data/animations/kick-right.png',(35,48))[0]
    punch_left = loadGrid('data/animations/punch-left.png',(35,48))[0]
    punch_right = loadGrid('data/animations/punch-right.png',(35,48))[0]
    die_forward_left = loadGrid('data/animations/die-forward-left.png',(45,48))[0]
    die_forward_right = loadGrid('data/animations/die-forward-right.png',(45,48))[0]
    die_back_left = loadGrid('data/animations/die-back-left.png',(45,48))[0]
    die_back_right = loadGrid('data/animations/die-back-right.png',(45,48))[0]
    button = loadGrid('data/animations/walk-left.png',(35,48))[0][0]

class Enemy:
    button = loadGrid('data/animations/enemy-left.png',(35,48))[0][0]
    walk_left = loadGrid('data/animations/enemy-left.png',(35,48))[0]
    walk_right = loadGrid('data/animations/enemy-right.png',(35,48))[0]
    punch_right = loadGrid('data/animations/enemy-punch-right.png',(35,48))[0]
    punch_left = loadGrid('data/animations/enemy-punch-left.png',(35,48))[0]
    kick_left = loadGrid('data/animations/enemy-kick-left.png',(35,48))[0]
    kick_right = loadGrid('data/animations/enemy-kick-right.png',(35,48))[0]

    die_forward_left = loadGrid('data/animations/enemy-die-forward-left.png',(45,48))[0]
    die_forward_right = loadGrid('data/animations/enemy-die-forward-right.png',(45,48))[0]
    die_back_left = loadGrid('data/animations/enemy-die-back-left.png',(45,48))[0]
    die_back_right = loadGrid('data/animations/enemy-die-back-right.png',(45,48))[0]

class Camera:
    anim = loadGrid('data/animations/camera.png',(35,30))[0]
    still = loadGrid('data/animations/camera.png',(35,30))[0][0]

stairs = pygame.image.load('data/stairs.png')

wall = pygame.image.load('data/wall.png').convert()
floor = pygame.image.load('data/floor.png').convert()
punch = ['data/sounds/punch.wav',
         'data/sounds/punch1.wav',
         'data/sounds/punch2.wav']
exitDoor = pygame.image.load('data/exit.png').convert()
exitDoor.set_colorkey(exitDoor.get_at((0,0)))

def texture(filename='',img=None,size=(20,20)):
    surf = pygame.Surface(size)
    if filename:
        img = pygame.image.load(filename)
    for y in range(size[1]/img.get_height()+1):
        y = y*img.get_height()
        for x in range(size[0]/img.get_width()+1):
            x = x*img.get_width()
            surf.blit(img,(x,y))
    return surf

icon = pygame.image.load('data/icon.png').convert()
icon.set_colorkey(icon.get_at((0,0)))

class Basement:
    _name = 'Basement'
    background = pygame.image.load('data/textures/brick.png').convert()
    stair = stairs
    wall = wall
    floor = floor
    exitDoor = exitDoor
