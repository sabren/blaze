"""
here we define some states for our console.
"""
import pygame, display, sys, eventnet.driver, cPickle, string
import pygame, display, sys, eventnet.driver
from constants import IMAGE
from pygame.locals import *
from scorelist import ScoreList
#from levellist import LevelList
#from menu import Menu
#from game import Game

# Menu moved to menu.py... and back again :)
# Game moved to game.py... and back again :)

class Gear(eventnet.driver.Handler):
    def __init__(self, display):
        super(Gear, self).__init__()
        self.display = display
        self.done = False
        self.capture() # listen for events

    def tick(self):
        """
        then it starts ticking...
        by default, each tick does nothing.
        """
        pass


# other states should do this:
class State(Gear):

    def __init__(self, display):
        super(State, self).__init__(display)
        self.next = None

    def kick(self):
        """
        you kick it to make it start. :)
        
        This is so we can pause the execution
        of a state and com back to it later.
        (eg, when a confirmation dialog pops
        up or whatever)
        """
        self.done = False

class Scores(State):

    def kick(self):
        super(Scores, self).kick()
        try:
            file = open('scores', 'r')
            names = cPickle.load(file)
            scores = cPickle.load(file)
            file.close()
        except:
            names = []
            scores = []
            file = open('scores', 'w')
            cPickle.dump(names, file)
            cPickle.dump(scores, file)
            file.close()
            pass
        self.scores = ScoreList(names, scores)
        scr = []
        scor = self.scores.getScores()
        for score in scor:
            scr += [string.join([score[0], str(score[1])], ': ')]
        print scr
        self.display.showImage(0,0, IMAGE.SCORES)
        self.display.addFont(30)
        pos=[640/2, 480/2]
        for text in scr:
            self.display.text (text, 30, pos, justify=self.display.CENTER)
            pos = [pos[0]+50, pos[1]+30]
        self.display.flip()

    def EVT_KeyDown(self, event):
        if not self.done:
            self.done = True

class Credits(State):

    def kick(self):
        super(Credits, self).kick()
        self.display.showImage(0,0, IMAGE.CREDITS)

    def EVT_KeyDown(self, event):
        if not self.done:
            self.done = True

class Help(State):

    def kick(self):
        super(Help, self).kick()
        self.display.showImage(0,0, IMAGE.HELP)

    def EVT_KeyDown(self, event):
        if not self.done:
            self.done = True

class TextInput(State):

    def kick(self):
        super(TextInput, self).kick()
        try:
            file = open('scores', 'r')
            list = cPickle.load(file)
            file.close()
        except:
            file = open('scores', 'w')
            file.close()
            list = []
            pass
        self.scores = ScoreList(list)
        self.display.showImage(0,0, IMAGE.SCORE)
        self.s = ''

    def tick(self):
        if not self.done:
            if len(self.s) == 3:
                self.done = True
                self.next = Scores(self.display)
            else:
                self.display.text(self.s, 30, [640/2, 480/2])

    def EVT_KeyDown(self, event):
        if not self.done:
            if event.key == K_ESCAPE:
                self.done = True
            elif event.key == K_a:
                self.s += 'A'
            elif event.key == K_b:
                self.s += 'B'
            elif event.key == K_c:
                self.s += 'C'
            elif event.key == K_d:
                self.s += 'D'
            elif event.key == K_e:
                self.s += 'E'
            elif event.key == K_f:
                self.s += 'F'
            elif event.key == K_g:
                self.s += 'G'
            elif event.key == K_h:
                self.s += 'H'
            elif event.key == K_i:
                self.s += 'I'
            elif event.key == K_j:
                self.s += 'J'
            elif event.key == K_k:
                self.s += 'K'
            elif event.key == K_l:
                self.s += 'L'
            elif event.key == K_m:
                self.s += 'M'
            elif event.key == K_n:
                self.s += 'N'
            elif event.key == K_o:
                self.s += 'O'
            elif event.key == K_p:
                self.s += 'P'
            elif event.key == K_q:
                self.s += 'Q'
            elif event.key == K_r:
                self.s += 'R'
            elif event.key == K_s:
                self.s += 'S'
            elif event.key == K_t:
                self.s += 'T'
            elif event.key == K_u:
                self.s += 'U'
            elif event.key == K_v:
                self.s += 'V'
            elif event.key == K_w:
                self.s += 'W'
            elif event.key == K_x:
                self.s += 'X'
            elif event.key == K_y:
                self.s += 'Y'
            elif event.key == K_z:
                self.s += 'Z'

