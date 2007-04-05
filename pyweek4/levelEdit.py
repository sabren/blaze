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
pygame.display.set_mode((800,600))
from directicus.engine import Engine,State
from lib.menus import GameMenu as menu
from lib import data, level, player, sprites
import sys, pygame

font = menu.regularFont

class LevelEditor(State):

    def __init__(self):
        State.__init__(self)
        if len(sys.argv) == 2:
            self.filename = sys.argv[1]
            self.level = level.load(self.filename)
        else:
            print 'usage: python %s <level>' % sys.argv[0]
            sys.exit()
        pygame.display.set_icon(data.icon)
        pygame.display.set_caption('Level Editor')
        self.bg = pygame.sprite.Group(self.level.s)

        self.buttons = pygame.sprite.Group()

        self.playerBtn = pygame.sprite.Sprite()
        self.playerBtn.image = data.Hero.button
        self.playerBtn.rect = self.playerBtn.image.get_rect()
        self.playerBtn.rect.topleft = (10,10)

        self.floorBtn = pygame.sprite.Sprite()
        self.floorBtn.image = self.level.tileset.floor
        self.floorBtn.rect = self.floorBtn.image.get_rect()
        self.floorBtn.rect.topleft = (10,self.playerBtn.rect.bottom+10)

        self.wallBtn = pygame.sprite.Sprite()
        self.wallBtn.image = self.level.tileset.wall
        self.wallBtn.rect = self.wallBtn.image.get_rect()
        self.wallBtn.rect.topleft = (10,self.floorBtn.rect.bottom+10)

        self.camBtn = pygame.sprite.Sprite()
        self.camBtn.image = data.Camera.still
        self.camBtn.rect = self.camBtn.image.get_rect()
        self.camBtn.rect.topleft = (10,self.wallBtn.rect.bottom+10)

        self.stairBtn = pygame.sprite.Sprite()
        self.stairBtn.image = self.level.tileset.stair
        self.stairBtn.rect = self.stairBtn.image.get_rect()
        self.stairBtn.rect.topleft = (10,self.camBtn.rect.bottom+10)

        self.enemyBtn = pygame.sprite.Sprite()
        self.enemyBtn.image = data.Enemy.button
        self.enemyBtn.rect = self.enemyBtn.image.get_rect()
        self.enemyBtn.rect.topleft = (10,self.stairBtn.rect.bottom+10)

        self.exitBtn = pygame.sprite.Sprite()
        self.exitBtn.image = self.level.tileset.exitDoor
        self.exitBtn.rect = self.exitBtn.image.get_rect()
        self.exitBtn.rect.topleft = (10,self.enemyBtn.rect.bottom+10)

        self.saveBtn = pygame.sprite.Sprite()
        self.saveBtn.image = font.render('Save',True,(255,255,255))
        self.saveBtn.rect = self.saveBtn.image.get_rect()
        self.saveBtn.rect.topleft = (10,self.exitBtn.rect.bottom+10)

        self.buttons.add(self.playerBtn,
                         self.floorBtn,
                         self.wallBtn,
                         self.camBtn,
                         self.stairBtn,
                         self.enemyBtn,
                         self.exitBtn,
                         self.saveBtn)

        self.keys = [0,0,0,0]
        self.selected = None
        self.cursor = None
        self.level.player.release()

    def EVT_MouseButtonDown(self,event):
        if self.saveBtn.rect.collidepoint(event.pos):
            level.save(self.level,self.filename)
            sys.exit()
        for button in self.buttons:
            if button.rect.collidepoint(event.pos):
                self.selected = button
                pygame.mouse.set_visible(False)
                self.cursor = pygame.sprite.Sprite()
                self.cursor.image = button.image.copy()
                self.cursor.rect = pygame.Rect(button)
                return
        event.pos = (event.pos[0]-self.level.s.rect.left,
                     event.pos[1]-self.level.s.rect.top)
        if event.button == 1:
            if self.selected == self.playerBtn:
                self.level.player.rect.center = event.pos
            elif self.selected == self.wallBtn:
                wall = sprites.Wall(event.pos,self.level)
            elif self.selected == self.floorBtn:
                floor = sprites.Floor(event.pos,self.level)
            elif self.selected == self.camBtn:
                camera = sprites.Camera(event.pos,self.level)
            elif self.selected == self.stairBtn:
                stair = sprites.Stair(event.pos,self.level)
            elif self.selected == self.enemyBtn:
                enemy = sprites.Enemy(event.pos,self.level)
            elif self.selected == self.exitBtn:
                self.level.exit.rect.center = event.pos
        else:
            if self.selected == self.wallBtn:
                for sprite in self.level.walls:
                    if sprite.rect.collidepoint(event.pos):
                        sprite.kill()
            elif self.selected == self.floorBtn:
                for sprite in self.level.floors:
                    if sprite.rect.collidepoint(event.pos):
                        sprite.kill()
            elif self.selected == self.camBtn:
                for sprite in self.level.cameras:
                    if sprite.rect.collidepoint(event.pos):
                        sprite.kill()
            elif self.selected == self.stairBtn:
                for sprite in self.level.stairs:
                    if sprite.rect.collidepoint(event.pos):
                        sprite.kill()
            elif self.selected == self.enemyBtn:
                for sprite in self.level.enemies:
                    if sprite.rect.collidepoint(event.pos):
                        sprite.kill()

    def EVT_MouseButtonUp(self,event):
        self.cursor = None
        pygame.mouse.set_visible(True)

    def EVT_tick(self,event):
        disp = pygame.display.get_surface()
        if self.keys[0]:
            self.level.s.rect.left += 10
        if self.keys[1]:
            self.level.s.rect.left -= 10
        if self.keys[2]:
            self.level.s.rect.top += 10
        if self.keys[3]:
            self.level.s.rect.top -= 10
        self.level.clear()
        self.level.draw()
        disp.fill((0,0,0))
        self.bg.draw(disp)
        self.buttons.draw(disp)
        for button in self.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()) or button == self.selected:
                pygame.draw.rect(disp,(255,255,255),button.rect,1)
        if self.cursor:
            self.cursor.rect.center = pygame.mouse.get_pos()
            disp.blit(self.cursor.image,self.cursor.rect)
        for enemy in self.level.enemies:
            enemy.release()
        pygame.display.flip()

    def EVT_KeyDown(self,event):
        if event.key == pygame.K_LEFT:
            self.keys[0] = 1
        elif event.key == pygame.K_RIGHT:
            self.keys[1] = 1
        elif event.key == pygame.K_UP:
            self.keys[2] = 1
        elif event.key == pygame.K_DOWN:
            self.keys[3] = 1
        elif event.key == pygame.K_ESCAPE:
            import sys
            sys.exit()

    def EVT_KeyUp(self,event):
        if event.key == pygame.K_LEFT:
            self.keys[0] = 0
        elif event.key == pygame.K_RIGHT:
            self.keys[1] = 0
        elif event.key == pygame.K_UP:
            self.keys[2] = 0
        elif event.key == pygame.K_DOWN:
            self.keys[3] = 0

if __name__=='__main__':
    e = Engine(40)
    e.DEFAULT = LevelEditor
    e.run()
