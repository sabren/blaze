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
      app=['Forest-Patrol.pyw'],
      data_files=[
          ('',['README.txt','LICENSE.txt']),
          ('data',glob.glob('data/*.png')+['data/font.ttf']),
          ('data/music',glob.glob('data/music/*.mp3')+glob.glob('data/music/*.wav')),
          ('data/sounds',glob.glob('data/sounds/*.wav')),
          ('data/cursors',glob.glob('data/cursors/*.png')),
          ('data/animations',glob.glob('data/animations/*.png')),
      ],
      name='Forest Patrol',
      version='0.1',
      author='Micah Ferrill',
      url='http://blazeofglory.org/projects/fp',
      author_email='mcferrill@blazeofglory.org',
      description='A fun little RTS developed pre-pyweek 4',
      license='GPL 2',
      keywords='pygame,RTS',
      install_requires=['pygame>=1.7.1','directicus>=0.1'],
      download_url='http://blazeofglory.org/projects/fp',
      zipfile=None,
      )