class Exit(State):
    """
    this state represents quitting the system.
    we should check for it explicitly.
    """
    def __init__(self):
        pass
    def kick(self):
        raise TypeError("never kick EXIT!")
    def tick(self):
        raise TypeError("never tick EXIT!")


# and only use the constant. It's a singleton:
EXIT = Exit()
del Exit

"""
Game : this is the main control
loop for actually playing the game.
"""
import unittest
import os

#import states
#from states import State
from events import GAME, LEVELLIST, MENU
import eventnet.driver
from constants import *
from health import Food
import sounds
from render import SpriteGear
from statusbox import StatusBox
from pygame import locals as pg

from display import MockDisplay
from display import Display
from controls import Controller
from render import BlockSprite, randomlyColoredSquare
from game import Game
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

	roomList = os.listdir (ROOM.DIRECTORY)

	display.addFont (self.FONTSIZE)

	self.roomList = []
	self.selected = 0

	for x in roomList:
		if len(x) > 4:
			if x[len(x)-4:] == ".svg":
				self.roomList.append (x)
				
        self.roomList = ["outside","joe1"]
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

	if self.selected >= len(self.roomList):
		self.selected = len(self.roomList)-1

    def EVT_LEVELLIST_UP(self, event):
        #self.hero.run(LEFT)
	self.selected-=1
	if self.selected < 0:
		self.selected = 0

    def EVT_LEVELLIST_ENTER(self, event):
        self.done = True
        print "SELECTED %s" % self.roomList[self.selected]        
        self.next = Game(self.display,
                         roomName=self.roomList[self.selected])
        
    def EVT_KeyDown(self, event):
        if not self.done:
            if event.key == pg.K_UP:
                eventnet.driver.post(LEVELLIST.UP)
            elif event.key == pg.K_DOWN:
                eventnet.driver.post(LEVELLIST.DOWN)
            elif event.key == pg.K_RETURN:
                eventnet.driver.post(LEVELLIST.ENTER)
            

    def tick(self):
	self.display.clear()

	i = 0

        for x in self.roomList:
		if i == self.selected:
			color = (255,255,255,255)
		else:
			color = (200,200,200,255)

		self.display.text (x[:len(x)], self.FONTSIZE, [320, 240-len(self.roomList)*self.FONTSIZE/1.3+i*self.FONTSIZE/1.3], color, Display.CENTER)
		i+=1

	self.display.flip()
        
    def kick(self):
        super(LevelList, self).kick()
        self.selected = 0
        self.tick()


#from states import State, EXIT, Scores, Credits, Help, TextInput
from game import Game
from constants import IMAGE
import eventnet.driver
from pygame.locals import *
from levellist import LevelList

class Menu(State):

    def kick(self):
        super(Menu, self).kick()
        self.display.showImage(0,0, IMAGE.MENU)

    def EVT_KeyDown(self, event):
        if not self.done:
            if event.key == K_p:
                eventnet.driver.post(MENU.PLAY)
            elif event.key == K_h:
                #eventnet.driver.post('SCORE')
                pass
            elif event.key == K_e:
                eventnet.driver.post('HELP')
            elif event.key == K_c:
                eventnet.driver.post('CREDITS')
            elif event.key == K_1:
                #eventnet.driver.post('HIGHSCORE')
                pass
            elif event.key == K_x:
                eventnet.driver.post(MENU.EXIT)

    def EVT_HIGHSCORE(self, event):
        self.done = True
        self.next = TextInput(self.display)
            
    def EVT_MENU_PLAY(self, event):
        # we need done = true in *here* because
        # of the tests...
        self.done = True
        #self.next = Game(self.display)
	self.next = LevelList(self.display)
        
    def EVT_MENU_EXIT(self, event):
        self.done = True
        self.next = EXIT

    def EVT_SCORE(self, event):
        self.done = True
        self.next = Scores(self.display)

    def EVT_CREDITS(self, event):
        self.done = True
        self.next = Credits(self.display)

    def EVT_HELP(self, event):
        self.done = True
        self.next = Help(self.display)

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


