"""
here we define some states for our console.
"""
import pygame, display, sys, eventnet.driver, images, cPickle, string
import pygame, display, sys, eventnet.driver
from constants import IMAGE
from pygame.locals import *
from scorelist import ScoreList

# Menu moved to menu.py
# Game moved to game.py

class Gear(eventnet.driver.Handler):
    def __init__(self, display):
        super(Gear, self).__init__()
        self.display = display
        self.done = False
        self.capture() # listen for events

    def tick(self):
        """
        then it starts ticking...
        by default, each tick does nothing.
        """
        pass


# other states should do this:
class State(Gear):

    def __init__(self, display):
        super(State, self).__init__(display)
        self.next = None

    def kick(self):
        """
        you kick it to make it start. :)
        
        This is so we can pause the execution
        of a state and com back to it later.
        (eg, when a confirmation dialog pops
        up or whatever)
        """
        self.done = False

class Scores(State):

    def kick(self):
        super(Scores, self).kick()
        try:
            file = open('scores', 'r')
            names = cPickle.load(file)
            scores = cPickle.load(file)
            file.close()
        except:
            names = []
            scores = []
            file = open('scores', 'w')
            cPickle.dump(names, file)
            cPickle.dump(scores, file)
            file.close()
            pass
        self.scores = ScoreList(names, scores)
        scr = []
        scor = self.scores.getScores()
        for score in scor:
            scr += [string.join([score[0], str(score[1])], ': ')]
        print scr
        self.display.showImage(0,0, images.SCORES)
        self.display.showImage(0,0, IMAGE.SCORES)
        self.display.addFont(30)
        pos=[640/2, 480/2]
        for text in scr:
            self.display.text (text, 30, pos, justify=self.display.CENTER)
            pos = [pos[0]+50, pos[1]+30]
        self.display.flip()

    def EVT_KeyDown(self, event):
        if not self.done:
            self.done = True

class Credits(State):

    def kick(self):
        super(Credits, self).kick()
        self.display.showImage(0,0, IMAGE.CREDITS)

    def EVT_KeyDown(self, event):
        if not self.done:
            self.done = True

class Help(State):

    def kick(self):
        super(Help, self).kick()
        self.display.showImage(0,0, IMAGE.HELP)

    def EVT_KeyDown(self, event):
        if not self.done:
            self.done = True

class TextInput(State):

    def kick(self):
        super(TextInput, self).kick()
        try:
            file = open('scores', 'r')
            list = cPickle.load(file)
            file.close()
        except:
            file = open('scores', 'w')
            file.close()
            list = []
            pass
        self.scores = ScoreList(list)
        self.display.showImage(0,0, images.SCORE)
        self.s = ''

    def tick(self):
        if not self.done:
            if len(self.s) == 3:
                self.done = True
                self.next = Scores(self.display)
            else:
                self.display.text(self.s, 30, [640/2, 480/2])

    def EVT_KeyDown(self, event):
        if not self.done:
            if event.key == K_ESCAPE:
                self.done = True
            elif event.key == K_a:
                self.s += 'A'
            elif event.key == K_b:
                self.s += 'B'
            elif event.key == K_c:
                self.s += 'C'
            elif event.key == K_d:
                self.s += 'D'
            elif event.key == K_e:
                self.s += 'E'
            elif event.key == K_f:
                self.s += 'F'
            elif event.key == K_g:
                self.s += 'G'
            elif event.key == K_h:
                self.s += 'H'
            elif event.key == K_i:
                self.s += 'I'
            elif event.key == K_j:
                self.s += 'J'
            elif event.key == K_k:
                self.s += 'K'
            elif event.key == K_l:
                self.s += 'L'
            elif event.key == K_m:
                self.s += 'M'
            elif event.key == K_n:
                self.s += 'N'
            elif event.key == K_o:
                self.s += 'O'
            elif event.key == K_p:
                self.s += 'P'
            elif event.key == K_q:
                self.s += 'Q'
            elif event.key == K_r:
                self.s += 'R'
            elif event.key == K_s:
                self.s += 'S'
            elif event.key == K_t:
                self.s += 'T'
            elif event.key == K_u:
                self.s += 'U'
            elif event.key == K_v:
                self.s += 'V'
            elif event.key == K_w:
                self.s += 'W'
            elif event.key == K_x:
                self.s += 'X'
            elif event.key == K_y:
                self.s += 'Y'
            elif event.key == K_z:
                self.s += 'Z'

class Exit(State):
    """
    this state represents quitting the system.
    we should check for it explicitly.
    """
    def __init__(self):
        pass
    def kick(self):
        raise TypeError("never kick EXIT!")
    def tick(self):
        raise TypeError("never tick EXIT!")


# and only use the constant. It's a singleton:
EXIT = Exit()
del Exit
