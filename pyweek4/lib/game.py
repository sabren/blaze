# Ascent of Justice
# Copyright (C) 2007 Team Trailblazer

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from directicus.engine import State, Menu
from directicus.sfx import Audio, Music
import level,pygame,eventnet.driver,os,data
from campaign import Campaign

class GameState(State):

    def __init__(self,lvl=None):
        State.__init__(self)
        if lvl == None:
            self.level = level.load(Campaign.next())
        else:
            self.level = lvl
        self.bg = pygame.sprite.Group(self.level.s)
        self.selected = None
        self.audio = Audio()
        self.music = Music()
        self.music.volume = 1
        self.audio.volume = 0.5
        self.alarm = 0
        self.music.stop(500)
        self.music.play('data/music/play.mp3',-1)
        self.playing = True

    def start(self):
        State.start(self)
        self.EVT_tick(None)
        self.playing = False
        pygame.display.get_surface().blit(self.level.intro(),(0,0))
        pygame.display.flip()

    def EVT_win(self,event):
        self.quit(Win(self.level.filename))

    def EVT_lose(self,event):
        self.quit(Lose(self.level.filename))

    def EVT_tick(self,event):
        if not self.playing:
            return
        disp = pygame.display.get_surface()
        disp.fill((0,0,0))
        self.level.clear()
        self.level.update()
        self.level.draw()
        self.level.s.rect.left = -self.level.player.rect.left + pygame.display.get_surface().get_width()/2
        self.level.s.rect.top = -self.level.player.rect.top + pygame.display.get_surface().get_height()/2
        self.bg.clear(disp,self.level.background)
        self.bg.draw(disp)
        pygame.display.flip()
        if self.alarm:
            self.alarm -= 1

    def EVT_KeyDown(self,event):
        if not self.playing:
            self.playing = True
        elif event.key == pygame.K_ESCAPE:
            self.quit(PauseMenu(self))

    def EVT_alarm(self,event):
        if not self.alarm:
            self.audio.play('data/sounds/alarm.wav')
            self.alarm = 520

    def quit(self,next=None):
        self.audio.stop(500)
        self.music.stop(500)
        self.music.play('data/music/menu.mp3',-1)
        State.quit(self,next)

class PauseMenu(Menu):
    title = 'Pause Menu'
    options = ['Resume Game',
               'Save Game',
               'Quit Game',
               'Exit to System']
    background = pygame.image.load('data/menu.png').convert()
    color = (0,0,0)

    def __init__(self,gamestate):
        self.gamestate = gamestate
        Menu.__init__(self)

    def EVT_Menu_ResumeGame(self,event):
        self.quit(self.gamestate)

    def EVT_Menu_SaveGame(self,event):
        if not os.path.exists('save.lvl'):
            level.save(self.gamestate.level,'save.lvl')
            self.quit(self.gamestate)
        else:
            self.quit(Overwrite(self))

    def EVT_Menu_QuitGame(self,event):
        self.quit(ConfirmQuit(self))

    def EVT_Menu_ExittoSystem(self,event):
        eventnet.driver.post('Quit')

class Overwrite(Menu):
    title = 'Overwrite old save game?'
    options = ['Yes',
               'No']
    background = pygame.image.load('data/menu.png').convert()
    color = (0,0,0)

    def __init__(self,pausestate):
        Menu.__init__(self)
        self.pausestate = pausestate

    def EVT_Menu_Yes(self,event):
        level.save(self.pausestate.gamestate.level,'save.lvl')
        self.quit(self.pausestate.gamestate)

    def EVT_Menu_No(self,event):
        self.quit(self.pausestate)

class ConfirmQuit(Menu):
    title = 'Quit this game?'
    options = ['Yes',
               'No']
    background = pygame.image.load('data/menu.png').convert()
    color = (0,0,0)

    def __init__(self,pauseMenu):
        self.pauseMenu = pauseMenu
        Menu.__init__(self)

    def EVT_Menu_Yes(self,event):
        self.quit()

    def EVT_Menu_No(self,event):
        s = self.pauseMenu.__new__(type(self.pauseMenu))
        s.__init__(self.pauseMenu.gamestate)
        self.quit(s)

