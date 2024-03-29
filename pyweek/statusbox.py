import pygame, events
import eventnet.driver
import unittest
from constants import IMAGE

"""
[19:56]sabren: david: look at the drawing routines in pygame for the bars..
[19:56]sabren: david: you'll either want to blit a sprite repeatedly to fill in the bar, or just draw
[19:56]sabren: i'd go with blitting
[20:08]sabren: eykd: they should be their own event handler
[20:09]sabren: eykd: we'll just call bars.update() or something from Game.tick()
"""

class BarTest(unittest.TestCase):
    def testBar(self):
        """I need a good bar.
        """
        b = Bar(color=(255, 0, 0), position=(0,0), width=32, height=160)

class Bar(pygame.sprite.Sprite):
    """A status bar.
    """
    def __init__(self, color, position, width, height):
        super(Bar, self).__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = position # origin is top left

    def updateSize(self, newsize):
        """Update my size.
        """
        surface = self.image
        surface = pygame.transform.scale(surface, newsize)
        self.image = surface

        # turns out the sprite engine always blits us, so
        # no need to post an event
        #eventnet.driver.post(events.SCREEN.STATUS_CHANGED)
                
class StatusBoxTest(unittest.TestCase):
    """
    """
    def setUp(self):
        import room, hero
        self.sb = StatusBox()
        self.sb.capture()
        from roomphysics import RoomPhysics
        self.r = room.Room()
        self.bird = hero.Bird(self.r, (0,0))
        self.bird.capture()
        self.rp = RoomPhysics(self.r, self.bird.geom.getBody())


    def testStatusBox(self):
        """Is there a complete score box?
        """
        assert self.sb
        #assert self.sb.bars["fatbar"]
        assert self.sb.bars["fatbar_black"]
        #assert self.sb.bars["bloodbar"]
        assert self.sb.bars["bloodbar_black"]
        #assert self.sb.bars["timebar"]
        #assert self.sb.bars["timebar_black"]

    def testStatusBoxAction(self):
        """Ready, set, action!
        """
        from pygame.locals import *
        from pygame import display
        import health
        
        pygame.init()
        screen = pygame.display.set_mode([640, 480])
        sb = StatusBox()
        screen.clear()
        for key in sb.bars.keys():
            bar = sb.bars[key]
            screen.blit(bar.image, bar.rect)
        pygame.display.update()
        while pygame.event.poll().type != KEYDOWN:
            self.bird.step()
            food = health.Food(100,100)
            self.bird.metabolism.eat(food)
            for key in sb.bars.keys():
                bar = sb.bars[key]
                screen.blit(bar.image, bar.rect)
            pygame.time.delay(10)


    def testBloodEvents(self):
        """Does the status bar handle blood sugar events?
        """
        oldheight = self.sb.bars["bloodbar_black"].image.get_height()
        self.bird.step()
        import health
        candy = health.Food(100, 0)
        self.bird.metabolism.eat(candy)
        self.bird.step()
        newheight = self.sb.bars["bloodbar_black"].image.get_height()
        self.assertNotEqual(oldheight, newheight)
        
        

class StatusBox(eventnet.driver.Handler):
    def __init__(self):
        super(StatusBox, self).__init__()
        bloodcolor = (255, 0, 0)
        fatcolor = (0, 255, 0)
        timecolor = (0, 0, 255)
        self.bg = (255,255,255)   # white
        self.barheight = 376
        self.barwidth = 38
        blackheight = 1
        right = 640
        S = IMAGE.STATUS
        self.bars = {}
        #self.bars["fatbar"] = Bar(fatcolor, S.FATS_POS, self.barwidth, self.barheight)
        self.bars["fatbar_black"] = Bar(self.bg, S.FATS_POS, self.barwidth, blackheight)
        #self.bars["bloodbar"] = Bar(bloodcolor, S.CARB_POS, self.barwidth, self.barheight)
        self.bars["bloodbar_black"] = Bar(self.bg, S.CARB_POS, self.barwidth, blackheight)

        #Not really a bar, this is an ugly hack to make a pretty effect:
        overlay = pygame.sprite.Sprite()
        overlay.image = pygame.image.load(S.TXT)
        overlay.rect = overlay.image.get_rect()
        overlay.rect.topleft = S.TEXT_POS
        self.bars["overlay_sprite"] = overlay
        
        #self.bars["timebar"] = Bar(timecolor, (self.timeloc, 0), self.barwidth, self.barheight)
        #self.bars["timebar_black"] = Bar(self.bg, (self.timeloc, 0), self.barwidth, blackheight)

    def EVT_HEALTH_BLOOD_CHANGED(self, event):
        """Updates the blood bar display.
        """
        #assert event.blood
        #assert event.ceiling
        newsize = self.figureNewBarBlackSize(event.blood, event.ceiling)
        self.bars["bloodbar_black"].updateSize(newsize)

    def EVT_HEALTH_FAT_CHANGED(self, event):
        #assert event.fat
        #assert event.ceiling
        newsize = self.figureNewBarBlackSize(event.fat, event.ceiling)
        self.bars["fatbar_black"].updateSize(newsize)

    def figureNewBarBlackSize(self, value, ceiling):
        """Figure the new size of the black bar.
        """
        value = float(value)
        ceiling = float(ceiling)
        # We want to figure out the decimal percentage of the bar to
        # cover w/ black
        percentblack = 1-value/ceiling
        # If percentblack goes negative, bad stuff happens.
        # Let's make sure that doesn't occur.
        if percentblack < 0.0:
            percentblack = 0.0
        newheight = int(self.barheight*percentblack)
        newsize = (self.barwidth, newheight)
        return newsize
        
if __name__ == "__main__":
    unittest.main()
    
