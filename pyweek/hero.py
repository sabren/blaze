import ode, room

class Bird:
    """This creates the PyODE stuff.

It creates the world and space in which the character will live
along with the characters collision detection stuff.
Most of the variables on the level will be passed in from the
level.physics pickle.
"""
    def __init__(self, world, space, room, position):
        self.world = world
        self.space = space
        self.room = room
        self.position = position
        
    def hero(self, fatness, height):
        """This function sets up the bird.
        
        Fatness is the radius of the sphere used to
        represent the hero in the world."""
        self.height = height
        self.fatness = fatness
        self.bird = ode.Body(self.world)
        fat = ode.Mass()
        fat.setSphere(1100.0, fatness)
        self.bird.setMass(fat)
        
        # Creates a box for collision detection.
        geom = self.room.addGeom(self.position, 2*self.fatness, self.height)
        geom.setBody(self.bird)
    
    def changeMass(self, value):
        """This function changes the mass of the hero.
        
        This function can be called when the hero eats or uses
        energy."""
        self.fatness += value
        fat = ode.Mass()
        fat.setSphere(1100.0, self.fatness)
        self.bird.setMass(fat)
        
        # Creates a box for collision detection.
        geom = self.room.addGeom(self.position, 2*self.fatness, self.height)
        geom.setBody(self.bird)        
        
    def move(self, force):
        """Pass in the 2d vector that you want the hero to
        travel in."""
        x, y = force
        self.bird.setForce((x,y,0))
        
            
def test():
    bird = Bird(ode.World(), ode.Space(), room.Room(), (0,0))
    bird.hero(1.2, 0.35)
    bird.changeMass(0.1)
    bird.move((8,0))
    
        
        
if __name__ == "__main__":
    test()