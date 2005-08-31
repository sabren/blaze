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
#from pygame.locals import KEYDOWN
from pygame.locals import *


from cgtypes import *
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


from ode_to_pixel import *





# prepare_GL
def prepare_GL():
    """Prepare drawing.
    """
    
    # Viewport
    glViewport(0,0,640,480)

    # Initialize
    glClearColor(0.8,0.8,0.9,0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glEnable(GL_LIGHTING)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_FLAT)

    # Projection
    doit = 1

    if doit:
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        P = mat4(1).perspective(45,1.3333,0.2,20)
        glMultMatrixd(P.toList())

    # Initialize ModelView matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    #glTranslate(-.5, -.5, 1.1)
    if not doit:
        glTranslate(1., .0, 1.5)
        glRotate(180, 0., 1.0, 0.)

    # Light source
    glLightfv(GL_LIGHT0,GL_POSITION,[0,0,1,0])
    glLightfv(GL_LIGHT0,GL_DIFFUSE,[1,1,1,1])
    glLightfv(GL_LIGHT0,GL_SPECULAR,[1,1,1,1])
    glEnable(GL_LIGHT0)
    if doit:
        # View transformation
        V = mat4(1).lookAt(1.2*vec3(2,3,4),(0.5,0.5,0), up=(0,-1,0))
        V.rotate(pi,vec3(0,1,0))  
        V = V.inverse()
        glMultMatrixd(V.toList())


# draw_body
def draw_body(body):
    """Draw an ODE body.
    """
    
    x,y,z = body.getPosition()
    R = body.getRotation()
    T = mat4()
    T[0,0] = R[0]
    T[0,1] = R[1]
    T[0,2] = R[2]
    T[1,0] = R[3]
    T[1,1] = R[4]
    T[1,2] = R[5]
    T[2,0] = R[6]
    T[2,1] = R[7]
    T[2,2] = R[8]
    T[3] = (x,y,z,1.0)

    glPushMatrix()
    glMultMatrixd(T.toList())
    if body.shape=="box":
        sx,sy,sz = body.boxsize
        glScale(sx, sy, sz)
        glutSolidCube(1)
    glPopMatrix()



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
#screen = pygame.display.set_mode([WIDTH,HEIGHT]) # pygame.FULLSCREEN)
srf = pygame.display.set_mode((640,480), OPENGL | DOUBLEBUF)

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


if 1:
    ## BACKGROUND
    background = pygame.image.load("gravdemo-back.png")
    #screen.blit(background, (0,0))

    ## FOREGROUND
    foreground = pygame.image.load("gravdemo-fore.png")
    #screen.blit(foreground, (0,0))

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
floor = rm.addGeom(pixel2world(WIDTH/2, HEIGHT-25), px2w(WIDTH), px2w(50))


class myBlockSprite(render.BlockSprite):
    def update(self):
        print self.block.getPosition()
        print self.block.getRotation()

        if self.old_position:
            #self.old_position = self.block.getPosition()[:2]
            new_pos = map(round, self.block.getPosition()[:2])
            x = new_pos[0] - self.old_position[0]
            y = new_pos[1] - self.old_position[1]


            self.rect.move_ip(world2pixel(x,y))
            self.old_position = new_pos

        else:
            self.old_position = map(round, self.block.getPosition()[:2])
            self.rect.center = world2pixel( *map(round, self.block.getPosition()[:2]) )


if 0:
    # here's a little drawing of the floor:
    floorImg = pygame.surface.Surface((WIDTH, 50))
    group.add(myBlockSprite(floor, floorImg))






## throw some blocks ##############

# this is just the default sprite: a randomly colored square
# (with an alpha channel)

def randomlyColoredSquare():
    image = pygame.Surface(render.SPRITE_SIZE)
    image = image.convert()
    image.fill(pygame.color.Color("0x%08x" % random.randint(0,256**4)))
    return image


def blockGenerator():
    Y = 50 # y position for blocks
    # drop some blocks from the edges, moving inward
    for x in range(WIDTH/2, 0, -render.SPRITE_SIZE[0]*2):

        yield group.add(myBlockSprite(rm.addBlock(pixel2world(WIDTH/2+x,Y), px2w(32), px2w(32)),
                                           randomlyColoredSquare()))
        yield group.add(myBlockSprite(rm.addBlock(pixel2world(WIDTH/2-x,Y), px2w(32), px2w(32)),
                                           randomlyColoredSquare()))
    # then drop a bunch randomly:
    for _ in range(50):
        X = random.randint(0,WIDTH)
        yield group.add(myBlockSprite(rm.addBlock(pixel2world(X,Y), px2w(32), px2w(32)),
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

#pygame.display.update()
pygame.display.flip()


tick = 0
#while pygame.event.poll().type != KEYDOWN:

going = True
clock = pygame.time.Clock()
fps = 30
while going:

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == KEYDOWN:
            going = False


    #speed = 0.3
    speed = 1.0 / fps
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

    #group.update()
    #rects = group.draw(screen)    
    #pygame.display.update(rects)
    #group.clear(screen, background)

    prepare_GL()
    for b in rm.blocks:
        draw_body(b)

    pygame.display.flip()
    clock.tick(fps)
