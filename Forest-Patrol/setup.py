from distutils.core import setup
import glob

# If we can't import py2exe we just won't use it
try:
    import py2exe
except ImportError:
    pass

# Same for py2app
try:
    import py2app
except ImportError:
    pass

setup(windows=['Forest-Patrol.py'],
      app=['Forest-Patrol.py'],
      data_files=[
          ('data',glob.glob('data/*.png')+['data/font.ttf']),
          ('data/music',glob.glob('data/music/*.mp3')+glob.glob('data/music/*.wav')),
          ('data/sounds',glob.glob('data/sounds/*.wav')),
          ('data/levels',glob.glob('data/levels/*.lvl')+['data/levels/test']),
          ('data/cursors',glob.glob('data/cursors/*.png')),
          ('data/animations',glob.glob('data/animations/*.png')),
      ])
