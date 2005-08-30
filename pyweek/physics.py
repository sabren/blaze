import ode

class Bird:
    """This creates the PyODE stuff.

It creates the world and space in which the character will live
along with the characters collision detection stuff.
Most of the variables on the level will be passed in from the
level.physics pickle.
"""
    def __init__(self, world, space, drag):
        self.world = world
        self.space = space
        self.coefficient = drag
        self.friction = 5000
        
    def atmosphere(self):
        """This simulates a frictional force caused by the atmosphere
on the level. It will control how quickly the hero will
slow down when no force is applied."""
        u, v, w = self.bird.getLinearVel()
        self.bird.addForce((u*self.coefficient,0,0))
        
    def bird(self, fatness, height):
        """This function sets up the bird.
        
        Fatness is the radius of the sphere used to
        represent the hero in the world."""
        self.height = height
        self.fatness = fatness
        self.bird = ode.Body(self.world)
        fat = ode.Mass()
        fat.setSphere(1100.0, fatness)
        self.bird.setMass(fat)
        fat.mass = 5.0
        self.bird.setMass(fat)
        
        # Creates a box for collision detection.
        size = (2*fatness, self.height, 2*fatness)
        geom = ode.GeomBox(self.space, lengths=size)
        geom.setBody(self.bird)
        return self.bird
    
    def changeMass(self, value):
        """This function changes the mass of the hero.
        
        This function can be called when the hero eats or uses
        energy."""
        self.fatness += value
        fat = ode.Mass()
        fat.setSphere(1100.0, self.fatness)
        self.bird.setMass(fat)
        
        # Creates a box for collision detection.
        size = (2*self.fatness, self.height, 2*self.fatness)
        geom = ode.GeomBox(self.space, lengths=size)
        geom.setBody(self.bird)
        
        
    def move(self, force):
        """Pass in the 2d vector that you want the hero to
        travel in."""
        x, y = force
        self.bird.setForce(x,y,0)
        
    # Collision callback
    def onNearCollision(contactgroup, geom1, geom2):
        """Callback function for the collide() method.
    
This function checks if the given geoms do collide and
creates contact joints if they do.
"""
    
        # Check if the objects do collide
        contacts = ode.collide(geom1, geom2)
    
        # Create contact joints
        for contact in contacts:
            contact.setBounce(0.05)
            contact.setMu(self.friction)
            cJoint = ode.ContactJoint(self.world, contactgroup, contact)
            cJoint.attach(geom1.getBody(), geom2.getBody())
            
    def step(self):
        contactgroup = ode.JointGroup()
        n = 2
        u, v, w = self.bird.getLinearVel()
        if w != 0: # This makes sure there is no movement in the z-axis
            self.bird.setLinearVel((u,v,0))
        for i in range(n):
            # Apply the atmosphere
            self.atmosphere()
            
            # Detect collisions and create contact joints
            self.space.collide(contactgroup, self.onNearCollision)
        
            # Simulation step
            self.world.step(0.01)
        
            # Remove all contact joints
            contactgroup.empty()
            
def test():
    bird = Bird(ode.World(), ode.Space(), 7)
    bird.bird(1.2, 0.35)
    bird.changeMass(0.1)
    for n in range(50000):
        bird.step()
    
        
        
if __name__ == "__main__":
    test()