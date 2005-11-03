import os, glob

# Ugly fix of my py2exe system.

# constants
old = 'c:\\\\cvs\\\\pyweek\main.py'
old_dir = os.path.split(old)[0]
setup_script = os.path.join(old_dir, 'setup.py')
new = 'c:\\test'
console = True
data_files = glob.glob(os.path.join(old_dir, '*.png'))
bundle = True
icon = None
xtra_mods = ['pygame.locals', 'pygame']
Xcludes = ['w9xpopen', 'msvcr71']
setup_code = '''# setup.py
from distutils.core import setup
import py2exe

setup(console=["%s"], data_files=[('', %s)], zipfile=None,
            options = {"py2exe": { "dll_excludes": ["msvcr71.dll", "w9xpopen.exe"]}})
''' % (old, data_files)

cmd = '%s py2exe -c --dist-dir %s -b 1 %s -e w9xpopen.exe' % (setup_script, new,
            ' '.join([' -i %s' % x for x in xtra_mods]))

# write script and run command line
#'''
open(setup_script, 'w').write(setup_code)
#print cmd
os.system(cmd)
raw_input() #'''
