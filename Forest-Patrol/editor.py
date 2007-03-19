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

import directicus.engine, pygame, menus, sprites, level

class LevelEditor(directicus.engine.State):

    level = None

    def __init__(self):
        directicus.engine.State.__init__(self)
        disp = pygame.display.get_surface()
        self.treeBtn = sprites.Tree()
        self.treeBtn.image = pygame.image.load('data/tree.bmp')
        self.treeBtn.rect.topleft = (5,5)
        self.rangerBtn = sprites.Ranger()
        self.rangerBtn.image = pygame.image.load('data/ranger.bmp')
        self.rangerBtn.rect.topleft = (5,self.treeBtn.rect.bottom + 5)
        self.castleBtn = sprites.Castle()
        self.castleBtn.image = pygame.image.load('data/castle-small.png')
        self.castleBtn.rect = self.castleBtn.image.get_rect()
        self.castleBtn.rect.topleft = (5,self.rangerBtn.rect.bottom + 5)
        self.save = pygame.sprite.Sprite()
        self.save.image = menus.MainMenu.regularFont.render('Save',True,(255,255,255))
        self.save.rect = self.save.image.get_rect()
        self.save.rect.topleft = (5,self.castleBtn.rect.bottom+5)
        self.btns = pygame.sprite.Group(self.rangerBtn,self.treeBtn,self.castleBtn,self.save)
        self.all = pygame.sprite.Group()
        self.pos = [0,0]
        self.keys = [0,0,0,0] #up,down,right,left
        self.selected = None

    def start(self):
        if self.level == None:
            self.quit(menus.editChoice())
        else:
            self.level.render()
            directicus.engine.State.start(self)
            pygame.display.get_surface().blit(self.level.background,self.pos)
            self.mini = sprites.MiniMap()
            self.mini.level = self.level
            self.EVT_tick(None)
            pygame.display.flip()

    def EVT_KeyDown(self,event):
        key = pygame.key.name(event.key)
        if key == 'right':
            self.keys[2] = 1
        elif key == 'left':
            self.keys[3] = 1
        elif key == 'up':
            self.keys[0] = 1
        elif key == 'down':
            self.keys[1] = 1
        elif pygame.key.name(event.key) == 'escape':
            self.level = None
            self.quit()

    def EVT_KeyUp(self,event):
        key = pygame.key.name(event.key)
        if key == 'right':
            self.keys[2] = 0
        elif key == 'left':
            self.keys[3] = 0
        elif key == 'up':
            self.keys[0] = 0
        elif key == 'down':
            self.keys[1] = 0

    def EVT_MouseButtonDown(self,event):
        if self.mini.rect.collidepoint(event.pos):
            relPos = self.mini.grow(
                (event.pos[0]-self.mini.rect.centerx,
                 event.pos[1]-self.mini.rect.centery))
            s = pygame.display.get_surface().get_size()
            self.sprite.rect.center = (-relPos[0]+s[0]/2,
                                       -relPos[1]+s[1]/2)
        elif self.save.rect.collidepoint(event.pos):
            level.save(self.level,self.level.filename)
            self.level = None
            self.quit()
        elif self.treeBtn.rect.collidepoint(event.pos):
            self.selected = self.treeBtn
        elif self.rangerBtn.rect.collidepoint(event.pos):
            self.selected = self.rangerBtn
        elif self.castleBtn.rect.collidepoint(event.pos):
            self.selected = self.castleBtn
        elif event.button == 1:
            event.pos = (event.pos[0]-self.pos[0],
                         event.pos[1]-self.pos[1])
            if self.selected == self.treeBtn:
                tree = sprites.Tree()
                tree.rect.center = event.pos
                self.level.trees.add(tree)
                self.level.sprites.add(tree)
            elif self.selected == self.rangerBtn:
                ranger = sprites.Ranger()
                ranger.rect.center = event.pos
                self.level.rangers.add(ranger)
                self.level.sprites.add(ranger)
            elif self.selected == self.castleBtn:
                castle = sprites.Castle()
                castle.rect.center = event.pos
                self.level.castles.add(castle)
                self.level.sprites.add(castle)
        else:
            event.pos = (event.pos[0]-self.pos[0],
                         event.pos[1]-self.pos[1])
            if self.selected == self.rangerBtn:
                for sprite in self.level.rangers:
                    if sprite.rect.collidepoint(event.pos) and sprite.collidePoint(event.pos):
                        sprite.kill()
            elif self.selected == self.treeBtn:
                for sprite in self.level.trees:
                    if sprite.rect.collidepoint(event.pos) and sprite.collidePoint(event.pos):
                        sprite.kill()
            elif self.selected == self.castleBtn:
                for sprite in self.level.castles:
                    if sprite.rect.collidepoint(event.pos) and sprite.collidePoint(event.pos):
                        sprite.kill()

    def EVT_tick(self,event):
        if self.keys[2]:
            self.pos[0] -= 30
        if self.keys[3]:
            self.pos[0] += 30
        if self.keys[0]:
            self.pos[1] += 30
        if self.keys[1]:
            self.pos[1] -= 30

        self.level.clear()
        disp = self.level.surface
        self.level.draw()
        pygame.display.get_surface().fill((0,0,0))
        pygame.display.get_surface().blit(self.level.surface,self.pos)
        self.btns.draw(pygame.display.get_surface())
        for button in self.btns:
            if button.rect.collidepoint(pygame.mouse.get_pos()) or self.selected == button:
                pygame.draw.rect(pygame.display.get_surface(),(255,255,255),button.rect,1)
        self.mini.pos = (-self.pos[0],-self.pos[1])
        self.mini.tick()
        self.mini.draw()
        pygame.display.flip()

if __name__=='__main__':
    e = directicus.engine.Engine()
    level.Level.size = (640,480)
    LevelEditor.level = level.Level()
    e.size = (800,600)
    e.DEFAULT = LevelEditor()
    e.run()
