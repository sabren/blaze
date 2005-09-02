"""
gravity demo: shows how to put render and room
together to move sprites around based on physics.

since theis is just a demo, I stole the physics
simulation from a pyODE tutorial:

http://pyode.sourceforge.net/tutorials/tutorial3.html

1,2 keys to toggle a rotation.

a - left
d - right
w - up
s - down

ESC - quit.

space - down space to bip, up space bar to climb.

"""
import sys,os
sys.path.append("..")

import room, ode, pygame, render, random, loader
from pygame.locals import *

from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from ode_to_pixel import *

import sounds


###########################################################33

if "2d" in sys.argv:
    sys.argv.remove("2d")
    DIMENSIONS=2

    #def pixel2world(a,b): return (a,b)
    #def px2w(a): return a
    #def world2pixel(a,b): return (a,b)
    
else:
    DIMENSIONS=3

if len(sys.argv) > 1:
    FILENAME = sys.argv[1]
else:
    FILENAME = "gravdemo-geom.svg"
        




camx, camy, camz = (-0.5, -0.5, 1.)
camx, camy, camz = -0.5, 0., -1.0


rot_keys = {}
rot_keys[K_1] = 0
rot_keys[K_2] = 0
rot_keys[K_3] = 0
rot_keys[K_4] = 0
rot_keys[K_5] = 0
rot_keys[K_6] = 0
rot_keys[K_7] = 0
rot_keys[K_8] = 0
rot_keys[K_9] = 0

# prepare_GL
def prepare_GL():
    global camx, camy, camz, rot_keys
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
    doit = 0

    #if doit:
    #    glMatrixMode(GL_PROJECTION)
    #    glLoadIdentity()
    #    P = mat4(1).perspective(45,1.3333,0.2,20)
    #    glMultMatrixd(P.toList())

    # Initialize ModelView matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    #glTranslate(-.5, -.5, 1.1)
    #glTranslate(-.5, -.5, camz)
    #if not doit:

    #glTranslate(0., .0, 1.1)
    #glRotate(180, 0., 1.0, 0.)
    glTranslate(camx, camy, camz)
    glRotate(180, 1., 0.0, 0.)

    if rot_keys[K_1]:
        glRotate(45, 0., 1.0, 0.)
    if rot_keys[K_2]:
        glRotate(-45, 0., 0.0, 1.)

    # Light source
    glLightfv(GL_LIGHT0,GL_POSITION,[0,0,1,0])
    glLightfv(GL_LIGHT0,GL_DIFFUSE,[1,1,1,1])
    glLightfv(GL_LIGHT0,GL_SPECULAR,[1,1,1,1])
    glEnable(GL_LIGHT0)
    #if doit:
    #    # View transformation
    #    V = mat4(1).lookAt(1.2*vec3(2,3,4),(0.5,0.5,0), up=(0,-1,0))
    #    V.rotate(pi,vec3(0,1,0))  
    #    V = V.inverse()
    #    glMultMatrixd(V.toList())



# draw_body
def draw_body(body):
    """Draw an ODE body.
    """
    
    x,y,z = body.getPosition()
    R = body.getRotation()
    usectypes = 0

    translation_part = (x,y,z,1.0)

    if 0:
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

        thelist = T.toList()


    T2 = [[0. for x in range(4)] for x in range(4)]
    T2[0][0] = R[0]
    T2[0][1] = R[1]
    T2[0][2] = R[2]
    T2[1][0] = R[3]
    T2[1][1] = R[4]
    T2[1][2] = R[5]
    T2[2][0] = R[6]
    T2[2][1] = R[7]
    T2[2][2] = R[8]





    thelist2 = []
    for ixx in range(4):
        for ix in range(4):
            thelist2.append(T2[ix][ixx])

    thelist2[-1] = translation_part[-1]
    thelist2[-2] = translation_part[-2]
    thelist2[-3] = translation_part[-3]
    thelist2[-4] = translation_part[-4]




    glPushMatrix()
    #glMultMatrixd(T.toList())
    glMultMatrixd(thelist2)
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
rm = loader.roomFromFile(open(FILENAME))

#import pdb; pdb.set_trace()
#rm.world.setGravity((0,9.81,0)) # in our world y++ is down. :)
rm.world.setERP(0.8) # ??
rm.world.setCFM(10E-5) # ??



### pygame : sprite layers ##############################

# fixes some patchy sound on some systems.
pygame.mixer.pre_init(44100,-16,2, 1024 * 3)
pygame.init()


