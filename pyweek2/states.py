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

import pygame, eventnet.driver, os, sys, glob, cPickle, random, time
from string import digits, lowercase

import sprites, scrolling, level, jukebox, effects

pygame.font.init()

class State(eventnet.driver.Handler):
    '''
    State superclass.
    '''

    def __init__(self, screen=None):
        '''
        __init__() an eventnet handler and define constants.
        '''
        eventnet.driver.Handler.__init__(self)
        self.next = None
        self.screen = pygame.display.get_surface()

    def start(self):
        '''
        Start the state running.
        '''

        self.done = False
        self.capture() #start listening for events

    def tick(self):
        '''
        Override.
        '''

        pass

    def quit(self, next=None):
        '''
        Exit state and specify next state (or just revert to main menu if none).
        '''

        self.done = True
        self.next = next
        self.release() # stop listening

class Story(State):
    '''
    Adam's scrolling story.
    '''
    def __init__(self, screen):
        State.__init__(self, screen)

    def start(self, colour=(155,0,0), size=40,
              story_path=os.path.join('data', "story.txt")):
        State.start(self)
        #try:
        #    import pygame.font
        #    pygame.font.init()
        #except ImportError:
        #    print "pygame.font is missing you'll have to read story.txt"
        #    return
        self.colour = colour
        self.size = size
        self.capture()
        self.render_story(open(story_path))

    def position_lines(self):
        mid_top = list(self.story_rect.midtop)
        for render, rect in self.story:
            rect.midtop = mid_top
            self.screen.blit(render, rect)
            mid_top[1] += self.height

    def render_story(self, story_file):
        """Create a list of rendered text from story_file"""
        font = pygame.font.SysFont('Verdana', self.size)
        story = []
        rect_list = []
        height = 600
        center = self.screen.get_width()/2
        for line in story_file:
            line = line.strip()
            render = font.render(line, True, self.colour)
            render_rect = render.get_rect(top=height)
            render_rect.center = center, render_rect.center[1]
            rect_list.append(render_rect)
            story.append((render, render_rect))
            height += font.size(line)[1]
        self.height = font.size(line)[1] # Gap between lines in position_lines
        # The last rect is used in the call so shouldn't be in the list
        del(rect_list[-1])
        self.story = story
        # rect for entire story, lines are position realative to this
        self.story_rect = render_rect.unionall(rect_list)

    def tick(self):
        if self.story_rect.bottom < 0:
            self.quit()
        self.position_lines()
        pygame.display.flip()
        time.sleep(.1)
        self.screen.fill((0,0,0))
        self.story_rect.move_ip(0,-3)

    def EVT_KeyDown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.quit()

class Menu(State):
    '''
    Menu superclass (doubles as main menu state). I use it mostly for the fonts.
    '''

    def __init__(self, screen=None, options=['Watch the Intro', 'Single Player',
                                        'Level Editor', 'Quit'],
                 title='Clad in Iron'):
        State.__init__(self, screen)
        self.selected = None
        title_font = pygame.font.SysFont('Verdana', 50, bold=True)
        title_font.set_underline(True)
        self.title = title_font.render(title, True, (0,0,0))
        self.title_pos = ((screen.get_width()/2)-(self.title.get_width()/2),
                          100)
        self.reg_font = pygame.font.SysFont('Verdana', 40)
        self.screen = pygame.display.get_surface()
        self.options = options
        self.evt_prefix = 'MENU_'
        self.background = pygame.image.load(
            os.path.join('data', 'background.bmp'))

    def over_coordinates(self, width, height, top_left):
        '''
        Method to check if the mouse is in a certain position
        '''
        ms_pos = pygame.mouse.get_pos()
        bottom_right = (top_left[0]+width,
                        top_left[1]+height)
        if ms_pos[0] > top_left[0] and ms_pos[0] < bottom_right[0]:
            x = True
        else:
            x = False
        if ms_pos[1] > top_left[1] and ms_pos[1] < bottom_right[1]:
            y = True
        else:
            y = False
        if x and y:
            return True
        else:
            return False

    def over_image(self, image, top_left):
        '''
        Method to check if the mouse is over an image
        '''
        return self.over_coordinates(image.get_width(),image.get_height(),
                                     top_left)

    def tick(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.title, self.title_pos)
        y = self.title_pos[1]+self.title.get_height()+10
        for option in self.options:
            if self.selected == option:
                img = self.reg_font.render(option, True, (255,255,255))
            else:
                img = self.reg_font.render(option, True, (0,0,0))
            x = (self.screen.get_width()/2)-(img.get_width()/2)
            self.screen.blit(img, (x,y))
            if self.over_image(img, (x,y)):
                self.selected = option
            elif self.selected == option:
                self.selected = None
            y += img.get_height()+5
        pygame.display.flip()

    def EVT_MouseButtonDown(self, event):
        if self.selected <> None: eventnet.driver.post(
            self.evt_prefix+''.join(self.selected.split()))

    def EVT_KeyDown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.quit()

    def EVT_MENU_Quit(self, event):
        print 'menu_quit'
        eventnet.driver.post('Quit')

    def EVT_MENU_WatchtheIntro(self, event):
        self.quit(Story(self.screen))

    def EVT_MENU_SinglePlayer(self, event):
        self.quit(SinglePlayerMenu(self.screen))

    def EVT_MENU_LevelEditor(self, event):
        self.quit(EditChoice(self.screen))

