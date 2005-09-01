"""
GameState : this is the main control
loop for actually playing the game.
"""
import unittest
from states import State
from events import INPUT
import eventnet.driver


"""
Okay. So the Game object is the main routine for the
actual game. There should be a room and a hero:
"""

class GameTest(unittest.TestCase):

    def testPieces(self):
        g = Game()
        assert g.hero, "we should have a hero"
        assert g.room, "we should have a room"


    """
    the INPUT_RIGHT event should move the hero
    to the right.
    """

    def test_INPUT_RIGHT(self):
        g = Game()
        
        oldx, oldy = g.heroPosition()
        
        # two things need to happen:
        # first, we need to post the input:
        eventnet.driver.post(INPUT.RIGHT)
        
        # then we need to give the physics
        # simulation a chance to run:
        g.tick()

        # now the hero should have moved:
        newx, newy = g.heroPosition()
        assert newx > oldx, "hero should move to the right"
        
    def test_INPUT_LEFT(self):
        g = Game()

        lastx, lasty = g.heroPosition()

        eventnet.driver.post(INPUT.LEFT)

        g.tick()

        newx, newy = g.heroPosition()

        assert newx < lastx, "hero should move left"

## goal: INPUT_left event to move left 
# goal: INPUT_down to go down ladder
# goal: INPUT_jump to jump/flap
# goal: tie keyboard keys to events

# goal: on collide with egg, increase score
# goal: on collide with food, talk to hero's health model
#       --  pass the food to hero_instance.metabolism.eat(food)

# goal: on collide with exit
# goal: GAME_up to go up (ladder) or through door


TEST_ROOM = "**this is a special flag to load the test room"

from room import Room
from hero import Bird
from roomphysics import RoomPhysics


def makeTestRoom():
    rm = Room()
    return rm


class Game(State):

    HERO_SPEED = 5

    def __init__(self, roomName=TEST_ROOM):
        super(Game, self).__init__()
        if roomName == TEST_ROOM:
            self.room = makeTestRoom()
        else:
            self.room = room

        ## @TODO: load hero position from level definition
        ## @TODO: clean this up. :)
        heroPos = (100,100)
        heroRadius = 32
        self.hero = Bird(self.room, heroPos, heroRadius)

        self.physics = RoomPhysics(self.room, self.hero.geom.getBody())

    def EVT_INPUT_RIGHT(self, event):
        """
        when the player tells us to go right, we
        should move the hero to the right in our world.
        """
        self.hero.walk((self.HERO_SPEED))

    def EVT_INPUT_LEFT(self, event):
        self.hero.walk((-self.HERO_SPEED))

    

    def heroPosition(self):
        return self.hero.getPosition()


    def tick(self):
        self.physics.step()


if __name__=="__main__":
    unittest.main()
