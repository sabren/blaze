"""
Game : this is the main control
loop for actually playing the game.
"""
import unittest
import images
from states import State
from events import GAME
import pygame.locals as pg
import eventnet.driver
from constants import *
from health import Food

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
    rm.physics = RoomPhysics(rm, drag=-0.01)
    return rm

#############################################################

from display import MockDisplay

class Game(State):

    def __init__(self, display, roomName=TEST_ROOM):
        super(Game, self).__init__(display) #@TODO: fix me!
        if roomName == TEST_ROOM:
            self.room = makeTestRoom()
        else:
            self.room = loader.roomFromFile(open(roomName))
            
        self.hero = self.room.hero
        self.manual = False # manual stepping with s key (toggle with `)


    def EVT_GAME_RIGHT(self, event):
        """
        when the player tells us to go right, we
        should move the hero to the right in our world.
        """
        self.hero.walk(RIGHT)

    def EVT_GAME_LEFT(self, event):
        self.hero.walk(LEFT)

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
        self.room.hero.metabolism.eat(Food(5,5))
        #print self.room.hero.geom.getPosition()
        


    def EVT_KeyDown(self, event):
        #@TODO: configurable keymap?
        keymap = {
            pg.K_x : GAME.QUIT,
            pg.K_RIGHT : GAME.RIGHT,
            pg.K_LEFT : GAME.LEFT,
            pg.K_SPACE : GAME.JUMP,
        }
        if event.key in keymap:
            eventnet.driver.post(keymap[event.key])
        elif event.key ==pg.K_BACKQUOTE:
            self.manual = not self.manual 
        elif event.key ==pg.K_s:
            self.tick()

    def kick(self):
        super(Game, self).kick()
        self.display.showImage(0,0,images.GAME)



if __name__=="__main__":
    import sys
    from display import Display
    from main import Console, pygame_events
    import pygame
    from constants import SCREEN
    from render    import WithForeground, BlockSprite, randomlyColoredSquare
    
    if "test" in sys.argv:
        sys.argv.remove("test")
        unittest.main()
    else:

        background = pygame.image.load("demo/gravdemo-back.png")       

        # FOREGROUND
        foreground = pygame.image.load("demo/gravdemo-fore.png")
        foreground = pygame.surface.Surface((1, 1))
        fgSprite = pygame.sprite.Sprite()
        fgSprite.image = foreground
        fgSprite.rect = foreground.get_rect()
        ## sprite group
        group = WithForeground(fgSprite)
        
        disp = Display(t='Kiwi Run')
        game = Game(disp)
        con = Console(disp)
        con.state.done= True
        con.state.next = game

        rm = game.room

        #add the hero
        group.add(BlockSprite(rm.hero, pygame.image.load(images.KIWI.PLAIN)))
        rm.hero.setPosition((150,SCREEN.HEIGHT-100))
        # and a floor:
        w = SCREEN.WIDTH
        h= 50
        group.add(BlockSprite(
            rm.addGeom((SCREEN.WIDTH/2,SCREEN.HEIGHT-h/2), w,h),
            pygame.Surface((w,h))))
        
        # and some block:
#        group.add(
#            BlockSprite(
#            rm.addBlock((SCREEN.WIDTH/2+150,SCREEN.HEIGHT-100), 32, 32),
#            randomlyColoredSquare()))

        screen = disp.screen
        screen.blit(background, (0,0))
        game.manual = False
        while not con.done:
            pygame_events()
            group.update()
            rects = group.draw(screen)    
            pygame.display.update(rects)
            group.clear(screen, background)
            if not game.manual:
                con.tick()
        pygame.quit()   


        screen.blit(background, (0,0))        
