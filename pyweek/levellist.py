"""
Game : this is the main control
loop for actually playing the game.
"""
import unittest
import os

import states
from states import State
from events import GAME
import eventnet.driver
from constants import *
from health import Food
import sounds
from render import SpriteGear
from statusbox import StatusBox

from display import MockDisplay
from display import Display
from controls import Controller
from render import BlockSprite, randomlyColoredSquare
import pygame

class LevelList(State):
    FONTSIZE = 30

    def __init__(self, display):
	import loader

        super(LevelList, self).__init__(display) #@TODO: fix me!
        self.controls = Controller()
        self.status = StatusBox()
        self.status.capture()
	self.display = display

	roomList = os.listdir ("./rooms/")

	display.addFont (self.FONTSIZE)

	self.roomList = []
	self.selected = 0

	for x in roomList:
		if len(x) > 4:
			if x[len(x)-4:] == ".svg":
				self.roomList.append (x)
				

	self.levelCount = len(self.roomList)


    def EVT_LEVELLIST_DOWN(self, event):
        """
        when the player tells us to go right, we
        should move the hero to the right in our world.
        """
        #self.hero.run(RIGHT)
	#self.moveDown();
	print "DOWN"
	self.selected += 1

	if self.selected > len(self.roomList):
		self.selected = len(self.roomList)

    def EVT_LEVELLIST_UP(self, event):
        #self.hero.run(LEFT)
	self.seleced-=1

	if self.selected < 0:
		self.selected = 0

    def EVT_LEVELLIST_QUIT(self, event):
        self.done = True

    def tick(self):
	self.display.clear()

	i = 0

        for x in self.roomList:
		if i == self.selected:
			color = (255,255,255,255)
		else:
			color = (200,200,200,255)

		self.display.text (x[:len(x)-4], self.FONTSIZE, [320, 240-len(self.roomList)*self.FONTSIZE/1.3+i*self.FONTSIZE/1.3], color, Display.CENTER)
		i+=1

	self.display.flip()
        
    def kick(self):
        super(LevelList, self).kick()
        

if __name__=="__main__":
    import main
    main.main()
    