class SaveLevel(Menu):
    '''
    Small input to save a level.
    '''

    def __init__(self, screen, lvl, lvl_name):
        Menu.__init__(self, screen, [], '')
        if lvl_name != '__NEW__':
            level.save(lvl_name, lvl)
            self.quit()
        self.label = self.reg_font.render('Name:', True, (0,0,0))
        self.name = ''
        self.lvl = lvl
        self.topleft = (300, 200)
        self.shift = False

    def tick(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.label, self.topleft)
        img = self.reg_font.render(self.name, True, (0,0,0))
        self.screen.blit(img, (
            self.topleft[0]+self.label.get_width()+5, self.topleft[1]))
        pygame.draw.line(
            self.screen, (0,0,0),
            (self.topleft[0]+self.label.get_width()+img.get_width()+5,
             self.topleft[1]),
            (self.topleft[0]+self.label.get_width()+img.get_width()+5,
             self.topleft[1]+img.get_height()))
        pygame.display.flip()

    def EVT_KeyDown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.quit()
        elif event.key == pygame.K_BACKSPACE:
            if len(self.name) > 0:
                self.name = self.name[:-1]
        elif pygame.key.name(event.key).startswith('['):
            if pygame.key.name(event.key)[1:-1] in digits:
                self.name += pygame.key.name(event.key)[1:-1]
        elif pygame.key.name(event.key) in digits:
            if pygame.key.name(event.key) in digits:
                self.name += pygame.key.name(event.key)
        elif pygame.key.name(event.key) in lowercase:
            if self.shift:
                self.name += pygame.key.name(event.key).upper()
            else:
                self.name += pygame.key.name(event.key)
        elif event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
            self.shift = True
        elif event.key in [pygame.K_RETURN, 271] and self.name != '':
            level.save(self.name, self.lvl)
            self.quit()

    def EVT_KeyUp(self, event):
        if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
            self.shift = False

