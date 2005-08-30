"""
will eventually become script to tie all components together and run game

I haven't done much on here thus far but I'm new to eventnet so hey!
I plan on working on this more tomorrow, please feel free to send me feedack
Micah
PS. It has a bug somewhere.
"""

import pygame, sys, os
import eventnet.driver
import events

#initialize pygame
pygame.init() 

# set screen size and put it up 
window = pygame.display.set_mode((640, 480)) 
pygame.display.set_caption('Test') 
screen = pygame.display.get_surface()

#loops to keep checking for events
while 1:
    #combine all event-getters (for lack of a better term) and make a single
    # list with all events to pass to event_handler
    events.Handler(pygame.event.get())
