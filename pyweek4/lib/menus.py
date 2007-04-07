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

from directicus.engine import Menu
from directicus.sfx import Music
from game import GameState
from campaign import Campaign
import pygame,eventnet.driver,sys,os,level,glob,posixpath

class GameMenu(Menu):
    '''
    Game-specific menu class, nothing for now.
    '''

    color = (0,0,0)

    def __init__(self):
        self.background = pygame.image.load('data/menu.png').convert()
        Menu.__init__(self)

class MainMenu(GameMenu):
    title = 'Ascent of Justice'
    options = ['New Game',
               'Play Custom',
               'Exit']

    def __init__(self):
        if os.path.exists('save.lvl') and len(self.options) < 3:
            self.options.insert(1,'Continue')
        GameMenu.__init__(self)
        self.music = Music()
        self.music.volume = 1
        self.music.play('data/music/menu.mp3')

    def EVT_Menu_NewGame(self,event):
        self.quit(GameState())

    def EVT_Menu_Continue(self,event):
        self.quit(GameState(level.load('save.lvl')))

    def EVT_Menu_PlayCustom(self,event):
        self.quit(Custom())

    def EVT_Menu_Exit(self,event):
        eventnet.driver.post('Quit')

class Custom(GameMenu):
    title = 'Choose a Level'
    options = []
    color = (255,255,255)

    def __init__(self):
        self.options = [f.replace('\\','/').split('/')[-1]
                        for f in Campaign.levels]
        for option in self.options:
            setattr(self,'EVT_Menu_%s' % option,self.launch)
        GameMenu.__init__(self)

    def EVT_KeyDown(self,event):
        if event.key == pygame.K_ESCAPE:
            self.quit()

    def launch(self,lvl):
        lvl = 'data/levels/' + self.selected
        self.quit(GameState(level.load(lvl)))

class ConfirmExit(GameMenu):
    title = 'Exit to system?'
    options = ['Yes',
               'No']

    def __init__(self,next=None):
        GameMenu.__init__(self)
        self.next = next

    def EVT_Menu_Yes(self,event):
        pygame.quit()
        sys.exit()

    def EVT_Menu_No(self,event):
        if self.next:
            old = self.next
            self.next = self.next.__new__(type(self.next))
            if hasattr(old,'gamestate'):
                self.next.__init__(old.gamestate)
            else:
                self.next.__init__()
        self.quit(self.next)
