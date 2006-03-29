import pygame, eventnet.driver, os, sys, sprites, scrolling, level, glob
import leveleditor
'''
Store states here.
'''

pygame.font.init()

class State(eventnet.driver.Handler):
    '''
    State superclass. Doubles as a dummy state.
    '''
    def __init__(self, screen):
        eventnet.driver.Handler.__init__(self)
        self.next = None
        self.screen = screen

    def start(self):
        '''
        Start the state running. (put initialization here)
        '''
        self.done = False
        self.capture() #start listening for events

    def tick(self):
        '''
        Called every frame, put updates here.
        '''
        pass

    def quit(self, next=None):
        '''
        Exit state and specify next state.
        '''
        self.done = True
        self.next = next
        self.release() # stop listening

class Menu(State):
    def __init__(self, screen, options=['New Game', 'Load Game', 'Level Editor',
                                        'Highscores', 'Help', 'Quit'],
                 title='Main Menu'):
        State.__init__(self, screen)
        self.selected = None
        title_font = pygame.font.SysFont('Arial', 50, bold=True)
        title_font.set_underline(True)
        self.title = title_font.render(title, True, (115,115,115))
        self.title_pos = ((screen.get_width()/2)-(self.title.get_width()/2),
                          100)
        self.reg_font = pygame.font.SysFont('Arial', 40)
        self.screen = screen
        self.options = options
        self.evt_prefix = 'MENU_'

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
        self.screen.fill((0,0,0))
        self.screen.blit(self.title, self.title_pos)
        y = self.title_pos[1]+self.title.get_height()+10
        for option in self.options:
            if self.selected == option:
                img = self.reg_font.render(option, True, (255,255,255))
            else:
                img = self.reg_font.render(option, True, (115,115,115))
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

    def EVT_MENU_Quit(self, event):
        eventnet.driver.post('Quit')

class SaveLevel(Menu):
    '''
    Small input to save a level.
    '''