class LevelEditor(Menu):
    '''
    A level editor.
    '''

    def __init__(self, screen, lvl, lvl_name):
        Menu.__init__(self, screen, ['Hero', 'Tiles', 'Enemies'], '')

        #The reload()s are here because the tiles and sprites kept dissappearing
        #in the toolbar when the editor was visited twice.
        reload(sprites)
        reload(level)

        self.lvl = lvl
        self.lvl_name = lvl_name
        self.background = pygame.Surface((len(lvl['tiles'])*20,
                                          len(lvl['tiles'][0])*20))

        #tiles
        self.tiles = sprites.Group()
        y = 0
        for row in lvl['tiles']:
            x = 0
            for tile in row:
                tile = level.tile(tile.image)
                tile.rect.center = (x,y)
                self.tiles.add(tile)
                x += 20
            y += 20
        self.tiles.draw(self.background)
        self.edit_window = pygame.Surface((650, 600))
        self.display = scrolling.scrolling_display(
            self.background, self.edit_window, (
                (self.background.get_width()/2)-(self.edit_window.get_width()/2),
                (self.background.get_height()/2)-(self.edit_window.get_height()/2)))

        #toolbar
        self.toolbar_background = pygame.image.load(
            os.path.join('data', 'flag2.bmp'))
        self.toolbar = pygame.Surface((150, 10000))
        self.toolbar.blit(self.toolbar_background, (0,0))
        self.toolbar.blit(self.toolbar_background, (0,600))
        self.toolbar.blit(self.toolbar_background, (0,1200))
        self.toolbar_items = sprites.Group()
        self.font = pygame.font.SysFont('Verdana', 30)
        self.font.set_underline(True)
        self.labels = [self.font.render(option, True, (0,0,0))
                       for option in self.options]
        self.font.set_underline(False)
        self.toolbar.blit(
            self.labels[0],
            ((self.toolbar.get_width()/2)-(self.labels[0].get_width()/2),
             50))
        if self.lvl_name == '__NEW__':
            self.hero = sprites.hero((-1000,0))
            self.hero.rect.center = (-1000,0)
        else:
            self.hero = sprites.hero(lvl['hero'])
            self.hero.rect.center = lvl['hero']
        self.h = sprites.Sprite(
            self.hero.image, [self.toolbar_items],
            ((self.toolbar.get_width()/2)-(self.hero.image.get_width()/2),
             self.labels[0].get_rect().bottom+55))
        self.hero.release()
        self.h.release()
        self.toolbar.blit(
            self.labels[1],
            ((self.toolbar.get_width()/2)-(self.labels[1].get_width()/2),
             self.h.rect.bottom+5))
        x = 0
        y = self.h.rect.bottom+self.labels[1].get_height()+10
        for tile in level.tiles:
            tile.rect = tile.rect.move((x,y))
            self.toolbar_items.add(tile)
            if tile.rect.right > 150:
                x = 0
                y += 22
            else:
                x += 22
        for sprite in self.toolbar_items.sprites():
            if sprite.rect.bottom > y: y = sprite.rect.bottom+5
        self.toolbar.blit(
            self.labels[2],
            ((self.toolbar.get_width()/2)-(self.labels[2].get_width()/2),
             y))
        x = 22
        y += 50
        for enemy in sprites.enemies:
            enemy.rect = enemy.rect.move((x,y))
            self.toolbar_items.add(enemy)
            if x == 22:
                x += 55
            else:
                x = 22
                y += 55
        self.toolbar_items.draw(self.toolbar)
        self.toolbar_pos = (0,0)

        self.sprites = sprites.Group(lvl['enemies']+[self.hero])
        self.scrolling = (0,0)
        self.selected = None
        self.mouse_down = False
        self.draw()
        self.toolbar_scrolling = 0

    def quit(self, next=None):
        pygame.mouse.set_visible(True)
        Menu.quit(self, next)

    def draw(self):
        self.tiles.draw(self.background)
        self.sprites.draw(self.background)
        self.display.background = self.background

    def tick(self):
        
        self.toolbar_pos = (self.toolbar_pos[0],
                            self.toolbar_pos[1]+self.toolbar_scrolling)
        if self.toolbar_pos[1] > 0:
            self.toolbar_pos = (0,0)
            self.toolbar_scrolling = 0
        if self.mouse_down:
            if isinstance(self.selected, level.tile):
                for tile in self.tiles.sprites():
                    pos = (tile.rect.left+150-self.display.pos[0],
                           tile.rect.top-self.display.pos[1])
                    if self.over_image(tile.image, pos):
                        tile.image = self.selected.image
                        tile.solid = self.selected.solid
                        try:
                            self.lvl['tiles'][tile.rect.top/20][
                                tile.rect.left/20] = tile
                        except:
                            print (tile.rect.top/20, tile.rect.left/20)
                        self.draw()

        self.display.pos = (self.display.pos[0]+self.scrolling[0],
                            self.display.pos[1]+self.scrolling[1])
        self.display.tick()
        if self.over_coordinates(150, 50, (0,0)):
            img = self.font.render('Save', True, (255,255,255))
        else:
            img = self.font.render('Save', True, (0,0,0))

        self.toolbar.blit(img, (
            ((self.toolbar.get_width()/2)-(self.font.size('Save')[0]/2), 2))
                         )
        self.screen.blit(self.toolbar, self.toolbar_pos)
        self.screen.blit(self.edit_window, (150,0))

        if self.selected != None:
            self.screen.blit(pygame.transform.scale(
                self.selected.image, (20,20)), (pygame.mouse.get_pos()[0]+20,
                                                pygame.mouse.get_pos()[1]+20))
        pygame.display.update(self.screen.get_rect())

    def EVT_MouseButtonDown(self, event):
        if event.button == 1:
            if self.over_image(self.toolbar, (0,0)):
                if self.over_coordinates(150, 50, (0,0)) and self.toolbar_pos[1] == 0:
                    self.quit(SaveLevel(self.screen, self.lvl, self.lvl_name))
                else:
                    for item in self.toolbar_items.sprites():
                        if self.over_image(item.image, (
                            item.rect.left, item.rect.top+self.toolbar_pos[1])):
                            if isinstance(item, level.tile):
                                self.selected = level.tile(item.image, item.solid)
                            elif isinstance(item, sprites.hero):
                                self.selected = self.hero
                            else:
                                self.selected = sprites.Sprite(item.image,
                                                               pos=item.pos)
            elif self.over_image(
                self.edit_window, (150,0)) and self.selected != None:

                if self.selected.image == self.hero.image:
                    pos = (
                        (pygame.mouse.get_pos()[0]-150)+self.display.pos[0],
                        pygame.mouse.get_pos()[1]+self.display.pos[1])
                    self.hero.rect.center = pos
                    self.lvl['hero'] = self.hero.rect.topleft
                    self.selected = None
                elif self.selected.image in [
                    sprite.image for sprite in sprites.enemies]:
                    pos = (
                        (pygame.mouse.get_pos()[0]-150)+self.display.pos[0],
                        pygame.mouse.get_pos()[1]+self.display.pos[1])
                    self.selected.pos = (pos[0]-(self.selected.rect.width/2),
                                         pos[1]-(self.selected.rect.height/2))
                    self.selected.update()
                    self.lvl['enemies'] += [self.selected]
                    self.sprites.add(self.selected)
                    self.selected = sprites.Sprite(self.selected.image,
                                                   pos=self.selected.pos)
                else:
                    self.mouse_down = True
                self.draw()

    def EVT_MouseButtonUp(self, event):
        self.mouse_down = False

    def EVT_KeyDown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.quit()
        elif event.key in [pygame.K_RIGHT, pygame.K_LEFT,
                           pygame.K_UP, pygame.K_DOWN]:
            if event.key == pygame.K_RIGHT:
                self.scrolling = (self.scrolling[0]+3,
                                  self.scrolling[1])
            elif event.key == pygame.K_LEFT:
                self.scrolling = (self.scrolling[0]-3,
                                  self.scrolling[1])
            elif event.key == pygame.K_UP:
                self.scrolling = (self.scrolling[0],
                                  self.scrolling[1]-3)
            elif event.key == pygame.K_DOWN:
                self.scrolling = (self.scrolling[0],
                                  self.scrolling[1]+3)

        elif event.key == pygame.K_PAGEUP:
            self.toolbar_scrolling = 5
        elif event.key == pygame.K_PAGEDOWN:
            if self.toolbar_pos[1]+self.toolbar.get_rect().bottom > self.screen.get_rect().bottom:
                self.toolbar_scrolling = -5

    def EVT_KeyUp(self, event):
        if event.key == pygame.K_RIGHT:
            self.scrolling = (self.scrolling[0]-3,
                              self.scrolling[1])
        elif event.key == pygame.K_LEFT:
            self.scrolling = (self.scrolling[0]+3,
                              self.scrolling[1])
        elif event.key == pygame.K_UP:
            self.scrolling = (self.scrolling[0],
                              self.scrolling[1]+3)
        elif event.key == pygame.K_DOWN:
            self.scrolling = (self.scrolling[0],
                              self.scrolling[1]-3)
        elif event.key == pygame.K_PAGEUP:
            self.toolbar_scrolling = 0
        elif event.key == pygame.K_PAGEDOWN:
            self.toolbar_scrolling = 0

