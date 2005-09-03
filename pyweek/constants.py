"""game_constants -- a place to keep constants.
"""
LEFT = -1
RIGHT = 1

SPRITE_SIZE = (32,32)

class SCREEN:
    WIDTH=640
    HEIGHT=480
    

class PHYSICS:
    GRAVITY= (0,9.81,0)
    ERP=0.8      # error reducing thingy in ode
    CFM=10E-5    # some other thing from ode

class HERO:
    RADIUS = 16 # 32x32

class ROOM:
    THICKNESS = 32 # arbitrary depth for all our blocks
    WIDTH = 540
    HEIGHT = 480