class LevelEditor(Menu):
    '''
    A level editor.
    '''

    def __init__(self, screen, lvl=level.empty_level):
        Menu.__init__(self, screen, ['Hero', 'Tiles', 'Enemies'], '')
        reload(level)
        self.background = pygame.Surface((len(lvl['tiles'])*50,
                                          len(lvl['tiles'][0])*50))

        #tiles
        self.tiles = sprites.Group(lvl['tiles'])
        y = 0
        for row in lvl['tiles']:
            x = 0
            for tile in row:
                self.background.blit(tile.image, (x,y))
                x += 50
            y += 50                

        self.edit_window = pygame.Surface((650, 600))
        self.display = scrolling.scrolling_display(
            self.background, self.edit_window,
            (-self.background.get_width(),
             -self.background.get_height()))

        #toolbar
        self.toolbar = pygame.Surface((150, 2000))
        self.toolbar.fill((100,100,100))
        self.toolbar_items = sprites.Group()
        self.font = pygame.font.SysFont('Arial', 30)
        self.font.set_underline(True)
        self.labels = [self.font.render(option, True, (0,0,0))
                       for option in self.options]
        self.font.set_underline(False)
        self.toolbar.blit(
            self.labels[0],
            ((self.toolbar.get_width()/2)-(self.labels[0].get_width()/2),
             50))
        self.hero = sprites.hero(lvl['hero'])
        self.h = sprites.Sprite(
            self.hero.image, [self.toolbar_items],
            ((self.toolbar.get_width()/2)-(self.hero.image.get_width()/2),
             self.labels[0].get_rect().bottom+55))
        self.toolbar.blit(
            self.labels[1],
            ((self.toolbar.get_width()/2)-(self.labels[1].get_width()/2),
             self.h.rect.bottom+5))
        x = 22
        y =  self.h.rect.bottom+self.labels[1].get_height()+10
        for tile in level.tiles:
            tile.rect = tile.rect.move((x,y))
            self.toolbar_items.add(tile)
            if x == 22:
                x += 55
            else:
                x = 22
                y += 55
        for sprite in self.toolbar_items.sprites():
            if sprite.rect.bottom > y: y = sprite.rect.bottom+5
        self.toolbar.blit(
            self.labels[2],
            ((self.toolbar.get_width()/2)-(self.labels[2].get_width()/2),
             y))
        x = 22
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

    def tick(self):
        self.display.background = self.background
        self.display.pos = (self.display.pos[0]+self.scrolling[0],
                            self.display.pos[1]+self.scrolling[1])
        self.display.tick()
        self.screen.blit(self.toolbar, self.toolbar_pos)
        self.screen.blit(self.edit_window, (150,0))
        if self.over_coordinates(
            150, self.font.get_ascent()+self.font.get_descent()+10, (0,0)):
            img = self.font.render('Save', True, (255,255,255),
                                   (0,0,0))
        else:
            img = self.font.render('Save', True, (0,0,0))
        self.screen.blit(img, (
            ((self.toolbar.get_width()/2)-(self.font.size('Save')[0]/2), 2)))

        if self.selected != None:
            self.screen.blit(self.selected, pygame.mouse.get_pos())
        pygame.display.update(self.screen.get_rect())

    def EVT_MouseButtonDown(self, event):
        for item in self.toolbar_items.sprites():
            if self.over_image(item.image, item.rect.topleft):
                self.selected = item.image
        if self.over_image(self.edit_window, (150,0)):
            for tile in self.tiles.sprites():
                pos = tile.rect.topleft
                if self.over_image(tile.image, pos):
                    tile.kill()
                    tile = level.tile(self.selected, pos)
                    self.tiles.add(tile)

    def EVT_KeyDown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.quit()
        elif event.key == pygame.K_RIGHT:
            self.scrolling = (self.scrolling[0]+1,
                              self.scrolling[1])
        elif event.key == pygame.K_LEFT:
            self.scrolling = (self.scrolling[0]-1,
                              self.scrolling[1])
        elif event.key == pygame.K_UP:
            self.scrolling = (self.scrolling[0],
                              self.scrolling[1]-1)
        elif event.key == pygame.K_DOWN:
            self.scrolling = (self.scrolling[0],
                              self.scrolling[1]+1)
        elif event.key == pygame.K_PAGEUP and self.toolbar_pos[1] < 0:
            self.toolbar_pos = (0, self.toolbar_pos[1] + 50)
        elif event.key == pygame.K_PAGEDOWN:
            if self.toolbar_pos[1]+self.toolbar.get_height() > self.screen.get_rect().bottom:
                self.toolbar_pos = (0, self.toolbar_pos[1] - 50)

    def EVT_KeyUp(self, event):
        if event.key == pygame.K_RIGHT:
            self.scrolling = (self.scrolling[0]-1,
                              self.scrolling[1])
        elif event.key == pygame.K_LEFT:
            self.scrolling = (self.scrolling[0]+1,
                              self.scrolling[1])
        elif event.key == pygame.K_UP:
            self.scrolling = (self.scrolling[0],
                              self.scrolling[1]+1)
        elif event.key == pygame.K_DOWN:
            self.scrolling = (self.scrolling[0],
                              self.scrolling[1]-1)

class EditChoice(Menu):
    '''
    This is a choice for the level editor.
    '''

    def __init__(self, screen):
        self.levels = ['Create New']+[os.path.splitext(
            os.path.split(lvl)[-1])[0]for lvl in glob.glob(os.path.join(
                'data','levels', '*.lvl'))]
        Menu.__init__(self, screen, self.levels, 'Choose a Level')

    def EVT_KeyDown(self, event):
        self.quit()

    def EVT_MouseButtonDown(self, event):
        if self.selected == 'Create New':
            self.quit(LevelEditor(self.screen))
        elif self.selected != None:
            self.quit(LevelEditor(self.screen,
                                  os.path.join('data','levels',
                                               self.selected+'.lvl')))

class GameState(State):
    '''
    Our gamestate.
    '''

    def __init__(self, screen):
        State.__init__(self, screen)
        self.level = level.level()
        self.display = scrolling.scrolling_display(self.level.level,
                                                   self.screen, (0,0))

    def tick(self):
        self.level.tick()
        self.display.background = self.level.level
        self.display.pos = (self.level.hero.rect.centerx-(self.screen.get_width()/2),
                            self.level.hero.rect.centery-(self.screen.get_height()/2))
        self.display.tick()
        self.level.hero.rect.move((self.level.hero.pos[0]-5,
                                   self.level.hero.pos[1]-5))

    def EVT_KeyDown(self, event):
        if event.key == pygame.K_ESCAPE:
            pygame.image.save(self.level.level, 'temp.bmp')
            self.quit()

