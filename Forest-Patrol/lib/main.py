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

from directicus.engine import Engine
import menus,pygame

class Game(Engine):

    def run(self):
        Engine.run(self)

    def EVT_KeyDown(self,event):
        key = pygame.key.name(event.key)
        if key.lower() == 'f12':
            pygame.image.save(pygame.display.get_surface(),'screenshot.bmp')

def run():
    #try:
    #    import psyco
    #    psyco.full()
    #except ImportError:
    #    print 'psyco not found! If your game runs slowly try installing \
    #it from http://psyco.sourceforge.net.'
    e = Game(20)
    e.DEFAULT = menus.MainMenu
    e.run()