class NewLevel(Menu):
    '''
    Input state to create a new level.
    '''

    def __init__(self, screen):
        Menu.__init__(self, screen, [], '')
        self.labels = [self.reg_font.render(label, True, (0,0,0))
                       for label in ['Height:', 'Width:']]
        self.height = ''
        self.width = ''
        self.topleft = (300, 200)
        self.selected = 'height'

    def tick(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.labels[0], self.topleft)
        self.screen.blit(self.labels[1],
                         (self.topleft[0],
                          self.topleft[1]+100))
        img = self.reg_font.render(self.height, True, (0,0,0))
        self.screen.blit(img, (
            self.topleft[0]+self.labels[0].get_width()+5, self.topleft[1]))
        img2 = self.reg_font.render(self.width, True, (0,0,0))
        self.screen.blit(img2, (
            self.topleft[0]+self.labels[1].get_width()+5,
            self.topleft[1]+100))

        if self.selected == 'height':
            pygame.draw.line(
                self.screen, (0,0,0),
                (self.topleft[0]+self.labels[0].get_width()+img.get_width()+5,
                 self.topleft[1]),
                (self.topleft[0]+self.labels[0].get_width()+img.get_width()+5,
                 self.topleft[1]+img.get_height()))
        else:
            pygame.draw.line(
                self.screen, (0,0,0),
                (self.topleft[0]+self.labels[1].get_width()+2+img2.get_width(),
                 self.topleft[1]+100),
                (self.topleft[0]+self.labels[1].get_width()+2+img2.get_width(),
                 self.topleft[1]+100+img2.get_height()))
        pygame.display.flip()

    def EVT_KeyDown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.quit()
        elif event.key == pygame.K_BACKSPACE:
            if self.selected == 'height' and len(self.height) > 0:
                self.height = self.height[:-1]
            elif len(self.width) > 0:
                self.width = self.width[:-1]

        elif event.key == pygame.K_TAB:
            if self.selected == 'height':
                self.selected = 'width'
            else:
                self.selected = 'height'
        elif pygame.key.name(event.key).startswith('['):
            if pygame.key.name(event.key)[1:-1] in digits:
                if self.selected == 'height':
                    self.height += pygame.key.name(event.key)[1:-1]
                else:
                    self.width += pygame.key.name(event.key)[1:-1]
        elif pygame.key.name(event.key) in digits:
            if self.selected == 'height':
                self.height += pygame.key.name(event.key)
            else:
                self.width += pygame.key.name(event.key)
        elif event.key in [pygame.K_RETURN, 271]:
            try:
                x = int(self.width)/20
                y = int(self.height)/20
                if x == 0:
                    x = 1
                if y == 0:
                    y = 1
                self.quit(LevelEditor(self.screen, level.new(x,y), '__NEW__'))
            except:
                pass

