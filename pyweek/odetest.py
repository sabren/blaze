
#################################################
###
### this is just a reference implementation of how
### to use pyODE to make a simple simulation
###
#################################################
import ode
import unittest

class GravityTest(unittest.TestCase):

    """
    if we create a world, add a sphere to the
    world, and turn on gravity, the sphere should
    fall.
    """

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

