"""events.py -- the general purpose event register.

Register your event today!

The purpose of this module is to register any events that we'll need
to fire and handle.

Please organize and describe your events in some way that makes sense. :)

"""



class Health:
    """Health-related Events
    """
    BLOOD_CHANGED = "HEALTH_BLOOD_CHANGED"
    FAT_CHANGED = "HEALTH_FAT_CHANGED"
    SUGAR_CRASH = "HEALTH_SUGAR_CRASH"
    HIGH_BLOOD = "HEALTH_HIGH_BLOOD"
