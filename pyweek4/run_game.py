#! /usr/bin/env python

import sys
import os
try:
    libdir = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, libdir)
except:
    # probably running inside py2exe which doesn't set __file__
    pass

from lib import main
main.main()
