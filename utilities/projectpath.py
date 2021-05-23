import os
import sys

bp = os.path.dirname(os.path.realpath('.')).split(os.sep)
modpath = os.sep.join(bp + ['server'])
sys.path.insert(0, modpath)
