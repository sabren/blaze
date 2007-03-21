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

import directicus.engine, pygame, editor, os, game, eventnet.driver, resources
from directicus.sfx import Music,Audio
from level import grass,load

class Menu(directicus.engine.Menu):

    color = (0,0,0)
    hover = (100,100,100)
    headerFont = pygame.font.Font('data/font.ttf',50)
    headerFont.set_underline(True)
    regularFont = pygame.font.Font('data/font.ttf',30)

    #def __init__(self):
    #    self.cursor = pygame.image.load('data/cursors/arrow.bmp')
    #    self.cursor.set_colorkey((14,56,102))

    #def EVT_tick(self,event):
    #    directicus.engine.Menu.EVT_tick(self,event)
    #    icon = pygame.image.load('data/cursors/sword.bmp')
    #    icon.set_colorkey((14,56,102))
    #    pygame.display.set_caption('Forest Patrol')
    #    pygame.display.set_icon(icon)
    #    rect = self.cursor.get_rect()
    #    rect.topleft = pygame.mouse.get_pos()
    #    pygame.display.get_surface().blit(self.cursor,rect)
    #    pygame.display.update(rect)

    def start(self):
        self.background = pygame.image.load('data/menu.png')
        self.audio = Audio()
        self.music = Music()
        self.audio.volume = 0.3
        self.music.volume = 0.5
        pygame.display.get_surface().blit(self.background,(0,0))
        icon = resources.Cursor.sword #pygame.image.load('data/cursors/sword.png')
        icon.set_colorkey((14,56,102))
        pygame.display.set_caption('Forest Patrol')
        pygame.display.set_icon(icon)

        directicus.engine.Menu.__init__(self)
        directicus.engine.Menu.start(self)
        #pygame.mouse.set_visible(False)

    def EVT_MouseButtonDown(self,event):
        if self.selected:
            self.audio.play('data/sounds/sword-draw.wav')
        directicus.engine.Menu.EVT_MouseButtonDown(self,event)

    def EVT_KeyDown(self,event):
        if pygame.key.name(event.key) == 'escape':
            self.quit()

    def quit(self,next=None):
        #pygame.mouse.set_visible(True)
        directicus.engine.Menu.quit(self,next)

class MainMenu(Menu):

    title = 'Forest Patrol'
    options = ['New Game','Level Editor','Exit to System']

    def start(self):
        Menu.start(self)
        pygame.display.set_mode((800,600),pygame.HWSURFACE)
        if not pygame.mixer.music.get_busy():
            self.music.play('data/music/menu.mp3',-1)

    def EVT_Menu_NewGame(self,event):
        self.quit(game.Game())

    def EVT_Menu_LevelEditor(self,event):
        self.quit(editor.LevelEditor())

    def EVT_Menu_ExittoSystem(self,event):
        self.quit()

    def quit(self,next=None):
        if not next:
            self.quit(ConfirmExit())
        else:
            Menu.quit(self,next)

class editChoice(Menu):
    
    title = 'Edit Level'
    options = []

    def __init__(self):
        self.options = list()
        for lvl in os.listdir('data/levels'):
            if not os.path.isdir(lvl):
                self.options.append(os.path.split(lvl)[1])
                setattr(self,'EVT_Menu_'+lvl,self.edit)
        Menu.__init__(self)

    def edit(self,e):
        lvl = load(os.path.join('data/levels',self.selected))
        editor.LevelEditor.level = lvl
        self.quit(editor.LevelEditor())

class ConfirmExit(Menu):
    title = 'Exit to system?'
    options = ['Yes','No']

    def EVT_Menu_Yes(self,event):
        pygame.quit()
        eventnet.driver.post('Quit')

    def EVT_Menu_No(self,event):
        self.quit()
