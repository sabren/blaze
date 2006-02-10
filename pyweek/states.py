'Here we define some states for our console.'

import pygame, display, sys, eventnet.driver, unittest, os
import events, sounds, loader, cPickle, string, random
from constants import *
from pygame.locals import *
from pygame import locals as pg
from scorelist import ScoreList
from events import GAME, LEVELLIST, MENU
from health import Food
from statusbox import StatusBox
from display import MockDisplay, Display
from room import Room
from hero import Bird
from ode_to_pixel import *

'----Base classes----'
class Gear(eventnet.driver.Handler):

    'Top-level "Gear" object.'

    def __init__(self, display):
        super(Gear, self).__init__()
        self.display = display
        self.done = False
        self.capture() # start event handlers

    def tick(self):
        'This is what the mainloop calls.'
        pass # do nothing by default

# Other states should do this:
class State(Gear):
    'Ahh, yes. Our State class.'
    
    def __init__(self, display):
        super(State, self).__init__(display)
        self.next = None

    def kick(self):
        '''
        You kick it to make it start. ;)
        
        This is so we can pause the execution
        of a state and come back to it later.
        (eg, when a confirmation dialog pops
        up or whatever)
        '''
        self.done = False #we're not finished yet :)

class Scores(State):
    "A Scores state object that'll (in theory) handle all of our score related details"
    
    def __init__(self, display, score=0):
        super(Scores, self).__init__(display)
        self.maxScores = 10 # max number of scores on the highscore list
        self.display = display
        self.new = False # bool to tell us if we have a new score to post
        self.score = score # the points score for our new winner (if any)

    def kick(self):
        super(Scores, self).kick()

        #load previous scores (a list of tuples ('player_name', score)  )
        try:
            f = open('scores')
            self.scores = cPickle.load(f)
            f.close()
        except: # if the scores file doesn't exist create one
            self.scores = []
            f = open('scores', 'w')
            cPickle.dump(self.scores, f)
            f.close()
            pass

        # prep our font sizes (do this automatically in future?)
        self.display.addFont(20)
        self.display.addFont(30)
        self.display.addFont(40)

        self.new = True
        if self.score: # if we're checking out a new score
            if len(self.scores) > 0 and self.score > self.scores[-1]:
                #if there are other scores and we beat the last one
                #get our position
                high = 0
                while self.score < self.scores[high][1]:
                    high += 1
                self.place = high+1
            elif len(self.scores) < 1: self.place = 0 # or just put us in front
            else: self.new = False
            self.text = ''
        else: self.new = False
        if not self.new:
            self.display.showImage(0,0, IMAGE.SCORES)

            pos=[640/2+50, 480/2-50]
            for score in range(len(self.scores)):
                score = ': '.join([str(score+1),
                                   self.scores[score][0],
                                   str(self.scores[score][1])])
                self.display.text (score, 20, pos, (255, 255, 255),
                                   self.display.RIGHT)
                pos = [pos[0]+72, pos[1]+20]

        self.display.flip()

    def tick(self):
        if self.new:
            self.display.clear()
            self.display.text('What are your initials?', 40,
                              (640/3.5, 480/3), (255, 255, 255))
            self.display.text(self.text, 30, [640/2, 480/2], (255, 255, 255),
                              self.display.CENTER)
            self.display.flip()

    def EVT_KeyDown(self, event):
        if self.new:
            if pygame.key.name(event.key) in string.ascii_lowercase:
                if len(self.text) < 3:
                    self.text += pygame.key.name(event.key).upper()
            elif event.key == K_BACKSPACE and self.text <> '':
                if self.text <> '': self.text = self.text[:-1]
            elif event.key == K_RETURN and len(self.text) == 3:
                print self.place
                self.scores.insert(self.place, (self.text, self.score))
                if len(self.scores) > 10: self.scores = self.scores[:10]
                cPickle.dump(self.scores, open('scores', 'w'))
                self.done = True
                self.next = Scores(self.display)
        elif not self.done: self.done = True

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

class LevelList(State):
    FONTSIZE = 30

    def __init__(self, display):

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

class Menu(State):

    def kick(self):
        super(Menu, self).kick()
        self.display.showImage(0,0, IMAGE.MENU)

    def EVT_KeyDown(self, event):
        if not self.done:
            if event.key == K_p:
                eventnet.driver.post(MENU.PLAY)
            elif event.key == K_1:
                self.done = True
                self.next = Scores(self.display, 1000)
            elif event.key == K_2:
                self.done = True
                self.next = Scores(self.display, 2000)
            elif event.key == K_h:
                eventnet.driver.post('SCORE')
                pass
            elif event.key == K_e:
                eventnet.driver.post('HELP')
            elif event.key == K_c:
                eventnet.driver.post('CREDITS')
            elif event.key == K_x:
                eventnet.driver.post(MENU.EXIT)

    def EVT_HIGHSCORE(self, event):
        self.done = True
        self.next = Scores(self.display)
            
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

def makeTestRoom():
    return Room()

#############################################################

class Game(State):

    def __init__(self, display, roomName=ROOM.TEST_ROOM):

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


# reference:
# http://kai.vm.bytemark.co.uk/~piman/writing/sprite-tutorial.shtml

