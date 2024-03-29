import ode, room, health
from constants import LEFT, RIGHT, HERO, CALORIES, PHYSICS
import unittest

class BirdTest(unittest.TestCase):
    """
    We're going to flip the Bird, er I mean, test it.
    """
    def setUp(self):
        from roomphysics import RoomPhysics
        self.r = room.Room()
        self.bird = Bird(self.r, (50.0, 50.0))
        self.bird.SPEED = 1000
        self.rp = RoomPhysics(self.r, self.bird.geom.getBody())
        self.steps = 100 # steps to take

    def testBirdGravity(self):
        """
        The kiwi bird in the sky keeps on falling:
        """
        oldx, oldy = self.bird.getPosition()
        for x in range(self.steps):
            self.rp.step()
        newx, newy = self.bird.getPosition()
        self.assertEqual(oldx, newx)
        assert newy > oldy # down is ++
    
    def testBirdMoveRight(self):
        """
        Can the bird move right?
        """
        oldposition = self.bird.getPosition()[0]
        self.bird.move((30,0))
        self.rp.step()
        newposition = self.bird.getPosition()[0]
        #print "Was at: %s, now at: %s" % (oldposition, newposition)
        assert newposition > oldposition

    def testBirdMoveLeft(self):
        """
        Can the bird move left?
        """
        oldposition = self.bird.getPosition()[0]
        self.bird.move((-30,0))
        self.rp.step()
        newposition = self.bird.getPosition()[0]
        print "Was at: %s, now at: %s" % (oldposition, newposition)
        assert newposition < oldposition


    def testBirdWalkRight(self):
        """
        Take a step to the right.
        """
        oldposition = self.bird.getPosition()[0]
        print "WALK RIGHT - Was at: %s" % oldposition
        self.bird.walk(1)
        for x in range(self.steps):
            self.rp.step()
            newposition = self.bird.getPosition()[0]
            #print "Now at: %s" % newposition
        assert newposition > oldposition

    def testBirdWalkLeft(self):
        """
        Take a step to the left.
        """
        oldposition = self.bird.getPosition()[0]
        self.bird.walk(-1)
        for x in range(self.steps):
            self.rp.step()
        newposition = self.bird.getPosition()[0]
        print "Was at: %s, now at: %s" % (oldposition, newposition)
        assert newposition < oldposition
        
    def testBirdRun(self):
	# This test should be scrapped most likely
        """
        Run, kiwi, run!
        """
        oldposition = self.bird.getPosition()
        self.bird.run(1)
        self.rp.step(self.bird.body)
        newposition = self.bird.getPosition()
        self.assertNotEqual(oldposition, newposition)
        self.bird.run((-1))
        self.rp.step(self.bird.body)
        newerposition = self.bird.getPosition()
        #self.assertNotEqual(newposition, newerposition)
        
    def testBirdJump(self):
        """
        JUMP!!!!
        """
        oldposition = self.bird.getPosition()
        self.bird.jump()
        self.rp.step(self.bird.body)
        newposition = self.bird.getPosition()
        self.assertNotEqual(oldposition, newposition)


    def testBirdMass(self):
        """
        Bird should gain mass when it eats.

        What is the mass of an unladen kiwi?
        """
        initialmass = self.bird.body.getMass().mass
        food = health.Food(0,100, self.bird.room, (50,50))
        self.bird.metabolism.eat(food)
        self.bird.updateMass()
        newmass = self.bird.body.getMass().mass
        self.assertNotEqual(initialmass, newmass)


import eventnet.driver
from constants import CODE # Michal's UgLy hack. :)
class Bird(eventnet.driver.Handler):
    """
    A plump little kiwi bird who likes physics, eggs, and running around.
    """
    def __init__(self, room, position):
        """This function sets us up the bird.
        """
        super(Bird, self).__init__()
        self.capture()
        
        self.SPEED = 10
        self.room = room
        self.space = room.space
        self.world = room.world
        self.radius = HERO.RADIUS
        self.hlthcfg = health.HealthModelConfig()
        self.metabolism = health.HealthModel(self.hlthcfg)
        
        # Creates a box for collision detection.
        self.geom = self.room.addBlock(position, 2*self.radius, 2*self.radius)
	self.geom.setPosition ((position[0], position[1], 0))
        self.geom.code = CODE.HERO
	self.body = self.geom.getBody()
        self.updateMass()

    
    def getPosition(self):
        """
        Get the position of our intrepid hero-kiwi.
        """
        return self.geom.getPosition()[:2] # x,y, but not z

    def setPosition(self, (x,y)):
        self.geom.setPosition((x,y,0))

    def updateMass(self):
        """
        Updates the mass of the hero by adjusting his density.
        
        This function can be called when the hero eats or uses
        energy.

        You must update your mass.  It is your density.
        """
        totalfatmass = self.hlthcfg.fatmass * self.metabolism.getFat()
        # density = mass / volume... sorta.  Okay, so we're fudging it.
        # The units are all arbitrary anyway. :)
        density = float(totalfatmass / self.hlthcfg.fatspace)
        mass = ode.Mass()
        mass.setSphere(density, self.radius)
        self.body.setMass(mass)

    def move(self, (x, y)):
        """
        Generic move method to move the hero.

        Pass in the 2d vector that you want the hero to travel in
        and the force you want to apply.
        """
        self.geom.getBody().addForce((x*PHYSICS.SCALEFORCE,
                                      y*PHYSICS.SCALEFORCE, 0))

    def walk(self, direction):
        """
        Do the bird walk.

        if value is positive, walk right.
        if value is negative, walk left.
        """
        assert direction in (LEFT, RIGHT)
        force = self.SPEED * direction
        self.move((force, 0))
        self.metabolism.exert(CALORIES.WALK)

    def run(self, direction):
        """
        Run, kiwi, run!

        if the value is positive, walk right.
        if the value is negative, walk right.
        """
        assert direction in (LEFT, RIGHT)
        force = self.SPEED * 2 * direction
        self.move((force, 0))
        self.metabolism.exert(CALORIES.RUN)
        
    def jump(self):
        self.move((0, HERO.JUMPFORCE))
        self.metabolism.exert(CALORIES.JUMP)

    def step(self):
        """
        Do the step thing.
        """
        self.metabolism.step()

    # Okay, here are the events we'll want to handle.
    def EVT_HEALTH_FAT_CHANGED(self, event):
        """
        When our fat changes, update our mass.
        """
        self.updateMass()

        
if __name__ == "__main__":
    unittest.main()
