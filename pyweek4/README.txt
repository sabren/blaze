Ascent of Justice
===============

Entry in PyWeek #4  <http://www.pyweek.org/4/>
Team: Trailblazer
Members: mcferrill


DEPENDENCIES:

You might need to install some of these before running the game:

    Python:     http://www.python.org/
    PyGame:     http://www.pygame.org/
    Directicus:   http://blazeofglory.org/projects/directicus


RUNNING THE GAME:

On Windows or Mac OS X, locate the "run_game.pyw" file and double-click it.

Othewise open a terminal / console and "cd" to the game directory and run:

  python run_game.py

  

  
HOW TO PLAY THE GAME:

		Once the game is started you can select "Start Game" or if you've saved 
	a previous game you can select "Load Game".
	
	Controls:
		Right Arrow:  Move right
		Left Arrow:   Move left
		Left Control: Kick
		Left Alt:     Punch
		Left Shift:   Sprint
		
		
		
LEVEL EDITOR (SOURCE DISTRIBUTION):

		To create a new level change directory into the game folder and run:
	python levelGen.py <filename> <width> <height> and a new level will be created.
	
		To edit levels use the levelEdit.py script like so: python levelEdit.py <filename>. 
	The arrow keys scroll the map, use left mouse button to select objects (drag to get a 
	placement preview) and click again to place. Right mouse button deletes selected object 
	type.


LICENSE:

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