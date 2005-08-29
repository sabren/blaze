"""
What should be done:
    - beautifying of code
    - more comments
    - safer code, more checks, etc (stupid C++ habits..)
    - (features)
"""
import unittest
import pygame
import os


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
            

"""
This's our display. Um. Yeah.
"""
class Display:
    def __init__(self, s=(640, 480), t=""):
        """
        Setup a pygame window
        """
        self.alive = True
        self.size = s
        
        assert pygame.init() # yes! I used an assert!

        self.screen = pygame.display.set_mode (s)
        self.setTitle (t)

        self.buffer = pygame.Surface (s)

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


"""
Can we successfully create a window? Yadda yadda yadda.
"""
class DisplayTest(unittest.TestCase):
    def setUp(self):
        pass

    def test(self):
        display = Display ((640, 480), "Waffles!")

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
            imanager.blit ("player.png", (55, 55))
            #imanager.blit ("foreground.png")
            
            display.flip()
            

if __name__ == "__main__":
    unittest.main()