"""
Our goal here is to display sprites on the
screen based on the positions calculated from
pyODE.

Remember, the room is modelled as blocks in pyODE,
and as pyODE works its magic, the blocks move around
in space. What we need to do on each frame is check
where the blocks are and put some sprites in the
corresponding places on the 2d screen.

However, we *only* need to do this for blocks
that move: since immobile platforms are just
static bitmaps, they don't need their own
sprites.

So, after reading piman's sprite tutorial, it seems
like we're in good shape. All we really need to do
is create a Sprite that's linked to a GeomBox:
"""

class BlockSpriteTest(unittest.TestCase):
    def test(self):
        # first we create the physics side:
        import room
        rm = room.Room()

        #@TODO: this really should be a sphere i think...
        bk = rm.addBlock((50, 50), *SPRITE_SIZE)

        # now the display side:
        bs = BlockSprite(bk, pygame.surface.Surface((5,5)))
        self.assertEquals((50,50), bs.rect.center)
        

# here's the implementation
class BlockSprite(pygame.sprite.Sprite):
    def __init__(self, block, image):
        self.old_position = None

        super(BlockSprite, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.block = block
        self.update()


    def update(self):
        # ode tracks the center, so we just assign that
        # directly to our rect.center ... the [:2] of
        # course just drops the Z coordinate, which is
        # always 0 for our 2d world. :)
        self.rect.center = map(round, self.block.getPosition()[:2])


class WithForeground(pygame.sprite.RenderUpdates):
    """
    simple sprite ordering: foreground is always on top
    """
    def __init__(self, fg, *sprites):
        pygame.sprite.RenderUpdates.__init__(self, *sprites)
        self.add(fg)
        self.fg = fg
        
    def sprites(self):
        all = pygame.sprite.RenderUpdates.sprites(self)
        all.remove(self.fg)
        all.append(self.fg)
        return all


class SpriteGear(Gear):
    def __init__(self, display):
        super(SpriteGear, self).__init__(display)
        self.foreground = None
        self.background = pygame.image.load(IMAGE.GAME)
        fgSprite = pygame.sprite.Sprite()
        fgSprite.image = pygame.image.load(IMAGE.STATUS.TXT)
        fgSprite.rect = fgSprite.image.get_rect()
        fgSprite.rect.topleft = IMAGE.STATUS.TEXT_POS
        self.sprites = WithForeground(fgSprite)
        self.refresh()        

        self.heroSprite = None
        self.heroLeft = pygame.image.load(IMAGE.KIWI.LEFT)
        self.heroRight = pygame.image.load(IMAGE.KIWI.RIGHT)

    def refresh(self):
        """
        refresh the screen completely. you
        probably don't need to call this yourself.
        """
        self.display.blit(self.background, (0,0))
        if self.foreground:
            self.display.blit(self.foreground, (0,0))
        if pygame.display.get_init(): pygame.display.flip()

        
    def tick(self):
        self.sprites.update()
        rects = self.sprites.draw(self.display.screen)
        if self.foreground:
            for r in rects:
                self.display.blit(self.foreground, r, r)
        if pygame.display.get_init(): pygame.display.update(rects)
        self.sprites.clear(self.display, self.background)

    def fromRoom(self, rm, rmName):  
        # make sprites based on the content of the level
        self.heroSprite =BlockSprite(rm.hero, self.heroRight)
        self.sprites.add(self.heroSprite)
        if rmName != ROOM.TEST_ROOM:
            self.foreground = pygame.image.load("rooms/%s-fore.png" % rmName)
            newBack = pygame.image.load("rooms/%s-back.png" % rmName)
            self.background.blit(newBack, (0,0),((0,0),(540,480)))
        self.refresh()

    def EVT_GAME_LEFT(self, event):
        self.heroSprite.image = self.heroLeft

    def EVT_GAME_RIGHT(self, event):
        self.heroSprite.image = self.heroRight
            


# this is just a handy sprite maker: a randomly colored square
# (with an alpha channel)

def randomlyColoredSquare():
    image = pygame.Surface(SPRITE_SIZE)
    image = image.convert()
    image.fill(pygame.color.Color("0x%08x" % random.randint(0,256**4)))
    return image

class Controller(Gear):
    """
    like a gamepad with repeating events...
    """
    def __init__(self):
        super(Controller, self).__init__(None)
        self.buttonsDown = []
        self.ticks = 0
        self.keymap = {
            pg.K_x : GAME.QUIT,
            pg.K_RIGHT : GAME.RIGHT,
            pg.K_LEFT : GAME.LEFT,
            pg.K_UP : GAME.UP,
            pg.K_DOWN : GAME.DOWN,
            pg.K_SPACE : GAME.JUMP,
        }

    def EVT_KeyDown(self, event):
        if event.key in self.keymap:
            eventnet.driver.post(self.keymap[event.key])
            self.buttonsDown.append(self.keymap[event.key])

    def EVT_KeyUp(self, event):
        if event.key in self.keymap:
            self.buttonsDown.remove(self.keymap[event.key])

    def tick(self):
        self.ticks += 1
        if self.ticks < REPEAT.TICKS:
            pass
        else:
            self.ticks = 0
            for button in self.buttonsDown:
                eventnet.driver.post(button)
