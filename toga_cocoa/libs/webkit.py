from __future__ import print_function, absolute_import, division

from ctypes import *
from ctypes import util

from .objc import ObjCClass
from .types import *

from toga.constants import *

######################################################################

# WEB KIT

# Even though we don't use this directly, it must be loaded so that
# we can find the WebKit class.
webkit = cdll.LoadLibrary(util.find_library('WebKit'))

# WebView = ObjCClass('WebView')
