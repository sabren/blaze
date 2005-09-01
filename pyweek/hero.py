import ode, room, health

import unittest
class BirdTest(unittest.TestCase):
    """We're going to flip the Bird, er I mean, test it.
    """
    def setUp(self):
        #import events
        #self.handler = events.event_handler()
        #self.handler.capture()
        self.bird = Bird(room.Room(), (0,0))
        config = health.HealthModelConfig()
        self.bird.makeHero(1.2, 0.35, config)
        self.bird.capture()
        
    
    def testBirdMove(self):
        """Is there a bird?  Can it move?
        """
        self.bird.move((8,0))

    def testBirdMass(self):
        """Bird should gain mass when it eats.

        What is the mass of an unladen kiwi?
        """
        initialmass = self.bird.bird.getMass().mass
        food = health.Food(0,100)
        self.bird.metabolism.eat(food)
        self.bird.updateMass()
        newmass = self.bird.bird.getMass().mass
        self.assertNotEqual(initialmass, newmass)


import eventnet
class Bird(eventnet.driver.Handler):
    """A plump little kiwi bird who likes physics, eggs, and running around.
    """
    def __init__(self, room, position):
        super(Bird, self).__init__()
        self.room = room
        self.space = room.space
        self.world = room.world
        self.position = position
        
    def makeHero(self, radius, height, healthconfig):
        """This function sets us up the bird.
        
        Fatness is the radius of the sphere used to
        represent the hero in the world.
        """
        self.height = height
        self.radius = radius
        self.hlthcfg = healthconfig
        self.metabolism = health.HealthModel(self.hlthcfg)
        self.bird = ode.Body(self.world)
        self.updateMass()
        
        # Creates a box for collision detection.
        self.geom = self.room.addGeom(self.position,
                                      2*self.radius, self.height)
        self.geom.setBody(self.bird)
    
    def updateMass(self):
        """Updates the mass of the hero by adjusting his density.
        
        This function can be called when the hero eats or uses
        energy.

        You must update your mass.  It is your density.
        """
        totalfatmass = self.hlthcfg.fatmass * self.metabolism.getFat()
        # density = mass * volume... sorta.  Okay, so we're fudging it.
        # The units are all arbitrary anyway. :)
        density = totalfatmass * self.hlthcfg.fatspace
        density = float(density)
        mass = ode.Mass()
        mass.setSphere(density, self.radius)
        self.bird.setMass(mass)

    def EVT_FAT_CHANGED(self, event):
        """When our fat changes, update our mass.
        """
        self.updateMass()
        

    def move(self, (dx, dy)):
        """Pass in the 2d vector that you want the hero to
        travel in."""
        self.bird.setForce((dx,dy,0))
        
if __name__ == "__main__":
    unittest.main()
