"""
sprite rendering engine
"""
import unittest
import pygame.sprite
from states import Gear
from constants import SPRITE_SIZE, IMAGE, ROOM
import random
from ode_to_pixel import *

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
        self.display.flip()

        
    def tick(self):
        self.sprites.update()
        rects = self.sprites.draw(self.display.screen)
        if self.foreground:
            for r in rects:
                self.display.blit(self.foreground, r, r)
        self.display.update(rects)
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


if __name__=="__main__":
    unittest.main()
