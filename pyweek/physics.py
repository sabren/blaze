
"""
Our first goal is to create the world, which will hold
the whole physics simulation. We'll use the the example
from:

 http://pyode.sourceforge.net/tutorials/tutorial2.html

as a guide because it uses pygame to display the simulation.
"""

"""
So... In theory the way this works is...
if we create a world, add a sphere to the
world, and turn on gravity, the sphere should
fall.
"""
import ode
import unittest

class GravityTest(unittest.TestCase):

    def setUp(self):
        self.fps = 50
        self.delta = 1.0/self.fps
        self.world = ode.World()


    def addObject(self):
        """
        make its own function so we can
        run this same test with our version
        from the svg file.. 
        """
        return createSphere(self.world)
        
    def test(self):
        obj = self.addObject()
        obj.setPosition((1,2,0))

        assert obj.getPosition() == (1,2,0) 

        # now turn on gravity and see what happens:
        self.world.setGravity( (0,-9.81,0) )

        for blah in range(500): # run for 500 frames
            self.world.step (self.delta)

        assert obj.getPosition() != (1,2,0), \
               "the object should have fallen."

  

"""
Now we have a world with gravity and we want to
add a spherical object to it.
"""

def createSphere(world):
    body = ode.Body(world)
    M = ode.Mass()
    M.setSphere(2500, 0.05)
    body.setMass(M)    
    return body


# Now we want to do the same for boxes:
# we'll also add space and geometry

class BoxTest(GravityTest):

    def addObject(self):
        return newBody(self.world,
                       newBox(density = 100,
                              lx = 10,
                              ly = 10,
                              lz = 10)) # a cube
                       







#########################################################
    
"""
BlockWorld

The idea is to 

"""

THICKNESS = 1 # arbitrary depth for all our blocks


class BlockWorldTest(unittest.TestCase):
    """
    add a 2d block to our world.

    we pass it the center and length
    """
    def test(self):
        world = BlockWorld()
        block = world.addBlock(cx=0, cy=0, lx=5, ly=10)
        assert len(world.blocks) == 1
        assert block.getLengths() == (5, 10, THICKNESS)
        


class BlockWorld:
    """
    Our world is composed of Bodies which have
    both a Mass and Geom(etry)... They're all just
    blocks though so this makes it a little
    easier to set up.
    """
    def __init__(self):
        self.world = ode.World()
        self.space = ode.Space()
        self.blocks = []

    def addBlock(self, cx, cy, lx, ly):
        """
        add a 2d block (no rotation yet)
        """
        body = ode.Body(self.world)
        geom = ode.GeomBox(self.space, [lx, ly, THICKNESS])
        geom.setBody(body)

        self.blocks.append(geom) # body?
        return geom



## class Block(object):
##     """
##     we make this a class so that we can map
##     between rectangles and ode.GeomBoxes
##
##     we can't have free standing blocks because
##     we need a world and space.
##  
##     so this is just not feasable here.
##     """
##     pass

      

def newBody(world, mass):
    body = ode.Body(world)
    body.setMass(mass)
    return body


def newBox(density, lx, ly, lz):
    M = ode.Mass()
    M.setBox(density, lx, ly, lz)
    return M



if __name__=="__main__":
    unittest.main()    
