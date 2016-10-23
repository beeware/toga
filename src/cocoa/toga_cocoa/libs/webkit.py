from ctypes import *
from ctypes import util

from rubicon.objc import *

from toga.constants import *

######################################################################

# WEB KIT

# Even though we don't use this directly, it must be loaded so that
# we can find the WebKit class.
webkit = cdll.LoadLibrary(util.find_library('WebKit'))

WebView = ObjCClass('WebView')
