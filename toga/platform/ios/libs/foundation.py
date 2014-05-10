from __future__ import print_function, absolute_import, division

from ctypes import *
from ctypes import util

from .types import *

######################################################################

# FOUNDATION

foundation = cdll.LoadLibrary(util.find_library('Foundation'))

foundation.NSMouseInRect.restype = c_bool
foundation.NSMouseInRect.argtypes = [NSPoint, NSRect, c_bool]
