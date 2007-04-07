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

import eventnet.driver

class Campaign(object):
    levels = [
        #'data/levels/tut1.lvl',
        #'data/levels/tut2.lvl',
        #'data/levels/tut3.lvl',
        #'data/levels/office.lvl',
        #'data/levels/server-room.lvl',
        #'data/levels/apartment.lvl',
        #'data/levels/roof.lvl',
        'data/levels/boss.lvl'
        ]

    @staticmethod
    def next(last=None):
        if last == None:
            return Campaign.levels[0]
        else:
            i = Campaign.levels.index(last)+1
            if i == len(Campaign.levels):
                return None
            else:
                return Campaign.levels[i]
