"""
sprite rendering engine
"""
import unittest
import pygame.sprite

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
SPRITE_SIZE = (32,32)
class BlockSpriteTest(unittest.TestCase):
    def test(self):
        # first we create the physics side:
        import room
        rm = room.Room()

        #@TODO: this really should be a sphere i think...
        bk = rm.addBlock((50, 50), *SPRITE_SIZE)

        # now the display side:
        bs = BlockSprite(bk)
        self.assertEquals((50,50), bs.rect.center)
        

# here's the implementation
class BlockSprite(pygame.sprite.Sprite):
    def __init__(self, block, image):
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
        self.rect.center = self.block.getPosition()[:2]


if __name__=="__main__":
    gravityDemo()
    unittest.main()
