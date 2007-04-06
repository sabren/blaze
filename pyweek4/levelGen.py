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

import sys,pygame
pygame.display.set_mode((800,600))
from lib import level,data

if __name__=='__main__':
    if len(sys.argv) == 4:
        filename = sys.argv[1]
        size = (int(sys.argv[2]),
                int(sys.argv[3]))
        lvl = level.Level(data.Basement,size)
        level.save(lvl,filename)
    else:
        print 'usage: python %s <filename> <width> <height>' % sys.argv[0]
