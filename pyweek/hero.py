import ode, room, health
import unittest

class BirdTest(unittest.TestCase):
    """We're going to flip the Bird, er I mean, test it.
    """
    def setUp(self):
        from roomphysics import RoomPhysics
        self.r = room.Room()
        self.bird = Bird(self.r, (0,0), 1.0)
        self.bird.capture()
        self.rp = RoomPhysics(self.r, self.bird.geom.getBody())
    
    def testBirdMove(self):
        """Can the bird move?
        """
        oldposition = self.bird.getPosition()
        self.bird.move((30,0))
        self.rp.step()
        self.assertNotEqual(oldposition, self.bird.getPosition())

    def testBirdWalk(self):
        """Walk or waddle, he should.
        """
        oldposition = self.bird.getPosition()
        self.bird.walk((30))
        self.rp.step(self.bird.bird)
        newposition = self.bird.getPosition()
        self.assertNotEqual(oldposition, newposition)
        self.bird.walk((-30))
        self.rp.step(self.bird.bird)
        newerposition = self.bird.getPosition()
        self.assertNotEqual(newposition, newerposition)

    def testBirdRun(self):
        """Run, kiwi, run!
        """
        oldposition = self.bird.getPosition()
        self.bird.run((30))
        self.rp.step(self.bird.bird)
        newposition = self.bird.getPosition()
        self.assertNotEqual(oldposition, newposition)
        self.bird.run((-30))
        self.rp.step(self.bird.bird)
        newerposition = self.bird.getPosition()
        self.assertNotEqual(newposition, newerposition)


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


import eventnet.driver
class Bird(eventnet.driver.Handler):
    """A plump little kiwi bird who likes physics, eggs, and running around.
    
    """
    def __init__(self, room, position, radius):
        """This function sets us up the bird.
        """
        super(Bird, self).__init__()
        self.SPEED = 5
        self.room = room
        self.space = room.space
        self.world = room.world
        self.position = position
        self.radius = radius
        self.hlthcfg = health.HealthModelConfig()
        self.metabolism = health.HealthModel(self.hlthcfg)
        self.bird = ode.Body(self.world)
        self.updateMass()
        
        # Creates a box for collision detection.
        self.geom = self.room.addGeom(self.position,
                                      2*self.radius, 2*self.radius)
        self.geom.setBody(self.bird)
    
    def getPosition(self):
        """Get the position of our intrepid hero-kiwi.
        """
        return self.geom.getPosition()[:2] # x,y, but not z

    def updateMass(self):
        """Updates the mass of the hero by adjusting his density.
        
        This function can be called when the hero eats or uses
        energy.

        You must update your mass.  It is your density.
        """
        totalfatmass = self.hlthcfg.fatmass * self.metabolism.getFat()
        # density = mass * volume... sorta.  Okay, so we're fudging it.
        # The units are all arbitrary anyway. :)
        density = float(totalfatmass * self.hlthcfg.fatspace)
        #density = float(density)
        mass = ode.Mass()
        mass.setSphere(density, self.radius)
        self.bird.setMass(mass)

    def move(self, (x, y)):
        """Generic move method to move the hero.

        Pass in the 2d vector that you want the hero to travel in.
        """
        self.bird.setForce((x,y,0))

    def walk(self, dist):
        self.move((dist*self.SPEED, 0))

    def run(self, dist):
        self.move((dist*self.SPEED * 2, 0))

    def step(self):
        """Do the step thing.
        """
        self.metabolism.step()

    # Okay, here are the events we'll want to handle.
    def EVT_HEALTH_FAT_CHANGED(self, event):
        """When our fat changes, update our mass.
        """
        self.updateMass()

        
if __name__ == "__main__":
    unittest.main()
