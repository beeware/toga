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
# WKWebView.h
WKWebView = ObjCClass('WKWebView')
