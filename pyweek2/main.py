#Clad in Iron (development version)
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

__version__ = 'Development Version'
__author__ = 'Team Trailblazer'

import sys, os

import pygame, eventnet.driver #external libs
import states, jukebox #our states system and the sound engine

class game(eventnet.driver.Handler):
    '''
    Master object to watch over our states.
    '''

    def __init__(self):
        eventnet.driver.Handler.__init__(self)

        pygame.init()
        pygame.display.set_caption('Clad in Iron (dev version)')
        pygame.display.set_icon(pygame.image.load(
            os.path.join('data', 'flag.jpg')))
        self.capture()
        self.done = False
        self.screen = pygame.display.set_mode((800, 600))
        self.volume = 0.2
        self.jkbx = jukebox.Jukebox()
        self.jkbx.load_song('confedmarch')
        self.jkbx.play_song('confedmarch')
        self.state = states.Story(self.screen)
        self.state.start()

    def tick(self):
        '''
        Set sound volume and, either tick() or change current state.
        '''

        self.jkbx.set_song_volume(self.volume)
        for sound in self.jkbx.get_sounds():
            sound.set_volume(self.volume)
        if not self.jkbx.is_song_playing(): self.jkbx.play_random_song()
        if not self.state.done:
            self.state.tick()
        elif self.state.next <> None:
            self.state = self.state.next
            self.state.start()
        else: self.load_default_state()

    def load_default_state(self):
        '''
        Quickly reverts back to the main menu.
        '''

        self.state.quit()
        self.state = states.Menu(self.screen)
        self.state.start()

    def EVT_Quit(self, event):
        '''
        Called when program ends.
        '''

        print 'done?' #DEBUGGING "PRINT"
        self.release()
        self.done = True

    def EVT_KeyDown(self, event):
        '''
        Global key events (screenshot and volume control).
        '''

        if event.key == pygame.K_F9:
            fn = 'screenshot.bmp'
            num = 0
            while 1:
                try:
                    open(fn).close()
                except:
                    break
                fn = 'screenshot%s.bmp' % str(num)
                num += 1
            pygame.image.save(self.screen, fn)
        elif event.key == pygame.K_KP_PLUS and self.volume < 1.0:
            self.volume += 0.1
        elif event.key == pygame.K_KP_MINUS and self.volume > 0.0:
            self.volume -= 0.1
        
def main():
    '''
    Primary function. Starts and runs the game() object.
    '''

    g = game()
    while not g.done:
        #post pygame events to eventnet
        for event in pygame.event.get():
            eventnet.driver.post(pygame.event.event_name(event.type),
                                 **event.dict)
        g.tick()
    print 'bye' #DEBUGGING "PRINT"
    pygame.quit()
        
if __name__=='__main__':
    main()
