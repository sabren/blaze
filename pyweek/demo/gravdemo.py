"""
gravity demo: shows how to put render and room
together to move sprites around based on physics.

since this is just a demo, I stole the physics
simulation from a pyODE tutorial:

http://pyode.sourceforge.net/tutorials/tutorial3.html
"""
import room, ode, pygame, render, random
from pygame.locals import KEYDOWN
WIDTH = 800
HEIGHT = 600
WHITE = [255, 255, 255]

# physics side
rm = room.Room()
rm.world.setGravity((0,9.81,0)) # in our world y++ is down. :)
rm.world.setERP(0.8) # ??
rm.world.setCFM(1E-5) # ??


# display side, mostly stolen from piman
pygame.init()
group = pygame.sprite.RenderUpdates()
screen = pygame.display.set_mode([WIDTH,HEIGHT], pygame.FULLSCREEN)

# clear the screen:
background = pygame.surface.Surface([WIDTH,HEIGHT])
background.fill(WHITE)
screen.blit(background, (0,0))
pygame.display.update()



## FLOORS ####################################
"""
this is tricky pyode tutorial3 uses a GeomPlane:

floor = ode.GeomPlane(space, (0,1,0),0)

but it doesn't make much sense to me. so, instead
I'm going to use a block:
"""
floor = rm.addBlock((WIDTH/2, HEIGHT-5), WIDTH, 10)

"""
okay, the next problem is that the floor is now
going to fall along with everything else. So we
need to fix it in place. The way to do this is
somewhat evil:
"""
#ref: http://ode.org/ode-latest-userguide.html#sec_12_4_0
#     "how can an immovable body be created?"
floor.setBody(None)

# here's a little drawing of the floor:
floorImg = pygame.surface.Surface((WIDTH, 10))
group.add(render.BlockSprite(floor, floorImg))




## throw some blocks ##############

def blockGenerator():
    Y = 50 # y position for blocks
    # drop some blocks from the edges, moving inward
    for x in range(WIDTH/2, 0, -render.SPRITE_SIZE[0]*2):
        yield group.add(render.BlockSprite(rm.addBlock((WIDTH/2+x,Y), 32, 32)))
        yield group.add(render.BlockSprite(rm.addBlock((WIDTH/2-x,Y), 32, 32)))
    # then drop a bunch randomly:
    for _ in range(50):
        X = random.randint(0,WIDTH)
        yield group.add(render.BlockSprite(rm.addBlock((X,Y), 32, 32)))

blocks = blockGenerator()
doneMakingBlocks = False



### collision stuff ######################


contactgroup = ode.JointGroup()

def onNearCollision(args, geom1, geom2):
    """
    taken directly from pyode tutorial3
    """
    # Check if the objects do collide
    contacts = ode.collide(geom1, geom2)

    # Create contact joints
    world,contactgroup = args
    for c in contacts:
        if floor in [geom1, geom2]:
            c.setBounce(0.25) # bouncy floor!
        else:
            c.setBounce(0.05)
        c.setMu(5000)
        j = ode.ContactJoint(world, contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())


### main loop ####################################

tick = 0
while pygame.event.poll().type != KEYDOWN:
    group.update()
    rects = group.draw(screen)
    pygame.display.update(rects)
    group.clear(screen, background)
    pygame.time.delay(15)

    rm.world.step(0.02)
    rm.space.collide((rm.world, contactgroup), onNearCollision)
    rm.world.step(0.02)
    contactgroup.empty()

    # add the blocks slowly:        
    tick += 1
    if (tick % 10)==0 and not doneMakingBlocks:
        try:
            blocks.next() 
        except StopIteration:
            doneMakingBlocks = True
            
