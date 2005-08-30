"""
will eventually become script to tie all components together and run game

I haven't done much on here thus far but I'm new to eventnet so hey!
I plan on working on this more tomorrow, please feel free to send me feedack
Micah
PS. It has a bug somewhere.
"""

import pygame, sys, os
import eventnet.driver, eventnet._pygame
from pygame.locals import *
import events
#initialize pygame
pygame.init() 

# set screen size and put it up 
window = pygame.display.set_mode((640, 480)) 
pygame.display.set_caption('Test') 
screen = pygame.display.get_surface()

# activate the event_handler
handle = events.event_handler()
handle.capture()

# func to use event_handler()
def Handler(events):
    for event in events:
        if event.type == KEYDOWN:
            eventnet.driver.post('QUIT')
        else:
            print event

#loops to keep checking for events
while 1:
    #combine all event-getters (for lack of a better term) and make a single
    # list with all events to pass to event_handler
    Handler(pygame.event.get())
