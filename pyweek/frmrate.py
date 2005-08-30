"""To use this module call start() at the start of
your main loop and at the end call stop(n), where
n is the frame rate you want."""

import time

def start():
    global t
    t = time.time()
        
def stop(rate):
    global t
    frmlen = 1.0/rate
    try:
        time.sleep(frmlen - (time.time() - t))
    except:
        IOError
        
if __name__ == "__main__":
    import pygame, math
    clock = pygame.time.Clock()
    for n in range(100):
        start()
        time.sleep(0.000001)
        clock.tick()
        stop(50)
    print clock.get_fps()