class EditChoice(Menu):
    '''
    This is a chooser for the level editor.
    '''

    def __init__(self, screen):
        Menu.__init__(self, screen, ['Create New']+[os.path.splitext(
            os.path.split(lvl)[-1])[0]for lvl in glob.glob(os.path.join(
                'data','levels', '*.lvl'))], 'Choose a Level')

    def EVT_MouseButtonDown(self, event):
        if self.selected == 'Create New':
            self.quit(NewLevel(self.screen))
        elif self.selected != None:
            self.quit(LevelEditor(self.screen, level.load(self.selected),
                                  self.selected))

class HUD(Menu):
    def __init__(self):
        Menu.__init__(self, pygame.display.get_surface(), [], '')
        self.background = pygame.Surface((600, 50))
        self.background.fill((255,255,255))
        self.background.set_alpha(100)
        self.health = 0
        self.armor = 0
        self.kills = 0

    def tick(self):
        if self.health < 0:
            self.health = 0
        if self.armor < 0:
            self.armor = 0
        self.background.fill((255,255,255))
        self.background.blit(self.reg_font.render('Health: %s' % self.health,
                                                  True, (0,255,0)),
                             (0,0))
        self.background.blit(self.reg_font.render('Armor: %s' % self.armor,
                                                  True, (100,100,100)),
                             (350,0))
        self.screen.blit(self.background, (100, 5))
        pygame.display.update(self.background.get_rect())

