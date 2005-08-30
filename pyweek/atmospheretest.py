# pyODE example 1: Getting started
    
import ode

# Create a world object
world = ode.World()
world.setGravity( (0,-9.81,0) )

# Create a body inside the world
body = ode.Body(world)
M = ode.Mass()
M.setSphere(2500.0, 0.05)
M.mass = 1.0
body.setMass(M)

def atmosphere():
    """This is the function I'm testing. It simulates a frictional force
    caused by the atmosphere on the level. It will control how quickly
    the hero will slow down when no force is applied in the x-axis.
    If u and direction have the same sign then a force will be applied
    in the opposite direction to slow down the hero."""
    pressure = 2.2
    u, v, w = body.getLinearVel()
    print "u=", u, "direction=", direction
    if u < 0 and direction <= 0:
        body.addForce((pressure,0,0))
    elif u > 0 and direction >= 0:
        body.addForce((-pressure,0,0))
    else:
        body.setLinearVel((0, v, w))

body.setPosition( (0,2,0) )
body.addForce( (30,0,0) )

# Do the simulation...
total_time = 0.0
dt = 0.04
while total_time<2.0:
    x,y,z = body.getPosition()
    u,v,w = body.getLinearVel()
    direction = u # This sets the direction the hero was travelling in.
    print "%1.2fsec: pos=(%6.3f, %6.3f, %6.3f)  vel=(%6.3f, %6.3f, %6.3f)" % \
          (total_time, x, y, z, u,v,w)
    world.step(dt)
    atmosphere()
    total_time+=dt