class Win(State):

    def __init__(self,level):
        State.__init__(self)
        self.level = level
        self.audio = Audio()
        self.audio.volume = 0.5
        self.music = Music()
        self.music.volume = 0.7
        seconds = 5
        self.delay = seconds*40

    def start(self):
        self.music.stop(500)
        self.music.play('data/sounds/winner.wav')
        fnt = pygame.font.SysFont('Verdana',30,italic=True)
        text = fnt.render('Level Completed!',True,(0,255,0))
        disp = pygame.display.get_surface()
        disp.blit(text,(400-text.get_width()/2,
                        300-text.get_height()/2))
        pygame.display.flip()
        State.start(self)

    def EVT_tick(self,event):
        if self.delay:
            self.delay -= 1
        else:
            filename = Campaign.next(self.level.replace('\\','/'))
            if filename:
                lvl = level.load(filename)
                level.save(lvl,'save.lvl')
                self.quit(GameState(lvl))
            else:
                self.quit(Ending())

class Lose(State):

    def __init__(self,level):
        State.__init__(self)
        self.level = level
        self.audio = Audio()
        self.audio.volume = 0.5
        self.music = Music()
        self.music.volume = 0.7
        seconds = 5
        self.delay = seconds*40

    def start(self):
        self.music.stop(500)
        self.music.play('data/sounds/loser.wav')
        fnt = pygame.font.SysFont('Verdana',30,italic=True)
        text = fnt.render('You Got Knocked Out!',True,(255,0,0))
        disp = pygame.display.get_surface()
        disp.blit(text,(400-text.get_width()/2,
                        300-text.get_height()/2))
        pygame.display.flip()
        State.start(self)

    def EVT_credits(self,event):
        self.quit()

    def EVT_tick(self,event):
        if self.delay:
            self.delay -= 1
        else:
            lvl = level.load(self.level)
            self.quit(GameState(lvl))

class Ending(State):

    def __init__(self):
        State.__init__(self)
        self.audio = Audio()
        self.audio.volume = 0.5
        self.music = Music()
        self.music.volume = 0.7
        self.music.stop(500)
        self.delay = 10*40
        self.playing = False
        self.image = data.candy
        self.image.set_alpha(0)

    def start(self):
        State.start(self)
        self.music.play('data/sounds/winner.wav')
        pygame.display.get_surface().fill((0,0,0))
        pygame.display.get_surface().blit(self.intro(),(0,0))
        pygame.display.flip()

    def EVT_KeyDown(self,event):
        self.playing = True
        self.music.stop(500)
        self.audio.play('data/sounds/fanfare.wav')

    def intro(self):
        '''
        Copied almost straight from level.py
        '''

        surf = pygame.Surface((800,600))
        surf.fill((0,0,0))
        surf.set_colorkey((0,0,0))
        try:
            intro_file = 'data/ending.txt'
            f = open(intro_file,'rb')
            intro = [line.strip() for line in f.readlines()]
            f.close()
            fnt = pygame.font.SysFont('Verdana',20,italic=True)
            y = 5
            for line in intro:
                line = fnt.render(line,True,(0,255,0))
                surf.blit(line,(400-(line.get_width()/2),y))
                y += line.get_height()+5
        except:
            pass
        return surf

    def EVT_tick(self,event):
        if not self.playing:
            return
        disp = pygame.display.get_surface()
        if self.image.get_alpha() != 255:
            self.image.set_alpha(self.image.get_alpha()+1)
        disp.fill((0,0,0))
        disp.blit(self.image,(400-self.image.get_width()/2,
                              300-self.image.get_height()/2))
        pygame.display.flip()
        if self.delay:
            self.delay -= 1
        else:
            self.quit()
