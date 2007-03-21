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

import directicus.engine,pygame,level,sprites
from directicus.sfx import Audio,Music

class Game(directicus.engine.State):

    level = level.load('data/levels/test')

    def __init__(self):
        directicus.engine.State.__init__(self)
        self.audio = Audio()
        self.music = Music()
        self.audio.volume = 0.7
        self.music.volume = 0.5
        self.level.render()
        self.selected = []
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.level.surface
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.topleft = (0,0)
        self.keys = [0,0,0,0]
        self.interface = pygame.sprite.Group()
        self.paused = False
        self.mouse = 0

    def start(self):
        directicus.engine.State.start(self)
        self.music.play('data/music/battle.mp3',-1)
        self.level.game()
        self.mini = sprites.MiniMap()
        self.mini.level = self.level

    def quit(self,next=None):
        self.music.stop(500)
        self.music.play('data/music/menu.mp3')
        directicus.engine.State.quit(self,next)

    def EVT_tick(self,event):
        self.level.clear()
        self.level.rangers.update(self.level)
        self.level.collideRects = list()
        for sprite in self.level.sprites:
            if hasattr(sprite,'baseRect'):
                self.level.collideRects.append(sprite.baseRect)

        for sprite in self.interface:
            sprite.kill()

        for sprite in self.selected:
            base = pygame.sprite.Sprite(self.level.sprites,self.interface)
            base.rect = pygame.rect.Rect(sprite)
            base.rect.height = sprite.rect.height/2
            base.rect.bottom = sprite.rect.bottom-1
            base.image = pygame.Surface(base.rect.size)
            base.image.fill((255,0,0))
            base.image.set_colorkey((255,0,0))
            pygame.draw.ellipse(base.image,(0,255,0),base.image.get_rect(),2)

        pygame.display.get_surface().fill((0,0,0))
        self.level.draw()
        pygame.display.get_surface().blit(self.sprite.image,self.sprite.rect)

        if self.mouse:
            msPos = pygame.mouse.get_pos()
            r = pygame.rect.Rect(0,0,0,0)
            r.width = msPos[0]-self.mouse[0]
            r.height = msPos[1]-self.mouse[1]
            r.normalize()
            if msPos[0] > self.mouse[0] and msPos[1] > self.mouse[1]:
                r.topleft = self.mouse
                r.bottomright = msPos
            elif msPos[0] < self.mouse[0] and msPos[1] < self.mouse[1]:
                r.bottomright = self.mouse
                r.topleft = msPos
            elif msPos[0] > self.mouse[0] and msPos[1] < self.mouse[1]:
                r.topright = msPos
                r.bottomleft = self.mouse
            else:
                r.bottomleft = msPos
                r.topright = self.mouse
            pygame.draw.rect(pygame.display.get_surface(),(0,255,0),r,1)

        if self.keys[2]:
            if -self.sprite.rect.x+pygame.display.get_surface().get_width() < self.level.size[0]:
                self.sprite.rect.x -= 30
        if self.keys[3]:
            if -self.sprite.rect.x > 0:
                self.sprite.rect.x += 30
        if self.keys[0]:
            if -self.sprite.rect.y > 0:
                self.sprite.rect.y += 30
        if self.keys[1]:
            if -self.sprite.rect.y+pygame.display.get_surface().get_height() < self.level.size[1]:
                self.sprite.rect.y -= 30

        self.mini.pos = (-self.sprite.rect.left,
                         -self.sprite.rect.top)
        self.mini.tick()
        self.mini.draw()
        pygame.display.flip()

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
        else:
            pos = (event.pos[0]-self.sprite.rect.left,
                   event.pos[1]-self.sprite.rect.top)
            if event.button == 1:
                self.mouse = event.pos
                self.selected = []
                for ranger in self.level.rangers:
                    if ranger.rect.collidepoint(pos) and ranger.collidePoint(pos):
                        self.selected.append(ranger)
            elif self.selected:
                for r in self.selected:
                    r.target((event.pos[0]-self.sprite.rect.left,
                              event.pos[1]-self.sprite.rect.top))

    def EVT_MouseButtonUp(self,event):
        if event.button == 1 and self.mouse:
            msPos = event.pos
            r = pygame.rect.Rect(0,0,0,0)
            r.width = msPos[0]-self.mouse[0]
            r.height = msPos[1]-self.mouse[1]
            r.normalize()
            if msPos[0] > self.mouse[0] and msPos[1] > self.mouse[1]:
                r.topleft = self.mouse
                r.bottomright = msPos
            elif msPos[0] < self.mouse[0] and msPos[1] < self.mouse[1]:
                r.bottomright = self.mouse
                r.topleft = msPos
            elif msPos[0] > self.mouse[0] and msPos[1] < self.mouse[1]:
                r.topright = msPos
                r.bottomleft = self.mouse
            else:
                r.bottomleft = msPos
                r.topright = self.mouse
            r.left -= self.sprite.rect.left
            r.top -= self.sprite.rect.top

            for ranger in self.level.rangers:
                if ranger.rect.colliderect(r):
                    self.selected.append(ranger)
            self.mouse = None

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
        elif key == 'escape':
            self.quit()
