from distutils.core import setup
import glob

import py2app

setup(app=['Forest-Patrol.py'],
      data_files=[
          ('',['README.txt','LICENSE.txt']),
          ('data',glob.glob('data/*.png')+['data/font.ttf']),
          ('data/music',glob.glob('data/music/*.mp3')+glob.glob('data/music/*.wav')),
          ('data/sounds',glob.glob('data/sounds/*.wav')),
          ('data/levels',glob.glob('data/levels/*.lvl')+['data/levels/test']),
          ('data/cursors',glob.glob('data/cursors/*.png')),
          ('data/animations',glob.glob('data/animations/*.png')),
      ],
      )
