#!/usr/bin/python2.4
"""
this file just collects and runs
all our tests...
"""
import unittest
from physics import * 
from loader import *
from health import *
from room import *
from game import *    
from hero import *
from main import *

# these are more tests of our understanding:
# (espionage)
from eventtest import *
from odetest import *

unittest.main()

