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
    JUMPFORCE= -8 # negative because y-- is up

class ROOM:
    THICKNESS = 32 # arbitrary depth for all our blocks
    WIDTH = 540
    HEIGHT = 480
    DIRECTORY = "./rooms/"
    TEST_ROOM = "**this is a special flag to load the test room"
    
class CALORIES:
    WALK = 1
    RUN = 3
    JUMP = 5
    
class COLORS:
    HERO = "#000000"
    GOAL = "#FF0000"
    EGG = "#0000FF"
    BALL = "#0000FF"
    FOOD = "#FFFF00"

class REPEAT:
    TICKS = 10 # number of ticks before a key repeats

class SOUND:
    MUSIC="data/music/1takeimprov.ogg"


# geom codes for physics
class CODE: 
    BALL = 0  # DO NOT CHANGE THESE TOP TWO! THE SORTING ORDER IS 
    HERO = 1  # VERY IMPORTANT DUE TO OUR UGLY HACK ROOMPHYSICS.COLLIDE!
    WALL = 2
    FOOD = 3
    GOAL = 4  # the goal for the soccer ball
    EGG  = 5  
    PIT  = 6  # the bottomless pit

class IMAGE:    
    MENU="menu_img.png"
    SCORES='high_scores.png'
    CREDITS='credits.png'
    HELP='help.png'
    GAME="data/game.png" # main room for the game

    SOCCER = "data/soccer.png"
    class STATUS:
        BAR="data/statusbar.png"
        TXT="data/statustxt.png"        
        CARB_POS=(549,99)
        FATS_POS=(596,99)
        TEXT_POS=(552,253)
        
    class KIWI:
        RIGHT="data/kiwi/right.png"
        LEFT="data/kiwi/left.png"


