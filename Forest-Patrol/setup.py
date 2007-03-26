from distutils.core import setup
import glob

extra_opts = dict(zipfile=None)

# If py2exe exists we'll import it
try:
    import py2exe
    extra_opts.update({'windows': ['Forest-Patrol.py']})
except ImportError:
    pass

# Same for py2app
try:
    import py2app
    extra_opts.update({'zipfile': '', # zipfile=None confuses py2app
                       'app': ['Forest-Patrol.py']})
except ImportError:
    pass

setup(data_files=[
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
      **extra_opts
      )
