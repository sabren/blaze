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

from directicus.engine import State
import level,pygame,eventnet.driver

class GameState(State):

    def __init__(self,level=level.Level()):
        State.__init__(self)
        self.level = level
        self.bg = pygame.sprite.Group(self.level.s)

    def start(self):
        State.start(self)
        pygame.display.get_surface().blit(self.level.background,(0,0))
        pygame.display.flip()

    def EVT_tick(self,event):
        disp = pygame.display.get_surface()
        self.level.clear()
        self.level.update()
        self.level.draw()
        self.level.s.rect.left = self.level.player.rect.left
        self.level.s.rect.top = self.level.player.rect.top
        self.bg.clear(disp,self.level.background)
        self.bg.draw(disp)

    def EVT_KeyDown(self,event):
        if event.key == pygame.K_ESCAPE:
            self.quit()
            #eventnet.driver.post('pause',game=self)
