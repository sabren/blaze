from directicus.engine import Engine,Menu,State
import os, subprocess, pygame

games = list()
for x in os.listdir(os.curdir):
    if os.path.isdir(x):
        games.append(x)

# Override with just one for demonstration purposes
games = ['demo']

class Game(object):
    def __init__(self,name='demo'):
        self.name = name
        self.readme = open(os.path.join(name,'README.txt')).read()
        lines = [line.replace('\r','') for line in self.readme.split('\n')]
        self.title = lines[0]
        self.team = lines[1][6:]
        self.members = lines[2][8:]
        self.link = '%s (by %s)' % (self.title,self.team)
        self.slug = ''.join(self.link.split())

games = [Game(name) for name in games]

class LauncherMenu(Menu):
    color = (0,100,0)
    highlight = (0,255,0)
    regularFont = pygame.font.SysFont('Verdana',20)
    titleFont = pygame.font.SysFont('Verdana',40)

    def __init__(self):
        Menu.__init__(self)
        pygame.display.set_caption('PyWeek Entry Launcher')

    def start(self):
        State.start(self)
        if self.background == None:
            self.background = pygame.display.get_surface().copy()
        title = self.headerFont.render(self.title, True, self.color)
        self.background.blit(title,
                             ((self.background.get_width()/2)-(title.get_width()/2),
                              20))
        opts = []
        y = 120
        for option in self.options:
            img = self.regularFont.render(option,True,self.color)
            rect = img.get_rect()
            rect.midtop = (self.background.get_width()/2,y)
            opts.append([option,img,rect])
            y += 30
        self.options = opts

class About(LauncherMenu):
    '''
    Page for an individual game.
    '''

    options = ['Play','Back']

    def __init__(self,name='demo'):
        self.background = pygame.display.get_surface().copy()
        self.background.fill((255,255,255))
        obj = [g for g in games if g.slug == name][0]
        self.name = obj.name
        self.title = '%s (%s)' % (obj.title, obj.members)
        LauncherMenu.__init__(self)

    def EVT_Menu_Play(self,event):
        script = os.path.join(name,'run_game.py')
        subprocess.Popen(['python',script])

    def EVT_Menu_Back(self,event):
        self.quit()

class Launcher(LauncherMenu):
    handler_prefix = 'EVT_'
    title = ''
    background = pygame.image.load('background.png')

    def __init__(self):
        self.options = []
        for game in games:
            self.options.append(game.link)
            setattr(self,'EVT_Menu_'+game.slug,self.launchProject)
        LauncherMenu.__init__(self)

    def start(self):
        State.start(self)
        opts = []
        y = 100
        for option in self.options:
            img = self.regularFont.render(option,True,self.color)
            rect = img.get_rect()
            rect.midtop = (self.background.get_width()/2,y)
            opts.append([option,img,rect])
            y += 30
        self.options = opts

    def launchProject(self,event):
        self.quit(About(self.selected))

if __name__=='__main__':
    e = Engine(40)
    e.DEFAULT = Launcher
    e.run()
