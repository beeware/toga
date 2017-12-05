##########################################################################
# System/Library/Frameworks/WebKit.framework
##########################################################################
from ctypes import *
from ctypes import util

from rubicon.objc import *

######################################################################

_webkit_path = util.find_library('WebKit')

if not _webkit_path:  # WebKit framework is only available under iOS 8.0 or newer.
    WKWebView = None
else:
    webkit = cdll.LoadLibrary(_webkit_path)

    WKWebView = ObjCClass('WKWebView')
