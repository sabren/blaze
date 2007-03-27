from directicus.engine import Engine,Menu
import os, subprocess

games = list()
for x in os.listdir(os.curdir):
    if os.path.isdir(x):
        games.append(x)

# Override with just one for demonstration purposes
games = ['demo']

class Launcher(Menu):
    handler_prefix = 'EVT_'
    title = 'PyWeek Entry Launcher'
    options = []

    def __init__(self):
        for game in games:
            self.options.append(game)
            game = ''.join(game.split())
            setattr(self,'EVT_Menu_'+game,self.launchProject)

    def launchProject(self,event):
        script = os.path.join(os.curdir,self.selected,'run_game.py')
        subprocess.Popen(['python',script])

if __name__=='__main__':
    e = Engine(40)
    e.DEFAULT = Launcher
    e.run()
