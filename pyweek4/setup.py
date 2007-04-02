from distutils.core import setup
import glob

extra_opts = dict(zipfile=None)

# If py2exe exists we'll import it
try:
    import py2exe
    extra_opts.update({'windows': ['run_game.py']})
except ImportError:
    pass

# Same for py2app
try:
    import py2app
    extra_opts.update({'zipfile': '', # zipfile=None confuses py2app
                       'app': ['run_game.py']})
except ImportError:
    pass

setup(scripts=['editor.py','levelGen.py'],
      data_files=[
          ('',['README.txt','LICENSE.txt']),
          ('data',glob.glob('data/*.png')),
          ('data/animations',glob.glob('data/animations/*.png')),
          ('data/levels',glob.glob('data/levels/*.lvl')),
          ('data/textures',glob.glob('data/textures/*.png')),
      ],
      name='Ascent of Justice',
      version='0.1',
      author='Micah Ferrill',
      url='http://blazeofglory.org/projects/ascent',
      author_email='mcferrill@blazeofglory.org',
      description='Trailblazer entry in pyweek 4',
      license='GPL 2',
      keywords='pygame',
      install_requires=['pygame>=1.7.1','directicus>=0.1'],
      download_url='http://blazeofglory.org/projects/ascent',
      **extra_opts
      )
