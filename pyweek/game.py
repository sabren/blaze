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


TEST_ROOM = "**this is a special flag to load the test room"

from room import Room
from hero import Bird
from display import MockDisplay
from roomphysics import RoomPhysics
from constants import SCREEN, ROOM


def makeTestRoom():
    rm = Room()
    ## @TODO: load hero position from level definition
    ## @TODO: clean this up. :)
    heroPos = (100,100)
    rm.hero = Bird(rm, heroPos)
    rm.physics = RoomPhysics(rm, drag=-1)
    rm.hero.setPosition((150,ROOM.HEIGHT-100))
    return rm

#############################################################

from display import MockDisplay
from controls import Controller
from render import BlockSprite, randomlyColoredSquare

class Game(State):

    def __init__(self, display, roomName=TEST_ROOM):
        super(Game, self).__init__(display) #@TODO: fix me!
        self.controls = Controller()
        self.sprites = SpriteGear(self.display)

        if roomName == TEST_ROOM:
            self.room = makeTestRoom()
            # a block to play with:
            self.sprites.sprites.add(
                BlockSprite(
                self.room.addBlock((SCREEN.WIDTH/2+150,SCREEN.HEIGHT-100), 32, 32),
                randomlyColoredSquare()))
        
        else:
            self.room = loader.roomFromFile(open(roomName))

            
        self.sprites.fromRoom(self.room)
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
        self.room.hero.metabolism.eat(Food(5,5)) # hack to lower metabolism
        self.controls.tick()
        self.sprites.tick()
        
    def kick(self):
        super(Game, self).kick()
        self.display.showImage(0,0,IMAGE.GAME)
        

if __name__=="__main__":
    import main
    main.main()
    
