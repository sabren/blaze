import ode


class RoomPhysics:
    def __init__(self, world, space, drag):
        self.world = world
        self.space = space
        self.coefficient = drag
        self.friction = 5000
        
    def atmosphere(self, chars):
            """This simulates a frictional force caused by the atmosphere
    on the level. It will control how quickly the characters will
    slow down when no force is applied. chars should be a list of ode Bodies."""
            for char in chars:
                u, v, w = char.getLinearVel()
                char.addForce((u*self.coefficient,0,0))
                
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
        for i in range(2):
            # Apply the atmosphere
            self.atmosphere()
            
            # Detect collisions and create contact joints
            self.space.collide(contactgroup, self.onNearCollision)
        
            # Simulation step
            self.world.step(0.01)
        
            # Remove all contact joints
            contactgroup.empty()