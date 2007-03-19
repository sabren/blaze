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

import directicus.engine, pygame, editor, os, game
from level import grass,load

class Menu(directicus.engine.Menu):

    color = (0,0,0)
    hover = (100,100,100)

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
        pygame.display.get_surface().blit(self.background,(0,0))
        icon = pygame.image.load('data/cursors/sword.bmp')
        icon.set_colorkey((14,56,102))
        pygame.display.set_caption('Forest Patrol')
        pygame.display.set_icon(icon)

        directicus.engine.Menu.__init__(self)
        directicus.engine.Menu.start(self)
        #pygame.mouse.set_visible(False)

    def EVT_KeyDown(self,event):
        if pygame.key.name(event.key) == 'escape':
            self.quit()

    def quit(self,next=None):
        #pygame.mouse.set_visible(True)
        directicus.engine.Menu.quit(self,next)

class MainMenu(Menu):

    title = 'Forest Patrol'
    options = ['New Game','Level Editor','Quit']

    def EVT_Menu_NewGame(self,event):
        self.quit(game.Game())

    def EVT_Menu_LevelEditor(self,event):
        self.quit(editor.LevelEditor())

class editChoice(Menu):
    
    title = 'Edit Level'
    options = []

    def __init__(self):
        for lvl in os.listdir('data/levels'):
            if not os.path.isdir(lvl):
                self.options.append(os.path.split(lvl)[1])
                setattr(self,'EVT_Menu_'+lvl,self.edit)
        Menu.__init__(self)

    def edit(self,e):
        lvl = load(os.path.join('data/levels',self.selected))
        editor.LevelEditor.level = lvl
        self.quit(editor.LevelEditor())
