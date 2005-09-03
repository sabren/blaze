"""
What should be done:
    - beautifying of code
    - more comments
    - safer code, more checks, etc (stupid C++ habits..)
    - (features)
"""
import unittest
import pygame


class ImageManager:
    def __init__(self, surface=None):
        self.images = {}
        self.surface = surface

    def load(self, filename):
        """
        If an image isn't already loaded, load it
        """
        if filename not in self.images:
            image = pygame.image.load (filename)
            self.images[filename] = (image, image.get_rect())

    def unload(self, filename):
        """
        Unload an image if it's loaded
        """
        if filename in self.images:
            del self.images[filename]

    def blit(self, filename, pos=(0, 0), surface=None):
        """
        Blit an image to a surface (i.e. back buffer)
        """
        if surface == None:
            surface = self.surface
        if filename in self.images:
            surface.blit (self.images[filename][0], pos)

    def getRect(self, filename):
        """
        Get the (already-created) rect of an image
        """
        if filename in self.images:
            return self.images[filename][1]
            


class MockDisplay(object):
    """
    fake display for testing.
    """
    def flip(self): pass
    def showImage(self, x,y, filename): pass



"""
This's our display. Um. Yeah.
"""
class Display:
    LEFT = 0
    CENTER = 1
    RIGHT = 2
    
    def __init__(self, s=(640, 480), t=""):
        """
        Setup a pygame window
        """
        self.alive = True
        self.size = s
        
        pygame.init()
        self.screen = pygame.display.set_mode (s)
        self.setTitle (t)

        # setup the font stuff..
        pygame.font.init()
        self.fonts = {}

        self.buffer = pygame.Surface (s)

    def addFont(self, size):
        """
        Add support for a font
        """
        self.fonts[str(size)] = pygame.font.Font (None, int(size))

    def text(self, words, size, pos=[0, 0], color=(0, 0, 0),
             justify=None):
        """
        Blit some text. I like text!
        """
        if str(size) in self.fonts:
            font = self.fonts[str(size)]
            
            if justify == Display.CENTER:
                pos[0] = pos[0] - font.size (words)[0]*0.5
            if justify == Display.RIGHT:
                pos[0] = pos[0] - font.size (words)[0]
                    
            self.buffer.blit (font.render (words, True, color), pos)

    def setTitle(self, t):
        """
        Change our window's caption
        """
        self.title = t
        
        pygame.display.set_caption (self.title)

    def flip(self):
        """
        Flippity flip flip
        """
        self.screen.blit (self.buffer, (0, 0))
        pygame.display.flip()

    def clear(self, color=(0, 0, 0)):
        """
        Fill the buffer with.. color!
        """
        self.buffer.fill (color)


    def showImage(self, x,y, filename):
        imanager = ImageManager (self.buffer)
        imanager.load (filename)
        imanager.blit (filename)
        self.flip()


"""
Can we successfully create a window? Yadda yadda yadda.
"""

def test():
    display = Display ((640, 480), "T-Rex and the Waffle House")

    display.addFont (30)

    imanager = ImageManager (display.buffer)

    imanager.load ("background.png")
    imanager.load ("player.png")
    #imanager.load ("foreground.png")

    blah = True
    while blah:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                blah = False

        display.clear()

        imanager.blit ("background.png")
        imanager.blit ("player.png", (55, 275))
        #imanager.blit ("foreground.png")

        display.text ("T-Rex sure does love his waffles!", 30, [320, 80], (0, 255, 0), Display.LEFT)
        display.text ("T-Rex sure does love his waffles!", 30, [320, 100], (0, 255, 0), Display.CENTER)
        display.text ("T-Rex sure does love his waffles!", 30, [320, 120], (0, 255, 0), Display.RIGHT)

        display.flip()




if __name__=="__main__":
    test()
