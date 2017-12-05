##########################################################################
# System/Library/Frameworks/WebKit.framework
##########################################################################
from ctypes import *
from ctypes import util

from rubicon.objc import *

######################################################################
webkit = cdll.LoadLibrary(util.find_library('WebKit'))
######################################################################

######################################################################
# WebView.h
WebView = ObjCClass('WebView')

try:
    WKWebView = ObjCClass('WKWebView')
except NameError:  # WKWebView is only available under macOS 10.10 or newer.
    WKWebView = None