"""
Okay. So the Game object is the main routine for the
actual game. There should be a room and a hero:
"""

class GameTest(unittest.TestCase):

    def testPieces(self):
        g = Game(MockDisplay())
        assert g.hero, "we should have a hero"
        assert g.room, "we should have a room"


    """
    the GAME_RIGHT event should move the hero
    to the right.
    """
    def test_GAME_RIGHT(self):
        g = Game(MockDisplay())
        
        oldx, oldy = g.heroPosition()
        
        # two things need to happen:
        # first, we need to post the input:
        eventnet.driver.post(GAME.RIGHT)
        
        # then we need to give the physics
        # simulation a chance to run:
        g.tick()

        # now the hero should have moved:
        newx, newy = g.heroPosition()
        assert newx > oldx, "hero should move to the right"
        
    def test_GAME_LEFT(self):
        g = Game(MockDisplay())
        lastx, lasty = g.heroPosition()
        eventnet.driver.post(GAME.LEFT)
        g.tick()
        
        newx, newy = g.heroPosition()
        assert newx < lastx, "hero should move left"


    def test_GAME_QUIT(self):
        self.done = True


# goal: GAME_down to go down ladder
# goal: GAME_jump to jump/flap
# goal: tie keyboard keys to events

# goal: on collide with egg, increase score
# goal: on collide with food, talk to hero's health model
#       --  pass the food to hero_instance.metabolism.eat(food)

# goal: on collide with exit
# goal: GAME_up to go up (ladder) or through door



from room import Room
from hero import Bird
from display import MockDisplay
from roomphysics import RoomPhysics
from constants import SCREEN, ROOM


def makeTestRoom():
    return Room()

#############################################################

from display import MockDisplay
from controls import Controller
from render import BlockSprite, randomlyColoredSquare
import pygame

class Game(State):

    def __init__(self, display, roomName=ROOM.TEST_ROOM):
	import loader

        super(Game, self).__init__(display) #@TODO: fix me!
        self.controls = Controller()
        self.status = StatusBox()
        self.status.capture()

        # add the status bar sprites. the status
        # box is an event handler so they'll just
        # change on their own, but we have to add
        # them to the sprite group so they show up
        # on screen...        
        self.sprites = SpriteGear(self.display)
        for bar in self.status.bars.values():
            self.sprites.sprites.add(bar)

        if roomName == ROOM.TEST_ROOM:
            self.room = makeTestRoom()
            # a block to play with:
            self.sprites.sprites.add(
                BlockSprite(
                self.room.addBlock((SCREEN.WIDTH/2+150,SCREEN.HEIGHT-100), 32, 32),
                pygame.image.load(IMAGE.SOCCER)))
        
        else:
            self.room = loader.roomFromFile(open(ROOM.DIRECTORY+roomName+"-geom.svg"))

            
        self.sprites.fromRoom(self.room, roomName)
        # finally, note the hero:
        self.hero = self.room.hero
        


    def EVT_GAME_RIGHT(self, event):
        """
        when the player tells us to go right, we
        should move the hero to the right in our world.
        """
        self.hero.run(RIGHT)

    def EVT_GAME_LEFT(self, event):
        self.hero.run(LEFT)

    def EVT_GAME_JUMP(self, event):
        self.hero.jump()

    def EVT_GAME_QUIT(self, event):
        self.done = True
        
    def heroPosition(self):
        """
        Get the position of our intrepid kiwi.
        """
        return self.hero.getPosition()

    def tick(self):
        self.room.physics.step()
        self.room.hero.step()
        self.room.hero.metabolism.eat(Food(5,5, self.room, (0,0))) # hack to lower metabolism
        self.controls.tick()
        self.sprites.tick()
        
    def kick(self):
        super(Game, self).kick()
        self.sprites.refresh()
