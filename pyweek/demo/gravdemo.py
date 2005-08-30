"""
gravity demo: shows how to put render and room
together to move sprites around based on physics.

since this is just a demo, I stole the physics
simulation from a pyODE tutorial:

http://pyode.sourceforge.net/tutorials/tutorial3.html
"""
import sys
sys.path.append("..")
import room, ode, pygame, render, random, loader
from pygame.locals import KEYDOWN
WIDTH = 640
HEIGHT = 480
WHITE = [255, 255, 255]

# physics side
rm = room.Room()

## @TODO: load geometry.
##
## this *sort of* works. you can see the blocks suddenly
## change course, but the collisions don't match where
## the rectangles show up on the screen.
##
rm = loader.roomFromFile(open("gravdemo-geom.svg"))

#import pdb; pdb.set_trace()
rm.world.setGravity((0,9.81,0)) # in our world y++ is down. :)
rm.world.setERP(0.8) # ??
rm.world.setCFM(0) # ??



### pygame : sprite layers ##############################

pygame.init()
screen = pygame.display.set_mode([WIDTH,HEIGHT]) # pygame.FULLSCREEN)
pygame.display.set_caption("trailblazer gravity demo")


class WithForeground(pygame.sprite.RenderUpdates):
    """
    simple sprite ordering: foreground is always on top
    """
    def __init__(self, fg, *sprites):
        pygame.sprite.RenderUpdates.__init__(self, *sprites)
        self.add(fg)
        self.fg = fg
        
    def sprites(self):
        all = pygame.sprite.RenderUpdates.sprites(self)
        all.remove(self.fg)
        all.append(self.fg)
        return all



## BACKGROUND
background = pygame.image.load("gravdemo-back.png")
screen.blit(background, (0,0))

## FOREGROUND
foreground = pygame.image.load("gravdemo-fore.png")
screen.blit(foreground, (0,0))

fgSprite = pygame.sprite.Sprite()
fgSprite.image = foreground
fgSprite.rect = foreground.get_rect()

## sprite group
group = WithForeground(fgSprite)


                            



## FLOORS ####################################
"""
this is tricky pyode tutorial3 uses a GeomPlane:

floor = ode.GeomPlane(space, (0,1,0),0)

but it doesn't make much sense to me. so, instead
I'm going to use a Geom

okay, the next problem is that the floor is now
going to fall along with everything else. So we
need to fix it in place. That's what addGeom is for:
"""
floor = rm.addGeom((WIDTH/2, HEIGHT-25), WIDTH, 50)

# here's a little drawing of the floor:
floorImg = pygame.surface.Surface((WIDTH, 50))
group.add(render.BlockSprite(floor, floorImg))



## throw some blocks ##############

# this is just the default sprite: a randomly colored square
# (with an alpha channel)

def randomlyColoredSquare():
    image = pygame.Surface(render.SPRITE_SIZE)
    image.fill(pygame.color.Color("0x%08x" % random.randint(0,256**4)))
    return image


def blockGenerator():
    Y = 50 # y position for blocks
    # drop some blocks from the edges, moving inward
    for x in range(WIDTH/2, 0, -render.SPRITE_SIZE[0]*2):
        yield group.add(render.BlockSprite(rm.addBlock((WIDTH/2+x,Y), 32, 32),
                                           randomlyColoredSquare()))
        yield group.add(render.BlockSprite(rm.addBlock((WIDTH/2-x,Y), 32, 32),
                                           randomlyColoredSquare()))
    # then drop a bunch randomly:
    for _ in range(50):
        X = random.randint(0,WIDTH)
        yield group.add(render.BlockSprite(rm.addBlock((X,Y), 32, 32),
                                           randomlyColoredSquare()))

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
        c.setBounce(0.05)
        c.setMu(5000)
        j = ode.ContactJoint(world, contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())
        

### main loop ####################################

pygame.display.update()


tick = 0
while pygame.event.poll().type != KEYDOWN:
    group.update()
    rects = group.draw(screen)    
    pygame.display.update(rects)
    group.clear(screen, background)

    speed = 0.3
    rm.world.step(speed/2)
    rm.space.collide((rm.world, contactgroup), onNearCollision)
    rm.world.step(speed/2)
    contactgroup.empty()

    # add the blocks slowly:        
    tick += 1
    if (tick % 3)==0 and not doneMakingBlocks:
        try:
            blocks.next() 
        except StopIteration:
            doneMakingBlocks = True


    # this is a hack for if they fall off the floor
    # if I don't do this, then they just keep acellerating
    # forever due to gravity
    if (tick % 50)==0:
        for block in rm.blocks:
            x,y,z = block.getPosition()
            if y > HEIGHT:
                block.setBody(None)
