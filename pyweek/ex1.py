#!/usr/bin/python

'''
pyODE / pygame,
graphics / physics
example

Micah
'''

#import and initialize
import ode, pygame, sys
from pygame.locals import *
pygame.init()

# set up our screen
screen = pygame.display.set_mode((800, 600))
screen.fill((0, 0, 0))
pygame.display.flip()
pygame.display.set_caption('ODE/pygame test')

#our physics environment
world = ode.World()

#information for our ball "body" and "ball.bmp"
img = pygame.image.load('ball.bmp')
body = ode.Body(world)
M = ode.Mass()
M.setSphere(2500.0, 0.05)
M.mass = 1.0
body.setMass(M)
body.setPosition( (0,2,0) )

if __name__=='__main__':
    #mainloop
    while 1:

        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            #keyboard controls (arrows and ESC)
            elif pygame.event.event_name(event.type) == 'KeyDown':
                if event.dict['key'] == K_ESCAPE: sys.exit(0)
                elif event.dict['key'] == K_RIGHT:
                    body.addForce((500,0,0))
                elif event.dict['key'] == K_LEFT:
                    body.addForce((-500,0,0))
                elif event.dict['key'] == K_UP:
                    body.addForce((0,-500,0))
                elif event.dict['key'] == K_DOWN:
                    body.addForce((0,500,0))
            elif pygame.event.event_name(event.type) == 'KeyUp':
                if event.dict['key'] == K_ESCAPE: sys.exit(0)
                elif event.dict['key'] == K_RIGHT:
                    body.addForce((-500,0,0))
                elif event.dict['key'] == K_LEFT:
                    body.addForce((500,0,0))
                elif event.dict['key'] == K_UP:
                    body.addForce((0,500,0))
                elif event.dict['key'] == K_DOWN:
                    body.addForce((0,-500,0))

        #update (physics AND graphics)
        x,y,z = body.getPosition()
        pos = (x, y)
        world.step(0.04)
        screen.fill((0, 0, 0))
        screen.blit(img, pos)
        pygame.display.flip()
