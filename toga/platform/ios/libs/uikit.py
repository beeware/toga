from __future__ import print_function, absolute_import, division

from ctypes import *
from ctypes import util

from .types import *

######################################################################

# UIKit

uikit = cdll.LoadLibrary(util.find_library('UIKit'))

uikit.UIApplicationMain.restype = c_int
uikit.UIApplicationMain.argtypes = [c_int, POINTER(c_char_p), c_void_p, c_void_p]
