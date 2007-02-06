#Directicus
#Copyright (C) 2006 Team Trailblazer
#
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

'''
Easy to use state engine.
'''

import pygame, eventnet.driver

class State(eventnet.driver.Handler):
    '''
    Our basic state object. See the methods for specifics.
    '''

    def __init__(self):
        '''
        __init__(self)

        __init__ superclasses, load data, etc.
        '''

        eventnet.driver.Handler.__init__(self)
        self.done = True
        self.next = None

    def start(self):
        '''
        State.start() - Called right before it starts ticking.
        '''

        self.capture() #start eventnet for this object
        self.done = False

    def EVT_tick(self,event):
        '''
        State.EVT_tick(event)

        Called once every frame.
        '''

        pass

    def quit(self, next=None):
        '''
        State.quit(next=None) - Called to stop, optionally points to successor.

        If next is none default state will load.
        '''
        
        self.release()
        self.next = next
        self.done = True

if not pygame.font.get_init():
    pygame.font.init()

class Menu(State):
    '''
    A class to display a very simple menu.
    Attributes are text, background, fonts, and color[s].
    '''

    headerFont = pygame.font.SysFont('Verdana',50)
    headerFont.set_underline(True)
    regularFont = pygame.font.SysFont('Verdana',30)
    color = (255,255,255)
    hover = (100,100,100)
    title = 'Menu Demo'
    options = ['Nothing','Quit']
    background = None
    prefix = 'Menu_'

    def start(self):
        '''
        Menu.start() - renders title onto background and parses options.
        '''

        State.start(self)
        if self.background == None:
            self.background = pygame.display.get_surface().copy()
        title = self.headerFont.render(self.title, True, self.color)
        self.background.blit(title,
                             ((self.background.get_width()/2)-(title.get_width()/2),
                              20))
        opts = []
        y = 100
        for option in self.options:
            img = self.regularFont.render(option,True,self.color)
            rect = img.get_rect()
            rect.midtop = (self.background.get_width()/2,y)
            opts.append([option,img,rect])
            y += 50
        self.options = opts
        self.selected = None

    def EVT_tick(self,event):
        '''
        Menu.EVT_tick(event) - reload options and check for a mouseover
        '''

        pygame.display.get_surface().blit(self.background,(0,0))
        self.selected = None
        for option in self.options:
            old = option
            if option[2].collidepoint(pygame.mouse.get_pos()):
                option[1] = self.regularFont.render(option[0],True,self.hover)
                self.selected = ''.join(option[0].split())
            else:
                option[1] = self.regularFont.render(option[0],True,self.color)
            self.options[self.options.index(old)] = option
            pygame.display.get_surface().blit(option[1],option[2])
        pygame.display.flip()

    def EVT_MouseButtonDown(self,event):
        '''
        Menu.EVT_MouseButtonDown(event) - if an option is clicked launch it.
        '''

        if self.selected != None:
            eventnet.driver.post(self.prefix + self.selected)

    def EVT_Menu_Quit(self,event):
        '''
        Menu.EVT_Menu_Quit(event) - "Quit" option clicked, exit program.
        '''

        eventnet.driver.post('Quit')

class Engine(eventnet.driver.Handler):
    '''
    Toplevel control object. "DEFAULT" will be loaded at start and whenever no
    "next" is supplied.
    '''

    DEFAULT = Menu

    def __init__(self,fps=20):
        '''
        Engine.__init__(fps) - compute settings and prepare to launch with "fps"
        '''

        eventnet.driver.Handler.__init__(self)
        self.state = None
        self.size = (800,600)
        self.fullscreen = False
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.capture()

    def run(self):
        '''
        Engine.run() - launch pygame and run the mainloop
        '''

        pygame.init()
        if self.fullscreen:
            pygame.display.set_mode(self.size,pygame.FULLSCREEN)
        else:
            pygame.display.set_mode(self.size)
        self.state = self.DEFAULT()
        self.state.start()

        #mainloop
        while 1:
            for event in pygame.event.get():
                eventnet.driver.post(pygame.event.event_name(event.type),
                                     **event.dict)
            if self.state.done and self.state.next:
                self.state = self.state.next
                self.state.start()
            elif self.state.done and not self.state.next:
                self.state = self.DEFAULT()
                self.state.start()
            else:
                self.clock.tick(self.fps)
                eventnet.driver.post('tick')

    def EVT_Quit(self,event):
        '''
        Engine.EVT_Quit(event) - shut down the program
        '''

        self.release()
        pygame.quit()
        import sys
        sys.exit(0)

if __name__=='__main__':
    e = Engine()
    e.run()
