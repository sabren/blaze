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

import pygame
pygame.display.set_mode((800,600)) # this is for our .convert()s

from directicus.engine import Engine
import menus,data,os

class Game(Engine):
    '''
    Our customized master object.
    '''

    DEFAULT = menus.MainMenu
    size = (800,600)
    oldState = None

    def __init__(self,fps=40):
        Engine.__init__(self,fps)
        pygame.display.set_caption('Ascent of Justice')
        pygame.display.set_icon(data.icon)

    def EVT_KeyDown(self,event):
        if event.key == pygame.K_F9:
            pygame.image.save(pygame.display.get_surface(),'screenshot.bmp')

    def EVT_Quit(self,event):
        self.oldState = self.state
        self.state.quit(menus.ConfirmExit(self.oldState))

def main():
    e = Game(40)
    e.run()
