"""events.py -- the general purpose event register.

Home for all event constants.
Home for the main event handler.
"""

"""
Register your event today!

The purpose of this module is to register any events that we'll need
to fire and handle.

Please organize and describe your events in some way that makes sense. :)

The idea is, assign your events a name like MODULE_EVENTNAME, then
assign that name to a constant here.

Then, when you post an event, post it like:
eventnet.driver.post(events.MODULE_EVENTNAME)

This should make refactoring easier.

Then, register your event with event_handler, using the appropriate
syntax.
"""
import pygame, eventnet.driver, sys, os
from pygame.locals import *

# Health-related events
HEALTH_BLOOD_CHANGED = "HEALTH_BLOOD_CHANGED"
HEALTH_FAT_CHANGED = "HEALTH_FAT_CHANGED"
HEALTH_SUGAR_CRASH = "HEALTH_SUGAR_CRASH"
HEALTH_HIGH_BLOOD = "HEALTH_HIGH_BLOOD"


#modified this to be a single class that's imported by main script
#Micah
class event_handler(eventnet.driver.Handler):
    """
    this class is imported by the main script and will handle ALL events,
    all handlers should call functions from the physics system when that is
    ready

    How to use this:
    http://lgt.berlios.de/#eventnet
    """
    #post events in this manner
    def EVT_KEYDOWN(self, event):
        sys.exit(0)

    # Metabolism-related events
    def EVT_HEALTH_BLOOD_CHANGED(self, event):
        # sugar = a_health_model.getBlood()
        pass

    def EVT_HEALTH_FAT_CHANGED(self, event): pass

    def EVT_HEALTH_SUGAR_CRASH(self, event): pass
    
    def EVT_HIGH_BLOOD(self, event): pass

