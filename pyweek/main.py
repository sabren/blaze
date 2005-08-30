"""
will eventually become script to tie all components together and run game,
please feel free to send me feedack!
Micah
"""

# not sure if we need all of these but they're here just in case
import pygame, sys, os, cPickle, loader, eventnet.driver, eventnet._pygame, events, string
from pygame.locals import *

#initialize pygame
pygame.init() 

# load all levels and parse into dict
lvl_list = []
for lvl in os.listdir('rooms'):

    # adds name of level to list
    if string.find(lvl, '-') == -1:
        lvl_list += [os.path.splitext(lvl)[0]]

#function to load all 3 level elements
def load(file):
    list = []
    lst = ['back.png', 'geom.svg', 'fore.png']
    for x in range(3):
        list += [string.join([file, lst[x]], '-')]
    return list

# set screen size and put it up 
window = pygame.display.set_mode((640, 480)) 
pygame.display.set_caption('Test') 
screen = pygame.display.get_surface()

# activate the event_handler
eventnet._pygame.register_events()
handle = events.event_handler()
handle.capture()

#loop to keep checking for events
while 1:
    for event in pygame.event.get():
        eventnet.driver.post(event.type, **event.dict)
