import states
import sounds
import pygame
import os
import time

class Soundtrack(states.Gear):
    def __init__(self):
        super(Soundtrack,self).__init__(display=None)

        # initialize pygame:
        #leave enough of a buffer for some machines.
        if os.name == 'posix' or 1:
            try:
                pygame.mixer.pre_init(44100,-16,2, 1024 * 3)
            except:
                pygame.mixer.pre_init()
        else:
            pygame.mixer.pre_init()
        pygame.mixer.init()

        self.sound_manager = sounds.SoundManager()
        self.sound_manager.PlayMusic("1takeimprov.ogg")
        self.sound_manager.Load()
        self.last_time = time.time()
        
    def tick(self):            
        now_time = time.time()
        elapsed_time = self.last_time - now_time
        self.sound_manager.Update(elapsed_time)
        self.last_time = time.time()


    def EVT_COLLIDE_FOOD(self, event):
        print "HI!!!"
    def EVT_COLLIDE_EGG(self, event):
        print "HI!!!"
    def EVT_COLLIDE_WALL(self, event):
        print "HI!!!"
    def EVT_COLLIDE_PIT(self, event):
        print "HI!!!"
    def EVT_GAME_JUMP(self, event):
        self.sound_manager.Play("bip")
