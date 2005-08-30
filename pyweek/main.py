"""
will eventually become script to tie all components together and run game

I haven't done much on here thus far but I'm new to eventnet so hey!
I plan on working on this more tomorrow, please feel free to send me feedack
Micah
PS. It has a bug somewhere.
"""

import pygame, sys, os
import eventnet.driver
from pygame.locals import * 

#initialize pygame
pygame.init() 

# set screen size and put it up 
window = pygame.display.set_mode((640, 480)) 
pygame.display.set_caption('Test01') 
screen = pygame.display.get_surface()

#process a list of events taken from pygame.event.get() (currently)
#will be replaced with our event handler (import?)
class Handler(eventnet.driver.Handler):
    def EVT_K_x(self, event):
        sys.exit(0)

def event_handler(events):
    for event in events:
        eventnet.driver.post(event.type)

#loops to keep checking for events
while 1:
    #combine all event-getters (for lack of a better term) and make a single
    # list with all events to pass to event_handler
    event_handler(pygame.event.get())
