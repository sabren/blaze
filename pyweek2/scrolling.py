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

'''
Contains scrolling_display class to handle scrolling displays.
'''

import pygame

class scrolling_display:
    '''
    Class to handle a scrolling display. Give it a pos and keep it ticking
    and it'll center the screen over the background.

    self.pos is the coords of the background to put in the top-left corner
    of the screen.
    '''

    def __init__(self, background, screen, pos):
        self.background = background
        self.screen = screen
        self.pos = pos

    def tick(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.background, (-self.pos[0], -self.pos[1]))
        pygame.display.update(self.screen.get_rect())

if __name__=='__main__':
    #visual scrolling test[s]
    background = pygame.Surface((900, 700))
    white = pygame.Surface((50,50))
    white.fill((255,255,255))
    black = pygame.Surface((50,50))
    black.fill((0,0,0))
    y = 0
    tile = white
    for row in range(background.get_height()/50):
        x = 0
        for col in range(background.get_width()/50):
            background.blit(tile, (x,y))
            if tile == white: tile = black
            else: tile = white
            x += 50
        if tile == white: tile = black
        else: tile = white
        y += 50

    screen = pygame.display.set_mode((800, 600))
    pos = (0,0)
    sd = scrolling_display(background, screen, pos)
    for x in range(100):
        sd.pos = (sd.pos[0]-5, sd.pos[1]-5)
        sd.tick()
        pygame.time.wait(1000)
    while 1:
        sd.tick()
