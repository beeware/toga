##########################################################################
# System/Library/Frameworks/WebKit.framework
##########################################################################
from ctypes import *
from ctypes import util

from rubicon.objc import *

######################################################################

webkit_path = util.find_library('WebKit')

if not webkit_path:  # WKWebView is only available under iOS 8.0 or newer.
    raise ImportError("WebKit is not available.")

webkit = cdll.LoadLibrary(webkit_path)
######################################################################

######################################################################
WKWebView = ObjCClass('WKWebView')
