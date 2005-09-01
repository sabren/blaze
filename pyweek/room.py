
"""
Our first goal is to create the world, which will hold
the whole physics simulation. We'll use the the example
from:

 http://pyode.sourceforge.net/tutorials/tutorial2.html

as a guide because it uses pygame to display the simulation.
"""
import ode
import unittest

from ode_to_pixel import *

#########################################################
##
## This is our actual model of the room: a simple
## project of 2d rectangles into 3d blocks
##
#########################################################
    
"""
Room

The idea is to 

"""

THICKNESS = 32 # arbitrary depth for all our blocks


class RoomTest(unittest.TestCase):
    """
    add a 2d block to our world.

    we pass it the center and length
    """
    def testAddBlock(self):
        world = Room()
        block = world.addBlock((40, 42), lx=5, ly=10)
        assert len(world.blocks) == 1
        assert block.getLengths() == (5, 10, THICKNESS)
        assert block.getPosition()[:2] == (40,42)
        assert block.getBody()

    def testAddGeom(self):
        """
        A Geom is like a block that doesn't move.
        It doesn't have a body so the physics
        engine can't see it, but the space/collision
        engine can.
        """
        rm = Room()
        floor = rm.addGeom((50, 95), 100, 10)
        assert not floor.getBody()



class Room(object):
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

    def addGeom(self, (cx, cy), lx, ly):
        #ref: http://ode.org/ode-latest-userguide.html#sec_12_4_0
        #     "how can an immovable body be created?"
        geom = ode.GeomBox(self.space, [lx, ly, px2w(THICKNESS)])
        geom.setPosition((cx, cy, 0))
        geom.shape = "box"
        geom.boxsize = [lx, ly, px2w(THICKNESS)]
        self.blocks.append(geom)
        return geom
    
    def addBlock(self, (cx, cy), lx, ly):
        """
        add a 2d block (a geom with a body)
        """
        block = self.addGeom((cx,cy), lx, ly)
        block.setBody(ode.Body(self.world))
        
        # i think setting the body resets the position,
        # because if you take this line out, the tests fail:
        block.setPosition((cx, cy, 0))
        return block


if __name__=="__main__":
    unittest.main()


##[ DISCARDED IDEAS ]###############################

## class BoxTest(GravityTest):

##     def addObject(self):
##         return newBody(self.world,
##                        newBox(density = 100,
##                               lx = 10,
##                               ly = 10,
##                               lz = 10)) # a cube
                       
## def newBody(world, mass):
##     body = ode.Body(world)
##     body.setMass(mass)
##     return body


## def newBox(density, lx, ly, lz):
##     M = ode.Mass()
##     M.setBox(density, lx, ly, lz)
##     return M

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

