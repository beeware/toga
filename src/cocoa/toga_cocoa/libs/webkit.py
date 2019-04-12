##########################################################################
# System/Library/Frameworks/WebKit.framework
##########################################################################
from ctypes import cdll, util

from rubicon.objc import ObjCClass

######################################################################
webkit = cdll.LoadLibrary(util.find_library('WebKit'))
######################################################################

######################################################################
# WebView.h
WebView = ObjCClass('WebView')

######################################################################
# WKWebView.h
WKWebView = ObjCClass('WKWebView')
