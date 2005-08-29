
"""
Our first goal is to create the world, which will hold
the whole physics simulation. We'll use the the example
from:

 http://pyode.sourceforge.net/tutorials/tutorial2.html

as a guide because it uses pygame to display the simulation.
"""
import ode
import unittest

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

THICKNESS = 1 # arbitrary depth for all our blocks


class RoomTest(unittest.TestCase):
    """
    add a 2d block to our world.

    we pass it the center and length
    """
    def test(self):
        world = Room()
        block = world.addBlock((0, 0), lx=5, ly=10)
        assert len(world.blocks) == 1
        assert block.getLengths() == (5, 10, THICKNESS)
        


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

    def addBlock(self, (cx, cy), lx, ly):
        """
        add a 2d block (no rotation yet)
        """
        body = ode.Body(self.world)
        geom = ode.GeomBox(self.space, [lx, ly, THICKNESS])
        geom.setBody(body)

        self.blocks.append(geom) # body?
        return geom






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

