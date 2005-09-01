"""events.py -- the general purpose event register.

Home for all event constants.

Register your event today!

The purpose of this module is to register any events that we'll need
to fire and handle.

Please organize and describe your events in some way that makes sense. :)

The idea is, assign your events a name like MODULE_EVENTNAME, then
assign that name to a constant here.

Then, when you post an event, post it like:
eventnet.driver.post(events.MODULE_EVENTNAME)

This should make refactoring easier.
"""
#import pygame
#from pygame.locals import *
import eventnet

# Health-related events
HEALTH_BLOOD_CHANGED = "HEALTH_BLOOD_CHANGED"
HEALTH_FAT_CHANGED = "HEALTH_FAT_CHANGED"
HEALTH_SUGAR_CRASH = "HEALTH_SUGAR_CRASH"
HEALTH_HIGH_BLOOD = "HEALTH_HIGH_BLOOD"


# INPUT EVENTS
# we're modelling a simple gamepad here,
# but really the events could be triggered
# by the keyboard, mouse, etc...

class INPUT:
    UP = "INPUT_UP"
    DOWN = "INPUT_DOWN"
    RIGHT = "INPUT_RIGHT"
    LEFT = "INPUT_LEFT"
    JUMP = "INPUT_JUMP"
    QUIT = "INPUT_QUIT"
    YES  = "INPUT_YES"
    NO   = "INPUT_NO"
    PAUSE = "INPUT_PAUSE"


class MENU:
    PLAY="MENU_PLAY"


