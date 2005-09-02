import pygame
import eventnet.driver
import unittest

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
        
class StatusBoxTest(unittest.TestCase):
    """
    """
    def setUp(self):
        import room, hero
        self.sb = StatusBox()
        self.sb.capture()
        from roomphysics import RoomPhysics
        self.r = room.Room()
        self.bird = hero.Bird(self.r, (0,0), 1.0)
        self.bird.capture()
        self.rp = RoomPhysics(self.r, self.bird.geom.getBody())


    def testStatusBox(self):
        """Is there a complete score box?
        """
        assert self.sb
        assert self.sb.bars["fatbar"]
        assert self.sb.bars["fatbar_black"]
        assert self.sb.bars["bloodbar"]
        assert self.sb.bars["bloodbar_black"]
        assert self.sb.bars["timebar"]
        assert self.sb.bars["timebar_black"]

    def testStatusBoxAction(self):
        """Ready, set, action!
        """
        from pygame.locals import *
        from pygame import display
        
        pygame.init()
        screen = pygame.display.set_mode([640, 480])
        sb = StatusBox()
        for key in sb.bars.keys():
            bar = sb.bars[key]
            screen.blit(bar.image, bar.rect)
        pygame.display.update()
        while pygame.event.poll().type != KEYDOWN:
            pygame.time.delay(10)


    def testBloodEvents(self):
        """Does the status bar handle blood sugar events?
        """
        oldheight = self.sb.bars["bloodbar_black"].image.get_height()
        self.bird.step()
        print "First step."
        import health
        candy = health.Food(100, 0)
        self.bird.metabolism.eat(candy)
        self.bird.step()
        print "Second step."
        newheight = self.sb.bars["bloodbar_black"].image.get_height()
        self.assertNotEqual(oldheight, newheight)
        
        

class StatusBox(eventnet.driver.Handler):
    def __init__(self):
        super(StatusBox, self).__init__()
        bloodcolor = (255, 0, 0)
        fatcolor = (0, 255, 0)
        timecolor = (0, 0, 255)
        self.black = (0,0,0)
        self.barheight = 160
        self.barwidth = 24
        blackheight = 1
        right = 640
        self.bloodloc = right-(32*3)+4
        self.fatloc = right-(32*2)+4
        self.timeloc = right-(32)+4
        self.bars = {}
        self.bars["fatbar"] = Bar(fatcolor, (self.fatloc, 0), self.barwidth, self.barheight)
        self.bars["fatbar_black"] = Bar(self.black, (self.fatloc, 0), self.barwidth, blackheight)
        self.bars["bloodbar"] = Bar(bloodcolor, (self.bloodloc, 0), self.barwidth, self.barheight)
        self.bars["bloodbar_black"] = Bar(self.black, (self.bloodloc, 0), self.barwidth, blackheight)
        self.bars["timebar"] = Bar(timecolor, (self.timeloc, 0), self.barwidth, self.barheight)
        self.bars["timebar_black"] = Bar(self.black, (self.timeloc, 0), self.barwidth, blackheight)

    def EVT_HEALTH_BLOOD_CHANGED(self, event):
        assert event.blood
        assert event.ceiling
        self.updateBloodBar(event.blood, event.ceiling)

    def updateBloodBar(self, blood, ceiling):
        # We want to figure out the decimal percentage of the bar to
        # cover w/ black
        percentblack = 1-blood/ceiling
        # The new height for bloodbar_black
        newheight = int(self.barheight*percentblack)
        newsize = (self.barwidth, newheight)
        # Now we're going to transform bloodbar_black's surface
        oldsurface = self.bars["bloodbar_black"].image
        newsurface = pygame.transform.scale(oldsurface, newsize)
        self.bars["bloodbar_black"].image = newsurface

        # Scratch that.  We're just going to replace it for now.  At
        # least until we figure out why pygame.transform.scale is
        # giving segmentation faults.
        
        #newbar = Bar(self.black, (self.bloodloc, 0), self.barwidth, newheight)
        #self.bars["bloodbar_black"] = newbar
        
        
        
    def EVT_HEALTH_FAT_CHANGED(self, event):
        assert event.fat
        assert event.ceiling
        newpercent = event.fat/event.ceiling
        
if __name__ == "__main__":
    unittest.main()
    
