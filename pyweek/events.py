"""events.py -- the general purpose event register.

Home for all event constants.

Register your event today!

The purpose of this module is to register any events that we'll need
to fire and handle.

Please organize and describe your events in some way that makes sense. :)

The idea is, assign your events a name like MODULE_EVENTNAME, then
assign that name to a constant here.

Then, when you post an event, post it like:
eventnet.driver.post(events.CLASS.EVENTNAME)

This should make refactoring easier.
"""

# Health-related events
class HEALTH:
    BLOOD_CHANGED = "HEALTH_BLOOD_CHANGED"
    FAT_CHANGED = "HEALTH_FAT_CHANGED"
    SUGAR_CRASH = "HEALTH_SUGAR_CRASH"
    HIGH_BLOOD = "HEALTH_HIGH_BLOOD"

class SCREEN:
    STATUS_CHANGED = "SCREEN_STATUS_CHANGED"

# GAME EVENTS
# we're modelling a simple gamepad here,
# but really the events could be triggered
# by the keyboard, mouse, etc...

class GAME:
    UP = "GAME_UP"
    DOWN = "GAME_DOWN"
    RIGHT = "GAME_RIGHT"
    LEFT = "GAME_LEFT"
    JUMP = "GAME_JUMP"
    QUIT = "GAME_QUIT"
    YES  = "GAME_YES"
    NO   = "GAME_NO"
    PAUSE = "GAME_PAUSE"


class MENU:
    PLAY="MENU_PLAY"
    EXIT="MENU_EXIT"
    SCORES="MENU_SCORES"
    # add more here...

class LEVELLIST:
    UP = "LEVELLIST_UP"
    DOWN = "LEVELLIST_DOWN"
    ENTER = "LEVELLIST_ENTER"