sound_path = os.path.join("..", "data", "sounds")
sounds.SOUND_LIST = sounds.get_sound_list(sound_path)
sm = sounds.SoundManager(sound_path = sound_path)
# don't load all the sounds to make speeding up the demo load quicker.
#sm.Load()
sm.Load(["bip", "climb"])



if DIMENSIONS==3:
    screen = pygame.display.set_mode((WIDTH,HEIGHT), OPENGL | DOUBLEBUF)
else:
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

## FOREGROUND
#foreground = pygame.image.load("gravdemo-fore.png")
foreground = pygame.surface.Surface((1, 1))

fgSprite = pygame.sprite.Sprite()
fgSprite.image = foreground
fgSprite.rect = foreground.get_rect()

## sprite group
group = WithForeground(fgSprite)

if DIMENSIONS==2:
    screen.blit(background, (0,0))
    #screen.blit(foreground, (0,0))
                         


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
#floor = rm.addGeom(pixel2world(WIDTH/2, HEIGHT-25), px2w(WIDTH), px2w(50))


class myBlockSprite(render.BlockSprite):
    def update(self):
        #print self.block.getPosition()
        #print self.block.getRotation()

        if self.old_position:
            #self.old_position = self.block.getPosition()[:2]
            new_pos = self.block.getPosition()[:2]
            x = (new_pos[0] - self.old_position[0])
            y = (new_pos[1] - self.old_position[1])


            self.rect.move_ip(world2pixel(x,y))
            self.old_position = new_pos
        else:
            self.old_position = map(round, self.block.getPosition()[:2])
            self.rect.center = world2pixel( *map(round, self.block.getPosition()[:2]) )

	


#if DIMENSIONS==2:
    # here's a little drawing of the floor:
    #floorImg = pygame.surface.Surface((WIDTH, 50))
    #group.add(myBlockSprite(floor, floorImg))






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
doneMakingBlocks = True

# Let's put our bird in and see if he can fly. Er, walk.
import hero, health
bird = hero.Bird(rm, pixel2world(400, 10), px2w(32))


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

if DIMENSIONS==2:
    pygame.display.update()
else:
    pygame.display.flip()


tick = 0
going = True
clock = pygame.time.Clock()
fps = 50
while going:

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == KEYDOWN:
            #going = False
            if event.key == K_p:
                camz += 0.1
            if event.key == K_o:
                camz += -0.1
            if event.key == K_d:
                camx += 0.1
            if event.key == K_a:
                camx += -0.1
            if event.key == K_w:
                camy += 0.1
            if event.key == K_s:
                camy += -0.1
            if event.key in [K_1, K_2, K_3, K_4]:
                rot_keys[event.key] = not rot_keys[event.key]

            if event.key == K_SPACE:
                sm.Play("bip")

            if event.key == K_ESCAPE:
                going = False

        if event.type == KEYUP:
            if event.key == K_SPACE:
                sm.Play("climb")

    #print camx, camy, camz

    #speed = 0.3

    speed = 1.0 / fps
    n = 2.0

    for i in range(int(n)):
        rm.space.collide ((rm.world, contactgroup), onNearCollision)

        rm.world.step (speed / n)

        contactgroup.empty()

    """speed = 1.0 / fps
    rm.world.step(speed/2)
    rm.space.collide((rm.world, contactgroup), onNearCollision)
    rm.world.step(speed/2)
    contactgroup.empty()"""

    # add the blocks slowly:        
    tick += 1
    if (tick % 3)==0 and not doneMakingBlocks:
        try:
            blocks.next() 
        except StopIteration:
            doneMakingBlocks = True

    # Walk the bird.
    try: bird.walk(1)
    except health.NotEnoughCalories:
        # Got to keep our strength up...
        food = health.Food(1000, 5000)
        bird.metabolism.eat(food)
    
    # this is a hack for if they fall off the floor
    # if I don't do this, then they just keep acellerating
    # forever due to gravity
    """if (tick % 50)==0:
        for block in rm.blocks:
            x,y,z = block.getPosition()
            if y > HEIGHT:
                block.setBody(None)"""

    if DIMENSIONS==2:
        group.update()
        rects = group.draw(screen)    
        pygame.display.update(rects)
        group.clear(screen, background)
    else:
        prepare_GL()
        for b in rm.blocks:
            draw_body(b)
        pygame.display.flip()
        
    sm.Update(speed)
    clock.tick(fps)
