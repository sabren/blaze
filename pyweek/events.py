"""events.py -- the general purpose event register.

Register your event today!

The purpose of this module is to register any events that we'll need
to fire and handle.

Please organize and describe your events in some way that makes sense. :)

"""
import pygame, eventnet.driver
from pygame.locals import *
#modified this to be a single class to be imported by main script (Micah)
class event_handler(eventnet.driver.Handler):
    """
    this class is imported by the main script and will handle ALL events,
    all handlers should call functions from the physics system when that is
    ready
    """
    BLOOD_CHANGED = "HEALTH_BLOOD_CHANGED"
    FAT_CHANGED = "HEALTH_FAT_CHANGED"
    SUGAR_CRASH = "HEALTH_SUGAR_CRASH"
    HIGH_BLOOD = "HEALTH_HIGH_BLOOD"

    #test that makes program close when a key is pressed
    def EVT_KEYDOWN(self, event):
        sys.exit(0)

#process a list of events taken from pygame.event.get() (currently)
#will be replaced with our event handler (import?)
def Handler(events):
    for event in events:
        if event.type == KEYDOWN:
            eventnet.driver.post('KEYDOWN')
        else:
            print event
