"""game_constants -- a place to keep constants.
"""
LEFT = -1
RIGHT = 1

SPRITE_SIZE = (32,32)

class SCREEN:
    WIDTH=640
    HEIGHT=480
    
class PHYSICS:
    GRAVITY= (0,98.1,0)
    ERP=0.8      # error reducing thingy in ode
    CFM=10E-5    # some other thing from ode
    FRICTION= 100
    DRAG = -50000
    SCALEFORCE=5000000 # for jumping and walking and running...
    
class HERO:
    RADIUS = 16 # 32x32
    JUMPFORCE= -10 # negative because y-- is up

class ROOM:
    THICKNESS = 32 # arbitrary depth for all our blocks
    WIDTH = 540
    HEIGHT = 480
    
class CALORIES:
    WALK = 1
    RUN = 3
    JUMP = 5
    

class REPEAT:
    TICKS = 10


class IMAGE:    
    MENU="menu.png"
    SCORES='high_scores.png'
    CREDITS='credits.png'
    HELP='help.png'
    GAME="data/game.png" # main room for the game

    class KIWI:
        RIGHT="data/kiwi/right.png"