class InGameMenu(Menu):
    def __init__(self, screen):
        Menu.__init__(self, screen, ['Resume Game', 'Quit Game'],
                      'Game Paused')

    def start(self, game):
        self.game = game
        Menu.start(self)

    def EVT_MouseButtonDown(self, event):
        if self.selected == 'Resume Game':
            for sprite in self.game.sprites.sprites():
                if sprite not in self.game.FX.sprites.sprites():
                    sprite.capture()
            self.game.jkbx.resume_all_sounds()
            self.game.paused = False
            self.game.capture()
            self.quit()
        elif self.selected == 'Quit Game':
            self.game.quit()
            self.quit()

    def EVT_MENU_QuitGame(self, event):
        self.game.quit()

class GameState(State):
    '''
    Our gamestate.
    '''

    def __init__(self, screen, lvl=None):
        State.__init__(self, screen)
        pygame.mixer.music.stop()
        self.jkbx = jukebox.Jukebox()
        self.jkbx.stop_song()
        self.jkbx.load_song('sisters')
        self.jkbx.set_song_volume(0.2)
        self.jkbx.play_song('sisters', 10)
        pygame.mouse.set_visible(False)
        self.cursor = pygame.image.load(os.path.join('data', 'crosshair.bmp'))
        self.cursor.set_colorkey((0,0,0))
        if lvl != None:
            lvl = level.load(lvl)
        else:
            lvl = lvl.new(5,5)
        self.background = pygame.Surface((len(lvl['tiles'])*20,
                                          len(lvl['tiles'][0])*20))
        self.game_window = pygame.Surface((800,600))
        self.tiles = sprites.Group()
        y = 0
        for row in lvl['tiles']:
            x = 0
            for t in row:
                t.rect = pygame.Rect((x,y),(20,20))
                t.add(self.tiles)
                x += 20
            y += 20
        self.tiles.draw(self.background)
        self.level = self.background.copy()
        self.sprites = sprites.Group()
        self.hero = sprites.hero(lvl['hero'], self.sprites)
        self.hero.rect = pygame.Rect(lvl['hero'], self.hero.rect.size)
        self.enemies = pygame.sprite.Group()
        for enemy in lvl['enemies']:
            pos = enemy.pos
            enemy = sprites.Howitzer([self.sprites, self.enemies])
            enemy.rect.center = pos
            enemy.target = self.hero
        self.display = scrolling.scrolling_display(self.level,
                                                   self.game_window, (0,0))
        self.FX = effects.Effects(self.screen, self.jkbx, self.background)
        self.tile_rects = [t.rect for t in self.tiles]
        self.HUD = HUD()
        self.paused = False
        self.won = False
        self.lost = False
        self.lose_delay = -1
        self.win_delay = -1
        self.old_time = pygame.time.get_ticks()

    def tick(self):
        t = pygame.time.get_ticks()
        if t - self.old_time < 50:
            return
        self.old_time = t
        if self.lose_delay == 0:
            self.lost = True
        else:
            self.lose_delay -= 1
        if self.win_delay == 0:
            self.won = True
        else:
            self.win_delay -= 1
        if self.won and not self.paused:
            msg = pygame.font.SysFont('Verdana', 40).render(
                'You Win!', True, (0,255,0))
            self.screen.blit(msg, (
                (self.screen.get_width()/2)-(msg.get_width()/2),
                (self.screen.get_height()/2)-(msg.get_width()/2)))
            pygame.display.update(msg.get_rect().move(self.screen.get_rect().center))
        elif self.lost and not self.paused:
            msg = pygame.font.SysFont('Verdana', 40).render(
                'You Lose', True, (255,0,0))
            self.screen.blit(msg, (
                (self.screen.get_width()/2)-(msg.get_width()/2),
                (self.screen.get_height()/2)-(msg.get_width()/2)))
            pygame.display.update(msg.get_rect().move(self.screen.get_rect().center))
        if not self.paused:
            collisions = self.hero.collide_rect.collidelistall(self.tile_rects)
            if collisions != []:
                for collide in self.tiles.sprites():
                    if collide.solid:
                        collide = collide.rect
                        if collide.collidepoint(
                            self.hero.rect.centerx, self.hero.rect.top):

                            self.hero.rect.top = collide.bottom
                        if collide.collidepoint(
                            self.hero.rect.left, self.hero.rect.centery):

                            self.hero.rect.left = collide.right
                        if collide.collidepoint(
                            self.hero.rect.centerx, self.hero.rect.bottom):

                            self.hero.rect.bottom = collide.top
                        if collide.collidepoint(
                            self.hero.rect.right, self.hero.rect.centery):

                            self.hero.rect.right = collide.left
            if self.hero.rect.left < 0:
                self.hero.rect.left = 0
            if self.hero.rect.right > self.level.get_width():
                self.hero.rect.right = self.level.get_width()
            if self.hero.rect.top < 0:
                self.hero.rect.top = 0
            if self.hero.rect.bottom > self.level.get_height():
                self.hero.rect.bottom = self.level.get_height()

            self.sprites.add(self.FX.sprites.sprites())
            self.sprites.update()
            self.sprites.clear(self.level, self.background)
            self.sprites.draw(self.level)
            self.FX.sprites.draw(self.level)
            self.HUD.health = self.hero.health
            self.HUD.armor = self.hero.armor
            self.HUD.tick()
            self.FX.smoke_pos = self.hero.steam_vent
            self.FX.tick()
            self.display.background = self.level
            self.display.pos = (
                (self.hero.rect.centerx-(self.screen.get_width()/2)),
                (self.hero.rect.centery-(self.screen.get_height()/2)))
            self.display.tick()
            self.screen.blit(self.game_window, (0,0))
            self.screen.blit(self.cursor, (
                pygame.mouse.get_pos()[0]-(self.cursor.get_width()/2),
                pygame.mouse.get_pos()[1]-(self.cursor.get_height()/2)))
            if len(self.enemies.sprites()) < 0:
                print 'you win!'
                self.win = True
        else:
            self.menu.tick()

    def EVT_MouseButtonDown(self, event):
        if event.button == 1:
            if self.hero.left_delay == 0:
                self.FX.shoot(self.hero.rect.center,
                              (event.pos[0]+self.display.pos[0],
                               event.pos[1]+self.display.pos[1]))
                self.hero.left_delay = 50
        elif event.button == 3 or event.button == 2:
            if self.hero.right_delay == 0:
                self.FX.shoot(self.hero.rect.center,
                              (event.pos[0]+self.display.pos[0],
                               event.pos[1]+self.display.pos[1]))
                self.hero.right_delay = 100

    def EVT_KeyDown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.paused = True
            self.menu = InGameMenu(self.screen)
            self.menu.start(self)
            pygame.mouse.set_visible(True)
            for sprite in self.sprites.sprites()+self.enemies.sprites():
                if sprite not in self.FX.sprites.sprites():
                    sprite.release()
            self.release()
            self.jkbx.pause_all_sounds()

    def EVT_HeroDied(self, event):
        for sprite in self.enemies.sprites():
            sprite.kill()
        self.hero.kill()
        for x in range(100):
            pos = (self.hero.rect.centerx+random.randint(-50,50),
                   self.hero.rect.centery+random.randint(-50,50))
            self.FX.explosion(pos)
        self.FX.smoke_pos = (-1000,0)
        self.lose_delay = 50

    def quit(self, next=None):
        pygame.mouse.set_visible(True)
        self.jkbx.stop_song()
        self.jkbx.play_song('confedmarch')
        State.quit(self, next)

class Skirmish(Menu):
    '''
    Single mission game for a single player.
    '''

    def __init__(self, screen):
        Menu.__init__(self, screen, [os.path.splitext(
            os.path.split(lvl)[-1])[0]for lvl in glob.glob(os.path.join(
                'data','levels', '*.lvl'))], 'Choose a Mission')
        self.playing = False

    def tick(self):
        if not self.playing:
            Menu.tick(self)

    def EVT_MouseButtonDown(self, event):
        if self.selected != None:
            self.quit(GameState(self.screen, self.selected))

class SinglePlayerMenu(Menu):
    def __init__(self, screen):
        Menu.__init__(self, screen, ['Campaign', 'Skirmish',
                                     'Load Game'], 'Single Player')

    #def start(self):
    #    self.quit(Skirmish(self.screen))

    def EVT_MENU_Skirmish(self, event):
        self.quit(Skirmish(self.screen))
